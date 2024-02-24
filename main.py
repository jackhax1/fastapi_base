from fastapi import FastAPI, Response, Depends, HTTPException, status, Header, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, api_key
import time, secrets,os
from sqlalchemy.orm import Session
from typing import Annotated

import models, schemas,crud
from database import SessionLocal, engine

from dotenv import load_dotenv
load_dotenv()

BASIC_AUTH_USER = os.getenv('BASIC_AUTH_USER')
BASIC_AUTH_PWD = os.getenv('BASIC_AUTH_PWD')
API_KEY = os.getenv('API_KEY')

models.Base.metadata.create_all(bind=engine)

security = HTTPBasic()
api_key_header = api_key.APIKeyHeader(name="X-API-KEY")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(BASIC_AUTH_USER,'utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(BASIC_AUTH_PWD,'utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

def check_api_key(key: Annotated[str, Security(api_key_header)]):
    correct_api_key = bytes(API_KEY,'utf-8')
    current_api_key = key.encode("utf8")
    is_correct_api_key = secrets.compare_digest(
        current_api_key, correct_api_key
    )
    if not is_correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid ApiKey"
        )
    
app = FastAPI(dependencies=[Depends(check_auth),Depends(check_api_key)])

@app.get("/")
async def root():

    return {"message": "hello"}


@app.post("/create_entity")
async def create_entity(entity:schemas.Entity,
                        db: Session = Depends(get_db)):

    d = crud.create_entity(db,entity)
    print(f"Creating entity: {d}")
    return {"message": d}


@app.get("/get_entity")
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


@app.post("/update_state")
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

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port='8000')