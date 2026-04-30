"""Add cascade delete for user posts

Revision ID: 020054266e9e
Revises: e45be199c322
Create Date: 2026-04-24 21:41:10.769180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '020054266e9e'
down_revision: Union[str, Sequence[str], None] = 'e45be199c322'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Используем batch mode для SQLite (обходной путь)
    with op.batch_alter_table('blog_post') as batch_op:
        # Убираем NOT NULL у колонки author_id
        batch_op.alter_column('author_id', existing_type=sa.INTEGER(), nullable=True)

    # То же самое для комментариев
    with op.batch_alter_table('blog_comment') as batch_op:
        batch_op.alter_column('author_id', existing_type=sa.INTEGER(), nullable=True)

def downgrade() -> None:
    # Откат: снова делаем NOT NULL
    with op.batch_alter_table('blog_post') as batch_op:
        batch_op.alter_column('author_id', existing_type=sa.INTEGER(), nullable=False)

    with op.batch_alter_table('blog_comment') as batch_op:
        batch_op.alter_column('author_id', existing_type=sa.INTEGER(), nullable=False)