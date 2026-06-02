"""Add performce indexes

Revision ID: f8bc334a308f
Revises: 2d932183d629
Create Date: 2026-06-02 12:04:48.743098

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f8bc334a308f"
down_revision: Union[str, Sequence[str], None] = "2d932183d629"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        "idx_match_participants_match_id",  # Index name
        "match_participants",  # Table name
        ["match_id"],  # Column(s)
    )

    op.create_index("idx_player_stats_player_id", "player_stats", ["player_id"])


def downgrade():
    op.drop_index("idx_player_stats_player_id", table_name="player_stats")

    op.drop_index("idx_match_participants_match_id", table_name="match_participants")
