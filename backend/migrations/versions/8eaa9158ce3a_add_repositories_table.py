"""Add repositories table

Revision ID: 8eaa9158ce3a
Revises: 907048ce1217
Create Date: 2026-01-08 19:50:31.135644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eaa9158ce3a'
down_revision: Union[str, Sequence[str], None] = '907048ce1217'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'repositories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('repository_url', sa.String(), nullable=False),
        sa.Column('repository_name', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('webhook_secret', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('repository_url')
    )
    op.create_index(op.f('ix_repositories_id'), 'repositories', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_repositories_id'), table_name='repositories')
    op.drop_table('repositories')
