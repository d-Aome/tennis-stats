# V2 Manual Example flow


## From V1, add both players
### Add Lu
```bash
curl -X 'POST' \
  'https://tennis-stats-v3o5.onrender.com/players/' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d'{
  "player": {
    "name": "Lu Sylvester",
    "utr": 7.8
  },
  "stats": {
    "first_serve_percentage": 0,
    "second_serve_percentage": 0,
    "matches_won": 0
  }
}'
```

### Response
```bash
{
  "success": true,
  "msg": "Player id: 1"
}
```

## Add Tyler
### Request
```bash
curl -X 'POST' \
  'https://tennis-stats-v3o5.onrender.com/players/' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "player": {
    "name": "Tyler Bodenhamer",
    "utr": 5.2
  },
  "stats": {
    "first_serve_percentage": 0,
    "second_serve_percentage": 0,
    "matches_won": 0
  }
}'
```
### Response
```json
{
  "success": true,
  "msg": "Player id: 2"
}
```

## Create event
### Request
```bash
curl -X 'POST' \
  'https://tennis-stats-v3o5.onrender.com/events/' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Spring General Tennis Club Tournament",
  "limit": 8,
  "location": "Cal Poly Tennis Courts"
}'
```

### Response
```json
{
  "success": true,
  "msg": "Event id: 1"
}
```


## Add Lu to event
### Request
```bash
curl -X 'POST' \
  'https://tennis-stats-v3o5.onrender.com/events/1/players' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "player_id": 1
}'
```

### Response
```json
{
  "success": true,
  "msg": "Player added to event"
}
```


## Add Tyler to event
### Request
```bash
curl -X 'POST' \
  'https://tennis-stats-v3o5.onrender.com/events/1/players' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "player_id": 2
}'
```

### Response
```json
{
  "success": true,
  "msg": "Player added to event"
}
```


## Get event players
### Request
```bash
curl -X 'GET' \
  'https://tennis-stats-v3o5.onrender.com/events/1/players' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxx'
```

### Response
```json
{
  "event_id": 1,
  "event_name": "Spring General Tennis Club Tournament",
  "participant_limit": 8,
  "participants": [
    {
      "player_id": 1,
      "name": "Lu Sylvester",
      "utr": 7.8
    },
    {
      "player_id": 2,
      "name": "Tyler Bodenhamer",
      "utr": 5.2
    }
  ]
}
```
