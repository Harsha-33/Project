from flask import Blueprint, request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from services.consultation_service import ConsultationService
from utils.helpers import success_response, error_response

consultation_bp = Blueprint('consultation', __name__)


@consultation_bp.route('/<int:consultation_id>', methods=['GET'])
@token_required
@role_required('DOCTOR', 'PATIENT', 'ADMIN')
def get_consultation(consultation_id):
    consultation_obj = ConsultationService.get_by_appointment(consultation_id)
    consultation = consultation_obj.to_dict() if consultation_obj else ConsultationService.get_by_id(consultation_id)
    if not consultation:
        return error_response('Consultation not found', 404)
    return success_response(consultation)


@consultation_bp.route('/<int:consultation_id>', methods=['PUT'])
@token_required
@role_required('DOCTOR', 'ADMIN')
def update_consultation(consultation_id):
    consultation, message = ConsultationService.update(consultation_id, request.get_json() or {})
    if not consultation:
        return error_response(message, 404)
    return success_response(consultation.to_dict(), message)
