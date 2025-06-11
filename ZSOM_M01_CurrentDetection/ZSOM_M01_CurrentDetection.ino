// Constants
#include <SPI.h>
#include <SD.h>
#include "wiring_private.h"
#include "FRAM_CTRL.h"

// Data structure definitions
#define SAMPLES_PER_SET 1000
#define MAX_SETS 10  // Maximum number of sets to store
#define BYTES_PER_CURRENT 2
#define TIMESTAMP_SIZE 4
#define SET_SIZE (2 * TIMESTAMP_SIZE + SAMPLES_PER_SET * BYTES_PER_CURRENT)  // 2008 bytes per set
#define CURRENT_SET_ADDRESS 0  // Address to store current set number
#define CURRENT_LIMIT_MA 2500  // 2.5A limit in milliamps
#define TOTAL_SETS 20 // Total sets (normal + abnormal)
#define ABNORMAL_SET_OFFSET (MAX_SETS * SET_SIZE + 4)  // Offset for abnormal partition
#define CURRENT_ABNORMAL_SET_ADDRESS (CURRENT_SET_ADDRESS + 4)  // Address to store current abnormal set number
#define AUTO_ABNORMAL_RESET_ADDRESS (CURRENT_ABNORMAL_SET_ADDRESS + 4)  // Address to store auto reset setting

#define AVERAGE_WINDOW 5  // Window size for running average
#define MAX_SPIKE_DIFFERENCE 500  // Maximum allowed difference between consecutive readings
#define SPIKE_FILTER_WINDOW 3  // Number of samples for spike detection
#define ZERO_THRESHOLD 100    // Threshold for near-zero readings
#define TRANSITION_WINDOW 10  // Number of samples to check for transition

// Deviation thresholds for different current ranges
#define DEV_0_30MA    300.0  // % deviation allowed for currents 0.0mA - 30.0mA
#define DEV_31_60MA   50.0  // % deviation allowed for currents 30.1mA - 60.0mA
#define DEV_61_90MA   25.0  // % deviation allowed for currents 60.1mA - 90.0mA
#define DEV_ABOVE_90MA 25.0  // % deviation allowed for currents > 90.1mA

// Global variables
uint16_t recentReadings[AVERAGE_WINDOW] = {0};
int recentReadingsIndex = 0;
uint16_t previousReadings[SPIKE_FILTER_WINDOW] = {0};
int readingIndex = 0;

struct DataSetInfo {
    uint32_t startTime;
    uint32_t endTime;
    uint16_t currentReadings[SAMPLES_PER_SET];
    uint16_t currentIndex;
    float avgCurrent;
};

// Global variables
DataSetInfo currentSet;
int currentSetNumber = 0;
int currentAbnormalSetNumber = 0;
int abnormalitiesCount = 0;
bool measuring = true;
bool isAbnormalPartitionFull = false;
unsigned long startMillis = 0;
float previousSetAverage = 0;
bool isFirstSet = true;
bool autoAbnormalReset = false;  // Default to manual reset mode

// Pin and measurement constants
const int CS = 5;
const int analogPin = A0;
const float refVoltage = 3.3;
const float gainResistor = 10000.0;
const float currentFactor = (refVoltage / 1023.0) * (10000.0 / gainResistor);
const int correction = -2;

// SPI Settings
#define speedMaximum 4000000
#define dataOrder MSBFIRST
#define dataMode SPI_MODE0
SPISettings mySetting(speedMaximum, dataOrder, dataMode);

// Add these variables at the top with other globals
float dev_0_30ma = DEV_0_30MA;
float dev_31_60ma = DEV_31_60MA;
float dev_61_90ma = DEV_61_90MA;
float dev_above_90ma = DEV_ABOVE_90MA;

void setup() {
    Serial.begin(9600);   // USB monitoring
    Serial1.begin(9600);  // Command interface
    while (!Serial);      // Wait for USB
    while (!Serial1);     // Wait for hardware serial
    
    pinMode(CS, OUTPUT);
    digitalWrite(CS, HIGH);
    SPI.begin();
    pinMode(analogPin, INPUT_PULLDOWN);

    startMillis = millis();

    // Force manual reset mode on startup
    autoAbnormalReset = false;
    FRAMWrite32(CS, AUTO_ABNORMAL_RESET_ADDRESS, 0, 1);  // Write manual mode to FRAM
    
    // Read last set numbers from FRAM
    currentSetNumber = FRAMRead32(CS, CURRENT_SET_ADDRESS, 4);
    currentAbnormalSetNumber = FRAMRead32(CS, CURRENT_ABNORMAL_SET_ADDRESS, 4);
    
    if (currentSetNumber < 0 || currentSetNumber >= MAX_SETS) {
        currentSetNumber = 0;
    }
    if (currentAbnormalSetNumber < 0 || currentAbnormalSetNumber >= MAX_SETS) {
        currentAbnormalSetNumber = 0;
    }
    
    currentSet.currentIndex = 0;
    
    // Status info goes to main Serial
    Serial.print("Continuing from normal set: ");
    Serial.println(currentSetNumber + 1);
    Serial.print("Abnormal partition: ");
    if (currentAbnormalSetNumber == 0) {
        Serial.println("Empty");
    } else {
        Serial.print(currentAbnormalSetNumber);
        Serial.print("/");
        Serial.println("5");
    }
}

