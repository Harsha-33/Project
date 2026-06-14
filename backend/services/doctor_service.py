from datetime import datetime, date
from database.db import db
from models.doctor_model import Doctor
from models.appointment_model import Appointment
from models.consultation_model import Consultation
from models.prescription_model import Prescription
from models.medical_test_model import MedicalTest

MEDICINES = [
    'Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Azithromycin', 'Cetirizine',
    'Metformin', 'Amlodipine', 'Atorvastatin', 'Omeprazole', 'Pantoprazole',
    'Losartan', 'Dolo 650', 'Aspirin', 'Cefixime', 'Montelukast',
    'Salbutamol', 'Levocetirizine', 'Vitamin D3', 'B Complex', 'ORS'
]
ACTIVE_STATUSES = ['PENDING', 'CONFIRMED', 'ACCEPTED']


class DoctorService:

    @staticmethod
    def get_doctor_by_user_id(user_id):
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if doctor:
            return doctor

        from models.user_model import User

        user = User.query.get(user_id)
        if not user or user.role != 'DOCTOR':
            return None

        doctor = Doctor(
            user_id=user_id,
            speciality='',
            experience=0,
            qualification='',
            designation=''
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor

    @staticmethod
    def get_appointments(user_id):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        appointments = Appointment.query.filter_by(
            doctor_id=doctor.doctor_id
        ).order_by(Appointment.appointment_date).all()

        return [a.to_dict() for a in appointments], 'Success'

    @staticmethod
    def accept_appointment(user_id, appointment_id):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        appointment = Appointment.query.get(appointment_id)
        if not appointment or appointment.doctor_id != doctor.doctor_id:
            return None, 'Appointment not found'

        if appointment.status != 'PENDING':
            return None, 'Only pending appointments can be accepted'

        appointment.status = 'CONFIRMED'
        db.session.commit()
        return appointment, 'Appointment accepted'

    @staticmethod
    def reject_appointment(user_id, appointment_id):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        appointment = Appointment.query.get(appointment_id)
        if not appointment or appointment.doctor_id != doctor.doctor_id:
            return None, 'Appointment not found'

        if appointment.status != 'PENDING':
            return None, 'Only pending appointments can be rejected'

        appointment.status = 'REJECTED'
        db.session.commit()
        return appointment, 'Appointment rejected'

    @staticmethod
    def add_consultation(user_id, data):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        appointment_id = data.get('appointment_id')
        if not appointment_id:
            return None, 'appointment_id is required'

        appointment = Appointment.query.get(appointment_id)
        if not appointment or appointment.doctor_id != doctor.doctor_id:
            return None, 'Appointment not found'

        if appointment.status not in ('CONFIRMED', 'ACCEPTED'):
            return None, 'Appointment must be confirmed before consultation'

        existing = Consultation.query.filter_by(appointment_id=appointment_id).first()
        if existing:
            existing.current_symptoms = data.get('current_symptoms', existing.current_symptoms)
            existing.physical_examination = data.get('physical_examination', existing.physical_examination)
            existing.treatment_plan = data.get('treatment_plan', existing.treatment_plan)
            existing.diagnosis = data.get('diagnosis', existing.diagnosis)
            consultation = existing
        else:
            consultation = Consultation(
                appointment_id=appointment_id,
                current_symptoms=data.get('current_symptoms', ''),
                physical_examination=data.get('physical_examination', ''),
                treatment_plan=data.get('treatment_plan', ''),
                diagnosis=data.get('diagnosis', '')
            )
            db.session.add(consultation)

        appointment.status = 'COMPLETED'
        db.session.commit()
        return consultation, 'Consultation saved successfully'

    @staticmethod
    def add_prescription(user_id, data):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        consultation_id = data.get('consultation_id')
        prescriptions = data.get('prescriptions')
        if prescriptions is None:
            prescriptions = [{
                'medicine_name': data.get('medicine_name'),
                'dosage': data.get('dosage', ''),
                'timing': data.get('timing', '')
            }]
        if not consultation_id or not prescriptions:
            return None, 'consultation_id and at least one prescription are required'

        consultation = Consultation.query.get(consultation_id)
        if not consultation:
            return None, 'Consultation not found'

        if consultation.appointment.doctor_id != doctor.doctor_id:
            return None, 'Access denied'

        saved = []
        for item in prescriptions:
            medicine_name = (item.get('medicine_name') or '').strip()
            if not medicine_name:
                continue
            prescription = Prescription(
                consultation_id=consultation_id,
                medicine_name=medicine_name,
                dosage=item.get('dosage', ''),
                timing=item.get('timing', '')
            )
            db.session.add(prescription)
            saved.append(prescription)

        if not saved:
            return None, 'At least one medicine name is required'

        db.session.commit()
        return saved, 'Prescriptions added'

    @staticmethod
    def search_medicines(search):
        term = (search or '').strip().lower()
        if not term:
            return MEDICINES[:10]
        return [name for name in MEDICINES if term in name.lower()][:10]

    @staticmethod
    def add_test(user_id, data):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        consultation_id = data.get('consultation_id')
        test_name = data.get('test_name')
        if not consultation_id or not test_name:
            return None, 'consultation_id and test_name are required'

        consultation = Consultation.query.get(consultation_id)
        if not consultation:
            return None, 'Consultation not found'

        if consultation.appointment.doctor_id != doctor.doctor_id:
            return None, 'Access denied'

        test = MedicalTest(consultation_id=consultation_id, test_name=test_name)
        db.session.add(test)
        db.session.commit()
        return test, 'Medical test recommended'

    @staticmethod
    def get_dashboard_stats(user_id):
        doctor = DoctorService.get_doctor_by_user_id(user_id)
        if not doctor:
            return None, 'Doctor profile not found'

        today = date.today()
        appointments = Appointment.query.filter_by(doctor_id=doctor.doctor_id).all()

        today_count = sum(
            1 for a in appointments
            if a.appointment_date and a.appointment_date.date() == today
            and a.status in ACTIVE_STATUSES
        )
        pending = sum(1 for a in appointments if a.status == 'PENDING')
        completed = sum(1 for a in appointments if a.status == 'COMPLETED')

        return {
            'today_appointments': today_count,
            'pending_requests': pending,
            'completed_consultations': completed
        }, 'Success'
