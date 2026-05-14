from pydantic import BaseModel
from .cliente import Client

class Facture(BaseModel):
    id: int | None = None
    date: str
    client: Client
    totalvalue: float