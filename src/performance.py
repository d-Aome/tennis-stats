import random
from faker import Faker
from src.database import engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta
from src.data_models import PlayerStat, Event, Match, MatchParticipant

fake = Faker()


def generate_events(num_events):
    if num_events <= 0:
        return []

    events = []
    for _ in range(num_events):
        events.append(
            Event(
                name=f"{fake.city()} Open",
                participant_limit=random.choice([32, 64, 128]),
                start_time=fake.date_time_this_year(),
                location=fake.address()[:50],
                format=random.choice(["Singles", "Doubles"]),
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
                first_serve_percentage=round(random.uniform(45.0, 75.0), 2),
                second_serve_percentage=round(random.uniform(70.0, 95.0), 2),
                matches_won=random.randint(0, 150),
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


def seed_million_rows(db_url):
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(Event).count() > 0:
        print("Database already seeded. Aborting.")
        session.close()
        return

    print("Seeding 1,000 events...")
    events = generate_events(1000)
    session.bulk_save_objects(events)
    session.commit()

    print("Seeding 20,000 player stats...")
    stats = generate_player_stats(20000)
    session.bulk_save_objects(stats)
    session.commit()

    print("Seeding 320,000 matches and 640,000 participants...")

    TOTAL_MATCHES = 320000
    TOTAL_PLAYERS = 20000
    CHUNK_SIZE = 10000

    current_match_id = 1

    for chunk in range(0, TOTAL_MATCHES, CHUNK_SIZE):
        matches = []
        participants = []

        for _ in range(CHUNK_SIZE):
            p1_id = random.randint(1, TOTAL_PLAYERS)
            p2_id = random.randint(1, TOTAL_PLAYERS)

            if p1_id == p2_id:
                p2_id = (p2_id % TOTAL_PLAYERS) + 1

            winner_id = random.choice([p1_id, p2_id])
            score = f"{random.randint(6, 7)}-{random.randint(0, 5)}, {random.randint(6, 7)}-{random.randint(0, 5)}"

            matches.append(Match(id=current_match_id, score=score))

            match_parts = get_match_participants(
                current_match_id, p1_id, p2_id, winner_id
            )
            participants.extend(match_parts)

            current_match_id += 1

        # Bulk save both tables for this chunk
        session.bulk_save_objects(matches)
        session.bulk_save_objects(participants)
        session.commit()
        print(f"Processed chunk up to match {current_match_id - 1}")

    session.close()
    print("Done generating 1,000,000+ rows.")
