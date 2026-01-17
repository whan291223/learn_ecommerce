"""change bath to baht, add order status

Revision ID: ae5f70e13fc4
Revises: 6e7114dd6381
Create Date: 2026-01-15 22:41:37.328792
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ae5f70e13fc4"
down_revision: Union[str, Sequence[str], None] = "6e7114dd6381"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1️⃣ Rename columns safely (keeps existing data)
    op.alter_column(
        "order",
        "total_price_baths",
        new_column_name="total_price_bahts",
        existing_type=sa.Integer(),
    )

    op.alter_column(
        "orderitem",
        "price_at_purchase_baths",
        new_column_name="price_at_purchase_bahts",
        existing_type=sa.Integer(),
    )

    # 2️⃣ Add new datetime columns (nullable = safe for existing rows)
    op.add_column("order", sa.Column("paid_at", sa.DateTime(), nullable=True))
    op.add_column("order", sa.Column("expired_at", sa.DateTime(), nullable=True))
    op.add_column("order", sa.Column("cancelled_at", sa.DateTime(), nullable=True))
    op.add_column("order", sa.Column("shipped_at", sa.DateTime(), nullable=True))
    op.add_column("order", sa.Column("delivered_at", sa.DateTime(), nullable=True))

    # 3️⃣ Create enum explicitly
    order_status_enum = sa.Enum(
        "pending",
        "paid",
        "cancelled",
        "expired",
        name="orderstatus",
    )
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # 4️⃣ Convert status column from VARCHAR -> ENUM (explicit cast)
    op.alter_column(
        "order",
        "status",
        existing_type=sa.VARCHAR(),
        type_=order_status_enum,
        postgresql_using="status::orderstatus",
        existing_nullable=False,
    )


def downgrade() -> None:
    # 1️⃣ Convert ENUM back to VARCHAR
    op.alter_column(
        "order",
        "status",
        existing_type=sa.Enum(
            "pending",
            "paid",
            "cancelled",
            "expired",
            name="orderstatus",
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    # 2️⃣ Drop datetime columns
    op.drop_column("order", "delivered_at")
    op.drop_column("order", "shipped_at")
    op.drop_column("order", "cancelled_at")
    op.drop_column("order", "expired_at")
    op.drop_column("order", "paid_at")

    # 3️⃣ Rename columns back
    op.alter_column(
        "order",
        "total_price_bahts",
        new_column_name="total_price_baths",
        existing_type=sa.Integer(),
    )

    op.alter_column(
        "orderitem",
        "price_at_purchase_bahts",
        new_column_name="price_at_purchase_baths",
        existing_type=sa.Integer(),
    )

    # 4️⃣ Drop enum type (cleanup)
    sa.Enum(
        "pending",
        "paid",
        "cancelled",
        "expired",
        name="orderstatus",
    ).drop(op.get_bind(), checkfirst=True)
