"""add_images_table

Revision ID: cf883acf37b4
Revises: 5a8ba52342cc
Create Date: 2026-05-02 02:31:29.778246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'cf883acf37b4'
down_revision: Union[str, Sequence[str], None] = '5a8ba52342cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу image
    op.create_table('image',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('content_type', sa.String(length=20), nullable=False),
        sa.Column('object_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Удаляем поле image из blog_post
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.drop_column('image')


def downgrade() -> None:
    # Восстанавливаем поле image в blog_post
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    # Удаляем таблицу image
    op.drop_table('image')