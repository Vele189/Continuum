"""add_skills_column_to_users

Revision ID: 6067a91502e7
Revises: 1ee4d637b125
Create Date: 2025-12-24 22:11:49.102652

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6067a91502e7"
down_revision: Union[str, Sequence[str], None] = "1ee4d637b125"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add skills column to users table as JSON (nullable)
    op.add_column(
        "users", sa.Column("skills", postgresql.JSON(astext_type=sa.Text()), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove skills column from users table
    op.drop_column("users", "skills")
