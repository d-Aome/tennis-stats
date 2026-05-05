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
    msg: str


class GetResponse(BaseModel):
    name: str
    utr: float
    first_serve_percentage: float
    second_serve_percentage: float
    matches_won: int


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_player(player: Player, stats: PlayerStatistics):
    try:
        with db.engine.begin() as conn:
            player_id = conn.execute(
                sa.text(
                    """
                        INSERT INTO players (name, utr_rating)
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
    except sa.exc.SQLAlchemyError:
        return PlayersResponse(success=False, msg="Internal Server Error")
    return PlayersResponse(success=True, msg=f"Player id: {player_id}")


@router.put("/{player_id}", status_code=status.HTTP_200_OK)
def update_player(statistics: PlayerStatistics, player_id: int):
    try:
        with db.engine.begin() as conn:
            conn.execute(
                sa.text(
                    """
                        UPDATE player_stats
                        SET
                            first_serve_percentage = :first,
                            second_serve_percentage = :second,
                            matches_won = :won
                        WHERE id = :id
                        RETURNING first_serve_percentage
                        """
                ),
                {
                    "first": statistics.first_serve_percentage,
                    "second": statistics.second_serve_percentage,
                    "won": statistics.matches_won,
                    "id": player_id,
                },
            )

    except sa.exc.SQLAlchemyError as e:
        print(f"Error updating player statistics {player_id}, {e}")
        raise
    return PlayersResponse(success=True, msg="")


@router.get("/{player_id}", status_code=status.HTTP_200_OK)
def get_player(player_id: int):
    try:
        with db.engine.begin() as conn:
            stats = conn.execute(
                sa.text(
                    """
                        SELECT name, utr_rating, first_serve_percentage, second_serve_percentage, matches_won
                        FROM players
                        LEFT JOIN player_stats ON player.id = player_stats.player_id
                        WHERE players.id = :id
                        """
                ),
                {"id": player_id},
            ).first()
            if not stats:
                return status.HTTP_404_NOT_FOUND

            return GetResponse(
                name=stats["name"],
                utr=stats["utr_rating"],
                first_serve_percentage=stats["first_serve_percentage"],
                second_serve_percentage=stats["second_serve_percentage"],
                matches_won=stats["matches_won"],
            )
    except sa.exc.SQLAlchemyError() as e:
        print(f"Error fetching Player statistics {player_id}, {e}")
        raise
