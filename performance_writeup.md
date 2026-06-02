# Fake Data Modeling

- players: 20,000
- player_stats: 20,000
- matches: 320,000
- match_particpants: 640,000
- events: 1,000
- event_particpants: 74,336

I Believe that the service would scale this way because players are unique, but matches
between players are not unique.

For events and event particpants i believe that it would scale this way as there
are only so many events that can happen in a year however each event typically
has a between 32 and 128 particpants, meaning that for every event there will
multiple event particpants.

# Performance results of hitting endpoints

## Times

- `/player/{player_id}` (GET): 0.03ms
- `/player/{player_id}` (Post): 0.01ms
- `/player/{player_id}` (PUT): 0.00ms

- `/event/{event_id}` (POST): 0.01ms
- `/event/{event_id}/{player_id}` (POST): 0.01ms
- `/events/{event_id}/players` (POST): 0.01ms

- `/match/{match_id}` (POST): 0.00ms
- `/match/{match_id}/score` (PUT): 0.00ms
- `/matches/{match_id}/complete` (POST): 0.04ms

The Slowest endpoints where the Getting a player and the Posting that a match was complete
all the other endpoint took roughly the same amount of time.

# Performance tuning

Because the the slowest Endpoints where

```sql
EXPLAIN
SELECT id
FROM matches
WHERE id = :match_id
FOR UPDATE
```

LockRows (cost=0.42..8.45 rows=1 width=10)
-> Index Scan using matches_pkey on matches (cost=0.42..8.44 rows=1 width=10)
Index Cond: (id = 288000)

This means that when selecting a match it doest not scan
very many of the rows before finding the correct one even when looking a larger indexes.

```sql
SELECT player_id, team
FROM match_participants
WHERE match_id = :match_id
```

Gather (cost=1000.00..8410.53 rows=2 width=8)
Workers Planned: 2
-> Parallel Seq Scan on match_participants (cost=0.00..7410.33 rows=1 width=8)
Filter: (match_id = 5000)

In Select the correct player_id and team the database has to look through a large amount of data
even for relatively small match_id's.

```sql
UPDATE matches
SET score = :score
WHERE id = :match_id
```

Update on matches (cost=0.42..8.44 rows=0 width=0)
-> Index Scan using matches_pkey on matches (cost=0.42..8.44 rows=1 width=38)
Index Cond: (id = 288000)

This query is pretty fast as it does not need to look through lots of rows
before updating the value for a specific row.

```sql
UPDATE match_participants
SET winner = (team = :winning_team)
WHERE match_id = :match_id
```

Update on match_participants (cost=0.00..12077.00 rows=0 width=0)
-> Seq Scan on match_participants (cost=0.00..12077.00 rows=2 width=7)
Filter: (match_id = 5000)

So far this is the slowest query with it looking through the entire database essentialy in order to update one value.

```sql
UPDATE player_stats
SET matches_won = matches_won + 1
WHERE player_id = :player_id
```

Update on player_stats (cost=0.00..398.08 rows=0 width=0)
-> Seq Scan on player_stats (cost=0.00..398.08 rows=1 width=10)
Filter: (player_id = 19888)

This query is not the fastest but also no the slowest we can still improve this one by adding an index

The indexes i plan on adding are the following.

```sql
CREATE INDEX idx_match_participants_match_id ON match_participants (match_id);
CREATE INDEX idx_player_stats_player_id ON player_stats (player_id);
```

After adding the index running the slowest queries i get the following

```sql
UPDATE match_participants
SET winner = (team = :winning_team)
WHERE match_id = :match_id
```

Improves to:

Update on match_participants (cost=0.42..8.47 rows=0 width=0)
-> Index Scan using idx_match_participants_match_id on match_participants (cost=0.42..8.47 rows=2 width=7)
Index Cond: (match_id = 298000)

```sql
UPDATE match_participants
SET winner = (team = :winning_team)
WHERE match_id = :match_id
```

Improves to:

Update on match_participants (cost=0.42..8.47 rows=0 width=0)
-> Index Scan using idx_match_participants_match_id on match_participants (cost=0.42..8.47 rows=2 width=7)
Index Cond: (match_id = 298000)

```sql
SELECT player_id, team
FROM match_participants
WHERE match_id = :match_id
```

Improves to:

Index Scan using idx_match_participants_match_id on match_participants (cost=0.42..8.46 rows=2 width=8)
Index Cond: (match_id = 298000)
