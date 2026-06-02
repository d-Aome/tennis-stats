from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Assuming your Player model from earlier
class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    utr_rating = Column(Float, nullable=True)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    participant_limit = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=True)
    location = Column(String, nullable=False)
    format = Column(String, nullable=True)


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(String, nullable=False)


class MatchParticipant(Base):
    __tablename__ = "match_participants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner = Column(Boolean, default=False)
    team = Column(Integer, nullable=True)


class PlayerStat(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    first_serve_percentage = Column(Float, nullable=True)
    second_serve_percentage = Column(Float, nullable=True)
    matches_won = Column(Integer, nullable=False, default=0)


class EventParticipant(Base):
    __tablename__ = "event_participants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
