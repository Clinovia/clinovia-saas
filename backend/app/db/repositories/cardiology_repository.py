from app.db.models.cardiology import CardiologyAssessment

from .base_repository import BaseRepository


class CardiologyRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(CardiologyAssessment, db)

    def get_by_patient(self, patient_id: int):
        return (
            self.db.query(self.model).filter(self.model.patient_id == patient_id).all()
        )
