from datetime import datetime, timedelta
from database.db import db
from models.user_model import User
from models.doctor_model import Doctor
from models.patient_model import Patient
from models.appointment_model import Appointment
from models.consultation_model import Consultation

APPOINTMENT_LEAD_TIME = timedelta(hours=1)
RESCHEDULE_LOCK_TIME = timedelta(hours=1)
APPOINTMENT_SLOT_MINUTES = 30
WORKING_HOURS = range(9, 17)
ACTIVE_STATUSES = ['PENDING', 'CONFIRMED', 'ACCEPTED']


def _parse_appointment_date(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (AttributeError, ValueError):
        return None

    if parsed.tzinfo:
        parsed = parsed.astimezone().replace(tzinfo=None)
    return parsed


def _has_doctor_conflict(doctor_id, appointment_date, exclude_appointment_id=None):
    query = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status.in_(ACTIVE_STATUSES)
    )
    if exclude_appointment_id:
        query = query.filter(Appointment.appointment_id != exclude_appointment_id)
    return query.first() is not None


def _is_valid_appointment_slot(appointment_date):
    return (
        appointment_date.hour in WORKING_HOURS
        and appointment_date.minute in (0, APPOINTMENT_SLOT_MINUTES)
        and appointment_date.second == 0
        and appointment_date.microsecond == 0
    )


