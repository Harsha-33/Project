from flask import Blueprint, request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from services.patient_service import PatientService
from utils.helpers import success_response, error_response

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/doctors', methods=['GET'])
@token_required
@role_required('PATIENT')
def get_doctors():
    doctors = PatientService.get_doctors(
        search=request.args.get('search'),
        speciality=request.args.get('speciality')
    )
    return success_response(doctors)


@patient_bp.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
@token_required
@role_required('PATIENT')
def get_doctor_availability(doctor_id):
    appointment_date = request.args.get('date')
    if not appointment_date:
        return error_response('date is required', 400)

    availability, message = PatientService.get_doctor_availability(doctor_id, appointment_date)
    if availability is None:
        return error_response(message, 400)
    return success_response(availability)


@patient_bp.route('/appointment', methods=['POST'])
@token_required
@role_required('PATIENT')
def book_appointment():
    data = request.get_json() or {}
    appointment, message = PatientService.book_appointment(request.current_user.id, data)
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message, 201)


@patient_bp.route('/upcoming', methods=['GET'])
@token_required
@role_required('PATIENT')
def get_upcoming():
    appointments, message = PatientService.get_upcoming_appointments(request.current_user.id)
    if appointments is None:
        return error_response(message, 404)
    return success_response(appointments)


@patient_bp.route('/reschedule/<int:appointment_id>', methods=['PUT'])
@token_required
@role_required('PATIENT')
def reschedule(appointment_id):
    data = request.get_json() or {}
    new_date = data.get('appointment_date')
    if not new_date:
        return error_response('appointment_date is required', 400)

    appointment, message = PatientService.reschedule_appointment(
        request.current_user.id, appointment_id, new_date
    )
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message)


@patient_bp.route('/history', methods=['GET'])
@token_required
@role_required('PATIENT')
def get_history():
    history, message = PatientService.get_consultation_history(request.current_user.id)
    if history is None:
        return error_response(message, 404)
    return success_response(history)


@patient_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('PATIENT')
def get_dashboard():
    stats, message = PatientService.get_dashboard_stats(request.current_user.id)
    if stats is None:
        return error_response(message, 404)
    return success_response(stats)


@patient_bp.route('/profile', methods=['GET'])
@token_required
@role_required('PATIENT')
def get_profile():
    patient = PatientService.get_patient_by_user_id(request.current_user.id)
    if not patient:
        return error_response('Patient profile not found', 404)
    return success_response(patient.to_dict())
