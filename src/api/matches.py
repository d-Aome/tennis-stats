from typing import List

import sqlalchemy as sa
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator, ConfigDict

from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    dependencies=[Depends(auth.get_api_key)],
)


class Match(BaseModel):
    score: str


class Particapant(BaseModel):
    player_id: int
    winner: bool
    team: int


@router.post("/", status_code=status.HTTP_200_OK)
def post_match(match: Match, players: List[Particapant]):
    with db.engine.begin() as conn:
        match_id = conn.execute(
            sa.text(
                """
                    INSERT INTO matches (score)
                    VALUES (:score)
                    RETURNING id
                    """
            ),
            {"score": match.score},
        ).scalar_one()

        players_list = [
            {
                "player_id": player.player_id,
                "match_id": match_id,
                "winner": player.winner,
                "team": player.team,
            }
            for player in players
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

    return


@router.put("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_match(match_id: int, score: Match):
    with db.engine.begin() as conn:
        conn.execute(
            sa.text(
                """
                    UPDATE matches
                    SET 
                    score = :score
                    WHERE id = :match_id
                    """
            ),
            {"score": score.score, "match_id": match_id},
        )
