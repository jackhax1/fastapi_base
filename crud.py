from sqlalchemy.orm import Session
import models, schemas,random



def create_entity(db: Session, entity: schemas.Entity):
    db_entity = models.Entity(entity_id=random.randint(0,100), name=entity.name,type=entity.type)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

def create_state(db: Session, state: schemas.State, timestamp: float):
    d1 = db.query(models.Entity).filter(models.Entity.entity_id == state.entity_id).first()
    if(d1):
        db_entity = models.State(state_id=random.randint(0,1_000_000_000_000), 
                                entity_id=state.entity_id,
                                timestamp=timestamp,
                                state_value=state.state)
        db.add(db_entity)
        db.commit()
        db.refresh(db_entity)
        return db_entity
    else:
        return False


def get_entity(db: Session, entity_id: int,limit):
    if limit == None:
        limit = 10
    d1 = db.query(models.Entity).filter(models.Entity.entity_id == entity_id).first()
    d2 = db.query(models.State.state_value,models.State.timestamp).filter(models.State.entity_id == entity_id).order_by(models.State.timestamp.desc()).limit(limit).all()
    return [d1,d2]

def get_all_entity(db: Session):
    return db.query(models.Entity).all()

def delete_entity(db: Session,entity_id: int):
    d2 = db.query(models.State).filter(models.State.entity_id == entity_id).delete()
    d1 = db.query(models.Entity).filter(models.Entity.entity_id == entity_id).delete()
    
    db.commit()
    return d1