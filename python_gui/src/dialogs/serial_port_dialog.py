from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QPushButton)
from serial.tools import list_ports

class PortSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial Port Configuration")
        self.setModal(True)
        self.setMinimumWidth(300)
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Port selection
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems([port.device for port in list_ports.comports()])
        port_layout.addWidget(self.port_combo)
        layout.addLayout(port_layout)
        
        # Baud rate selection
        baud_layout = QHBoxLayout()
        baud_layout.addWidget(QLabel("Baud Rate:"))
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600'])
        self.baud_combo.setCurrentText('9600')
        baud_layout.addWidget(self.baud_combo)
        layout.addLayout(baud_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_settings(self):
        return {
            'port': self.port_combo.currentText(),
            'baud': int(self.baud_combo.currentText())
        } 
        
    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        
        self.move(x, y) 