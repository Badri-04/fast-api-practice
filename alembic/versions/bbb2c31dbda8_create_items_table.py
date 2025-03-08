"""create items table

Revision ID: bbb2c31dbda8
Revises: 
Create Date: 2025-03-08 13:01:23.800547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbb2c31dbda8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False)
        # sa.Column("count", sa.Integer, nullable=False),
        # sa.Column("rating", sa.Integer, server_default="3", nullable=False),
        # sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        # sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("items")
