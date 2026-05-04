import sqlalchemy as sa
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator, ConfigDict

from src import database as db
from src.api import auth


router = APIRouter(
    prefix="/players",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)
