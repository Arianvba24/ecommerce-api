"""create posts table

Revision ID: 025521f3f162
Revises: 
Create Date: 2025-09-13 19:18:23.927395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '025521f3f162'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
    sa.Column("username",sa.String(length=17),nullable=False,unique=True),
    sa.Column("email",sa.String(length=30),nullable=False,unique=True),
    sa.Column("password",sa.String(length=150),nullable=False),
    # sa.Column("passwordddd",sa.String(length=150),nullable=False),
    sa.Column("create_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()")))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    # pass