void loop() {
    // Check both Serial ports for commands
    if (Serial.available()) {
        handleSerialCommands(Serial);
    }
    if (Serial1.available()) {
        handleSerialCommands(Serial1);
    }

    if (measuring) {
        measureAndAverageCurrent();
    }
}

// Modify handleSerialCommands to accept which Serial port to use
void handleSerialCommands(Stream &serialPort) {
    String input = serialPort.readStringUntil('\n');
    input.trim();  // Remove any whitespace, including \r

    // Command echo only goes to the port that sent the command
    serialPort.print("Received command: '");
    serialPort.print(input);
    serialPort.println("'");

    if (input.equalsIgnoreCase("manabrst") || input.equals("ManABrst")) {
        autoAbnormalReset = false;
        FRAMWrite32(CS, AUTO_ABNORMAL_RESET_ADDRESS, 0, 1);
        serialPort.println("Manual abnormal partition reset enabled");
    }
    else if (input.equalsIgnoreCase("autoabrst") || input.equals("AutoABrst")) {
        autoAbnormalReset = true;
        FRAMWrite32(CS, AUTO_ABNORMAL_RESET_ADDRESS, 1, 1);
        serialPort.println("Automatic abnormal partition reset enabled");
    }
    else if (input.equalsIgnoreCase("s")) {
        measuring = false;
        serialPort.println("Measurement stopped. Press 'R' to resume.");
    }
    else if (input.equalsIgnoreCase("r")) {
        measuring = true;
        serialPort.println("Measurement resumed.");
    }
    else if (input.equalsIgnoreCase("rst")) {
        Clear_FRAM_Partition(false, serialPort);
    }
    else if (input.equalsIgnoreCase("ab_rst")) {
        Clear_FRAM_Partition(true, serialPort);
    }
    else if (input.startsWith("read")) {
        readFromFRAM(input, serialPort);
    }
    else if (input.startsWith("THR:")) {
        handleThresholdUpdate(input);
        serialPort.println("Threshold updated");
    }
    else {
        serialPort.println("Invalid command. Available commands:");
        serialPort.println("'S' - Stop measuring");
        serialPort.println("'R' - Resume measuring");
        serialPort.println("'AutoABrst' - Enable auto reset of abnormal partition");
        serialPort.println("'ManABrst' - Enable manual reset of abnormal partition");
        serialPort.println("'RST' - Reset normal partition");
        serialPort.println("'AB_RST' - Reset abnormal partition");
        serialPort.println("'read X' - Read sets (X: 1-10 or A1-A10)");
        serialPort.println("'THR:range:value' - Update threshold");
    }
}

