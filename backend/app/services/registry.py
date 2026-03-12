from typing import Callable, Dict, Type
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class AssessmentConfig:
    specialty: str
    predict_fn: Callable
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]


ASSESSMENT_REGISTRY: Dict[str, AssessmentConfig] = {}


def register_assessment(
    assessment_type: str,
    specialty: str,
    predict_fn: Callable,
    input_schema: Type[BaseModel],
    output_schema: Type[BaseModel],
):

    if assessment_type in ASSESSMENT_REGISTRY:
        raise ValueError(f"Assessment already registered: {assessment_type}")

    ASSESSMENT_REGISTRY[assessment_type] = AssessmentConfig(
        specialty=specialty,
        predict_fn=predict_fn,
        input_schema=input_schema,
        output_schema=output_schema,
    )


def get_assessment_config(assessment_type: str) -> AssessmentConfig:

    config = ASSESSMENT_REGISTRY.get(assessment_type)

    if not config:
        raise ValueError(f"Unknown assessment type: {assessment_type}")

    return config


def list_supported_assessments():
    return list(ASSESSMENT_REGISTRY.keys())