import sys
import subprocess
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit)

class SteamWorkshopDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.game_id_label = QLabel("Enter Game ID:")
        layout.addWidget(self.game_id_label)
        
        self.game_id_input = QLineEdit()
        self.game_id_input.setPlaceholderText("e.g., 4000 for Garry's Mod")
        layout.addWidget(self.game_id_input)

        self.workshop_id_label = QLabel("Enter Workshop ID:")
        layout.addWidget(self.workshop_id_label)
        
        self.workshop_id_input = QLineEdit()
        self.workshop_id_input.setPlaceholderText("e.g., 123456789")
        layout.addWidget(self.workshop_id_input)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_workshop)
        layout.addWidget(self.download_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        self.setLayout(layout)
        self.setWindowTitle("Steam Workshop Downloader by GooG")
        self.resize(500, 400)
    
    def download_workshop(self):
        game_id = self.game_id_input.text().strip()
        workshop_id = self.workshop_id_input.text().strip()
        
        if not game_id or not workshop_id:
            self.log_output.append("Error: Please enter both Game ID and Workshop ID!")
            return
        
        command = f"steamcmd +login anonymous +workshop_download_item {game_id} {workshop_id} +quit"
        self.log_output.append(f"Starting download...\nGame ID: {game_id}\nWorkshop ID: {workshop_id}")
        
        try:
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = process.stdout
            
            success = re.search(r'Success\. Downloaded item .*? to \"(.+?)\"', output)
            error = re.search(r'ERROR! Download item .*? failed \((.*?)\)', output)
            
            if success:
                path = success.group(1)
                self.log_output.append(f"\n✅ Download successful!\nPath: {path}")
            elif error:
                reason = error.group(1)
                self.log_output.append(f"\n❌ Download failed! Reason: {reason}")
            else:
                self.log_output.append("\n⚠️ Unknown result - check if SteamCMD is installed correctly")
                
        except Exception as e:
            self.log_output.append(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteamWorkshopDownloader()
    window.show()
    sys.exit(app.exec_())