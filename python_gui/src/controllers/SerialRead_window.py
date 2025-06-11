from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QWidget
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg
from threading import Thread
from queue import Queue
import collections
import time
import serial
from serial.tools import list_ports
from PySide6.QtGui import QPixmap, QIcon
import re
import logging

from ui.main_window_ui import Ui_MainWindow
from dialogs.serial_port_dialog import PortSelectionDialog
from dialogs.info_dialog import InfoDialog

class MainWindow(QMainWindow):
    def __init__(self, app_instance):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing MainWindow")
        self.app_instance = app_instance
        self.initialized = False
        self.collecting_read_data = False
        self.read_data_buffer = []
        self.first_data = True
        
        # Initialize UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Center the window
        self.center_window()
        
        # Set window icon
        icon_path = r"C:\Users\Ravinraj Seva\Downloads\V3\PythonV3\ZES_LOGOpng.png"
        self.setWindowIcon(QIcon(icon_path))
        
        # Set window title
        self.setWindowTitle("Current Sense V3.2 - Serial Read Mode [ Powered By ZSOM ]")
        
        # Add logo
        self.setup_logo()
        
        # Setup plot
        self.setup_plot()
        
        # Initialize progress bars
        self.ui.Normal_Parti_storage_2.setValue(0)
        self.ui.Normal_Parti_storage_2.setMaximum(10)
        self.ui.Abnormal_Partition_Storage_2.setValue(0)
        self.ui.Abnormal_Partition_Storage_2.setMaximum(10)
        
        # Initialize progress bar colors
        self.update_progress_bar_color(self.ui.Normal_Parti_storage_2, 0)
        self.update_progress_bar_color(self.ui.Abnormal_Partition_Storage_2, 0)
        
        # Connect signals
        self.connect_signals()
        
        # Initialize serial communication
        if not self.initialize_serial():
            return
        
        # Add back button
        self.setup_back_button()

    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        
        self.move(x, y)

    def setup_logo(self):
        """Setup the threshold table instead of logo"""
        try:
            # Create container widget and layout
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(2)  # Minimal spacing
            
            # Create horizontal layout for title and button
            header_layout = QHBoxLayout()
            
            # Add title label
            title_label = QLabel("Detection Threshold")
            title_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-weight: bold;
                    font-size: 11pt;
                    background-color: #2b2b2b;
                    padding: 2px;
                    border-radius: 4px;
                }
            """)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setFixedHeight(25)  # Fixed height for title
            
            # Add update button
            self.update_thresh_button = QPushButton("Update")
            self.update_thresh_button.setMaximumWidth(60)
            self.update_thresh_button.setFixedHeight(25)  # Match title height
            self.update_thresh_button.clicked.connect(self.update_thresholds)
            self.update_thresh_button.setStyleSheet("""
                QPushButton {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #505050;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #505050;
                    border: 1px solid #606060;
                }
                QPushButton:pressed {
                    background-color: #353535;
                }
            """)
            
            header_layout.addWidget(title_label)
            header_layout.addWidget(self.update_thresh_button)
            container_layout.addLayout(header_layout)
            
            # Create table widget
            self.threshold_table = QTableWidget(4, 2)
            self.threshold_table.setHorizontalHeaderLabels(["Current Range", "Deviation %"])
            
            # Set very compact row heights
            self.threshold_table.verticalHeader().setDefaultSectionSize(18)  # Reduced row height
            self.threshold_table.horizontalHeader().setFixedHeight(20)  # Reduced header height
            
            # Calculate and set fixed table height
            total_height = (
                self.threshold_table.horizontalHeader().height() +  # Header height
                (4 * self.threshold_table.verticalHeader().defaultSectionSize()) +  # 4 rows
                2  # Border buffer
            )
            self.threshold_table.setFixedHeight(total_height)
            
            # Set data
            ranges = [
                "0.0mA - 30.0mA",
                "30.1mA - 60.0mA",
                "60.1mA - 90.0mA",
                "> 90.1mA"
            ]
            
            deviations = [
                "300",  # Removed % symbol to make editing easier
                "200",
                "100",
                "50"
            ]
            
            # Populate table
            for i in range(4):
                range_item = QTableWidgetItem(ranges[i])
                deviation_item = QTableWidgetItem(deviations[i])
                range_item.setTextAlignment(Qt.AlignCenter)
                deviation_item.setTextAlignment(Qt.AlignCenter)
                self.threshold_table.setItem(i, 0, range_item)
                self.threshold_table.setItem(i, 1, deviation_item)
                # Make only the range column read-only
                range_item.setFlags(range_item.flags() & ~Qt.ItemIsEditable)
                # Make sure deviation column is editable
                deviation_item.setFlags(deviation_item.flags() | Qt.ItemIsEditable)
            
            # Style the table
            self.threshold_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.threshold_table.verticalHeader().setVisible(False)
            
            # Update the table and container styling
            self.threshold_table.setStyleSheet("""
                QTableWidget {
                    background-color: #2b2b2b;
                    color: white;
                    gridline-color: #404040;
                    border: 1px solid #404040;
                    border-radius: 8px;
                    padding: 2px;
                }
                QHeaderView::section {
                    background-color: #404040;
                    color: white;
                    padding: 4px;
                    border: none;
                    font-weight: bold;
                }
                QHeaderView::section:first {
                    border-top-left-radius: 8px;
                }
                QHeaderView::section:last {
                    border-top-right-radius: 8px;
                }
                QTableWidget::item {
                    border: none;
                    border-bottom: 1px solid #404040;
                    padding: 2px;
                }
                QTableWidget::item:selected {
                    background-color: #505050;
                }
                /* Highlight editable cells */
                QTableWidget::item:!read-only {
                    background-color: #353535;
                }
                QTableWidget::item:!read-only:hover {
                    background-color: #454545;
                }
            """)
            
            # Add table to container layout
            container_layout.addWidget(self.threshold_table)
            
            # Set fixed height for the entire container
            container.setFixedHeight(
                title_label.height() +  # Title height
                self.threshold_table.height() +  # Table height
                container_layout.spacing() +  # Spacing
                4  # Small buffer
            )
            
            # Replace logo with container
            layout = QVBoxLayout(self.ui.ZESLOGO_2)
            layout.addWidget(container)
            layout.setContentsMargins(0, 0, 0, 0)
            
        except Exception as e:
            print(f"Error setting up threshold table: {e}")

    def setup_plot(self):
        # Setup the PyQtGraph plot
        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout(self.ui.Graph)
        layout.addWidget(self.plot_widget)
        
        # Set background to black and grid to white
        self.plot_widget.setBackground('k')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Add title
        self.plot_widget.setTitle("Current vs Time", color='w', size='10pt')
       
        # Add axis labels
        self.plot_widget.setLabel('left', 'Current', units='mA')
        self.plot_widget.setLabel('bottom', 'Time', units='ms')
        
        # Create the plot curve
        self.curve = self.plot_widget.plot(pen=pg.mkPen('g', width=2))
        
        # Initialize data storage
        self.max_points = 5000
        self.time_data = collections.deque(maxlen=self.max_points)
        self.current_data = collections.deque(maxlen=self.max_points)
        
        self.start_time = time.time()
        self.sample_count = 0
        self.last_sample_time = time.time()
        self.total_current = 0
        self.total_samples = 0
        self.time_window = 5

    def connect_signals(self):
        # Connect button signals
        self.ui.Start_button_2.clicked.connect(lambda: self.send_function_command("R"))
        self.ui.Stop_button_2.clicked.connect(lambda: self.send_function_command("S"))
        self.ui.ResetGraph_button_2.clicked.connect(self.reset_graph)
        self.ui.Input_2.returnPressed.connect(self.send_serial_data)
        self.ui.Norm_Clear_Button_2.clicked.connect(self.norm_reset)
        self.ui.Ab_Clear_Button_2.clicked.connect(self.ab_reset)
        self.ui.Recall_Button_3.clicked.connect(lambda: self.recall_data("normal"))
        self.ui.Recall_Button_4.clicked.connect(lambda: self.recall_data("abnormal"))
        self.ui.AB_Auto_Clear_Checkbox_2.stateChanged.connect(self.handle_auto_clear)

    def initialize_serial(self):
        # Check if any ports are available
        if not list_ports.comports():
            QMessageBox.critical(self, "Error", "No serial ports found!")
            # Return to mode selection
            self.logger.debug("No serial ports found, returning to mode selection")
            self.close()
            self.app_instance.show_mode_selection()
            return False

        # Show port selection dialog
        port_dialog = PortSelectionDialog()
        if port_dialog.exec():
            settings = port_dialog.get_settings()
            
            try:
                self.ser = serial.Serial(
                    port=settings['port'],
                    baudrate=settings['baud'],
                    timeout=1
                )
                
                # Initialize data queue and thread control
                self.data_queue = Queue()
                self.running = True
                self.first_data = True

                # Start serial reading thread
                self.serial_thread = Thread(target=self.read_serial_data, daemon=True)
                self.serial_thread.start()

                # Setup update timer
                self.timer = QTimer()
                self.timer.timeout.connect(self.update_plot)
                self.timer.start(10)

                self.initialized = True
                return True

            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Could not open port {settings['port']}: {str(e)}")
                # Return to mode selection
                self.logger.debug("Serial port error, returning to mode selection")
                self.close()
                self.app_instance.show_mode_selection()
                return False
        else:
            # User cancelled port selection, return to mode selection
            self.logger.debug("Port selection cancelled, returning to mode selection")
            self.close()
            self.app_instance.show_mode_selection()
            return False

    def send_function_command(self, command):
        print(f"Sending {command}")
        self.ser.write(f"{command}\n".encode('utf-8'))

    def recall_data(self, partition_type):
        if partition_type == "normal":
            set_num = self.ui.NormalDataRecall_2.currentText().split()[1]
            command = f"read {set_num}"
        else:
            set_num = self.ui.Abnormal_DataRecall_2.currentText().split()[1]
            command = f"read {set_num}"
        
        print(f"Sending {command}")
        self.ser.write(f"{command}\n".encode('utf-8'))

    def read_serial_data(self):
        buffer = ""
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8')
                    if line:
                        buffer += line
                        lines = buffer.split('\n')
                        buffer = lines[-1]
                        
                        for line in lines[:-1]:
                            line = line.strip()
                            if "FRAM READING" in line:
                                print("Starting FRAM reading")
                                self.collecting_read_data = True
                                self.read_data_buffer = []
                            if line:
                                self.parse_read_data(line)
                                self.data_queue.put(line)
                        
            except Exception as e:
                print(f"Error reading serial data: {e}")
                time.sleep(0.001)

    def update_progress_bar_color(self, progress_bar, value):
        """Update progress bar color based on percentage"""
        # Calculate percentage (value out of maximum)
        maximum = progress_bar.maximum()
        if maximum == 0:
            return
        
        percentage = (value / maximum) * 100
        
        # Define the style based on percentage
        if percentage <= 50:
            color = "green"
        elif percentage <= 90:
            color = "orange"
        else:
            color = "red"
        
        # Set the style sheet
        progress_bar.setStyleSheet(
            f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
            """
        )

    def update_plot(self):
        while not self.data_queue.empty():
            line = self.data_queue.get()
            self.ui.Output_2.setText(line)
            
            # Process normal storage index
            if "Index:" in line:
                try:
                    index_str = line.split('Index:')[1].strip()
                    index_value = int(index_str)
                    self.ui.Normal_Parti_storage_2.setValue(min(index_value, 10))
                    self.update_progress_bar_color(self.ui.Normal_Parti_storage_2, index_value)
                except (IndexError, ValueError) as e:
                    print(f"Error parsing index: {e}")

            # Process abnormal storage status
            if "Abnormal Storage status:" in line:
                try:
                    status = line.split('status:')[1].strip()
                    current, total = map(int, status.split('/'))
                    self.ui.Abnormal_Partition_Storage_2.setValue(current)
                    self.update_progress_bar_color(self.ui.Abnormal_Partition_Storage_2, current)
                except (IndexError, ValueError) as e:
                    print(f"Error parsing abnormal storage status: {e}")

            # Only process regular current data if we're not collecting read data
            if not self.collecting_read_data and "Current:" in line:
                try:
                    parts = line.split('|')
                    if len(parts) == 3:
                        # Update index/set number
                        index_str = parts[2].split(':')[1].strip()
                        index_value = int(index_str)
                        self.ui.Normal_Parti_storage_2.setValue(min(index_value, 10))
                        
                        # Process current value
                        current_value_str = parts[0].split(':')[1].replace(" mA", "").strip()
                        current_value = float(current_value_str) / 1000  # Convert mA to A
                        
                        # Update average current calculation
                        self.total_current += float(current_value_str)
                        self.total_samples += 1
                        avg_current = self.total_current / self.total_samples
                        self.ui.AverageCurrent_Box_2.setText(f"{avg_current:.2f} mA")
                        
                        if self.first_data:
                            self.start_time = time.time()
                            self.first_data = False
                        
                        current_time = max(0, time.time() - self.start_time)
                        
                        self.time_data.append(current_time)
                        self.current_data.append(current_value)
                        self.sample_count += 1
                        
                        # Update Y-axis range based on current value
                        current_value_ma = float(current_value_str)  # Already in mA
                        y_max = max(current_value_ma + 500, 1000)  # At least 1000mA range
                        self.plot_widget.setYRange(0, y_max)
                except (IndexError, ValueError) as e:
                    print(f"Error parsing line: {e}")
                    continue

        if time.time() - self.last_sample_time >= 1:
            self.sample_count = 0
            self.last_sample_time = time.time()

        if len(self.time_data) > 1:
            current_time = time.time() - self.start_time
            cutoff_time = current_time - self.time_window
            
            while len(self.time_data) > 0 and self.time_data[0] < cutoff_time:
                self.time_data.popleft()
                self.current_data.popleft()
            
            time_list = list(self.time_data)
            current_list = list(self.current_data)
            
            if time_list:
                window_start = max(0, current_time - self.time_window)
                window_end = max(self.time_window, current_time)
                self.plot_widget.setXRange(window_start, window_end)
                self.curve.setData(time_list, current_list)

    def send_serial_data(self):
        """Send data from Input box to serial port"""
        data_to_send = self.ui.Input_2.text()
        self.ser.write(f"{data_to_send}\n".encode('utf-8'))
        self.ui.Input_2.clear()

    def norm_reset(self):
        """Reset normal storage"""
        print("Sending rst")
        self.ser.write("rst\n".encode('utf-8'))
        self.ui.Normal_Parti_storage_2.setValue(0)
        self.update_progress_bar_color(self.ui.Normal_Parti_storage_2, 0)

    def ab_reset(self):
        """Reset abnormal storage"""
        print("Sending ab_rst")
        self.ser.write("ab_rst\n".encode('utf-8'))
        self.ui.Abnormal_Partition_Storage_2.setValue(0)
        self.update_progress_bar_color(self.ui.Abnormal_Partition_Storage_2, 0)

    def reset_graph(self):
        """Reset the graph display"""
        self.time_data.clear()
        self.current_data.clear()
        self.first_data = True
        self.curve.setData([], [])
        self.plot_widget.setXRange(0, 5)  # Reset to default time window
        self.total_current = 0
        self.total_samples = 0
        self.ui.AverageCurrent_Box_2.setText("0 mA")
        self.ui.lineEdit.clear()

    def parse_read_data(self, line):
        """Parse incoming serial data"""
        if "Set " in line and "Start Time:" not in line:
            try:
                set_nums = line.split()[1].strip()
                print(f"Set numbers: {set_nums}")
                self.ui.lineEdit.setText(f"Set {set_nums}")
            except IndexError:
                pass
        elif "Start Time:" in line:
            start_time = line.split(":")[1].replace("ms", "").strip()
            self.ui.StartTime_Box_2.setText(f"{start_time}")
        elif "End Time:" in line:
            end_time = line.split(":")[1].replace("ms", "").strip()
            self.ui.EndTime_Box_2.setText(f"{end_time}")
        elif "Average Current:" in line:
            avg_current = line.split(":")[1].replace("mA", "").strip()
            self.ui.AverageCurrent_Box_2.setText(f"{avg_current} mA")
        elif "----------" in line:
            if not self.collecting_read_data:  # Start of data
                self.collecting_read_data = True
                self.read_data_buffer = []
            elif self.read_data_buffer:  # End of data
                print(f"Plotting {len(self.read_data_buffer)} points")
                self.plot_read_data()
                self.collecting_read_data = False
        elif self.collecting_read_data and line.strip():
            try:
                if line[0].isdigit():
                    sample_num, current = line.strip().split()
                    self.read_data_buffer.append((int(sample_num), float(current)))
            except (ValueError, IndexError) as e:
                print(f"Error parsing line: {line}, Error: {e}")

    def plot_read_data(self):
        """Plot data from read buffer"""
        if not self.read_data_buffer:
            print("No data to plot")
            return

        times_ms = [point[0] for point in self.read_data_buffer]
        currents = [point[1] for point in self.read_data_buffer]
        
        # Clear previous data
        self.time_data.clear()
        self.current_data.clear()
        
        # Calculate appropriate x-axis range
        max_time = max(times_ms)
        x_padding = max_time * 0.05  # Add 5% padding
        
        # Calculate appropriate y-axis range
        avg_current = sum(currents) / len(currents)
        y_max = avg_current + 500  # 500mA above average
        
        # Update plot with dynamic range
        self.plot_widget.setXRange(0, max_time + x_padding)
        self.plot_widget.setYRange(0, y_max)
        
        try:
            # Create a new curve with the data
            self.curve.setData(times_ms, currents)
            self.plot_widget.replot()  # Force a replot
        except Exception as e:
            print(f"Error plotting data: {e}")

    def handle_auto_clear(self, state):
        """Handle auto clear checkbox state change"""
        if self.ui.AB_Auto_Clear_Checkbox_2.isChecked():
            print("Sending AutoABrst")
            self.ser.write("AutoABrst\n".encode('utf-8'))
        else:
            print("Sending ManABrst")
            self.ser.write("ManABrst\n".encode('utf-8'))

    def closeEvent(self, event):
        """Handle application close"""
        self.logger.debug("Handling close event")
        try:
            if hasattr(self, 'running'):
                self.logger.debug("Cleaning up serial connection")
                self.running = False
                if hasattr(self, 'serial_thread'):
                    self.serial_thread.join(timeout=1.0)
                if hasattr(self, 'ser') and self.ser.is_open:
                    self.ser.close()
            super().closeEvent(event)
        except Exception as e:
            self.logger.error(f"Error in closeEvent: {str(e)}", exc_info=True)

    def update_storage_status(self, status_text):
        """Update the storage status progress bars"""
        try:
            # Extract normal and abnormal storage values
            normal_match = re.search(r'Normal Storage: ([\d]+|Empty)', status_text)
            abnormal_match = re.search(r'Abnormal Storage: ([\d]+|Empty)', status_text)
            
            if normal_match:
                normal_value = normal_match.group(1)
                # Convert 'Empty' to 0, otherwise use the number
                normal_percentage = 0 if normal_value == 'Empty' else int(normal_value)
                self.ui.Normal_Parti_storage_2.setValue(normal_percentage)
                
            if abnormal_match:
                abnormal_value = abnormal_match.group(1)
                # Convert 'Empty' to 0, otherwise use the number
                abnormal_percentage = 0 if abnormal_value == 'Empty' else int(abnormal_value)
                self.ui.Abnormal_Partition_Storage_2.setValue(abnormal_percentage)
                
        except Exception as e:
            print(f"Error updating storage status: {e}")

    def setup_back_button(self):
        """Add back button"""
        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setMaximumWidth(100)
        self.back_button.clicked.connect(self.return_to_mode_selection)
        
        # Add button to layout
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()  # This pushes button to the left
        
        # Add layout to the main vertical layout
        self.ui.verticalLayout_13.insertLayout(0, button_layout)

    def return_to_mode_selection(self):
        """Return to mode selection dialog"""
        self.logger.debug("Returning to mode selection")
        try:
            # Cleanup serial connection
            if hasattr(self, 'running'):
                self.logger.debug("Cleaning up serial connection")
                self.running = False
                if hasattr(self, 'serial_thread'):
                    self.serial_thread.join(timeout=1.0)
                if hasattr(self, 'ser') and self.ser.is_open:
                    self.ser.close()
            
            # Close current window
            self.logger.debug("Closing window")
            self.close()
            
            # Show new window
            self.logger.debug("Showing mode selection")
            self.app_instance.show_mode_selection()
        except Exception as e:
            self.logger.error(f"Error in return_to_mode_selection: {str(e)}", exc_info=True)

    def update_thresholds(self):
        """Send updated thresholds to Arduino"""
        try:
            ranges = ["0.0-30.0", "30.1-60.0", "60.1-90.0", ">90.1"]
            for i in range(4):
                deviation = self.threshold_table.item(i, 1).text().strip()
                if not deviation.isdigit():
                    QMessageBox.warning(self, "Invalid Input", 
                                      f"Please enter a valid number for {ranges[i]}mA range")
                    return
                
                # Send command to Arduino: "THR:range:value"
                command = f"THR:{ranges[i]}:{deviation}\n"
                if hasattr(self, 'ser') and self.ser.is_open:
                    self.ser.write(command.encode())
                    time.sleep(0.1)  # Small delay between commands
            
            QMessageBox.information(self, "Success", "Thresholds updated successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update thresholds: {str(e)}") 