import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from controllers.SerialRead_window import MainWindow
from controllers.FileRead_window import FileReadWindow
from dialogs.mode_selection_dialog import ModeSelectionDialog

class Application:
    def __init__(self):
        # Setup logging
        logging.basicConfig(level=logging.DEBUG,
                          format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing Application")
        
        self.app = QApplication([])
        
        # Set application icon using resources path
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                "resources", "images", "ZES_LOGOpng.png")
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        else:
            self.logger.warning(f"Could not find icon at {icon_path}")
        
    def show_mode_selection(self):
        self.logger.debug("Showing mode selection dialog")
        mode_dialog = ModeSelectionDialog()
        if mode_dialog.exec():
            mode = mode_dialog.get_mode()
            self.logger.debug(f"Selected mode: {mode}")
            
            try:
                # Ensure any existing windows are properly closed
                if hasattr(self, 'current_window'):
                    self.logger.debug("Cleaning up existing window")
                    if hasattr(self.current_window, 'cleanup'):
                        self.current_window.cleanup()
                    self.current_window.close()
                    delattr(self, 'current_window')
                
                if mode == "serial":
                    self.logger.debug("Creating MainWindow")
                    window = MainWindow(self)
                    # Only show and store the window if initialization was successful
                    if hasattr(window, 'initialized') and window.initialized:
                        window.show()
                        self.current_window = window
                        return window
                    # If initialization failed, the window will handle returning to mode selection
                    return None
                elif mode == "file":
                    self.logger.debug("Creating FileReadWindow")
                    window = FileReadWindow(self)
                    window.show()
                    self.current_window = window
                    return window
            except Exception as e:
                self.logger.error(f"Error creating window: {str(e)}", exc_info=True)
                self.app.quit()
        else:
            self.logger.debug("Mode selection cancelled")
            self.app.quit()
            
    def run(self):
        window = self.show_mode_selection()
        if window:
            return self.app.exec()
        # If window is None (initialization failed), keep the application running
        # to allow returning to mode selection
        if hasattr(self, 'app'):
            return self.app.exec()
        return 1

def main():
    app = Application()
    return app.run()

if __name__ == "__main__":
    sys.exit(main()) 