"""merge_repositories_and_work_sessions

Revision ID: 44eede3a242f
Revises: 8eaa9158ce3a, 9e70db09a665
Create Date: 2026-01-12 17:47:24.940624

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "44eede3a242f"
down_revision: Union[str, Sequence[str], None] = ("8eaa9158ce3a", "9e70db09a665")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
