from fastapi import FastAPI
from src.api import player, matches
from starlette.middleware.cors import CORSMiddleware

description = """
Central Coast Cauldrons is the premier ecommerce site for all your alchemical desires.
"""
tags_metadata = [
    {"name": "player", "description": "Add, Update and View Player Statistics"},
    {
        "name": "events",
        "description": "Create, Update and View Current and Upcoming Events",
    },
    {"name": "matches", "description": "Add, Update and view Past matches and score"},
]

app = FastAPI(
    title="Central Coast Cauldrons",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Lucas Pierce",
        "email": "lupierce@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://tennis-stats-v3o5.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(player.router)
app.include_router(matches.router)


@app.get("/")
async def root():
    return {"message": "Shop is open for business!"}
