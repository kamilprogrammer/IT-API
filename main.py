from fastapi import FastAPI, HTTPException, Depends, status, Request
from pydantic import BaseModel
from typing import Annotated
import models
from db import engine, session
from sqlalchemy.orm import Session
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from secret import SECRET_KEY, ALGO

app = FastAPI()

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGO
ACCESS_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

class DeviceBase(BaseModel):
    type:str
    model:str
    place:str
    Mac:str
    IP:str
    Notes:str 
    show:bool
    Date:str

class CameraBase(BaseModel):
    type:str
    model:str
    place:str
    Mac:str
    IP:str
    Notes:str 
    show:bool
    Date:str

class TeloBase(BaseModel):
    type:str
    model:str
    place:str
    Mac:str
    IP:str
    Notes:str 
    show:bool
    Date:str

class AccessPointBase(BaseModel):
    type:str
    model:str
    place:str
    Mac:str
    IP:str
    Notes:str 
    show:bool
    Date:str

class CabinetBase(BaseModel):
    type:str
    model:str
    place:str
    #Mac:str
    #IP:str
    Notes:str 
    show:bool
    Date:str

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()   


db_dependency = Annotated[Session, Depends(get_db)]

#fetch Api routes ---------------------------------------


@app.get("/fetch",status_code=status.HTTP_200_OK)
def full_fetch(mac:str, ip:str, model:str, place:str, db:db_dependency):
    devices = db.query(models.Devices).filter(models.Devices.Mac == mac).filter(models.Devices.IP == ip).filter(models.Devices.model == model).filter(models.Devices.place == place).all()
    if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
    return devices
    


@app.get("/fetch/{filter}", status_code=status.HTTP_200_OK)
def fetch_Devices(filter:str, db:db_dependency):
     

        devices_mac = db.query(models.Devices).filter(models.Devices.Mac == filter).all()
        devices_ip = db.query(models.Devices).filter(models.Devices.IP == filter).all()
        devices_model = db.query(models.Devices).filter(models.Devices.model == filter).all()
        devices_place = db.query(models.Devices).filter(models.Devices.place == filter).all()
        devices = devices_mac + devices_ip + devices_model + devices_place
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices


@app.get("/fetch_mac/{mac}", status_code=status.HTTP_200_OK)
def fetch_Devices(mac:str, db:db_dependency):
     

        devices = db.query(models.Devices).filter(models.Devices.Mac == mac).all()
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices
    

@app.get("/fetch_ip/{ip}", status_code=status.HTTP_200_OK)
def fetch_Devices(ip:str, db:db_dependency):
     

        devices = db.query(models.Devices).filter(models.Devices.IP == ip).all()
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices
    

@app.get("/fetch_place/{place}", status_code=status.HTTP_200_OK)
def fetch_Devices(place:str, db:db_dependency):
     

        devices = db.query(models.Devices).filter(models.Devices.place == place).all()
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices
    

@app.get("/fetch_model/{model}", status_code=status.HTTP_200_OK)
def fetch_Devices(model:str, db:db_dependency):
     

        devices = db.query(models.Devices).filter(models.Devices.model == model).all()
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices

    

#--- this code is just for the process of adding devices to our database
@app.post("/add", status_code=status.HTTP_201_CREATED)
def add(db:db_dependency, device:DeviceBase):
        db_device = models.Devices(**device.__dict__)
        db.add(db_device)
        db.commit()

        if db_device.type == "camera":
            db_device = models.Cameras(**device.__dict__)
            db.add(db_device)
            db.commit()

        elif db_device.type == "telephone":
            db_device = models.Telos(**device.__dict__)
            db.add(db_device)
            db.commit()

        elif db_device.type == "nursing":
            db_device = models.Nursing(**device.__dict__)
            db.add(db_device)
            db.commit()

        elif db_device.type == "access_point":
            db_device = models.AccessPoints(**device.__dict__)
            db.add(db_device)
            db.commit()
    









#this code is just for running the fastapi project without trying to use uvicorn from the terminal .... :)
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3666,
        log_level="debug",
        reload=True,
    )