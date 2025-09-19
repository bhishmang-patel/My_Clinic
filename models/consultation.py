# Consultation data model

class Consultation:
    def __init__(self, id, patient_id, doctor_id, date, notes):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.notes = notes
