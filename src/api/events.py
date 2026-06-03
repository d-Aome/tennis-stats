from typing import List

import sqlalchemy as sa
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)


class Event(BaseModel):
    name: str
    limit: int
    location: str


class AddPlayer(BaseModel):
    player_id: int


class EventResponse(BaseModel):
    success: bool
    msg: str


class EventParticipant(BaseModel):
    player_id: int
    name: str
    utr: float | None


class EventParticipantsResponse(BaseModel):
    event_id: int
    event_name: str
    participant_limit: int
    participants: List[EventParticipant]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(new_event: Event):
    try:
        with db.engine.begin() as conn:
            event_id = conn.execute(
                sa.text(
                    """
                    INSERT INTO events (name, participant_limit, location)
                    VALUES (:name, :participant_limit, :location)
                    RETURNING id
                    """
                ),
                {
                    "name": new_event.name,
                    "participant_limit": new_event.limit,
                    "location": new_event.location,
                },
            ).scalar_one()
    except sa.exc.SQLAlchemyError:
        return EventResponse(success=False, msg="Internal Server Error")
    return EventResponse(success=True, msg=f"Event id: {event_id}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_events(name: str = None, location: str = None):
    try:
        with db.engine.begin() as conn:
            query = "SELECT id, name, participant_limit, location FROM events WHERE 1=1"
            params = {}
            if name:
                query += " AND name ILIKE :name"
                params["name"] = f"%{name}%"
            if location:
                query += " AND location ILIKE :location"
                params["location"] = f"%{location}%"

            events = conn.execute(sa.text(query), params).mappings().all()
            return [dict(e) for e in events]
    except sa.exc.SQLAlchemyError:
        return EventResponse(success=False, msg="Internal Server Error")


@router.post("/{event_id}/players", status_code=status.HTTP_200_OK)
def add_player_to_event(event_id: int, player: AddPlayer):
    try:
        with db.engine.begin() as conn:
            event = (
                conn.execute(
                    sa.text(
                        """
                        SELECT id, participant_limit
                        FROM events
                        WHERE id = :event_id
                        FOR UPDATE
                        """
                    ),
                    {"event_id": event_id},
                )
                .mappings()
                .first()
            )

            if not event:
                return EventResponse(success=False, msg="Event not found")

            player_exists = conn.execute(
                sa.text(
                    """
                    SELECT id
                    FROM players
                    WHERE id = :player_id
                    """
                ),
                {"player_id": player.player_id},
            ).first()

            if not player_exists:
                return EventResponse(success=False, msg="Player not found")

            already_joined = conn.execute(
                sa.text(
                    """
                    SELECT id
                    FROM event_participants
                    WHERE event_id = :event_id AND player_id = :player_id
                    """
                ),
                {"event_id": event_id, "player_id": player.player_id},
            ).first()

            if already_joined:
                return EventResponse(success=False, msg="Player already in event")

            participant_count = conn.execute(
                sa.text(
                    """
                    SELECT COUNT(*)
                    FROM event_participants
                    WHERE event_id = :event_id
                    """
                ),
                {"event_id": event_id},
            ).scalar_one()

            if participant_count >= event["participant_limit"]:
                return EventResponse(success=False, msg="Event is full")

            conn.execute(
                sa.text(
                    """
                    INSERT INTO event_participants (event_id, player_id)
                    VALUES (:event_id, :player_id)
                    """
                ),
                {"event_id": event_id, "player_id": player.player_id},
            )
    except sa.exc.SQLAlchemyError:
        return EventResponse(success=False, msg="Internal Server Error")
    return EventResponse(success=True, msg="Player added to event")


@router.get("/{event_id}/players", status_code=status.HTTP_200_OK)
def get_event_players(event_id: int):
    try:
        with db.engine.begin() as conn:
            event = (
                conn.execute(
                    sa.text(
                        """
                        SELECT id, name, participant_limit
                        FROM events
                        WHERE id = :event_id
                        """
                    ),
                    {"event_id": event_id},
                )
                .mappings()
                .first()
            )

            if not event:
                return EventResponse(success=False, msg="Event not found")

            participants = (
                conn.execute(
                    sa.text(
                        """
                        SELECT players.id AS player_id, players.name, players.utr_rating
                        FROM event_participants
                        JOIN players ON event_participants.player_id = players.id
                        WHERE event_participants.event_id = :event_id
                        ORDER BY players.utr_rating DESC NULLS LAST, players.name
                        """
                    ),
                    {"event_id": event_id},
                )
                .mappings()
                .all()
            )

            return EventParticipantsResponse(
                event_id=event["id"],
                event_name=event["name"],
                participant_limit=event["participant_limit"],
                participants=[
                    EventParticipant(
                        player_id=row["player_id"],
                        name=row["name"],
                        utr=row["utr_rating"],
                    )
                    for row in participants
                ],
            )
    except sa.exc.SQLAlchemyError:
        return EventResponse(success=False, msg="Internal Server Error")