import random as rand
from faker import Faker
from sqlalchemy.orm import sessionmaker

from src.database import engine

from src.models import (
    Event,
    Player,
    PlayerStat,
    Match,
    MatchParticipant,
    EventParticipant,
)

fake = Faker()


def generate_players(num_players):
    if num_players <= 0:
        return []

    players = []
    for _ in range(num_players):
        players.append(
            Player(name=fake.name(), utr_rating=round(rand.uniform(1.0, 16.5), 2))
        )
    return players


def generate_events(num_events):
    if num_events <= 0:
        return []

    events = []
    for _ in range(num_events):
        events.append(
            Event(
                name=f"{fake.city()} Open",
                participant_limit=rand.choice([32, 64, 128]),
                start_time=fake.date_time_this_year(),
                location=fake.address()[:50],
                format=rand.choice(["Singles", "Doubles"]),
            )
        )
    return events


def generate_player_stats(num_players):
    if num_players <= 0:
        return []

    stats = []
    for player_id in range(1, num_players + 1):
        stats.append(
            PlayerStat(
                player_id=player_id,
                first_serve_percentage=round(rand.uniform(45.0, 75.0), 2),
                second_serve_percentage=round(rand.uniform(70.0, 95.0), 2),
                matches_won=rand.randint(0, 150),
            )
        )
    return stats


def get_match_participants(match_id, p1_id, p2_id, winner_id):
    if p1_id == p2_id:
        return []

    p1_won = p1_id == winner_id
    p2_won = p2_id == winner_id

    return [
        MatchParticipant(match_id=match_id, player_id=p1_id, winner=p1_won, team=1),
        MatchParticipant(match_id=match_id, player_id=p2_id, winner=p2_won, team=2),
    ]


def seed_million_rows():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if session.query(Player).count() > 0:
            print("Database already seeded. Aborting.")
            return

        TOTAL_PLAYERS = 20000
        TOTAL_MATCHES = 320000
        TOTAL_EVENTS = 1000
        CHUNK_SIZE = 10000

        print(f"Seeding {TOTAL_PLAYERS} players...")
        players = generate_players(TOTAL_PLAYERS)
        session.bulk_save_objects(players)
        session.commit()

        print(f"Seeding {TOTAL_EVENTS} events...")
        events = generate_events(TOTAL_EVENTS)
        session.bulk_save_objects(events)
        session.commit()

        print("Seeding event participants...")
        db_events = session.query(Event).all()
        event_participants = []

        for event in db_events:
            roster_ids = rand.sample(
                range(1, TOTAL_PLAYERS + 1), event.participant_limit
            )

            for pid in roster_ids:
                event_participants.append(
                    EventParticipant(event_id=event.id, player_id=pid)
                )

        session.bulk_save_objects(event_participants)
        session.commit()
        print(f"Inserted {len(event_participants)} event participants.")

        print(f"Seeding {TOTAL_PLAYERS} player stats...")
        stats = generate_player_stats(TOTAL_PLAYERS)
        session.bulk_save_objects(stats)
        session.commit()

        print(f"Seeding {TOTAL_MATCHES} matches and participants...")
        current_match_id = 1

        for chunk in range(0, TOTAL_MATCHES, CHUNK_SIZE):
            matches = []
            participants = []

            for _ in range(CHUNK_SIZE):
                p1_id = rand.randint(1, TOTAL_PLAYERS)
                p2_id = rand.randint(1, TOTAL_PLAYERS)

                if p1_id == p2_id:
                    p2_id = (p2_id % TOTAL_PLAYERS) + 1

                winner_id = rand.choice([p1_id, p2_id])
                score = f"{rand.randint(6, 7)}-{rand.randint(0, 5)}, {rand.randint(6, 7)}-{rand.randint(0, 5)}"

                matches.append(Match(id=current_match_id, score=score))

                match_parts = get_match_participants(
                    current_match_id, p1_id, p2_id, winner_id
                )
                participants.extend(match_parts)

                current_match_id += 1

            session.bulk_save_objects(matches)
            session.bulk_save_objects(participants)
            session.commit()
            print(f"Processed chunk up to match {current_match_id - 1}")

        print("Successfully generated rows.")

    except Exception as e:
        session.rollback()
        print(f"Insertion failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_million_rows()
