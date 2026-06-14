from database.db import db


class Consultation(db.Model):
    __tablename__ = 'consultations'

    consultation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'), nullable=False)
    current_symptoms = db.Column(db.Text)
    physical_examination = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    diagnosis = db.Column(db.Text)

    prescriptions = db.relationship('Prescription', backref='consultation', lazy=True, cascade='all, delete-orphan')
    medical_tests = db.relationship('MedicalTest', backref='consultation', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'consultation_id': self.consultation_id,
            'appointment_id': self.appointment_id,
            'current_symptoms': self.current_symptoms,
            'physical_examination': self.physical_examination,
            'treatment_plan': self.treatment_plan,
            'diagnosis': self.diagnosis,
            'prescriptions': [p.to_dict() for p in self.prescriptions],
            'medical_tests': [t.to_dict() for t in self.medical_tests],
            'appointment': self.appointment.to_dict() if self.appointment else None
        }
