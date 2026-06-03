Peer Review Response
Here's what we changed from the peer review feedback and what we decided to leave alone and why.

Code Review — Daniel Kullman
1. The Events model used date as a field but the actual database column is called start_time
Fixed. We updated the model to use start_time so it matches the migration.
2. GET /events shouldn't need a request body
Fixed. We switched it to use query parameters instead, which is how GET filtering is supposed to work.
3. When a player isn't found, the code was returning the 404 status code number as the response instead of actually raising a 404
Fixed. It now raises a proper HTTPException(status_code=404).
4. update_player was filtering by the wrong column — it said WHERE id = :id but id there refers to player_stats.id, not the player's id
Fixed. Changed to WHERE player_id = :id so it actually finds the right row.
5. Success/failure should be handled by HTTP status codes, not a boolean in the response body
We kept the success field in responses but we also added proper HTTPExceptions for error cases. We think having a consistent response shape is fine as long as errors still get the right status codes, which they now do.
6. post_match should only allow 2 or 4 players
Fixed. It now returns an error if you pass anything other than 2 or 4 players.
7. Score is required but the example flows showed creating a match before a score exists
Fixed. Score is now optional when creating a match. You can add it later with the update endpoint.
8. update_match didn't check if the match actually exists
Fixed. It now checks whether any rows were actually updated and returns a 404 if nothing was found.
9. No input validation — someone could submit negative serve percentages or negative matches won
Fixed. The PlayerStatistics model now validates that serve percentages are between 0 and 100 and matches_won can't be negative.
10. Nothing was stopping someone from registering the same player in the same event twice
Fixed. POST /events/{event_id}/players now checks if the player is already in the event before inserting.
11. Unused imports in a few files
Fixed. Removed Field, field_validator, and ConfigDict from files that weren't using them, and removed the duplicate import sqlalchemy in player.py.
12. update_player requires you to send all stats fields even if you only want to change one
We left this as a full replacement PUT for now. Making it a PATCH with optional fields would mean reworking the model and we didn't want to scope creep V4. A full update still works correctly, it just means you have to re-send fields you're not changing.

Schema/API Design — Daniel Kullman 
1. The spec and example flows used /player but the code uses /players
Fixed. Everything is consistently /players now.
2. The spec listed GET /match/{id} and DELETE /match/{id} but those weren't implemented
We removed them from the spec instead of implementing them. They weren't needed for any of our core flows.
3. Overall the spec didn't match the actual code — different field names, different routes
Fixed. We rewrote the spec to reflect what the API actually does.
4. Events should use a proper datetime type instead of a string
We kept it as a string input since FastAPI automatically parses ISO datetime strings into datetime objects, so it works correctly either way.
5. GET /events was using a request body for filtering
Fixed, same as Kullman item 2 above.
6. No UNIQUE constraint on event_participants or match_participants
Fixed for event_participants — added UNIQUE(event_id, player_id). For match_participants we added a check in post_match to reject duplicate player IDs in a single request instead, since in theory you could have edge cases where a player appears on different teams.
7. player_stats should be 1-to-1 with players using player_id as the primary key
We added a UNIQUE constraint on player_id in player_stats to enforce the 1-to-1 relationship. We didn't drop the id primary key because that would require dropping and recreating the table in a migration, which felt risky for something already deployed.
8. post_match had two separate body parameters instead of one combined body
Fixed. Match and players are now one single request body.
9. Creating an event with missing required fields was throwing a 500 instead of a validation error
Fixed. The Event model now properly marks name, location, and participant_limit as required so FastAPI will return a 422 with a helpful message instead of crashing.
10. post_event just returned an integer id instead of a proper JSON response
Fixed. It now returns {"success": true, "msg": "Event id: X"}.
11. update_event was returning 204 (no content) but still had a response body
Fixed. Changed to 200.
12. post_match should reject duplicate player IDs in the players list
Fixed. It now checks for duplicates before inserting.

Test Results — Daniel Kullman 
The tests showed POST /events failing with a 422 because the example flow sent participantLimit (camelCase) but the model expected participant_limit (snake_case). Fixed — the model field is now just limit and the spec and examples are updated to match it.
POST /matches was also failing with a JSON decode error because of the two-body-parameter issue mentioned in #3. That's fixed now too.

Code Review — Daniel Pineda (#6)
1 & 4. update_player ran even if the player didn't exist, and had the wrong WHERE clause
Same as Kullman #2 items 4 and 8 above — both fixed.
2. get_player returned a 404 integer as JSON instead of raising an HTTPException
Fixed, same as Kullman #2 item 3.
3. Duplicate imports and unused imports
Fixed, same as Kullman #2 item 11.
5. Error messages were leaking the raw exception text to clients
Fixed. Generic "Internal Server Error" is returned to the client now. The actual exception still gets printed server-side so we can debug it.
6. Players list accepted any length
Fixed, same as Kullman #2 item 6.
7. post_match returned 200 instead of 201
Fixed.
8. No GET or DELETE for matches
We left these out. They weren't part of our core use cases and adding them just for the sake of it felt like unnecessary work for V4.
9, 10. Wrong return types in events.py
Fixed.
11. No validation that the event and player exist before inserting into event_participants
Fixed. POST /events/{event_id}/players now checks both exist first.
12. get_events used a request body
Fixed, same as the others above.

Schema/API Design — Daniel Pineda (#7)
Most of this overlaps with Kullman #3 and is addressed above. The one thing specific to this issue:
Two different responses coming from the same GET /player/{id} path
Fixed. Player stats are at GET /players/{player_id} and match history is at GET /players/{player_id}/matches — separate routes now.

Product Ideas — Daniel Pineda (#9) and Daniel Kullman (#5)
Both reviewers suggested adding tournament bracket generation and a way to look up suggested opponents based on UTR.

Player match history (GET /players/{player_id}/matches): Added. This also solved the duplicate path problem from #7.
Tournament bracket generation: We didn't add this for V4. It would need new tables, seeding logic, and a lot of extra work that's outside what V4 is asking for. 
Suggested players by stats/UTR: Same reasoning — cool idea but out of scope for now.
