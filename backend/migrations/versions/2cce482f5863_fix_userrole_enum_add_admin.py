"""fix_userrole_enum_add_admin

Revision ID: 2cce482f5863
Revises: 6067a91502e7
Create Date: 2025-12-30 23:21:37.327374

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2cce482f5863"
down_revision: Union[str, Sequence[str], None] = "6067a91502e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add ADMIN to userrole enum."""
    # Add ADMIN value to the existing userrole enum
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'ADMIN'")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL doesn't support removing enum values easily
    # This would require recreating the enum, which is complex
    # For now, we'll leave ADMIN in the enum even on downgrade
