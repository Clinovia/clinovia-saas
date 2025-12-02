from app.db.models.alzheimer import AlzheimerAssessment

from .base_repository import BaseRepository


class AlzheimerRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(AlzheimerAssessment, db)

    def get_by_patient(self, patient_id: int):
        return (
            self.db.query(self.model).filter(self.model.patient_id == patient_id).all()
        )
