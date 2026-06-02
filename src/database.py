from sqlalchemy import create_engine
from src.config import get_settings

connection_url = get_settings().POSTGRES_URI
engine = create_engine(connection_url, pool_pre_ping=True)
