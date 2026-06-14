from datetime import datetime, timedelta
from database.db import db
from models.appointment_model import Appointment

APPOINTMENT_LEAD_TIME = timedelta(hours=1)
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


def _is_valid_appointment_slot(appointment_date):
    return (
        appointment_date.hour in WORKING_HOURS
        and appointment_date.minute in (0, APPOINTMENT_SLOT_MINUTES)
        and appointment_date.second == 0
        and appointment_date.microsecond == 0
    )


class AppointmentService:

    @staticmethod
    def get_all_appointments():
        appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
        return [a.to_dict() for a in appointments]

    @staticmethod
    def reschedule_appointment(appointment_id, new_date):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return None, 'Appointment not found'

        appt_date = _parse_appointment_date(new_date)
        if not appt_date:
            return None, 'Invalid date format'
        if appt_date < datetime.utcnow() + APPOINTMENT_LEAD_TIME:
            return None, 'Appointments must be scheduled at least 1 hour in advance'
        if not _is_valid_appointment_slot(appt_date):
            return None, 'Please choose one of the available 30-minute slots between 09:00 and 16:30'

        conflict = Appointment.query.filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_date == appt_date,
            Appointment.status.in_(ACTIVE_STATUSES),
            Appointment.appointment_id != appointment_id
        ).first()
        if conflict:
            return None, 'Doctor is not available at the selected time'

        appointment.appointment_date = appt_date
        db.session.commit()
        return appointment, 'Appointment rescheduled successfully'
