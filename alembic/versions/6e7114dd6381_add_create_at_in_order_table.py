"""add create at in order table

Revision ID: 6e7114dd6381
Revises: b667c4998a4e
Create Date: 2026-01-11 21:38:21.068742

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision: str = '6e7114dd6381'
down_revision: Union[str, Sequence[str], None] = 'b667c4998a4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Add columns as NULLABLE first
    op.add_column('order', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('order', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Step 2: Set default value for existing rows
    op.execute(
        f"UPDATE \"order\" SET created_at = '{datetime.now(timezone.utc).isoformat()}' WHERE created_at IS NULL"
    )
    
    # Step 3: Make created_at NOT NULL
    op.alter_column('order', 'created_at', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('order', 'updated_at')
    op.drop_column('order', 'created_at')