# app/db/repositories/base_repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """
    Generic repository for SQLAlchemy models.
    Provides basic CRUD operations and optional bulk operations.
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    # -------------------
    # Basic CRUD
    # -------------------
    
    def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by primary key"""
        return self.db.query(self.model).get(id)
    
    def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Return a list of records with optional pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj_in: Any, commit: bool = True) -> ModelType:
        """
        Create a single record.
        Accepts either:
        - Pydantic model with .dict() or .model_dump() method
        - SQLAlchemy model instance (already instantiated)
        - Dict
        """
        # If it's already a SQLAlchemy model instance, just add it
        if isinstance(obj_in, self.model):
            obj = obj_in
        # If it's a Pydantic model or has dict() method
        elif hasattr(obj_in, 'model_dump'):
            obj = self.model(**obj_in.model_dump())
        elif hasattr(obj_in, 'dict'):
            obj = self.model(**obj_in.dict())
        # If it's a plain dict
        elif isinstance(obj_in, dict):
            obj = self.model(**obj_in)
        else:
            raise ValueError(f"Unsupported input type: {type(obj_in)}")
        
        self.db.add(obj)
        if commit:
            self.db.commit()
            self.db.refresh(obj)
        return obj
    
    def create_many(self, objs_in: List[Any], commit: bool = True) -> List[ModelType]:
        """Bulk create records"""
        objs = []
        for obj_in in objs_in:
            if isinstance(obj_in, self.model):
                objs.append(obj_in)
            elif hasattr(obj_in, 'model_dump'):
                objs.append(self.model(**obj_in.model_dump()))
            elif hasattr(obj_in, 'dict'):
                objs.append(self.model(**obj_in.dict()))
            elif isinstance(obj_in, dict):
                objs.append(self.model(**obj_in))
            else:
                raise ValueError(f"Unsupported input type: {type(obj_in)}")
        
        self.db.add_all(objs)
        if commit:
            self.db.commit()
            for obj in objs:
                self.db.refresh(obj)
        return objs
    
    def delete(self, obj: ModelType, commit: bool = True) -> None:
        """Delete a record. Accepts the ORM object directly."""
        self.db.delete(obj)
        if commit:
            self.db.commit()
    
    def update(self, obj: ModelType, update_data: Dict[str, Any], commit: bool = True) -> ModelType:
        """
        Update an object partially using a dict of fields.
        Only updates keys present in update_data.
        """
        for key, value in update_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        if commit:
            self.db.commit()
            self.db.refresh(obj)
        return obj
    
    # -------------------
    # Utilities
    # -------------------
    
    def exists(self, id: int) -> bool:
        """Check if a record exists by ID"""
        return self.get(id) is not None