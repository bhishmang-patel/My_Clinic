import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import db_queries

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clinic Login")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                max-width: 400px;
            }
        """)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)

        logo_label = QLabel("LOGO")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont("Arial", 24, QFont.Bold))

        welcome_label = QLabel("Welcome back! Log in to your APP account")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 10))

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.phone_input.setFixedHeight(40)
        self.phone_input.setStyleSheet("font-size: 18px; padding: 8px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("font-size: 18px; padding: 8px;")

        login_btn = QPushButton("Log in to APP")
        login_btn.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; font-size: 18px; padding: 10px;")
        login_btn.setFixedHeight(40)
        login_btn.clicked.connect(self.login)

        reset_btn = QPushButton("Reset password")
        reset_btn.setFixedHeight(30)
        reset_btn.clicked.connect(self.reset_password)

        card_layout.addWidget(logo_label)
        card_layout.addWidget(welcome_label)
        card_layout.addWidget(self.phone_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(login_btn)

        register_btn = QPushButton("Register")
        register_btn.setFixedHeight(40)
        register_btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; font-size: 18px; padding: 10px;")
        register_btn.clicked.connect(self.open_register)
        card_layout.addWidget(register_btn)

        card_layout.addWidget(reset_btn)

        card.setLayout(card_layout)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def login(self):
        phone = self.phone_input.text()
        password = self.password_input.text()
        doctor = db_queries.check_login(phone, password)
        if doctor:
            self.close()
            self.dashboard = db_queries.load_dashboard(doctor)
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid Credentials!")

    def reset_password(self):
        QMessageBox.information(self, "Reset Password", "Password reset functionality is not implemented yet.")

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Doctor")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Doctor Name")
        self.clinic_input = QLineEdit()
        self.clinic_input.setPlaceholderText("Clinic Name")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("Developer PIN")

        reg_btn = QPushButton("Register")
        reg_btn.clicked.connect(self.register)

        layout.addWidget(self.name_input)
        layout.addWidget(self.clinic_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.pin_input)
        layout.addWidget(reg_btn)

        self.setLayout(layout)

    def register(self):
        pin = self.pin_input.text()
        if pin != '1111':
            QMessageBox.warning(self, "Error", "Invalid PIN!")
            return

        db_queries.register_doctor(
            self.name_input.text(),
            self.clinic_input.text(),
            self.phone_input.text(),
            self.password_input.text(),
            pin
        )
        QMessageBox.information(self, "Success", "Registered Successfully!")
        self.close()
