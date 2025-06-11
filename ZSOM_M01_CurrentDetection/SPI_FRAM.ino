void completeCurrentSet() {
    currentSet.endTime = (millis() - startMillis) / 1000;
    
    // Calculate average
    long sum = 0;
    int validReadings = 0;
    for (int i = 0; i < SAMPLES_PER_SET; i++) {
        if (currentSet.currentReadings[i] <= CURRENT_LIMIT_MA) {
            sum += currentSet.currentReadings[i];
            validReadings++;
        }
    }
    currentSet.avgCurrent = validReadings > 0 ? sum / (float)validReadings : 0;
    
    // If this set was marked abnormal, store the rest of it
    if (abnormalitiesCount > 0) {
        // Store timestamps
        long abnormalBaseAddress = ABNORMAL_SET_OFFSET + 
                                 (currentAbnormalSetNumber * SET_SIZE);
        FRAMWrite32(CS, abnormalBaseAddress + 4, currentSet.startTime, 4);
        FRAMWrite32(CS, abnormalBaseAddress + 8, currentSet.endTime, 4);
        
        // Store any remaining readings
        for (int i = 0; i < SAMPLES_PER_SET; i++) {
            long abnormalAddress = abnormalBaseAddress + 
                                 12 + // Skip set number (4) and timestamps (8)
                                 (i * BYTES_PER_CURRENT);
            FRAMWrite32(CS, abnormalAddress, currentSet.currentReadings[i], BYTES_PER_CURRENT);
        }
        
        // Update abnormal set counter
        currentAbnormalSetNumber++;
        
        // Debug message for partition status
        Serial.print("Abnormal Storage status: ");
        Serial.print(currentAbnormalSetNumber);
        Serial.print("/");
        Serial.println(MAX_SETS);
        
        if (currentAbnormalSetNumber >= MAX_SETS) {
            if (autoAbnormalReset) {
                Serial.println("Performing automatic reset of abnormal partition...");
                Clear_FRAM_Partition(true, Serial);  // Reset abnormal partition
                currentAbnormalSetNumber = 0;
                isAbnormalPartitionFull = false;
                abnormalitiesCount = 0;  // Reset abnormalities count
                Serial.println("Abnormal partition auto-reset completed");
            } else {
                isAbnormalPartitionFull = true;
                currentAbnormalSetNumber = MAX_SETS - 1;  // Stay at max
                Serial.println("WARNING: Abnormal partition full - Manual reset required");
            }
        }
        
        // Store the updated abnormal set number
        FRAMWrite32(CS, CURRENT_ABNORMAL_SET_ADDRESS, currentAbnormalSetNumber, 4);
    }
    
    // Write complete set to FRAM
    writeSetToFRAM(currentSetNumber);
    
    // Print summary
    Serial.print("Timestamp: "); 
    Serial.print(currentSet.endTime); 
    Serial.println("s");
    Serial.print("Avg current: "); 
    Serial.print(currentSet.avgCurrent); 
    Serial.println("mA");
    Serial.print("Total time taken: ");
    Serial.print(currentSet.endTime - currentSet.startTime);
    Serial.println("s");
    
    // Reset for next set
    currentSet.currentIndex = 0;
    abnormalitiesCount = 0;
    currentSetNumber++;
    
    if (currentSetNumber >= MAX_SETS) {
        Clear_FRAM_Partition(false, Serial);
        currentSetNumber = 0;
        isFirstSet = true;
        Serial.println("All normal sets complete (10 sets). Normal partition cleared. Starting over.");
    }
    
    // Store current set number
    FRAMWrite32(CS, CURRENT_SET_ADDRESS, currentSetNumber, 4);
}

void writeSetToFRAM(int setNumber) {
    long baseAddress = setNumber * SET_SIZE + 4; // Add 4 to skip the current set number storage
    
    // Write timestamps
    FRAMWrite32(CS, baseAddress, currentSet.startTime, 4);
    FRAMWrite32(CS, baseAddress + 4, currentSet.endTime, 4);
    
    // Write current readings
    for (int i = 0; i < SAMPLES_PER_SET; i++) {
        FRAMWrite32(CS, baseAddress + 8 + i * 2, currentSet.currentReadings[i], 2);
    }
}

