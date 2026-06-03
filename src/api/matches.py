from typing import List, Optional

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    dependencies=[Depends(auth.get_api_key)],
)


class Match(BaseModel):
    score: Optional[str] = None


class Particapant(BaseModel):
    player_id: int
    winner: bool
    team: int


class MatchRequest(BaseModel):
    match: Match
    players: List[Particapant]


class Response(BaseModel):
    success: bool
    msg: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_match(body: MatchRequest):
    if len(body.players) not in (2, 4):
        return Response(success=False, msg="A match must have exactly 2 or 4 players")

    player_ids = [p.player_id for p in body.players]
    if len(player_ids) != len(set(player_ids)):
        return Response(success=False, msg="Duplicate player_id in players list")

    try:
        with db.engine.begin() as conn:
            match_id = conn.execute(
                sa.text(
                    """
                    INSERT INTO matches (score)
                    VALUES (:score)
                    RETURNING id
                    """
                ),
                {"score": body.match.score},
            ).scalar_one()

            players_list = [
                {
                    "player_id": player.player_id,
                    "match_id": match_id,
                    "winner": player.winner,
                    "team": player.team,
                }
                for player in body.players
            ]

            conn.execute(
                sa.text(
                    """
                    INSERT INTO match_participants (player_id, match_id, winner, team)
                    VALUES (:player_id, :match_id, :winner, :team)
                    """
                ),
                players_list,
            )
    except sa.exc.SQLAlchemyError:
        return Response(success=False, msg="Internal Server Error")
    return Response(success=True, msg=f"match id: {match_id}")


@router.put("/{match_id}", status_code=status.HTTP_200_OK)
def update_match(match_id: int, score: Match):
    try:
        with db.engine.begin() as conn:
            result = conn.execute(
                sa.text(
                    """
                    UPDATE matches
                    SET score = :score
                    WHERE id = :match_id
                    """
                ),
                {"score": score.score, "match_id": match_id},
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Match not found")
    except sa.exc.SQLAlchemyError:
        return Response(success=False, msg="Internal Server Error")
    return Response(success=True, msg="")