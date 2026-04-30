"""add_cascade_delete_for_comments

Revision ID: 5a8ba52342cc
Revises: 020054266e9e
Create Date: 2026-05-01 01:09:12.128936

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '5a8ba52342cc'
down_revision: Union[str, Sequence[str], None] = '020054266e9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Отключаем проверку foreign keys
    op.execute("PRAGMA foreign_keys=OFF")

    # Создаем новую таблицу с CASCADE
    op.execute("""
        CREATE TABLE blog_comment_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME NOT NULL,
            text TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES auth_user (id),
            FOREIGN KEY (post_id) REFERENCES blog_post (id) ON DELETE CASCADE
        )
    """)

    # Копируем данные
    op.execute("""
        INSERT INTO blog_comment_new (id, created_at, text, author_id, post_id)
        SELECT id, created_at, text, author_id, post_id FROM blog_comment
    """)

    # Удаляем старую таблицу
    op.drop_table('blog_comment')

    # Переименовываем новую
    op.rename_table('blog_comment_new', 'blog_comment')

    # Включаем проверку обратно
    op.execute("PRAGMA foreign_keys=ON")

def downgrade() -> None:
    op.execute("PRAGMA foreign_keys=OFF")

    op.execute("""
        CREATE TABLE blog_comment_old (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME NOT NULL,
            text TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES auth_user (id),
            FOREIGN KEY (post_id) REFERENCES blog_post (id)
        )
    """)

    op.execute("""
        INSERT INTO blog_comment_old (id, created_at, text, author_id, post_id)
        SELECT id, created_at, text, author_id, post_id FROM blog_comment
    """)

    op.drop_table('blog_comment')
    op.rename_table('blog_comment_old', 'blog_comment')

    op.execute("PRAGMA foreign_keys=ON")