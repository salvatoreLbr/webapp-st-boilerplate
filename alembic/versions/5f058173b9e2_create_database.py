"""create database

Revision ID: 5f058173b9e2
Revises:
Create Date: 2025-05-12 22:38:31.610152

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5f058173b9e2"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "Entity",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entityName", sa.String(length=100)),
    )
    op.create_table(
        "User",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entityId", sa.Integer(), sa.ForeignKey("Entity.id")),
        sa.Column("name", sa.String(length=100)),
        sa.Column("email", sa.String(length=100)),
        sa.Column("password", sa.String(length=100)),
        sa.Column("role", sa.String(length=5)),
        sa.Column("disabled", sa.Boolean()),
        sa.Column("lastLogin", sa.DateTime()),
        sa.Column("createdDate", sa.DateTime()),
        sa.Column("updatedDate", sa.DateTime()),
    )


def downgrade():
    op.drop_table("User")
    op.drop_table("Entity")
