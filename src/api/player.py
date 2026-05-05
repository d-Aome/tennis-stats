import sqlalchemy as sa
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator, ConfigDict

from src import database as db
from src.api import auth
import sqlalchemy as sa

router = APIRouter(
    prefix="/players",
    tags=["player"],
    dependencies=[Depends(auth.get_api_key)],
)


class Player(BaseModel):
    name: str
    utr: float


class PlayerStatistics(BaseModel):
    first_serve_percentage: float
    second_serve_percentage: float
    matches_won: int


class PlayersResponse(BaseModel):
    success: bool


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_player(player: Player, stats: PlayerStatistics):
    with db.engine.begin() as conn:
        player_id = conn.execute(
            sa.text(
                """
                    INSERT INTO players (name, utr)
                    VALUES (:name, :utr)
                    RETURNING id
                    """
            ),
            {"name": player.name, "utr": player.utr},
        ).scalar_one()

        conn.execute(
            sa.text(
                """
                INSERT INTO  player_stats (player_id, first_serve_percentage, second_serve_percentage, matches_won)
                VALUES (:id, :first, :second, :won)
            """
            ),
            {
                "id": player_id,
                "first": stats.first_serve_percentage,
                "second": stats.second_serve_percentage,
                "won": stats.matches_won,
            },
        )


@router.put("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_player(statistics: PlayerStatistics, player_id: int):
    with db.engine.begin() as conn:
        conn.execute(
            sa.text(
                """
                    UPDATE player_stats
                    SET
                        first_serve_percentage = :first,
                        second_server_percentage = :second,
                        matches_won = :won
                    WHERE id = :id
                    """
            ),
            {
                "first": statistics.first_serve_percentage,
                "second": statistics.second_serve_percentage,
                "won": statistics.matches_won,
            },
        )
