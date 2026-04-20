# API Specification for Tennis Stats

## Player Statistics
1. `Get Player statistic`
2. `Add New Player`
3. `Update Player Statistics`
4. `Get Player Matches`
5. `Remove player`
# 1.1 Get Player statistics - `/player/{player_id}` (GET)
 Retrives the statistics for specific player.

 **Response**: 
 ```json
[
{
  "firstServesPercentage": "float" /* between 0 and 100 */
  "secondServesWon": "float" /* between 0 and 100 */
  "utrRating": "float" /* betwen 1 and 16.5 */ 
  "matchesWon": "integer"  /* between 0 and 10000 */
  "matchesLost": "integer" /* between 0 and 10000 */ 
}
]
 ```

# 1.2 Add New Player - `/player/{player_id}` (Post)
Add a new Player to the database

**Request**:
```json
{
"playerName": "string"
"utrRating": "float " /* betwen 1 and 16.5 (Optional)*/
}
```

**Response**:
```json
{
    "success": "boolean"
}
```

# 1.3 Update Player Statistics - `/player/{player_id}` (PUT)

**Request**:
NOTE: Every field here is optional, but a request should have a least one field that is being updated
```json
{
  "firstServesPercentage": "float" /* between 0 and 100 */
  "secondServesWon": "float" /* between 0 and 100 */
  "utrRating": "float" /* betwen 1 and 16.5 */ 
  "matchesWon": "integer"  /* between 0 and 10000 */
  "matchesLost": "integer" /* between 0 and 10000 */
}
```
**Response**:
```json
{
    "success": "boolean"
}
```

# 1.4 Get Player Matches - `/player/{playar_id}` (GET)

**Request**:
The API returns a json Object of the following structure: 
  - `matches_won` : A list of JSON objects with the matches won. 
  - `matches_lost` : A list of Json Objects with matches lost.

# 1.5 Remove Player - `/player/{player_id}` (DELETE)

**Response**: 
A 204 reponse code indicating data was deleted.

## Matches

1. `Create match`
2. `Remove match`
4. `Get Match score`
5. `Update Match score`
6. `Get match Particapants`

# 1.1 Create a match - `/match/{match_id} (POST)

# 1.2 Remove match - `/match/{match_id}` (DELETE)
# 1.3 Get a match - `/match/{match_id}` (GET)
# 1.5 Update Match score - `/match/{match_id}/score` (PUT)
# 1.5 Get match Particapants` - `/match/{match_id}/players` (GET)


## Events
1. `Create an Event` - `/event/{event_id}`  (POST)
2. `Update Event Information` `/event/{event_id}` (PUT)
3. `Add Player to Event` - `event/{event_id}/{player_id}` (POST)

# 1.1 Create an Event - `/event/{event_id} (POST)
# 1.2 Update Event Information - `/event/{event_id}}` (PUT)
# 1.3 Add Player to Event - `event/{event_id}/{player_id}` (POST)