void readFromFRAM(String inputString, Stream &serialPort) {
    String sets = inputString.substring(5); // Remove "read " from string
    
    int maxSetNum = -1;
    int minSetNum = MAX_SETS;
    long totalSum = 0;
    int validSets = 0;
    int totalReadings = 0;
    bool isAbnormalRead = false;
    
    // First validate all set numbers
    String currentNumber = "";
    sets += ","; // Add comma to handle last number
    
    serialPort.print("\nFRAM READING\nSet ");
    
    // First pass to validate and print set numbers
    for (int i = 0; i < sets.length(); i++) {
        if (sets[i] == 'A' || sets[i] == 'a') {
            isAbnormalRead = true;
            // Get the abnormal set number
            if (i + 1 < sets.length() && isDigit(sets[i + 1])) {
                int setNum = (sets[i + 1] - '0') - 1;
                if (setNum >= 0 && setNum < MAX_SETS) {
                    maxSetNum = max(maxSetNum, setNum);
                    minSetNum = min(minSetNum, setNum);
                    validSets++;
                    serialPort.print("A");
                    serialPort.print(setNum + 1);
                    serialPort.print(",");
                }
                i++; // Skip the next digit as we've processed it
            }
        } else if (isDigit(sets[i])) {
            int setNum = (sets[i] - '0') - 1;
            if (setNum >= 0 && setNum < MAX_SETS) {
                maxSetNum = max(maxSetNum, setNum);
                minSetNum = min(minSetNum, setNum);
                validSets++;
                serialPort.print(setNum + 1);
                serialPort.print(",");
            }
        }
    }
    serialPort.println("\n----------");
    
    if (validSets > 0) {
        long baseOffset = isAbnormalRead ? ABNORMAL_SET_OFFSET : 0;
        uint32_t firstStartTime = FRAMRead32(CS, baseOffset + minSetNum * SET_SIZE + 4, 4);
        uint32_t lastEndTime = FRAMRead32(CS, baseOffset + maxSetNum * SET_SIZE + 8, 4);
        
        // Print all readings sequentially
        int globalIndex = 1;
        
        // Reset for second pass
        for (int i = 0; i < sets.length(); i++) {
            int setNum = -1;
            bool isAbnormal = false;
            
            if (sets[i] == 'A' || sets[i] == 'a') {
                isAbnormal = true;
                if (i + 1 < sets.length() && isDigit(sets[i + 1])) {
                    setNum = (sets[i + 1] - '0') - 1;
                    i++; // Skip the next digit
                }
            } else if (isDigit(sets[i])) {
                setNum = (sets[i] - '0') - 1;
            }
            
            if (setNum >= 0 && setNum < MAX_SETS) {
                long baseAddress = (isAbnormal ? ABNORMAL_SET_OFFSET : 0) + setNum * SET_SIZE + 4;
                
                // Print set header
                serialPort.print("\nSet ");
                if (isAbnormal) serialPort.print("A");
                serialPort.print(setNum + 1);
                serialPort.println(" readings:");
                
                // Read and print all samples from this set
                for (int j = 0; j < SAMPLES_PER_SET; j++) {
                    uint16_t current = FRAMRead32(CS, baseAddress + 8 + j * 2, 2);
                    totalSum += current;
                    totalReadings++;
                    
                    serialPort.print(globalIndex);
                    serialPort.print(" ");
                    serialPort.println(current);
                    globalIndex++;
                }
            }
        }
        
        float totalAverage = totalSum / (float)totalReadings;
        
        serialPort.println("\n----------");
        serialPort.print("Start Time: "); 
        serialPort.print(firstStartTime); 
        serialPort.println(" s");
        serialPort.print("End Time: "); 
        serialPort.print(lastEndTime); 
        serialPort.println(" s");
        serialPort.print("Average Current: "); 
        serialPort.print(totalAverage, 1);
        serialPort.println(" mA");
        serialPort.println("----------\n");
    } else {
        serialPort.println("No valid sets specified. Use format 'read 1,2,3' or 'read A1,A2' (numbers 1-10)");
    }
}

