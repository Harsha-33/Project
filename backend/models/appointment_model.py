from datetime import datetime
from database.db import db


class Appointment(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    symptoms = db.Column(db.Text)
    visit_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    consultation = db.relationship('Consultation', backref='appointment', uselist=False)

    def to_dict(self):
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient_name': self.patient.user.name if self.patient and self.patient.user else None,
            'patient_mobile': self.patient.mobile if self.patient else None,
            'doctor_name': self.doctor.user.name if self.doctor and self.doctor.user else None,
            'doctor_speciality': self.doctor.speciality if self.doctor else None,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'symptoms': self.symptoms,
            'visit_type': self.visit_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
