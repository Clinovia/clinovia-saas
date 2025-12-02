from app.db.models.patients import Patient

from .base_repository import BaseRepository


class PatientRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(Patient, db)
