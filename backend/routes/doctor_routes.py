from flask import Blueprint, request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from services.doctor_service import DoctorService
from utils.helpers import success_response, error_response

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/appointments', methods=['GET'])
@token_required
@role_required('DOCTOR')
def get_appointments():
    appointments, message = DoctorService.get_appointments(request.current_user.id)
    if appointments is None:
        return error_response(message, 404)
    return success_response(appointments)


@doctor_bp.route('/accept/<int:appointment_id>', methods=['PUT'])
@token_required
@role_required('DOCTOR')
def accept_appointment(appointment_id):
    appointment, message = DoctorService.accept_appointment(request.current_user.id, appointment_id)
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message)


@doctor_bp.route('/reject/<int:appointment_id>', methods=['PUT'])
@token_required
@role_required('DOCTOR')
def reject_appointment(appointment_id):
    appointment, message = DoctorService.reject_appointment(request.current_user.id, appointment_id)
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message)


@doctor_bp.route('/consultation', methods=['POST'])
@token_required
@role_required('DOCTOR')
def add_consultation():
    data = request.get_json() or {}
    consultation, message = DoctorService.add_consultation(request.current_user.id, data)
    if not consultation:
        return error_response(message, 400)
    return success_response(consultation.to_dict(), message, 201)


@doctor_bp.route('/prescription', methods=['POST'])
@token_required
@role_required('DOCTOR')
def add_prescription():
    data = request.get_json() or {}
    prescriptions, message = DoctorService.add_prescription(request.current_user.id, data)
    if not prescriptions:
        return error_response(message, 400)
    return success_response([p.to_dict() for p in prescriptions], message, 201)


@doctor_bp.route('/medicines', methods=['GET'])
@token_required
@role_required('DOCTOR')
def search_medicines():
    return success_response(DoctorService.search_medicines(request.args.get('search')))


@doctor_bp.route('/test', methods=['POST'])
@token_required
@role_required('DOCTOR')
def add_test():
    data = request.get_json() or {}
    test, message = DoctorService.add_test(request.current_user.id, data)
    if not test:
        return error_response(message, 400)
    return success_response(test.to_dict(), message, 201)


@doctor_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('DOCTOR')
def get_dashboard():
    stats, message = DoctorService.get_dashboard_stats(request.current_user.id)
    if stats is None:
        return error_response(message, 404)
    return success_response(stats)


@doctor_bp.route('/profile', methods=['GET'])
@token_required
@role_required('DOCTOR')
def get_profile():
    doctor = DoctorService.get_doctor_by_user_id(request.current_user.id)
    if not doctor:
        return error_response('Doctor profile not found', 404)
    return success_response(doctor.to_dict())
