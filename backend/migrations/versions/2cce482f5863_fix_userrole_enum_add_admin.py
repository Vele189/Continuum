"""fix_userrole_enum_add_admin

Revision ID: 2cce482f5863
Revises: 6067a91502e7
Create Date: 2025-12-30 23:21:37.327374

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2cce482f5863"
down_revision: Union[str, Sequence[str], None] = "6067a91502e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
