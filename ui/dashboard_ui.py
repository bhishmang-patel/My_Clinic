from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPixmap
import sqlite3
from utils.printer import generate_bill_pdf
from datetime import datetime


class Dashboard(QWidget):
    def __init__(self, doctor):
        super().__init__()
        self.doctor = doctor
        self.setWindowTitle("Clinic Dashboard")
        self.setGeometry(200, 100, 1200, 700)
        self.log_dialog = None

        # === Background label ===
        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/image/bgimg.jpg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # Keep background behind widgets

        self.initUI()

    def initUI(self):
        # === Main layout ===
        main_layout = QVBoxLayout(self)

        # === Header ===
        doc_label = QGroupBox(f"{self.doctor[1]}")
        clinic_label = QGroupBox(f"{self.doctor[2]}")
        doc_label.setStyleSheet("""
            QGroupBox {
                font-family: 'Freestyle Script';
                font-size: 60px;   /* adjust as needed */
                font-weight: bold;
                padding: 5px;
                margin: 0px;
                max-height: 80px;  /* ensure enough height for text */
                min-hight: 80px;  /* ensure enough height for text */
            }
        """)

        clinic_label.setStyleSheet("""
            QGroupBox {
                font-size: 60px;   /* adjust as needed */
                font-weight: bold;
                padding: 5px;
                margin: 0px;
                font-family: 'Freestyle Script';
                min-height: 80px;  /* ensure enough height for text */
                max-height: 80px;  /* ensure enough height for text */
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.addWidget(doc_label, 1)    # 1 part → 1/3
        header_layout.addWidget(clinic_label, 1)
        main_layout.addLayout(header_layout)

        # === Patient Info ===
        patient_group = QGroupBox("Patient Info")
        patient_layout = QGridLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.set_completer(self.name_input, "name")
        self.name_input.editingFinished.connect(self.load_patient_data)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])

        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText("Mobile")
        self.set_completer(self.mobile_input, "phone")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")
        self.set_completer(self.address_input, "address")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")

        patient_layout.addWidget(QLabel("Name"), 0, 0)
        patient_layout.addWidget(self.name_input, 0, 1)
        patient_layout.addWidget(QLabel("Gender"), 0, 2)
        patient_layout.addWidget(self.gender_input, 0, 3)
        patient_layout.addWidget(QLabel("Mobile"), 1, 0)
        patient_layout.addWidget(self.mobile_input, 1, 1)
        patient_layout.addWidget(QLabel("Address"), 1, 2)
        patient_layout.addWidget(self.address_input, 1, 3)
        patient_layout.addWidget(QLabel("Age"), 2, 0)
        patient_layout.addWidget(self.age_input, 2, 1)

        patient_group.setLayout(patient_layout)

        # === Consultation ===
        consult_group = QGroupBox("Consultation")
        consult_layout = QGridLayout()

        self.complains_input = QLineEdit()
        self.complains_input.setPlaceholderText("Complaints")
        self.complains_completer = QCompleter()
        self.complains_input.setCompleter(self.complains_completer)
        self.add_complain_btn = QPushButton("+")
        self.add_complain_btn.clicked.connect(self.add_complain)

        self.treatment_input = QLineEdit()
        self.treatment_input.setPlaceholderText("Treatments")
        self.treatment_completer = QCompleter()
        self.treatment_input.setCompleter(self.treatment_completer)
        self.add_treatment_btn = QPushButton("+")
        self.add_treatment_btn.clicked.connect(self.add_treatment)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Duration")

        self.report_input = QLineEdit()
        self.report_input.setPlaceholderText("Report History")

        consult_layout.addWidget(QLabel("Complaints"), 0, 0)
        consult_layout.addWidget(self.complains_input, 0, 1)
        consult_layout.addWidget(self.add_complain_btn, 0, 2)
        consult_layout.addWidget(QLabel("Treatments"), 1, 0)
        consult_layout.addWidget(self.treatment_input, 1, 1)
        consult_layout.addWidget(self.add_treatment_btn, 1, 2)
        consult_layout.addWidget(QLabel("Duration"), 2, 0)
        consult_layout.addWidget(self.duration_input, 2, 1)
        consult_layout.addWidget(QLabel("Report"), 2, 2)
        consult_layout.addWidget(self.report_input, 2, 3)

        consult_group.setLayout(consult_layout)

        # === Billing ===
        billing_group = QGroupBox("Billing")
        billing_layout = QHBoxLayout()

        self.charge_input = QLineEdit()
        self.charge_input.setPlaceholderText("Charge")

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.save_consultation)

        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self.preview_bill)

        logbook_btn = QPushButton("Log Book")
        logbook_btn.clicked.connect(self.show_logs)

        billing_layout.addWidget(self.charge_input)
        billing_layout.addWidget(submit_btn)
        billing_layout.addWidget(preview_btn)
        billing_layout.addWidget(logbook_btn)
        billing_group.setLayout(billing_layout)

        main_layout.addWidget(patient_group)
        main_layout.addWidget(consult_group)
        main_layout.addWidget(billing_group)

        self.setLayout(main_layout)
        self.set_complaints_treatments_completers()

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def set_completer(self, line_edit, column):
        conn = sqlite3.connect("clinic.db")
        c = conn.cursor()
        c.execute(f"SELECT DISTINCT {column} FROM patient")
        data = [row[0] for row in c.fetchall()]
        conn.close()
        completer = QCompleter(data)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        line_edit.setCompleter(completer)

    def set_complaints_treatments_completers(self):
        conn = sqlite3.connect("clinic.db")
        c = conn.cursor()
        c.execute("SELECT DISTINCT complaints FROM consultation")
        complaints = []
        for row in c.fetchall():
            if row[0]:
                complaints.extend([x.strip() for x in row[0].split(",")])
        complaints = list(set(complaints))
        c.execute("SELECT DISTINCT treatments FROM consultation")
        treatments = []
        for row in c.fetchall():
            if row[0]:
                treatments.extend([x.strip() for x in row[0].split(",")])
        treatments = list(set(treatments))
        conn.close()

        self.complains_completer.setModel(QStringListModel(complaints))
        self.treatment_completer.setModel(QStringListModel(treatments))

    def load_patient_data(self):
        name = self.name_input.text().strip()
        if not name:
            return
        conn = sqlite3.connect("clinic.db")
        c = conn.cursor()
        c.execute("SELECT gender, phone, address, age FROM patient WHERE name=?", (name,))
        patient = c.fetchone()
        conn.close()
        if patient:
            gender, phone, address, age = patient
            index = self.gender_input.findText(gender, Qt.MatchFixedString)
            if index >= 0:
                self.gender_input.setCurrentIndex(index)
            self.mobile_input.setText(phone)
            self.address_input.setText(address)
            self.age_input.setText(str(age))

    def add_complain(self):
        text, ok = QInputDialog.getText(self, "Add Complaint", "Enter complaint:")
        if ok and text.strip():
            if self.complains_input.text():
                self.complains_input.setText(self.complains_input.text() + ", " + text.strip())
            else:
                self.complains_input.setText(text.strip())

    def add_treatment(self):
        text, ok = QInputDialog.getText(self, "Add Treatment", "Enter treatment:")
        if ok and text.strip():
            if self.treatment_input.text():
                self.treatment_input.setText(self.treatment_input.text() + ", " + text.strip())
            else:
                self.treatment_input.setText(text.strip())

    def save_consultation(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation", "Name is required.")
            return
        gender = self.gender_input.currentText()
        phone = self.mobile_input.text().strip()
        address = self.address_input.text().strip()
        age = self.age_input.text().strip()
        complaints = self.complains_input.text().strip()
        treatments = self.treatment_input.text().strip()
        duration = self.duration_input.text().strip()
        report = self.report_input.text().strip()
        charge = self.charge_input.text().strip()
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("clinic.db")
        c = conn.cursor()
        c.execute("SELECT id FROM patient WHERE name=?", (name,))
        patient = c.fetchone()
        if patient:
            patient_id = patient[0]
        else:
            c.execute("INSERT INTO patient (name, gender, phone, address, age) VALUES (?, ?, ?, ?, ?)",
                      (name, gender, phone, address, age))
            patient_id = c.lastrowid
        c.execute("""INSERT INTO consultation 
                     (patient_id, complaints, treatments, duration, report, charge, date) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (patient_id, complaints, treatments, duration, report, charge, date))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Entry Submitted ✔️")

    def preview_bill(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation", "Enter patient details before preview.")
            return
        generate_bill_pdf(
            doctor_name=self.doctor[1],
            clinic_name=self.doctor[2],
            patient_name=self.name_input.text(),
            age=self.age_input.text(),
            gender=self.gender_input.currentText(),
            phone=self.mobile_input.text(),
            disease=self.complains_input.text(),
            tablets=self.treatment_input.text(),
            bill_amount=self.charge_input.text()
        )

    def show_logs(self):
        conn = sqlite3.connect("clinic.db")
        c = conn.cursor()
        c.execute("""SELECT c.id, p.name, c.complaints, c.treatments, c.duration, c.report, c.charge, c.date
                     FROM consultation c JOIN patient p ON c.patient_id = p.id ORDER BY c.id DESC""")
        logs = c.fetchall()
        conn.close()

        if not logs:
            QMessageBox.information(self, "Log Book", "No logs found.")
            return

        if self.log_dialog:
            self.log_dialog.close()

        self.log_dialog = QDialog(self)
        self.log_dialog.setWindowTitle("Log Book")
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setRowCount(len(logs))
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Complaints", "Treatments", "Duration", "Report", "Charge", "Date", "Actions"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(60)
        for i, row in enumerate(logs):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

            preview_btn = QPushButton("Prev")
            preview_btn.clicked.connect(lambda _, name=row[1]: generate_bill_pdf(
                doctor_name=self.doctor[1],
                clinic_name=self.doctor[2],
                patient_name=name,
                disease=row[2],
                tablets=row[3],
                bill_amount=row[6]
            ))

            delete_btn = QPushButton("Del")
            delete_btn.clicked.connect(lambda _, row_idx=i, log_id=row[0]: self.delete_log(log_id, row_idx))

            action_layout = QHBoxLayout()
            action_layout.addWidget(preview_btn)
            action_layout.addWidget(delete_btn)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(i, 8, action_widget)

        layout.addWidget(self.table)
        self.log_dialog.setLayout(layout)
        self.log_dialog.showMaximized()

    def delete_log(self, log_id, row_idx):
        reply = QMessageBox.question(self, "Delete?", "Confirm delete?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect("clinic.db")
            c = conn.cursor()
            c.execute("DELETE FROM consultation WHERE id=?", (log_id,))
            conn.commit()
            conn.close()
            self.table.removeRow(row_idx)
            QMessageBox.information(self, "Deleted", "Log deleted.")