void measureAndAverageCurrent() {
    if (currentSet.currentIndex == 0) {
        currentSet.startTime = (millis() - startMillis) / 1000;
        FRAMWrite32(CS, currentSetNumber * SET_SIZE + 4, currentSet.startTime, 4);
        
        // Reset spike detection buffer
        for(int i = 0; i < SPIKE_FILTER_WINDOW; i++) {
            previousReadings[i] = 0;
        }
        readingIndex = 0;
        
        Serial.print("\nIndex: "); 
        Serial.println(currentSetNumber + 1);
        Serial.print("Timestamp: "); 
        Serial.print(currentSet.startTime); 
        Serial.println("s");
        Serial.println("Reading 1000 samples...");
        
        if (isAbnormalPartitionFull) {
            Serial.println("WARNING: Abnormal partition is full!");
        }
    }

    // Read current value
    int analogValue = analogRead(analogPin);
    int current_mA = ((analogValue * currentFactor * 1000) + (correction));
    
    // Check if reading is valid
    bool isValidReading = true;
    
    // Check absolute limits
    if (current_mA > CURRENT_LIMIT_MA || current_mA < 0) {
        isValidReading = false;
    }
    
    // Special handling for near-zero readings
    if (abs(current_mA) < ZERO_THRESHOLD) {
        // If we have previous readings, check the trend
        if (currentSet.currentIndex >= TRANSITION_WINDOW) {
            // Calculate trend from previous readings
            int sumDiff = 0;
            for (int i = 1; i < TRANSITION_WINDOW; i++) {
                sumDiff += currentSet.currentReadings[currentSet.currentIndex - i] - 
                          currentSet.currentReadings[currentSet.currentIndex - i - 1];
            }
            float avgTrend = sumDiff / (float)(TRANSITION_WINDOW - 1);
            
            // If we're in a trending direction, maintain the trend
            if (abs(avgTrend) > 5) {  // Minimum trend threshold
                // Use trend to predict next value
                int predictedValue = currentSet.currentReadings[currentSet.currentIndex - 1] + avgTrend;
                // Blend predicted value with actual reading
                current_mA = (predictedValue * 2 + current_mA) / 3;
            } else {
                // If no clear trend, smooth the transition
                current_mA = (currentSet.currentReadings[currentSet.currentIndex - 1] * 3 + current_mA) / 4;
            }
        }
    }
    // For non-zero readings, check for spikes
    else if (isValidReading && currentSet.currentIndex > 0) {
        int prevReading = currentSet.currentReadings[currentSet.currentIndex - 1];
        if (abs(current_mA - prevReading) > MAX_SPIKE_DIFFERENCE) {
            // Use weighted average favoring the previous reading
            current_mA = (prevReading * 2 + current_mA) / 3;
        }
    }
    
    // Check for abnormal conditions
    bool isAbnormal = false;
    
    // Calculate average of last 10 readings for context
    long sum = 0;
    int validReadings = 0;
    for(int i = max(0, currentSet.currentIndex - 10); i < currentSet.currentIndex; i++) {
        if (currentSet.currentReadings[i] <= 3300) {
            sum += currentSet.currentReadings[i];
            validReadings++;
        }
    }
    float recentAvg = validReadings > 0 ? sum / (float)validReadings : 0;
    
    // Check for large deviations
    if (currentSet.currentIndex > 0) {
        int prevReading = currentSet.currentReadings[currentSet.currentIndex - 1];
        float deviation = 0;
        
        // Calculate deviation for both positive and negative changes
        if (prevReading != 0) {
            // Calculate absolute percentage change
            deviation = abs(current_mA - prevReading) / (float)prevReading * 100.0;
            
            // Get threshold based on previous reading range
            float threshold = getThreshold(prevReading);
            
            // Check if deviation exceeds threshold
            if (deviation > threshold) {
                isAbnormal = true;
            }
        }
        
        if (isAbnormal && !isAbnormalPartitionFull && abnormalitiesCount == 0) {
            abnormalitiesCount = 1;
            
            // Store in abnormal partition
            long abnormalAddress = ABNORMAL_SET_OFFSET + 
                                 (currentAbnormalSetNumber * SET_SIZE) + 
                                 8 + // Skip timestamps
                                 (currentSet.currentIndex * BYTES_PER_CURRENT);
            
            // Store the entire set up to this point
            for (int i = 0; i <= currentSet.currentIndex; i++) {
                FRAMWrite32(CS, abnormalAddress + (i * BYTES_PER_CURRENT), 
                          currentSet.currentReadings[i], BYTES_PER_CURRENT);
            }
        }
    }

    // Store in normal partition
    currentSet.currentReadings[currentSet.currentIndex] = current_mA;
    currentSet.currentIndex++;

    if (currentSet.currentIndex >= SAMPLES_PER_SET) {
        completeCurrentSet();
    }

    mymsdelay(1);
}

// Add this function to handle threshold updates
void handleThresholdUpdate(String command) {
    // Expected format: "THR:range:value"
    // Example: "THR:0.0-30.0:350"
    int firstColon = command.indexOf(':');
    int secondColon = command.indexOf(':', firstColon + 1);
    
    if (firstColon == -1 || secondColon == -1) return;
    
    String range = command.substring(firstColon + 1, secondColon);
    float value = command.substring(secondColon + 1).toFloat();
    
    if (range == "0.0-30.0") {
        dev_0_30ma = value;
    } else if (range == "30.1-60.0") {
        dev_31_60ma = value;
    } else if (range == "60.1-90.0") {
        dev_61_90ma = value;
    } else if (range == ">90.1") {
        dev_above_90ma = value;
    }
}

// Modify the threshold checking code to use the variables instead of defines
float getThreshold(float prevReading) {
    if (prevReading <= 30.0) {
        return dev_0_30ma;
    } else if (prevReading <= 60.0) {
        return dev_31_60ma;
    } else if (prevReading <= 90.0) {
        return dev_61_90ma;
    } else {
        return dev_above_90ma;
    }
}