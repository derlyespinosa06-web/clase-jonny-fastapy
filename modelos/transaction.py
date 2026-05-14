from pydantic import BaseModel
from .facture import Facture

class Transaction(BaseModel):
    id: int | None = None
    description: str
    facture: Facture