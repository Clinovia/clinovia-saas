from fastapi import APIRouter
from app.services.registry import ASSESSMENT_REGISTRY
from app.api.routes.utils.assessment_endpoint import create_assessment_endpoint

router = APIRouter()

def register_assessment_routes():

    specialty_routers = {}

    for assessment_type, config in ASSESSMENT_REGISTRY.items():

        specialty = config["specialty"]
        input_schema = config["input_schema"]

        # convert ALZHEIMER_DIAGNOSIS_BASIC → diagnosis-basic
        endpoint_path = assessment_type.lower().replace(f"{specialty}_", "").replace("_", "-")

        path = f"/{endpoint_path}"

        if specialty not in specialty_routers:

            specialty_routers[specialty] = APIRouter(
                prefix=f"/{specialty}",
                tags=[specialty.capitalize()]
            )

        create_assessment_endpoint(
            path=path,
            input_schema=input_schema,
            output_schema=dict,   # or your AssessmentOutputSchema
            assessment_type=assessment_type,
            router=specialty_routers[specialty],
        )

    return specialty_routers