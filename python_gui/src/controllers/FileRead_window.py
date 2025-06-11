from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QPushButton, QHBoxLayout
import pyqtgraph as pg
from PySide6.QtCore import QTimer
from ui.file_read_window_ui import Ui_MainWindow
import re
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import logging
from dialogs.info_dialog import InfoDialog
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
import os

class FileReadWindow(QMainWindow):
    def __init__(self, app_instance):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing FileReadWindow")
        self.app_instance = app_instance
        
        try:
            self.logger.debug("Setting up UI")
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            
            # Center the window
            self.center_window()
            
            self.logger.debug("Setting window title")
            self.setWindowTitle("Current Sense V3.2 - File Read Mode [ Powered By ZSOM ]")
            
            self.logger.debug("Setting up plot")
            self.setup_plot()
            
            self.logger.debug("Connecting signals")
            self.connect_signals()
            
            self.logger.debug("Initializing data")
            self.current_data = []
            self.time_data = []
            
            self.logger.debug("Setting up logo")
            self.setup_logo()
            
            self.logger.debug("Setting up back button")
            self.setup_back_button()
            
            self.logger.debug("FileReadWindow initialization complete")
            
        except Exception as e:
            self.logger.error(f"Error during FileReadWindow initialization: {str(e)}", exc_info=True)
            raise

    def cleanup(self):
        """Clean up resources before closing"""
        self.logger.debug("Starting FileReadWindow cleanup")
        try:
            # Clear plot data
            if hasattr(self, 'curve'):
                self.curve.setData([], [])
            
            # Clear data arrays
            self.current_data = []
            self.time_data = []
            
            # Remove plot widget
            if hasattr(self, 'plot_widget'):
                layout = self.ui.Graph.layout()
                if layout is not None:
                    layout.removeWidget(self.plot_widget)
                self.plot_widget.deleteLater()
                
            self.logger.debug("FileReadWindow cleanup complete")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}", exc_info=True)

    def closeEvent(self, event):
        """Handle window close event"""
        self.logger.debug("FileReadWindow close event triggered")
        try:
            self.cleanup()
            super().closeEvent(event)
        except Exception as e:
            self.logger.error(f"Error in closeEvent: {str(e)}", exc_info=True)

    def setup_plot(self):
        self.logger.debug("Setting up plot widget")
        try:
            self.plot_widget = pg.PlotWidget()
            
            # Get or create layout
            layout = self.ui.Graph.layout()
            if layout is None:
                self.logger.debug("Creating new layout for Graph widget")
                layout = QVBoxLayout(self.ui.Graph)
            else:
                self.logger.debug("Using existing layout for Graph widget")
                # Clear any existing widgets
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
            
            layout.addWidget(self.plot_widget)
            
            # Set background to black and grid to white
            self.plot_widget.setBackground('k')
            self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
            
            # Add title and labels
            self.plot_widget.setTitle("Current vs Time", color='w', size='10pt')
            self.plot_widget.setLabel('left', 'Current', units='mA')
            self.plot_widget.setLabel('bottom', 'Time', units='ms')
            
            # Create plot curve
            self.curve = self.plot_widget.plot(pen=pg.mkPen('g', width=2))
            
            self.logger.debug("Plot setup complete")
        except Exception as e:
            self.logger.error(f"Error setting up plot: {str(e)}", exc_info=True)
            raise
        
    def connect_signals(self):
        self.ui.FileSelect_Button.clicked.connect(self.select_file)
        self.ui.ResetGraph_button_2.clicked.connect(self.reset_graph)
        
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        
        if file_path:
            self.ui.Selected_file.setText(file_path)
            self.process_file(file_path)
            
    def process_file(self, file_path):
        self.ui.Stauts_Output.setText("Opening...")
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
            self.ui.Stauts_Output.setText("Processing...")
            
            # Validate format
            if self.validate_format(content):
                self.ui.Stauts_Output.setText("Validated")
                self.parse_and_plot_data(content)
            else:
                self.ui.Stauts_Output.setText("Invalid Format")
                QMessageBox.warning(self, "Error", "Invalid file format")
                
        except Exception as e:
            self.ui.Stauts_Output.setText("Error")
            QMessageBox.critical(self, "Error", f"Error reading file: {str(e)}")
            
    def validate_format(self, content):
        # Check for required sections
        required_sections = [
            "FRAM READING",
            "Set",
            "----------",
            "Start Time:",
            "End Time:",
            "Average Current:"
        ]
        
        return all(section in content for section in required_sections)
        
    def parse_and_plot_data(self, content):
        # Extract data points
        data_pattern = r'\d+\s+\d+'
        matches = re.findall(data_pattern, content)
        
        self.time_data = []
        self.current_data = []
        
        for match in matches:
            time, current = map(float, match.split())
            self.time_data.append(time)
            self.current_data.append(current)
            
        # Extract metadata
        start_time = re.search(r'Start Time: (\d+)', content)
        end_time = re.search(r'End Time: (\d+)', content)
        avg_current = re.search(r'Average Current: ([\d.]+)', content)
        set_number = re.search(r'Set ([\w\d]+)', content)
        
        # Update UI with units (changed from ms to s)
        if start_time:
            self.ui.StartTime_Box_2.setText(f"{start_time.group(1)} s")
        if end_time:
            self.ui.EndTime_Box_2.setText(f"{end_time.group(1)} s")
        if avg_current:
            self.ui.AverageCurrent_Box_2.setText(f"{avg_current.group(1)} mA")
        if set_number:
            self.ui.lineEdit.setText(set_number.group(1))
            
        # Plot data with dynamic y-axis range
        if self.current_data:
            max_current = max(self.current_data)
            y_max = max_current + 400  # Changed from 200mA to 400mA padding
            
            # Update plot with dynamic range
            self.plot_widget.setYRange(0, y_max)
            self.curve.setData(self.time_data, self.current_data)
        
    def reset_graph(self):
        self.time_data = []
        self.current_data = []
        self.curve.setData([], [])
        self.ui.StartTime_Box_2.clear()
        self.ui.EndTime_Box_2.clear()
        self.ui.AverageCurrent_Box_2.clear()
        self.ui.lineEdit.clear() 

    def setup_back_button(self):
        """Add back and info buttons"""
        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setMaximumWidth(100)
        self.back_button.clicked.connect(self.return_to_mode_selection)
        
        # Info button
        self.info_button = QPushButton("Info", self)
        self.info_button.setMaximumWidth(100)
        self.info_button.clicked.connect(self.show_info)
        
        # Add buttons to layout
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.info_button)
        button_layout.addStretch()  # This pushes buttons to the left
        
        # Add layout to the main vertical layout
        self.ui.verticalLayout_13.insertLayout(0, button_layout)

    def return_to_mode_selection(self):
        """Return to mode selection dialog"""
        self.logger.debug("Returning to mode selection")
        try:
            self.cleanup()
            self.logger.debug("Closing window")
            self.close()
            
            self.logger.debug("Showing mode selection")
            self.app_instance.show_mode_selection()
        except Exception as e:
            self.logger.error(f"Error in return_to_mode_selection: {str(e)}", exc_info=True) 

    def show_info(self):
        """Show the info dialog"""
        dialog = InfoDialog(self)
        dialog.exec()

    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        
        self.move(x, y) 

    def setup_logo(self):
        """Setup the ZES logo"""
        try:
            # Create QLabel for logo
            logo_label = QLabel()
            
            # Get path to resources directory
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                    "resources", "images", "ZES_LOGOpng.png")
            
            if not os.path.exists(logo_path):
                self.logger.error(f"Could not find logo at {logo_path}")
                return
                
            # Load and set the logo image
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                self.logger.error(f"Failed to load logo from {logo_path}")
                return
                
            # Scale the logo to fit the space while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(191, 131, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            
            # Add logo to the ZESLOGO_2 widget
            layout = QVBoxLayout(self.ui.ZESLOGO_2)
            layout.addWidget(logo_label)
            layout.setContentsMargins(0, 0, 0, 0)
            
        except Exception as e:
            self.logger.error(f"Error setting up logo: {e}") 