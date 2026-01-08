"""fix_userrole_enum_add_admin

Revision ID: 688c93541523
Revises: 6067a91502e7
Create Date: 2025-12-27 09:03:35.381907

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "688c93541523"
down_revision: Union[str, Sequence[str], None] = "6067a91502e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add 'ADMIN' value to userrole enum
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'ADMIN'")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type, which is complex
    # For now, we'll leave it as-is
    pass
