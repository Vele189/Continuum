"""merge_userrole_and_columns

Revision ID: 907048ce1217
Revises: 2cce482f5863, 9432fed5a01d
Create Date: 2025-12-31 00:43:15.904014

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "907048ce1217"
down_revision: Union[str, Sequence[str], None] = ("2cce482f5863", "9432fed5a01d")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Merge migration - no changes needed as both branches are already applied


def downgrade() -> None:
    """Downgrade schema."""
    # Merge migration - no changes needed
