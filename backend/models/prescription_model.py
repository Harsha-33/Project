from database.db import db


class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultations.consultation_id'), nullable=False)
    medicine_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(50))
    timing = db.Column(db.String(50))

    def to_dict(self):
        return {
            'prescription_id': self.prescription_id,
            'consultation_id': self.consultation_id,
            'medicine_name': self.medicine_name,
            'dosage': self.dosage,
            'timing': self.timing
        }
