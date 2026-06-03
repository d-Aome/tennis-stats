from fastapi import FastAPI, Request
from src.api import player, matches, events
from starlette.middleware.cors import CORSMiddleware
import time
from datetime import datetime


tags_metadata = [
    {"name": "player", "description": "Add, Update and View Player Statistics"},
    {
        "name": "events",
        "description": "Create, Update and View Current and Upcoming Events",
    },
    {"name": "matches", "description": "Add, Update and view Past matches and score"},
]

app = FastAPI(
    title="Tennis Stats",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "David Montiel",
        "email": "dmonti01@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://tennis-stats-v3o5.onrender.com"]


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()

    # Process the request and get the response
    response = await call_next(request)

    # Calculate execution time
    process_time_ms = time.perf_counter() - start_time

    # Add the duration to a custom response header
    response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}ms"

    print(f"Request path: {request.url.path} | Duration: {process_time_ms:.2f} ms")
    return response


@app.get("/time")
async def get_current_time():
    return {"current_time": datetime.now().isoformat(), "status": "success"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.include_router(player.router)
app.include_router(matches.router)
app.include_router(events.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Tennis Statistics"}
