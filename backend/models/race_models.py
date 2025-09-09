from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    name: str
    datetime: str

class NextRace(BaseModel):
    race_name: str
    location: str
    country: str
    race_date: str
    sessions: list[Session]
