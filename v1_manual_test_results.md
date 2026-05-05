# V1 Manual Example flow
## Add Players to database
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


## Create match between two players
### Request: 
```bash
curl -X 'POST' \
  'https://tennis-stats-v3o5.onrender.com/matches/' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "match": {
    "score": "6-4, 6-3"
  },
  "players": [
    {
      "player_id": 1,
      "winner": true,
      "team": 0
    },
    {
    "player_id": 2,
    "winner": false,
    "team": 1
    }
  ]
}'
```

### Response:
```json
{
  "success": true,
  "msg": "match id: 1"
}
```


## Player Updates their Stats

### Request: 
```bash
curl -X 'PUT' \
  'https://tennis-stats-v3o5.onrender.com/players/1' \
  -H 'accept: application/json' \
  -H 'access_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_serve_percentage": 62.5,
  "second_serve_percentage": 55.0,
  "matches_won": 6
}'
```
### Response: 
```json
{
  "success": true,
  "msg": ""
}
```


## Player gets their stats

### Request:
```bash
curl -X 'GET' \
  'https://tennis-stats-v3o5.onrender.com/players/1' \
  -H 'accept: application/json' \
  -H 'access_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

### Response:
```json
{
  "name": "Lu Slyvester",
  "utr": 7.8,
  "first_serve_percentage": 62.5,
  "second_serve_percentage": 55,
  "matches_won": 6
}
```
