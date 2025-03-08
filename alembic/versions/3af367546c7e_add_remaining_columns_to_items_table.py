"""add remaining columns to items table

Revision ID: 3af367546c7e
Revises: b1da9901fb10
Create Date: 2025-03-08 15:20:08.891087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3af367546c7e'
down_revision: Union[str, None] = 'b1da9901fb10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("items", sa.Column("count", sa.Integer, nullable=False))
    op.add_column("items", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("items", "created_at")
    op.drop_column("items", "count")
