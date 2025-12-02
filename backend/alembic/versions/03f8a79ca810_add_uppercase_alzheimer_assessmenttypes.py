"""Add uppercase Alzheimer assessmenttypes

Revision ID: 03f8a79ca810
Revises: eb0dc38ea2bf
Create Date: 2025-11-24 16:40:50.107112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03f8a79ca810'
down_revision: Union[str, Sequence[str], None] = 'eb0dc38ea2bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE assessmenttype ADD VALUE IF NOT EXISTS 'ALZHEIMER_DIAGNOSIS_SCREENING';")
    op.execute("ALTER TYPE assessmenttype ADD VALUE IF NOT EXISTS 'ALZHEIMER_DIAGNOSIS_BASIC';")
    op.execute("ALTER TYPE assessmenttype ADD VALUE IF NOT EXISTS 'ALZHEIMER_DIAGNOSIS_EXTENDED';")
    op.execute("ALTER TYPE assessmenttype ADD VALUE IF NOT EXISTS 'ALZHEIMER_PROGNOSIS_2YR_BASIC';")
    op.execute("ALTER TYPE assessmenttype ADD VALUE IF NOT EXISTS 'ALZHEIMER_PROGNOSIS_2YR_EXTENDED';")

def downgrade():
    # Postgres cannot safely remove enum values
    pass
