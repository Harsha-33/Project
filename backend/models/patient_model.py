from database.db import db


class Patient(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.String(255))
    medical_history = db.Column(db.Text)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'user_id': self.user_id,
            'name': self.user.name if self.user else None,
            'email': self.user.email if self.user else None,
            'dob': self.dob.isoformat() if self.dob else None,
            'gender': self.gender,
            'mobile': self.mobile,
            'address': self.address,
            'medical_history': self.medical_history
        }
