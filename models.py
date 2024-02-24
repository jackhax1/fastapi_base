from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, BigInteger, Double
from sqlalchemy.orm import relationship

from database import Base


class Entity(Base):
    __tablename__ = "entities"

    entity_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    type = Column(String)
    state = relationship("State", back_populates="entity")

class State(Base):
    __tablename__ = "states"

    state_id = Column(BigInteger, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.entity_id"))
    timestamp = Column(BigInteger)
    state_value = Column(Double)
    entity = relationship("Entity", back_populates="state")
    
    