# API Specification for Tennis Stats

## Player Statistics
1. `Get Player statistic`
2. `Add New Player`
3. `Update Player Statistics`
4. `Get Player Matches`
5. `Remove player`

### 1.1 Get Player statistics - `/player/{player_id}` (GET)
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

### 1.2 Add New Player - `/player/{player_id}` (Post)

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

### 1.3 Update Player Statistics - `/player/{player_id}` (PUT)

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

### 1.4 Get Player Matches - `/player/{playar_id}` (GET)

**Request**:
The API returns a json Object of the following structure: 
  - `matches_won` (optional) : A list of JSON objects with the matches won. 
  - `matches_lost` (optional) : A list of Json Objects with matches lost.

**Response**:
A JSON Object of the following Structure
 - `playerName`: The Players name
 - `matchHistory`: A list of JSON Objects with the following representation: 
    - `particapnts`: A list of the particpants
    - `score`: A list of of varying length with JSON Objects representing Score for the set with
      - `gameScore`: The game score
      - `TieBreakerScore` (optional): the score for the tiebreaker of the set
 - `matchesWon`: An Integer representing the number of matches won
 - `matcheslost`: An Integer representing the number of matches won

### 1.5 Remove Player - `/player/{player_id}` (DELETE)

**Response**: 

A 204 reponse code indicating data was deleted.

## Matches

1. `Create match`
2. `Remove match`
4. `Get Match score`
5. `Update Match score`
7. `Get match Particapants`

### 2.1 Create a match - `/match/{match_id}` (POST)

Create a new match within the database

**Request**: 

- `Particapants`: A list of the JSON Objects representing particpants wither length 2 or 4.
   - `name` : The First and Last name of the particpant.
   - `utrRating` : The utr rating of the player if they have one.
- `winners`: A list of names which are the particpants who won the match.
- `score`: The score of the match
- `timeDate`: the time and date of when the match took place

**Response**:
```json
{
 "success": "boolean" 
}
```
### 2.2 Remove match - `/match/{match_id}` (DELETE)

**Response**:
```json
{
 "success": "boolean"
}
```
### 2.3 Get a match - `/match/{match_id}` (GET)

**Response**

- `Particapants`: A list of the JSON Objects representing particpants wither length 2 or 4.
   - `name` : The First and Last name of the particpant.
   - `utrRating` : The utr rating of the player if they have one.
- `winners`: A list of names which are the particpants who won the match.
- `score`: The score of the match
- `startTimeDate`: The time and date of when the match took place
- `length` (DateTime): The length of the match

### 2.4 Update Match score - `/match/{match_id}/score` (PUT)

Update the match score 

**Response**: 

- `score` : A list representing the new score of the match
- `timeDate`: The time of how long the match has been going on for.

### 2.5 Get match Particapants` - `/match/{match_id}/players` (GET)

**Response**:

- `particapants` : A list of JSON Object with the following representation:
   - `name` : Particapants name.
   - `utr`: Partipants utr rating.
   - `firstServesPercentage` (Optional): First serve percetage within the match.
   - `secondServesWon` (Optional): Second serve percetage within the match.
   - `unforcedErrors` (Optional): Integer representing Unforced errors

## Events
1. `Create an Event`
2. `Update Event Information` 
3. `Add Player to Event`
4. `Get Current Events` 

### 3.1 Create an Event - `/event/{event_id} (POST)

Create an Event.

**Request**: 

- `name`: the name of the event.
- `particapant limit`: the maximum number of particpants.
- `location`: A physcial Address of where the event is located.
- `dateTime`: The time of when the event is happening.

**Response**:

A status code 200.

```json
{
 "success": "boolean"
}
```

### 3.2 Update Event Information - `/event/{event_id}}` (PUT)

Update information about an event

**Request**: 

- `name` (optional) : the name of the event.
- `particapantLimit` (optional) : the maximum number of particpants.
- `location` (optional) : A physcial Address of where the event is located.
- `dateTime` (optional) : The time of when the event is happening.

**Response**

- `name` : the name of the event.
- `particapantLimit` : the maximum number of particpants.
- `location` : A physcial Address of where the event is located.
- `dateTime` : The time of when the event is happening.

### 3.3 Add Player to Event - `/event/{event_id}/{player_id}` (POST)



```json
{
 "success": "boolean"
}
```

### Get  Events -  `/event/{query_params}` (GET)

Find Events witt certain search parameters

**Request**:

- `Organizer` : Search by who is organinzing an event
- `StartdateTime` : An dateTime which is the earlist date and time a tournament starts
- `EnddateTime`: A dateTime which is the latest of when a tournament can end.
- `Location` : The Location where Event is happening
- `Format`: The number of sets to win a match 3 or 5. 


**Response**:
```json
{
"organizer": "string"/*  Search by who is organinzing an event /* 
"startdateTime" : "DateTime" /* An dateTime which is the earlist date and time a tournament starts */ 
"EnddateTime" : "DateTime" /* A dateTime which is the latest of when a tournament can end. */ 
"Location" : "string" /* The Location where Event is happening */
"Format" :  "integer" /* The number of sets to win a match 3 or 5. /*
}
```
