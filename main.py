from fastapi import FastAPI, HTTPException, Depends, status, Request
from pydantic import BaseModel
from typing import Annotated, Optional
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
from re import findall
from icmplib  import ping , Host
import os


app = FastAPI()

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGO
ACCESS_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

class DeviceBase(BaseModel):
    type:str
    name:str
    model:str
    floor:int
    place:str
    Mac:str
    IP:str
    Notes:str 
    show:bool
    active:bool

class DeviceUpdate(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    model: Optional[str] = None
    floor: Optional[int] = None
    place: Optional[str] = None
    Mac: Optional[str] = None
    IP: Optional[str] = None
    Notes: Optional[str] = None
    show: Optional[bool] = None
    active: Optional[bool] = None

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

@app.get("/devices",status_code=status.HTTP_200_OK)
async def full_fetch(db:db_dependency):

    devices = db.query(models.Devices).all()
    if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
    return devices
    """listofips = []
    for device in devices:
        if device.show == True:
            if device.IP != "":
                ping_ip = os.system("ping -n 1 -w 10 " + device.IP)
                updated = False
                if ping_ip == 0:
                    if(device.active != True):
                        device.active = True
                        updated = True
                else:
                    if(device.active != False):
                        device.active = False
                        updated = True                
                if(updated):
                    db.query(models.Devices).filter(models.Devices.id == device.id).update({"active": device.active})
                    db.commit()
                listofips.append(device.IP)
            else:
                device.active = False
                db.query(models.Devices).filter(models.Devices.id == device.id).update({"active": device.active})
                db.commit()
    
    Devices_DB = db.query(models.Devices).all()
    return Devices_DB"""


#--- this code is just for the process of adding devices to our database
@app.post("/add", status_code=status.HTTP_201_CREATED)
def add(db:db_dependency, device:DeviceBase):
        db_device = models.Devices(**device.__dict__, Date=datetime.now())
        db.add(db_device)
        db.commit()


@app.put("/edit/{id}", status_code=status.HTTP_200_OK)
def edit(db:db_dependency, id:int, device:DeviceUpdate):
    db_device = db.query(models.Devices).filter(models.Devices.id == id).first()
    if db_device is None:
        raise HTTPException(status_code=404 , detail='Device not found')

    update_data = device.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device


"""if db_device.type == "camera":
            db_device = models.Devices(**device.__dict__)
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
        
        elif db_device.type == "access_door":
            db_device = models.Cabinet(**device.__dict__)
            db.add(db_device)
            db.commit()"""

        #else:
            #raise HTTPException(status_code=404 , detail='There is No Devices!')
# @app.get("/fetch/{type}",status_code=status.HTTP_200_OK)
# """
#     This route is used to fetch devices based on their type.
#     :param db: The database session object.
#     :param type: The type of devices to fetch.
#     :return: The list of devices matching the provided type.
# """
"""
async def full_fetch(db:db_dependency, type:str):

    devices = db.query(models.Devices).filter(models.Devices.type == type).all()
    if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
    
    #working = []
    #not_working = []
    listofips = []
    for device in devices:
        if device.IP != "":
            ping_ip = os.system("ping -n 1 -w 10 " + device.IP)
            if ping_ip ==0:
                device.show = True
            else:
                device.show = False 
                listofips.append(device.IP)
    print(listofips)
    return devices
"""

"""@app.get("/fetch/camera/{filter}", status_code=status.HTTP_200_OK)
def camera_fetch(filter:str, db:db_dependency):
     

        devices_mac = db.query(models.Devices).filter(models.Devices.Mac == filter).filter(models.Devices.type == "camera").all()
        devices_ip = db.query(models.Devices).filter(models.Devices.IP == filter).filter(models.Devices.type == "camera").all()
        devices_model = db.query(models.Devices).filter(models.Devices.model == filter).filter(models.Devices.type == "camera").all()
        devices_place = db.query(models.Devices).filter(models.Devices.place == filter).filter(models.Devices.type == "camera").all()
        devices = devices_mac + devices_ip + devices_model + devices_place
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        
        for device in devices:
            if device.IP != "":
                
                ping_ip = os.system("ping -n 1 -w 90 -l 8 "+device.IP) 
                if ping_ip == 0:
                     device.show = True
                else:
                     device.show = False
                     

     
        return devices

"""
"""@app.get("/fetch/telephone/{filter}", status_code=status.HTTP_200_OK)
def telo_fetch(filter:str, db:db_dependency):
     

        devices_mac = db.query(models.Devices).filter(models.Devices.Mac == filter).filter(models.Devices.type == "telephone").all()
        devices_ip = db.query(models.Devices).filter(models.Devices.IP == filter).filter(models.Devices.type == "telephone").all()
        devices_model = db.query(models.Devices).filter(models.Devices.model == filter).filter(models.Devices.type == "telephone").all()
        devices_place = db.query(models.Devices).filter(models.Devices.place == filter).filter(models.Devices.type == "telephone").all()
        devices = devices_mac + devices_ip + devices_model + devices_place
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices

@app.get("/fetch/AccesssPoint/{filter}", status_code=status.HTTP_200_OK)
def ac_fetch(filter:str, db:db_dependency):
     

        devices_mac = db.query(models.Devices).filter(models.Devices.Mac == filter).filter(models.Devices.type == "accesspoint").all()
        devices_ip = db.query(models.Devices).filter(models.Devices.IP == filter).filter(models.Devices.type == "accesspoint").all()
        devices_model = db.query(models.Devices).filter(models.Devices.model == filter).filter(models.Devices.type == "accesspoint").all()
        devices_place = db.query(models.Devices).filter(models.Devices.place == filter).filter(models.Devices.type == "accesspoint").all()
        devices = devices_mac + devices_ip + devices_model + devices_place
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices


@app.get("/fetch/nursing/{filter}", status_code=status.HTTP_200_OK)
def nursing_fetch(filter:str, db:db_dependency):
     

        devices_mac = db.query(models.Devices).filter(models.Devices.Mac == filter).filter(models.Devices.type == "nursing").all()
        devices_ip = db.query(models.Devices).filter(models.Devices.IP == filter).filter(models.Devices.type == "nursing").all()
        devices_model = db.query(models.Devices).filter(models.Devices.model == filter).filter(models.Devices.type == "nursing").all()
        devices_place = db.query(models.Devices).filter(models.Devices.place == filter).filter(models.Devices.type == "nursing").all()
        devices = devices_mac + devices_ip + devices_model + devices_place
        if devices is None:
            raise HTTPException(status_code=404 , detail='There is No Devices!')
        return devices


@app.get("/fetch/cabinet/{filter}", status_code=status.HTTP_200_OK)
def cabinet_fetch(filter:str, db:db_dependency):
     

        devices_mac = db.query(models.Devices).filter(models.Devices.Mac == filter).filter(models.Devices.type == "cabinet").all()
        devices_ip = db.query(models.Devices).filter(models.Devices.IP == filter).filter(models.Devices.type == "cabinet").all()
        devices_model = db.query(models.Devices).filter(models.Devices.model == filter).filter(models.Devices.type == "cabinet").all()
        devices_place = db.query(models.Devices).filter(models.Devices.place == filter).filter(models.Devices.type == "cabinet").all()
        devices = devices_mac + devices_ip + devices_model + devices_place
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

 """   
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