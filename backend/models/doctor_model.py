from database.db import db


class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    speciality = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    qualification = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def to_dict(self):
        return {
            'doctor_id': self.doctor_id,
            'user_id': self.user_id,
            'name': self.user.name if self.user else None,
            'email': self.user.email if self.user else None,
            'speciality': self.speciality,
            'experience': self.experience,
            'qualification': self.qualification,
            'designation': self.designation,
            'phone': self.phone
        }
