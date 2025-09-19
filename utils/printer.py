# utils/printer.py

from fpdf import FPDF
import os
import platform
import subprocess
import re

def generate_bill_pdf(doctor_name, clinic_name, patient_name, age, gender, phone, complains, duration, treatment, charge):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.cell(200, 10, txt=clinic_name, ln=True, align='C')
    pdf.cell(200, 10, txt=f"Doctor: {doctor_name}", ln=True, align='C')
    pdf.ln(10)

    # Patient details
    pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age} | Gender: {gender}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
    pdf.cell(200, 10, txt=f"Complains: {complains}", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {duration}", ln=True)
    pdf.cell(200, 10, txt=f"Treatment: {treatment}", ln=True)
    pdf.cell(200, 10, txt=f"Charge: Rs. {charge}", ln=True)

    # Output folder
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Safe filename
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', patient_name.strip())
    filename = f"{output_dir}/{safe_name}_bill.pdf"
    pdf.output(filename)

    # Open the PDF
    if os.path.exists(filename):
        open_file(filename)
    else:
        raise FileNotFoundError(f"PDF not created: {filename}")

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.call(['open', path])
    else:
        subprocess.call(['xdg-open', path])
