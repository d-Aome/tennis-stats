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


class Response(BaseModel):
    success: bool
    msg: str


@router.post("/", status_code=status.HTTP_200_OK)
def post_match(match: Match, players: List[Particapant]):
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
    except sa.exc.SQLAlchemyError:
        return Response(success=False, msg="Internal Server Error")
    return Response(success=True, msg=f"match id: {match_id}")


@router.put("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_match(match_id: int, score: Match):
    try:
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
    except sa.exc.SQLAlchemyError:
        raise status.HTTP_500_INTERNAL_SERVER_ERROR


class CompleteMatch(BaseModel):
    score: str
    winning_team: int


@router.post("/{match_id}/complete", status_code=status.HTTP_200_OK)
def complete_match(match_id: int, completed_match: CompleteMatch):
    try:
        with db.engine.begin() as conn:
            match_exists = conn.execute(
                sa.text(
                    """
                    SELECT id
                    FROM matches
                    WHERE id = :match_id
                    FOR UPDATE
                    """
                ),
                {"match_id": match_id},
            ).first()

            if not match_exists:
                return Response(success=False, msg="Match not found")

            participants = (
                conn.execute(
                    sa.text(
                        """
                        SELECT player_id, team
                        FROM match_participants
                        WHERE match_id = :match_id
                        """
                    ),
                    {"match_id": match_id},
                )
                .mappings()
                .all()
            )

            if len(participants) < 2:
                return Response(success=False, msg="Match needs at least two players")

            teams = {player["team"] for player in participants}
            if completed_match.winning_team not in teams:
                return Response(success=False, msg="Winning team is not in this match")

            conn.execute(
                sa.text(
                    """
                    UPDATE matches
                    SET score = :score
                    WHERE id = :match_id
                    """
                ),
                {"score": completed_match.score, "match_id": match_id},
            )

            conn.execute(
                sa.text(
                    """
                    UPDATE match_participants
                    SET winner = (team = :winning_team)
                    WHERE match_id = :match_id
                    """
                ),
                {"winning_team": completed_match.winning_team, "match_id": match_id},
            )

            winning_players = [
                player["player_id"]
                for player in participants
                if player["team"] == completed_match.winning_team
            ]

            for player_id in winning_players:
                conn.execute(
                    sa.text(
                        """
                        UPDATE player_stats
                        SET matches_won = matches_won + 1
                        WHERE player_id = :player_id
                        """
                    ),
                    {"player_id": player_id},
                )
    except sa.exc.SQLAlchemyError:
        return Response(success=False, msg="Internal Server Error")
    return Response(success=True, msg="Match completed")
