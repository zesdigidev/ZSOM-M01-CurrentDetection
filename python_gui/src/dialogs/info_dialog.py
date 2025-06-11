from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Threshold Information")
        self.setModal(True)  # Makes the dialog modal (blocks interaction with parent window)
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create info text
        info_text = """
        <h3>Abnormality Detection Thresholds (by Default)</h3>
        <ul>
        <li>300% deviation allowed for currents 0.0mA - 30.0mA</li>
        <li>200% deviation allowed for currents 30.1mA - 60.0mA</li>
        <li>100% deviation allowed for currents 60.1mA - 90.0mA</li>
        <li>50% deviation allowed for currents > 90.1mA</li>
        </ul>
        <p>Thresholds can be edited in IDE code</p>
        """
        
        # Create and style the label
        info_label = QLabel(info_text)
        info_label.setTextFormat(Qt.RichText)
        info_label.setStyleSheet("QLabel { padding: 20px; }")
        
        # Create close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setMaximumWidth(100)
        
        # Add widgets to layout
        layout.addWidget(info_label)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        
        self.move(x, y) 