from pydantic import BaseModel

class Client(BaseModel):
    name: str
    age: int
    description: str | None = None

class Clientcreate(Client):
    pass

class Clientt(Client):
    id: int |None = None