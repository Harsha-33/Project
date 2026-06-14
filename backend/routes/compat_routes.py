from flask import Blueprint, request

from database.db import db
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from models.appointment_model import Appointment
from models.doctor_model import Doctor
from models.patient_model import Patient
from services.admin_service import AdminService
from services.auth_service import AuthService
from services.consultation_service import ConsultationService
from services.doctor_service import DoctorService
from services.patient_service import PatientService
from utils.helpers import error_response, success_response

compat_bp = Blueprint('compat', __name__)


@compat_bp.route('/register', methods=['POST'])
def register():
    user, message = AuthService.register(request.get_json() or {})
    if not user:
        return error_response(message, 400)
    return success_response(user.to_dict(), message, 201)


@compat_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    result, message = AuthService.login(data.get('email'), data.get('password'))
    if not result:
        return error_response(message, 401)
    return success_response(result, message)


@compat_bp.route('/doctors', methods=['GET'])
@token_required
@role_required('ADMIN', 'PATIENT', 'DOCTOR')
def get_doctors():
    if request.current_user.role == 'ADMIN':
        return success_response(AdminService.get_all_doctors())
    return success_response(PatientService.get_doctors(
        search=request.args.get('search'),
        speciality=request.args.get('speciality')
    ))


@compat_bp.route('/doctor/<int:doctor_id>', methods=['GET'])
@token_required
@role_required('ADMIN', 'PATIENT', 'DOCTOR')
def get_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return error_response('Doctor not found', 404)
    return success_response(doctor.to_dict())


@compat_bp.route('/doctor', methods=['POST'])
@token_required
@role_required('ADMIN')
def add_doctor():
    doctor, message = AdminService.add_doctor(request.get_json() or {})
    if not doctor:
        return error_response(message, 400)
    return success_response(doctor.to_dict(), message, 201)


@compat_bp.route('/doctor/<int:doctor_id>', methods=['PUT'])
@token_required
@role_required('ADMIN')
def update_doctor(doctor_id):
    doctor, message = AdminService.update_doctor(doctor_id, request.get_json() or {})
    if not doctor:
        return error_response(message, 404)
    return success_response(doctor.to_dict(), message)


@compat_bp.route('/doctor/<int:doctor_id>', methods=['DELETE'])
@token_required
@role_required('ADMIN')
def delete_doctor(doctor_id):
    result, message = AdminService.delete_doctor(doctor_id)
    if not result:
        return error_response(message, 404)
    return success_response(message=message)


@compat_bp.route('/patients', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_patients():
    return success_response(AdminService.get_all_patients())


@compat_bp.route('/patient', methods=['POST'])
@token_required
@role_required('ADMIN')
def add_patient():
    patient, message = AdminService.add_patient(request.get_json() or {})
    if not patient:
        return error_response(message, 400)
    return success_response(patient.to_dict(), message, 201)


@compat_bp.route('/patient/<int:patient_id>', methods=['PUT'])
@token_required
@role_required('ADMIN')
def update_patient(patient_id):
    patient, message = AdminService.update_patient(patient_id, request.get_json() or {})
    if not patient:
        return error_response(message, 404)
    return success_response(patient.to_dict(), message)


@compat_bp.route('/patient/<int:patient_id>', methods=['DELETE'])
@token_required
@role_required('ADMIN')
def delete_patient(patient_id):
    result, message = AdminService.delete_patient(patient_id)
    if not result:
        return error_response(message, 404)
    return success_response(message=message)


@compat_bp.route('/appointment', methods=['POST'])
@token_required
@role_required('PATIENT')
def book_appointment():
    appointment, message = PatientService.book_appointment(request.current_user.id, request.get_json() or {})
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message, 201)


@compat_bp.route('/appointments', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_appointments():
    return success_response(AdminService.get_all_appointments())


@compat_bp.route('/appointments/patient/<int:patient_id>', methods=['GET'])
@token_required
@role_required('ADMIN', 'PATIENT')
def get_patient_appointments(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return error_response('Patient not found', 404)
    if request.current_user.role == 'PATIENT' and patient.user_id != request.current_user.id:
        return error_response('Access denied', 403)
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.appointment_date).all()
    return success_response([item.to_dict() for item in appointments])


@compat_bp.route('/appointments/doctor/<int:doctor_id>', methods=['GET'])
@token_required
@role_required('ADMIN', 'DOCTOR')
def get_doctor_appointments(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return error_response('Doctor not found', 404)
    if request.current_user.role == 'DOCTOR' and doctor.user_id != request.current_user.id:
        return error_response('Access denied', 403)
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.appointment_date).all()
    return success_response([item.to_dict() for item in appointments])


@compat_bp.route('/appointment/<int:appointment_id>', methods=['PUT'])
@token_required
@role_required('ADMIN', 'PATIENT')
def reschedule_appointment(appointment_id):
    data = request.get_json() or {}
    new_date = data.get('appointment_date')
    if not new_date:
        return error_response('appointment_date is required', 400)
    if request.current_user.role == 'PATIENT':
        appointment, message = PatientService.reschedule_appointment(
            request.current_user.id, appointment_id, new_date
        )
    else:
        appointment, message = AdminService.reschedule_appointment(appointment_id, new_date)
    if not appointment:
        return error_response(message, 400)
    return success_response(appointment.to_dict(), message)


@compat_bp.route('/appointment/<int:appointment_id>', methods=['DELETE'])
@token_required
@role_required('ADMIN')
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return error_response('Appointment not found', 404)
    db.session.delete(appointment)
    db.session.commit()
    return success_response(message='Appointment deleted successfully')


@compat_bp.route('/consultation', methods=['POST'])
@token_required
@role_required('DOCTOR')
def add_consultation():
    consultation, message = DoctorService.add_consultation(request.current_user.id, request.get_json() or {})
    if not consultation:
        return error_response(message, 400)
    return success_response(consultation.to_dict(), message, 201)


@compat_bp.route('/consultation/<int:appointment_id>', methods=['GET'])
@token_required
@role_required('ADMIN', 'DOCTOR', 'PATIENT')
def get_consultation_by_appointment(appointment_id):
    consultation = ConsultationService.get_by_appointment(appointment_id)
    if not consultation:
        return error_response('Consultation not found', 404)
    return success_response(consultation.to_dict())


@compat_bp.route('/consultation/<int:consultation_id>', methods=['PUT'])
@token_required
@role_required('ADMIN', 'DOCTOR')
def update_consultation(consultation_id):
    consultation, message = ConsultationService.update(consultation_id, request.get_json() or {})
    if not consultation:
        return error_response(message, 404)
    return success_response(consultation.to_dict(), message)
