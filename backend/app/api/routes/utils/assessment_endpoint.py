# backend/app/api/routes/utils/assessment_endpoint.py

"""
Supabase-only assessment endpoint factory.
"""

import traceback
from fastapi import APIRouter, HTTPException, status
from typing import Type

from app.api.deps import CurrentUser
from app.schemas.base import AssessmentInputSchema, AssessmentOutputSchema
from app.services.assessment_engine import AssessmentEngine

engine = AssessmentEngine()


def create_assessment_endpoint(
    *,
    path: str,
    input_schema: Type[AssessmentInputSchema],
    output_schema: Type[AssessmentOutputSchema],
    assessment_type: str,
    router: APIRouter,
):

    @router.post(
        path,
        response_model=output_schema,
        status_code=status.HTTP_200_OK,
    )
    async def assessment_endpoint(
        input_data: input_schema,
        current_user: CurrentUser,
    ):
        try:

            result = engine.run_assessment(
                assessment_type=assessment_type,
                clinician_id=current_user.id,
                patient_id=input_data.patient_id,
                input_data=input_data.model_dump(),
            )

            return result

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{assessment_type} failed: {str(e)} | {traceback.format_exc()}",
            )

    assessment_endpoint.__name__ = f"{assessment_type.replace('-', '_')}_endpoint"

    return assessment_endpoint