void readSetFromFRAM(int setNumber, bool isAbnormal) {
    long baseAddress = isAbnormal ? 
        (ABNORMAL_SET_OFFSET + setNumber * SET_SIZE + 4) :
        (setNumber * SET_SIZE + 4);
    
    // ... implement reading logic for the specific set ...
}

void Clear_FRAM_Partition(bool isAbnormal, Stream &serialPort) {
    long startAddress = isAbnormal ? ABNORMAL_SET_OFFSET : CURRENT_SET_ADDRESS;
    long endAddress = isAbnormal ? 
        (ABNORMAL_SET_OFFSET + MAX_SETS * SET_SIZE) :
        (MAX_SETS * SET_SIZE + 4);
    
    serialPort.print("\nClearing ");
    serialPort.print(isAbnormal ? "abnormal" : "normal");
    serialPort.println(" partition...");
    
    // Clear the specified partition
    for (long i = startAddress; i < endAddress; i++) {
        FRAMWrite32(FRAM_CS, i, 0, 1);
        delayMicroseconds(1);
    }
    
    // Reset appropriate variables
    if (isAbnormal) {
        currentAbnormalSetNumber = 0;
        isAbnormalPartitionFull = false;
        abnormalitiesCount = 0;
        FRAMWrite32(CS, CURRENT_ABNORMAL_SET_ADDRESS, currentAbnormalSetNumber, 4);
    } else {
        currentSetNumber = 0;
        currentSet.currentIndex = 0;
        FRAMWrite32(CS, CURRENT_SET_ADDRESS, currentSetNumber, 4);
    }
    
    serialPort.println("Partition cleared!");
}

void myusdelay(int period) {
    unsigned long time = micros();
    while (micros() < time + period) {};
}

void mymsdelay(int period) {
    unsigned long time = millis();
    while (millis() < time + period) {};
}

void FRAMWrite32(int CS_pin, int address, int value, int N_BYTE) {
    unsigned int temp_data[N_BYTE];

    for (int i = 0; i < N_BYTE; i++) {
        temp_data[i] = (value) >> ((8 * (i + 1)) - 8);
    }

    digitalWrite(CS_pin, LOW);
    myusdelay(1);

    SPI.transfer(0x06);
    myusdelay(1);
    digitalWrite(CS_pin, HIGH);
    myusdelay(1);
    digitalWrite(CS_pin, LOW);
    SPI.transfer(0x02);
    SPI.transfer(highByte(address));
    SPI.transfer(lowByte(address));

    for (int i = 0; i < N_BYTE; i++) {
        SPI.transfer(temp_data[i]);
    }

    myusdelay(1);
    digitalWrite(CS_pin, HIGH);
}

unsigned int FRAMRead32(int CS_pin, int address, int N_BYTE) {
    unsigned int temp_data[N_BYTE];
    unsigned int result = 0;

    digitalWrite(CS_pin, LOW);
    myusdelay(1);

    SPI.transfer(0x03);
    SPI.transfer(highByte(address));
    SPI.transfer(lowByte(address));

    for (int i = 0; i < N_BYTE; i++) {
        temp_data[i] = SPI.transfer(0x00);
    }

    myusdelay(1);
    digitalWrite(CS_pin, HIGH);

    result = (((temp_data[3]) << 24) & (N_BYTE >= 4 ? 0xFFFFFFFF : 0x00000000)) |
             (((temp_data[2]) << 16) & (N_BYTE >= 3 ? 0xFFFFFFFF : 0x00000000)) |
             (((temp_data[1]) << 8) & (N_BYTE >= 2 ? 0xFFFFFFFF : 0x00000000)) |
             temp_data[0];

    return result;
}