# Example Flows

##### 1. Tennis Club Officer Creating an Event and Matches

A Tennis Club officer wants to organize an event for players in the club and create matches so players can compete against each other in friendly matches.

First, the officer creates an event by calling:

POST /event/10

Request:
{
"name": "Spring General Tennis Club Tournament"
"particapant limit": 8
"location": "Cal Poly Tennis Courts"
"dateTime": "5-10-2026, 10am"
}

Response:
{
"success": true
}

Next, the officer adds players to the event:

POST /event/10/21

Response:
{
"success": true
}

POST /event/10/24

Response:
{
"success": true
}

Then the officer creates a match for the event:

POST /match/50

Request:
{
"particapants": [{"name": "Garret Chan", "utrRating": 1.0},
{"name": "Arhant Shroff", "utrRating": 9.0}
],
"winners": [],
"score": [],
"timeDate": "5-10-2026, 11am"
}

Response:
{
"success": true
}

Finally, the club officer can view the match:

GET /match/50

Response:
{
"particapants": [
{"name": "Garret Chan", "utrRating": 1.0},
{"name": "Arhant Shroff", "utrRating": 9.0}
],
"winners": [],
"score": [],
"startTimeDate": "5-10-2026, 11am"
}

This flow connects to organizing events and setting up matches for players.

--------------------
--------------------

##### 2. Tennis Player Tracking Match Stats

A Tennis player wants to track their serve stats and match results so they can improve their tennis skill level.

First, a match is created:

POST /match/60

Request:
{
"particapants": [
{"name": "Lu Sylvester", "utrRating": 7.8},
{"name": "Tyler Bodenhamer", "utrRating": 5.2}
],
"winners": [],
"score": [],
"timeDate": "5-5-26, 2pm"
}

Response:
{
"success": true
}

After the match, the score is updated:

PUT /match/60/score

Response:
{
"score": ["6-4", "6-3"],
"timeDate": "5-5-26, 2:52pm"
}

Then the player updates their stats:

PUT /player/30

Request:
{
"firstServesPercentage": 62.5,
"secondServesWon": 55.0,
"matchesWon": 6
}

Response:
{
"success": true
}

Finally, the player checks their stats:

GET /player/30

Response:
[
{
"firstServesPercentage": 62.5,
"secondServesWon": 55.0,
"utrRating": 7.8,
"matchesWon": 6,
"matchesLost": 3
}
]

This flow connects to tracking first serve %, second serve %, and match results.

---------------
---------------
