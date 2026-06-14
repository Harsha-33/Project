from flask import Blueprint, request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from services.admin_service import AdminService
from utils.helpers import success_response, error_response

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_dashboard():
    return success_response(AdminService.get_dashboard_stats())


@admin_bp.route('/doctor', methods=['POST'])
@token_required
@role_required('ADMIN')
def add_doctor():
    data = request.get_json() or {}
    doctor, message = AdminService.add_doctor(data)
    if not doctor:
        return error_response(message, 400)
    return success_response(doctor.to_dict(), message, 201)


@admin_bp.route('/doctor/<int:doctor_id>', methods=['PUT'])
@token_required
@role_required('ADMIN')
def update_doctor(doctor_id):
    data = request.get_json() or {}
    doctor, message = AdminService.update_doctor(doctor_id, data)
    if not doctor:
        return error_response(message, 404)
    return success_response(doctor.to_dict(), message)


@admin_bp.route('/doctor/<int:doctor_id>', methods=['DELETE'])
@token_required
@role_required('ADMIN')
def delete_doctor(doctor_id):
    result, message = AdminService.delete_doctor(doctor_id)
    if not result:
        return error_response(message, 404)
    return success_response(message=message)


@admin_bp.route('/doctors', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_doctors():
    return success_response(AdminService.get_all_doctors())


@admin_bp.route('/patient', methods=['POST'])
@token_required
@role_required('ADMIN')
def add_patient():
    data = request.get_json() or {}
    patient, message = AdminService.add_patient(data)
    if not patient:
        return error_response(message, 400)
    return success_response(patient.to_dict(), message, 201)


@admin_bp.route('/patient/<int:patient_id>', methods=['PUT'])
@token_required
@role_required('ADMIN')
def update_patient(patient_id):
    data = request.get_json() or {}
    patient, message = AdminService.update_patient(patient_id, data)
    if not patient:
        return error_response(message, 404)
    return success_response(patient.to_dict(), message)


@admin_bp.route('/patient/<int:patient_id>', methods=['DELETE'])
@token_required
@role_required('ADMIN')
def delete_patient(patient_id):
    result, message = AdminService.delete_patient(patient_id)
    if not result:
        return error_response(message, 404)
    return success_response(message=message)


@admin_bp.route('/patients', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_patients():
    return success_response(AdminService.get_all_patients())


@admin_bp.route('/appointments', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_appointments():
    return success_response(AdminService.get_all_appointments())


@admin_bp.route('/reschedule/<int:appointment_id>', methods=['PUT'])
@token_required
@role_required('ADMIN')
def reschedule_appointment(appointment_id):
    data = request.get_json() or {}
    new_date = data.get('appointment_date')
    if not new_date:
        return error_response('appointment_date is required', 400)

    appointment, message = AdminService.reschedule_appointment(appointment_id, new_date)
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message)
