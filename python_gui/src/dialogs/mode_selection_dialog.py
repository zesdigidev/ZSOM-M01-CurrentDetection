from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton

class ModeSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Operation Mode")
        self.setMinimumSize(190, 100)
        self.mode = None
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        serial_button = QPushButton("Serial Read Mode")
        file_button = QPushButton("File Read Mode")
        
        serial_button.clicked.connect(lambda: self.select_mode("serial"))
        file_button.clicked.connect(lambda: self.select_mode("file"))
        
        layout.addWidget(serial_button)
        layout.addWidget(file_button)
        
        self.setLayout(layout)
        
    def select_mode(self, mode):
        self.mode = mode
        self.accept()
        
    def get_mode(self):
        return self.mode 
        
    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        
        self.move(x, y) 