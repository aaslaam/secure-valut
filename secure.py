import sys
import os
import hashlib
import base64
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, 
                             QMessageBox, QFrame, QProgressBar, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

class SecureVault(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file_path = ""
        self.initUI()

    def initUI(self):
        # Window Setup
        self.setWindowTitle('AES-256 Secure Vault')
        self.setFixedSize(550, 650)
        self.setObjectName("MainWindow")
        
        # Main Dark Theme Stylesheet
        self.setStyleSheet("""
            #MainWindow { background-color: #0f172a; }
            QLabel { color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
            
            /* Card Styling */
            .QFrame { 
                background-color: #1e293b; 
                border-radius: 12px; 
                border: 1px solid #334155;
            }
            
            /* Inputs */
            QLineEdit {
                background-color: #0f172a;
                border: 2px solid #334155;
                border-radius: 8px;
                color: #38bdf8;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #0ea5e9; }
            
            /* Buttons */
            QPushButton {
                background-color: #0ea5e9;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #0284c7; }
            QPushButton#decryptBtn { background-color: #7c3aed; }
            QPushButton#decryptBtn:hover { background-color: #6d28d9; }
            QPushButton#selectBtn { background-color: #334155; color: #cbd5e1; }
            
            /* Progress Bar */
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 5px;
                text-align: center;
                background-color: #0f172a;
                color: white;
            }
            QProgressBar::chunk { background-color: #0ea5e9; width: 10px; }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- HEADER SECTION ---
        header = QVBoxLayout()
        title = QLabel("AES-256 SECURE VAULT")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #38bdf8; letter-spacing: 1px;")
        subtitle = QLabel("Military-Grade File Encryption Tool")
        subtitle.setStyleSheet("font-size: 12px; color: #94a3b8;")
        header.addWidget(title)
        header.addWidget(subtitle)
        main_layout.addLayout(header)

        # --- FILE SELECTION CARD ---
        file_card = QFrame()
        file_layout = QVBoxLayout(file_card)
        
        self.file_info_label = QLabel("No file selected")
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setStyleSheet("color: #94a3b8; font-style: italic;")
        
        select_btn = QPushButton("📁 Select Target File")
        select_btn.setObjectName("selectBtn")
        select_btn.setCursor(Qt.PointingHandCursor)
        select_btn.clicked.connect(self.select_file)
        
        file_layout.addWidget(QLabel("TARGET SELECTION"))
        file_layout.addWidget(self.file_info_label)
        file_layout.addWidget(select_btn)
        main_layout.addWidget(file_card)

        # --- AUTHENTICATION CARD ---
        auth_card = QFrame()
        auth_layout = QVBoxLayout(auth_card)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Master Security Password...")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        auth_layout.addWidget(QLabel("MASTER KEY"))
        auth_layout.addWidget(self.password_input)
        main_layout.addWidget(auth_card)

        # --- ACTION SECTION ---
        actions_layout = QHBoxLayout()
        
        self.encrypt_btn = QPushButton("🔒 Encrypt & Save")
        self.encrypt_btn.setCursor(Qt.PointingHandCursor)
        self.encrypt_btn.clicked.connect(self.encrypt_action)
        
        self.decrypt_btn = QPushButton("🔓 Decrypt & Verify")
        self.decrypt_btn.setObjectName("decryptBtn")
        self.decrypt_btn.setCursor(Qt.PointingHandCursor)
        self.decrypt_btn.clicked.connect(self.decrypt_action)
        
        actions_layout.addWidget(self.encrypt_btn)
        actions_layout.addWidget(self.decrypt_btn)
        main_layout.addLayout(actions_layout)

        # --- STATUS & PROGRESS ---
        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        main_layout.addWidget(self.pbar)

        self.status_area = QLabel("System Status: Ready")
        self.status_area.setAlignment(Qt.AlignCenter)
        self.status_area.setStyleSheet("color: #0ea5e9; font-weight: bold; background: #1e293b; padding: 10px; border-radius: 8px;")
        main_layout.addWidget(self.status_area)

        self.setLayout(main_layout)

    # --- UI LOGIC ---
    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.selected_file_path = path
            file_name = os.path.basename(path)
            file_size = os.path.getsize(path) / 1024 # KB
            self.file_info_label.setText(f"File: {file_name}\nSize: {file_size:.2f} KB")
            self.status_area.setText("File Loaded. Enter password to proceed.")
            self.pbar.setValue(0)

    def update_status(self, msg, color="#0ea5e9"):
        self.status_area.setText(f"System Status: {msg}")
        self.status_area.setStyleSheet(f"color: {color}; font-weight: bold; background: #1e293b; padding: 10px; border-radius: 8px;")

    # --- CRYPTOGRAPHIC BACKEND (UNTOUCHED LOGIC) ---
    def get_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_action(self):
        path = self.selected_file_path
        pwd = self.password_input.text()
        if not path or not pwd:
            QMessageBox.warning(self, "Missing Data", "Please select a file and enter a password.")
            return

        try:
            self.update_status("Encrypting file...", "#38bdf8")
            self.pbar.setValue(45)
            
            salt = os.urandom(16)
            key = self.get_key(pwd, salt)
            fernet = Fernet(key)

            with open(path, "rb") as f:
                data = f.read()
            
            file_hash = hashlib.sha256(data).hexdigest()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            payload = f"{file_hash}|{timestamp}|".encode() + data

            encrypted = fernet.encrypt(payload)
            with open(path + ".enc", "wb") as f:
                f.write(salt + encrypted)
            
            self.pbar.setValue(100)
            self.update_status("Encryption Successful!", "#22c55e")
            QMessageBox.information(self, "Success", "File successfully encrypted with .enc extension.")
        except Exception as e:
            self.update_status("Encryption Error", "#ef4444")
            QMessageBox.critical(self, "Error", str(e))

    def decrypt_action(self):
        path = self.selected_file_path
        pwd = self.password_input.text()
        if not path or not pwd:
            QMessageBox.warning(self, "Missing Data", "Please select a file and enter a password.")
            return

        try:
            self.update_status("Verifying & Decrypting...", "#7c3aed")
            self.pbar.setValue(30)

            with open(path, "rb") as f:
                content = f.read()

            salt, encrypted_data = content[:16], content[16:]
            key = self.get_key(pwd, salt)
            fernet = Fernet(key)

            decrypted_payload = fernet.decrypt(encrypted_data)
            self.pbar.setValue(70)
            
            parts = decrypted_payload.split(b"|", 2)
            original_hash = parts[0].decode()
            original_data = parts[2]

            current_hash = hashlib.sha256(original_data).hexdigest()
            if current_hash != original_hash:
                raise ValueError("Integrity compromised (Tampering detected).")

            out_path = path.replace(".enc", ".restored")
            with open(out_path, "wb") as f:
                f.write(original_data)
            
            self.pbar.setValue(100)
            self.update_status("Decryption Successful!", "#22c55e")
            QMessageBox.information(self, "Verified", "Access Granted. File integrity verified.")

        except InvalidToken:
            self.update_status("Invalid Password!", "#ef4444")
            QMessageBox.critical(self, "Access Denied", "Incorrect Master Password.")
        except Exception as e:
            self.update_status("Security Alert!", "#ef4444")
            QMessageBox.critical(self, "Error", f"Tampering or Error: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SecureVault()
    window.show()
    sys.exit(app.exec_())
