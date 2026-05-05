"""add columns to match participants

Revision ID: 2d932183d629
Revises: 0bdf2d51315c
Create Date: 2026-05-04 23:47:18.567802

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d932183d629"
down_revision: Union[str, Sequence[str], None] = "0bdf2d51315c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "match_participants", sa.Column("winner", sa.Boolean(), server_default="False")
    )
    op.add_column(
        "match_participants",
        sa.Column(
            "team",
            sa.Integer(),
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("match_participants", "winner")
    op.drop_column("match_participants", "team")
    pass
