"""add_unique_constraint_to_location_name

Revision ID: c616bffdde46
Revises: 93d6e353a017
Create Date: 2026-04-14 01:13:46.545736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c616bffdde46'
down_revision: Union[str, Sequence[str], None] = '93d6e353a017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
