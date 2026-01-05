"""add_missing_columns_api_key_and_updated_at

Revision ID: 9432fed5a01d
Revises: 688c93541523
Create Date: 2025-12-27 09:17:24.335751

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9432fed5a01d"
down_revision: Union[str, Sequence[str], None] = "688c93541523"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add api_key column to clients table
    op.add_column(
        "clients",
        sa.Column("api_key", sa.String(length=255), nullable=True),
    )
    # Create unique index on api_key
    op.create_index("ix_clients_api_key", "clients", ["api_key"], unique=True)

    # Add updated_at column to clients table
    op.add_column(
        "clients",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    # Add updated_at column to projects table
    op.add_column(
        "projects",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("projects", "updated_at")
    op.drop_column("clients", "updated_at")
    op.drop_index("ix_clients_api_key", table_name="clients")
    op.drop_column("clients", "api_key")
