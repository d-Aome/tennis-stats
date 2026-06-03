import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator

from src import database as db
from src.api import auth

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

    @field_validator("first_serve_percentage", "second_serve_percentage")
    @classmethod
    def percentage_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Percentage must be between 0 and 100")
        return v

    @field_validator("matches_won")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("matches_won cannot be negative")
        return v


class PlayersResponse(BaseModel):
    success: bool
    msg: str


class GetResponse(BaseModel):
    name: str
    utr: float
    first_serve_percentage: float
    second_serve_percentage: float
    matches_won: int


class MatchHistoryItem(BaseModel):
    match_id: int
    score: str
    winner: bool
    team: int


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
                    INSERT INTO player_stats (player_id, first_serve_percentage, second_serve_percentage, matches_won)
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
            result = conn.execute(
                sa.text(
                    """
                    UPDATE player_stats
                    SET
                        first_serve_percentage = :first,
                        second_serve_percentage = :second,
                        matches_won = :won
                    WHERE player_id = :id
                    """
                ),
                {
                    "first": statistics.first_serve_percentage,
                    "second": statistics.second_serve_percentage,
                    "won": statistics.matches_won,
                    "id": player_id,
                },
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Player not found")
    except sa.exc.SQLAlchemyError:
        return PlayersResponse(success=False, msg="Internal Server Error")
    return PlayersResponse(success=True, msg="")


@router.get("/{player_id}", status_code=status.HTTP_200_OK)
def get_player(player_id: int):
    try:
        with db.engine.begin() as conn:
            stats = (
                conn.execute(
                    sa.text(
                        """
                        SELECT name, utr_rating, first_serve_percentage, second_serve_percentage, matches_won
                        FROM players
                        LEFT JOIN player_stats ON players.id = player_stats.player_id
                        WHERE players.id = :id
                        """
                    ),
                    {"id": player_id},
                )
                .mappings()
                .first()
            )

            if not stats:
                raise HTTPException(status_code=404, detail="Player not found")

            return GetResponse(
                name=stats["name"],
                utr=stats["utr_rating"],
                first_serve_percentage=stats["first_serve_percentage"],
                second_serve_percentage=stats["second_serve_percentage"],
                matches_won=stats["matches_won"],
            )
    except sa.exc.SQLAlchemyError:
        return PlayersResponse(success=False, msg="Internal Server Error")


@router.get("/{player_id}/matches", status_code=status.HTTP_200_OK)
def get_player_matches(player_id: int):
    try:
        with db.engine.begin() as conn:
            player = conn.execute(
                sa.text("SELECT id FROM players WHERE id = :id"),
                {"id": player_id},
            ).first()

            if not player:
                raise HTTPException(status_code=404, detail="Player not found")

            matches = (
                conn.execute(
                    sa.text(
                        """
                        SELECT matches.id AS match_id, matches.score, match_participants.winner, match_participants.team
                        FROM match_participants
                        JOIN matches ON match_participants.match_id = matches.id
                        WHERE match_participants.player_id = :player_id
                        ORDER BY matches.id DESC
                        """
                    ),
                    {"player_id": player_id},
                )
                .mappings()
                .all()
            )

            return [
                MatchHistoryItem(
                    match_id=row["match_id"],
                    score=row["score"],
                    winner=row["winner"],
                    team=row["team"],
                )
                for row in matches
            ]
    except sa.exc.SQLAlchemyError:
        return PlayersResponse(success=False, msg="Internal Server Error")
