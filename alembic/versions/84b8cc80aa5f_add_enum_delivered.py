"""add enum delivered

Revision ID: 84b8cc80aa5f
Revises: a25a3c36aa48
Create Date: 2026-01-28 00:03:41.664054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84b8cc80aa5f'
down_revision: Union[str, Sequence[str], None] = 'a25a3c36aa48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE orderstatus ADD VALUE IF NOT EXISTS 'delivered'")

def downgrade() -> None:
    raise NotImplementedError("Cannot safely downgrade enum change")
