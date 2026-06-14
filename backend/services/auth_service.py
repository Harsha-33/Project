import bcrypt
from flask_jwt_extended import create_access_token
from database.db import db
from models.user_model import User
from models.doctor_model import Doctor
from models.patient_model import Patient
from utils.validators import validate_email, validate_password, validate_required_fields
from datetime import date


def _parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


class AuthService:

    @staticmethod
    def register(data):
        valid, message = validate_required_fields(data, ['name', 'email', 'password', 'role'])
        if not valid:
            return None, message

        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        role = data['role'].upper()

        if role not in ('ADMIN', 'DOCTOR', 'PATIENT'):
            return None, 'Invalid role. Must be ADMIN, DOCTOR, or PATIENT'

        if not validate_email(email):
            return None, 'Invalid email format'

        valid_pw, pw_message = validate_password(password)
        if not valid_pw:
            return None, pw_message

        if User.query.filter_by(email=email).first():
            return None, 'Email already registered'

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(name=name, email=email, password=hashed, role=role)
        db.session.add(user)
        db.session.flush()

        if role == 'DOCTOR':
            doctor = Doctor(
                user_id=user.id,
                speciality=data.get('speciality', ''),
                experience=data.get('experience', 0),
                qualification=data.get('qualification', ''),
                designation=data.get('designation', ''),
                phone=data.get('phone', '')
            )
            db.session.add(doctor)
        elif role == 'PATIENT':
            patient = Patient(
                user_id=user.id,
                dob=_parse_date(data.get('dob')),
                gender=data.get('gender', ''),
                mobile=data.get('mobile', ''),
                address=data.get('address', ''),
                medical_history=data.get('medical_history', '')
            )
            db.session.add(patient)

        db.session.commit()
        return user, 'Registration successful'

    @staticmethod
    def login(email, password):
        if not email or not password:
            return None, 'Email and password are required'

        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user:
            return None, 'Invalid email or password'

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return None, 'Invalid email or password'

        token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        return {'user': user.to_dict(), 'token': token}, 'Login successful'
