from datetime import datetime
import bcrypt
from database.db import db
from models.user_model import User
from models.doctor_model import Doctor
from models.patient_model import Patient
from models.appointment_model import Appointment
from services.appointment_service import AppointmentService


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


class AdminService:

    @staticmethod
    def get_dashboard_stats():
        return {
            'total_doctors': Doctor.query.count(),
            'total_patients': Patient.query.count(),
            'total_appointments': Appointment.query.count()
        }

    @staticmethod
    def add_doctor(data):
        email = data.get('email', '').strip().lower()
        if User.query.filter_by(email=email).first():
            return None, 'Email already exists'

        hashed = bcrypt.hashpw(
            data.get('password', 'Password123').encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(
            name=data.get('name', ''),
            email=email,
            password=hashed,
            role='DOCTOR'
        )
        db.session.add(user)
        db.session.flush()

        doctor = Doctor(
            user_id=user.id,
            speciality=data.get('speciality', ''),
            experience=data.get('experience', 0),
            qualification=data.get('qualification', ''),
            designation=data.get('designation', ''),
            phone=data.get('phone', '')
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor, 'Doctor added successfully'

    @staticmethod
    def update_doctor(doctor_id, data):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None, 'Doctor not found'

        if data.get('name'):
            doctor.user.name = data['name']
        if data.get('email'):
            doctor.user.email = data['email'].strip().lower()
        if data.get('speciality') is not None:
            doctor.speciality = data['speciality']
        if data.get('experience') is not None:
            doctor.experience = data['experience']
        if data.get('qualification') is not None:
            doctor.qualification = data['qualification']
        if data.get('designation') is not None:
            doctor.designation = data['designation']
        if data.get('phone') is not None:
            doctor.phone = data['phone']

        db.session.commit()
        return doctor, 'Doctor updated successfully'

    @staticmethod
    def delete_doctor(doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None, 'Doctor not found'

        user = doctor.user
        db.session.delete(doctor)
        db.session.delete(user)
        db.session.commit()
        return True, 'Doctor deleted successfully'

    @staticmethod
    def add_patient(data):
        email = data.get('email', '').strip().lower()
        if User.query.filter_by(email=email).first():
            return None, 'Email already exists'

        hashed = bcrypt.hashpw(
            data.get('password', 'Password123').encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(
            name=data.get('name', ''),
            email=email,
            password=hashed,
            role='PATIENT'
        )
        db.session.add(user)
        db.session.flush()

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
        return patient, 'Patient added successfully'

    @staticmethod
    def update_patient(patient_id, data):
        patient = Patient.query.get(patient_id)
        if not patient:
            return None, 'Patient not found'

        if data.get('name'):
            patient.user.name = data['name']
        if data.get('email'):
            patient.user.email = data['email'].strip().lower()
        if data.get('gender') is not None:
            patient.gender = data['gender']
        if data.get('mobile') is not None:
            patient.mobile = data['mobile']
        if data.get('dob') is not None:
            patient.dob = _parse_date(data.get('dob'))
        if data.get('address') is not None:
            patient.address = data['address']
        if data.get('medical_history') is not None:
            patient.medical_history = data['medical_history']

        db.session.commit()
        return patient, 'Patient updated successfully'

    @staticmethod
    def delete_patient(patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return None, 'Patient not found'

        user = patient.user
        db.session.delete(patient)
        db.session.delete(user)
        db.session.commit()
        return True, 'Patient deleted successfully'

    @staticmethod
    def get_all_doctors():
        return [d.to_dict() for d in Doctor.query.all()]

    @staticmethod
    def get_all_patients():
        return [p.to_dict() for p in Patient.query.all()]

    @staticmethod
    def get_all_appointments():
        return AppointmentService.get_all_appointments()

    @staticmethod
    def reschedule_appointment(appointment_id, new_date):
        return AppointmentService.reschedule_appointment(appointment_id, new_date)
