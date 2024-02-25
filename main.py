from fastapi import FastAPI, Response, Depends
import time
from sqlalchemy.orm import Session
import models, schemas,crud
from database import engine, get_db
from security.auth import check_auth,check_api_key
from security.ratelimit import lifespan, RATE_LIMIT_TIMES, RATE_LIMIT_SECS
from fastapi_limiter.depends import RateLimiter


models.Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan, dependencies=[Depends(check_auth),Depends(check_api_key)])


@app.get("/", dependencies=[Depends(RateLimiter(times=RATE_LIMIT_TIMES, seconds=RATE_LIMIT_SECS))])
async def root():

    return {"message": "hello"}


@app.post("/create_entity")
async def create_entity(entity:schemas.Entity,
                        db: Session = Depends(get_db)):

    d = crud.create_entity(db,entity)
    print(f"Creating entity: {d}")
    return {"message": d}


@app.get("/get_entity", dependencies=[Depends(RateLimiter(times=RATE_LIMIT_TIMES, seconds=RATE_LIMIT_SECS))])
async def get_entities(db: Session = Depends(get_db)):
    
    items = crud.get_all_entity(db)
    return items


@app.get("/get_entity/")
async def get_entity(entity_id :int,
                     limit: int = 10,
                     db: Session = Depends(get_db)):
    
    item = crud.get_entity(db,entity_id,limit)
    if item:
        result_dict = {
        "entity_id" :item[0].entity_id,
        "name" :item[0].name,
        "type" :item[0].type,
        "timestamp": [timestamp for _, timestamp in item[1]],
        "state": [state_value for state_value, _ in item[1]]
        }
        return result_dict
    else:
        return Response("Entity ID not found",status_code=404)


@app.post("/update_state", dependencies=[Depends(RateLimiter(times=RATE_LIMIT_TIMES, seconds=RATE_LIMIT_SECS))])
async def update_state(state:schemas.State,
                       db: Session = Depends(get_db)):

    loc_ts = int(time.time()*1000) if state.timestamp is None else state.timestamp
    d = crud.create_state(db,state,loc_ts)
    if d:
        return d
    else:
        return Response("Entity ID not found",status_code=404)


@app.get("/delete_entity/")
async def delete_entity(entity_id:int,
                        db: Session = Depends(get_db)):
    d = crud.delete_entity(db,entity_id)
    if d:
        return Response(f"Successfully deleted {d} items",status_code = 200)
    else:
        return Response("Entity ID not found",status_code=404)
