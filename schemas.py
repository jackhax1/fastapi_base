from pydantic import BaseModel

class Entity(BaseModel):
    name: str
    type: str
    class Config:
        orm_mode = True

class State(BaseModel):
    entity_id: int
    state: float
    timestamp: float = None
    class Config:
        orm_mode = True

class ProtoC(BaseModel):
    data: bytes

