"""add foreign key to post table

Revision ID: b1da9901fb10
Revises: c311f821d275
Create Date: 2025-03-08 15:15:19.551730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1da9901fb10'
down_revision: Union[str, None] = 'c311f821d275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("items", sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("items", "owner_id")
