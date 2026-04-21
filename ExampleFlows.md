# Example Flows

## 1. Tennis Club Officer Creating an Event and Matches

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

---
