"""Fix duration column type

Revision ID: fix_duration_column
Revises: [get_previous_revision_id]  # Replace this with actual previous revision ID
Create Date: [current_date]
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fix_duration_column'
down_revision: Union[str, None] = '[previous_revision_id]'  # Replace with actual previous revision
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convert duration column to integer
    op.alter_column('courses', 'duration',
                    existing_type=sa.String(),
                    type_=sa.Integer(),
                    postgresql_using='duration::integer')


def downgrade() -> None:
    # Convert duration column back to string
    op.alter_column('courses', 'duration',
                    existing_type=sa.Integer(),
                    type_=sa.String(),
                    postgresql_using='duration::text') 