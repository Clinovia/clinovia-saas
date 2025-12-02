"""add_alzheimer_prognosis_2yr_extended_enum

Revision ID: eb0dc38ea2bf
Revises: 50398906740c
Create Date: 2025-11-24 15:46:40.430668
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'eb0dc38ea2bf'
down_revision: Union[str, Sequence[str], None] = '50398906740c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add alzheimer_prognosis_2yr_extended to assessmenttype enum."""
    # Add new enum value if it doesn't exist
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'alzheimer_prognosis_2yr_extended' 
                AND enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'assessmenttype'
                )
            ) THEN
                ALTER TYPE assessmenttype ADD VALUE 'alzheimer_prognosis_2yr_extended';
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema.
    
    Note: PostgreSQL does not support removing enum values directly.
    To remove an enum value, you would need to:
    1. Create a new enum type without the value
    2. Alter all columns using the old enum to use the new enum
    3. Drop the old enum type
    4. Rename the new enum type to the old name
    
    This is complex and risky, so we skip it in downgrade.
    """
    pass