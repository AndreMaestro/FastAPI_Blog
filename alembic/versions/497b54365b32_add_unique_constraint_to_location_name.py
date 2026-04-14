"""add_unique_constraint_to_location_name

Revision ID: 497b54365b32
Revises: 93d6e353a017
Create Date: 2026-04-14 01:13:46.545736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '497b54365b32'
down_revision: Union[str, Sequence[str], None] = '93d6e353a017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('blog_location') as batch_op:
        batch_op.create_unique_constraint('uq_blog_location_name', ['name'])


def downgrade() -> None:
    with op.batch_alter_table('blog_location') as batch_op:
        batch_op.drop_constraint('uq_blog_location_name', type_='unique')
