from database.db import db


class MedicalTest(db.Model):
    __tablename__ = 'medical_tests'

    test_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultations.consultation_id'), nullable=False)
    test_name = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'test_id': self.test_id,
            'consultation_id': self.consultation_id,
            'test_name': self.test_name
        }
