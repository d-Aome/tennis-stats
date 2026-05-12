from typing import List

from dns import name
import sqlalchemy as sa
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator, ConfigDict

from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)


class Events(BaseModel):
    name: str | None
    participants_limit: int | None
    location: str | None
    date: str | None

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_event(event: Events):
    try:
        with db.engine.begin() as conn:
            event_id = conn.execute(
                sa.text(
                    """
                        INSERT INTO events (name, participants_limit, location, date)
                        VALUES (:name, :participants_limit, :location, :date)
                        RETURNING id
                        """
                ),
                {
                    "name": event.name,
                    "participants_limit": event.participants_limit,
                    "location": event.location,
                    "date": event.date
                },
            ).scalar_one()
    except sa.exc.SQLAlchemyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_201_CREATED


@router.get("/{events}", status_code=status.HTTP_200_OK, response_model=List[Events])
def get_events(events: Events):
    try:
        with db.engine.begin() as conn:
            result = conn.execute(
                sa.text(
                    """
                        SELECT name, participants_limit, location, date
                        FROM events
                        WHERE (:name IS NULL OR name = :name)
                            AND (:participants_limit IS NULL OR participants_limit = :participants_limit)
                            AND (:location IS NULL OR location = :location)
                            AND (:date IS NULL OR date = :date)
                    """
                ),
                {
                    "name": events.name,
                    "participants_limit": events.participants_limit,
                    "location": events.location,
                    "date": events.date,
                },
            ).mappings().all()
    except sa.exc.SQLAlchemyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return [Events(**i) for i in result]


@router.put("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_event(event_id: int, event: Events):
    try:
        with db.engine.begin() as conn:
            conn.execute(
                sa.text(
                    """
                        UPDATE events
                        SET 
                        name = COALESCE(:name, name),
                        participants_limit = COALESCE(:participants_limit, participants_limit),
                        location = COALESCE(:location, location),
                        date = COALESCE(:date, date)
                        WHERE id = :event_id
                        """
                ),
                {
                    "name": event.name,
                    "participants_limit": event.participants_limit,
                    "location": event.location,
                    "date": event.date,
                    "event_id": event_id
                },
            )
    except sa.exc.SQLAlchemyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_204_NO_CONTENT


@router.post("/{event_id}/{player_id}", status_code=status.HTTP_200_OK)
def add_player_to_event(event_id: int, player_id: int):
    try:
        with db.engine.begin() as conn:
            conn.execute(
                sa.text(
                    """
                        INSERT INTO event_participants (event_id, player_id)
                        VALUES (:event_id, :player_id)
                        """
                ),
                {
                    "event_id": event_id,
                    "player_id": player_id,
                },
            )
    except sa.exc.SQLAlchemyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_200_OK


    
 
