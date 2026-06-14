from database.db import db
from models.consultation_model import Consultation


class ConsultationService:

    @staticmethod
    def get_by_appointment(appointment_id):
        return Consultation.query.filter_by(appointment_id=appointment_id).first()

    @staticmethod
    def get_by_id(consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation:
            return consultation.to_dict()
        return None

    @staticmethod
    def update(consultation_id, data):
        consultation = Consultation.query.get(consultation_id)
        if not consultation:
            return None, 'Consultation not found'

        for field in ('current_symptoms', 'physical_examination', 'treatment_plan', 'diagnosis'):
            if data.get(field) is not None:
                setattr(consultation, field, data[field])

        db.session.commit()
        return consultation, 'Consultation updated successfully'
