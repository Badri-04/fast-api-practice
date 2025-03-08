"""add rating column to items table

Revision ID: 241d66769cf9
Revises: bbb2c31dbda8
Create Date: 2025-03-08 15:06:40.686436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '241d66769cf9'
down_revision: Union[str, None] = 'bbb2c31dbda8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("items", sa.Column("rating", sa.Integer, server_default="3", nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("items", "rating")
