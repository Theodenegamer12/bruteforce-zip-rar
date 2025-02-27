import sys
import zipfile
import rarfile
import os
import subprocess
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QProgressBar, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from threading import Thread
from tqdm import tqdm

rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\UnRAR.exe"

DEFAULT_WORDLIST_DIR = "bruteforce_txt"
DEFAULT_WORDLIST_PATH = os.path.join(DEFAULT_WORDLIST_DIR, "crack-default.txt")

if not os.path.exists(DEFAULT_WORDLIST_DIR):
    os.makedirs(DEFAULT_WORDLIST_DIR)

if not os.path.exists(DEFAULT_WORDLIST_PATH):
    with open(DEFAULT_WORDLIST_PATH, "w") as f:
        f.write("password123\n123456\nletmein\nadmin\n")

class ZipRarCrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🔓 Brute-Force ZIP/RAR")
        self.setWindowIcon(QIcon("icons/bruteforce-icon.png"))
        self.setGeometry(100, 100, 520, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: white;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #88C0D0;
            }
            QProgressBar {
                border: 2px solid #4C566A;
                border-radius: 5px;
                background-color: #3B4252;
            }
            QProgressBar::chunk {
                background-color: #A3BE8C;
            }
        """)

        layout = QVBoxLayout()

        title_label = QLabel("🔑 Archive Decryptor")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        self.label_file = QLabel("📂 ZIP/RAR File: Not selected")
        layout.addWidget(self.label_file)

        self.btn_select_file = QPushButton("📁 Select a file")
        self.btn_select_file.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select_file)

        self.label_wordlist = QLabel(f"📜 Password file: {DEFAULT_WORDLIST_PATH}")
        layout.addWidget(self.label_wordlist)

        self.btn_select_wordlist = QPushButton("📖 Select a wordlist")
        self.btn_select_wordlist.clicked.connect(self.select_wordlist)
        layout.addWidget(self.btn_select_wordlist)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.btn_start = QPushButton("🚀 Start Attack")
        self.btn_start.clicked.connect(self.start_crack)
        layout.addWidget(self.btn_start)

        button_layout = QHBoxLayout()

        self.btn_youtube = QPushButton()
        self.btn_youtube.setIcon(QIcon("icons/youtube_icon.png"))
        self.btn_youtube.setIconSize(QSize(32, 32))
        self.btn_youtube.clicked.connect(self.open_youtube)
        button_layout.addWidget(self.btn_youtube)

        self.btn_github = QPushButton()
        self.btn_github.setIcon(QIcon("icons/github_icon.png"))
        self.btn_github.setIconSize(QSize(32, 32))
        self.btn_github.clicked.connect(self.open_github)
        button_layout.addWidget(self.btn_github)

        self.btn_linktree = QPushButton()
        self.btn_linktree.setIcon(QIcon("icons/linktree_icon.png"))
        self.btn_linktree.setIconSize(QSize(32, 32))
        self.btn_linktree.clicked.connect(self.open_linktree)
        button_layout.addWidget(self.btn_linktree)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.file_path = None
        self.wordlist_path = DEFAULT_WORDLIST_PATH

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a ZIP/RAR file", "", "Archives (*.zip *.rar)")
        if file_path:
            self.file_path = file_path
            self.label_file.setText(f"📂 Selected file: {file_path}")

    def select_wordlist(self):
        wordlist_path, _ = QFileDialog.getOpenFileName(self, "Select a password file", "", "Text files (*.txt)")
        if wordlist_path:
            self.wordlist_path = wordlist_path
            self.label_wordlist.setText(f"📜 Password file: {wordlist_path}")

    def start_crack(self):
        if not self.file_path or not os.path.exists(self.file_path):
            QMessageBox.critical(self, "Error", "❌ ZIP/RAR file not found.")
            return
        if not os.path.exists(self.wordlist_path):
            QMessageBox.critical(self, "Error", "❌ Password file not found.")
            return

        self.btn_start.setEnabled(False)
        self.progress_bar.setValue(0)

        thread = Thread(target=self.crack_archive)
        thread.start()

    def crack_archive(self):
        ext = self.file_path.split('.')[-1].lower()

        with open(self.wordlist_path, "r", encoding="latin-1") as wordlist:
            passwords = [line.strip() for line in wordlist]

        total_passwords = len(passwords)
        self.progress_bar.setMaximum(total_passwords)

        output_folder = os.path.join(os.path.dirname(self.file_path), "extracted")
        os.makedirs(output_folder, exist_ok=True)

        if ext == "zip":
            result = self.brute_force_zip(passwords, output_folder)
        elif ext == "rar":
            result = self.brute_force_rar(passwords, output_folder)
        else:
            QMessageBox.critical(self, "Error", "❌ Unsupported format.")
            self.btn_start.setEnabled(True)
            return

        if result:
            QMessageBox.information(self, "Success", f"🔓 Password found: {result}\n📂 Files extracted to: {output_folder}")
            subprocess.Popen(f'explorer "{output_folder}"')
        else:
            QMessageBox.warning(self, "Failure", "🚫 Password not found.")

        self.btn_start.setEnabled(True)

    def brute_force_zip(self, passwords, output_folder):
        with zipfile.ZipFile(self.file_path, 'r') as zip_file:
            for i, password in enumerate(tqdm(passwords, desc="Brute-forcing ZIP", unit="password")):
                try:
                    zip_file.extractall(path=output_folder, pwd=password.encode('utf-8'))
                    return password
                except:
                    pass
                self.progress_bar.setValue(i + 1)
        return None

    def brute_force_rar(self, passwords, output_folder):
        with rarfile.RarFile(self.file_path) as rar_file:
            for i, password in enumerate(tqdm(passwords, desc="Brute-forcing RAR", unit="password")):
                try:
                    rar_file.extractall(path=output_folder, pwd=password)
                    return password
                except:
                    pass
                self.progress_bar.setValue(i + 1)
        return None

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com/@theodenegamer1263")

    def open_github(self):
        webbrowser.open("https://github.com/theodenegamer12")

    def open_linktree(self):
        webbrowser.open("https://linktr.ee/theodenegamer12")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ZipRarCrackerApp()
    ex.show()
    sys.exit(app.exec_())