class PatientService:

    @staticmethod
    def get_doctors(search=None, speciality=None):
        query = Doctor.query

        terms = [value.strip() for value in (search, speciality) if value and value.strip()]
        if terms:
            query = query.join(User)
            for value in terms:
                term = f"%{value}%"
                query = query.filter(
                    db.or_(Doctor.speciality.ilike(term), User.name.ilike(term))
                )

        doctors = query.order_by(Doctor.speciality, Doctor.doctor_id).all()
        return [d.to_dict() for d in doctors]

    @staticmethod
    def get_doctor_availability(doctor_id, appointment_date):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None, 'Doctor not found'

        day = _parse_appointment_date(f'{appointment_date}T00:00:00')
        if not day:
            return None, 'Invalid date format. Use YYYY-MM-DD.'

        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date >= day_start,
            Appointment.appointment_date < day_end,
            Appointment.status.in_(ACTIVE_STATUSES)
        ).all()
        occupied = {a.appointment_date.strftime('%H:%M') for a in appointments}
        now = datetime.utcnow()
        slots = []
        for hour in WORKING_HOURS:
            for minute in (0, APPOINTMENT_SLOT_MINUTES):
                slot_dt = day_start.replace(hour=hour, minute=minute)
                slot = slot_dt.strftime('%H:%M')
                if slot not in occupied and slot_dt >= now + APPOINTMENT_LEAD_TIME:
                    slots.append(slot)

        return {
            'doctor': doctor.to_dict(),
            'date': appointment_date,
            'occupied_slots': sorted(occupied),
            'available_slots': slots
        }, 'Success'

    @staticmethod
    def get_patient_by_user_id(user_id):
        patient = Patient.query.filter_by(user_id=user_id).first()
        if patient:
            return patient

        user = User.query.get(user_id)
        if not user or user.role != 'PATIENT':
            return None

        patient = Patient(user_id=user_id, gender='', mobile='', address='', medical_history='')
        db.session.add(patient)
        db.session.commit()
        return patient

    @staticmethod
    def book_appointment(user_id, data):
        patient = PatientService.get_patient_by_user_id(user_id)
        if not patient:
            return None, 'Patient profile not found'

        doctor_id = data.get('doctor_id')
        appointment_date = data.get('appointment_date')
        if not doctor_id or not appointment_date:
            return None, 'doctor_id and appointment_date are required'

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None, 'Doctor not found'

        appt_date = _parse_appointment_date(appointment_date)
        if not appt_date:
            return None, 'Invalid appointment_date format. Use ISO format.'
        if appt_date < datetime.utcnow() + APPOINTMENT_LEAD_TIME:
            return None, 'Appointments must be booked at least 1 hour in advance'
        if not _is_valid_appointment_slot(appt_date):
            return None, 'Please choose one of the available 30-minute slots between 09:00 and 16:30'
        if _has_doctor_conflict(doctor_id, appt_date):
            return None, 'Doctor is not available at the selected time'

        appointment = Appointment(
            patient_id=patient.patient_id,
            doctor_id=doctor_id,
            appointment_date=appt_date,
            symptoms=data.get('symptoms', ''),
            visit_type=data.get('visit_type', 'In-Person'),
            status='PENDING'
        )
        db.session.add(appointment)
        db.session.commit()
        return appointment, 'Appointment booked successfully'

    @staticmethod
    def get_upcoming_appointments(user_id):
        patient = PatientService.get_patient_by_user_id(user_id)
        if not patient:
            return None, 'Patient profile not found'

        now = datetime.utcnow()
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.patient_id,
            Appointment.appointment_date >= now,
            Appointment.status.in_(ACTIVE_STATUSES)
        ).order_by(Appointment.appointment_date).all()

        return [a.to_dict() for a in appointments], 'Success'

    @staticmethod
    def reschedule_appointment(user_id, appointment_id, new_date):
        patient = PatientService.get_patient_by_user_id(user_id)
        if not patient:
            return None, 'Patient profile not found'

        appointment = Appointment.query.get(appointment_id)
        if not appointment or appointment.patient_id != patient.patient_id:
            return None, 'Appointment not found'

        if appointment.status in ('COMPLETED', 'REJECTED'):
            return None, 'Cannot reschedule this appointment'

        now = datetime.utcnow()
        if appointment.created_at and now < appointment.created_at + RESCHEDULE_LOCK_TIME:
            return None, 'Appointment cannot be rescheduled within 1 hour after booking'

        appt_date = _parse_appointment_date(new_date)
        if not appt_date:
            return None, 'Invalid date format'
        if appt_date < now + APPOINTMENT_LEAD_TIME:
            return None, 'Appointments must be scheduled at least 1 hour in advance'
        if not _is_valid_appointment_slot(appt_date):
            return None, 'Please choose one of the available 30-minute slots between 09:00 and 16:30'
        if _has_doctor_conflict(appointment.doctor_id, appt_date, appointment.appointment_id):
            return None, 'Doctor is not available at the selected time'

        appointment.appointment_date = appt_date
        appointment.status = 'PENDING'
        db.session.commit()
        return appointment, 'Appointment rescheduled successfully'

    @staticmethod
    def get_consultation_history(user_id):
        patient = PatientService.get_patient_by_user_id(user_id)
        if not patient:
            return None, 'Patient profile not found'

        appointments = Appointment.query.filter_by(
            patient_id=patient.patient_id,
            status='COMPLETED'
        ).all()

        history = []
        for appt in appointments:
            if appt.consultation:
                entry = appt.consultation.to_dict()
                entry['doctor_name'] = appt.doctor.user.name if appt.doctor and appt.doctor.user else None
                entry['appointment_date'] = appt.appointment_date.isoformat()
                history.append(entry)

        return history, 'Success'

    @staticmethod
    def get_dashboard_stats(user_id):
        patient = PatientService.get_patient_by_user_id(user_id)
        if not patient:
            return None, 'Patient profile not found'

        now = datetime.utcnow()
        upcoming = Appointment.query.filter(
            Appointment.patient_id == patient.patient_id,
            Appointment.appointment_date >= now,
            Appointment.status.in_(ACTIVE_STATUSES)
        ).count()

        completed = Appointment.query.filter_by(
            patient_id=patient.patient_id, status='COMPLETED'
        ).count()

        prescriptions = 0
        appointments = Appointment.query.filter_by(patient_id=patient.patient_id).all()
        for appt in appointments:
            if appt.consultation:
                prescriptions += len(appt.consultation.prescriptions)

        return {
            'upcoming_appointments': upcoming,
            'completed_consultations': completed,
            'prescriptions': prescriptions
        }, 'Success'
