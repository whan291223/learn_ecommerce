"""add enum shipped2

Revision ID: a25a3c36aa48
Revises: 9afc8b12164a
Create Date: 2026-01-27 23:53:59.360579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a25a3c36aa48'
down_revision: Union[str, Sequence[str], None] = '9afc8b12164a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE orderstatus ADD VALUE IF NOT EXISTS 'shipped'")

def downgrade() -> None:
    raise NotImplementedError("Cannot safely downgrade enum change")
