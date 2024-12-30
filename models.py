from sqlalchemy import Boolean, String, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Devices(Base):
    __tablename__ = "DEVICES"

    id= Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    model = Column(String(120))
    place = Column(String(100))
    Mac = Column(String(100))
    IP = Column(String(100))
    Notes  = Column(String(120))
    show = Column(Boolean)
    Date = Column(String(100))

class Cameras(Base):
    __tablename__ = "CAMERAS"

    id= Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    model = Column(String(120))
    place = Column(String(100))
    Mac = Column(String(100))
    IP = Column(String(100))
    Notes  = Column(String(120))
    show = Column(Boolean)
    Date = Column(String(100))


class Telos(Base):
    __tablename__ = "TELEPHONES"

    id= Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    model = Column(String(120))
    place = Column(String(100))
    Mac = Column(String(100))
    IP = Column(String(100))
    Notes  = Column(String(120))
    show = Column(Boolean)
    Date = Column(String(100))


class Nursing(Base):
    __tablename__ = "NURSING"

    id= Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    model = Column(String(120))
    place = Column(String(100))
    Mac = Column(String(100))
    IP = Column(String(100))
    Notes  = Column(String(120))
    show = Column(Boolean)
    Date = Column(String(100))


class AccessPoints(Base):
    __tablename__ = "ACCESS_POINTS"

    id= Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    model = Column(String(120))
    place = Column(String(100))
    Mac = Column(String(100))
    IP = Column(String(100))
    Notes  = Column(String(120))
    show = Column(Boolean)
    Date = Column(String(100))


class Cabinet(Base):
    __tablename__ = "CABINETS"

    id= Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    model = Column(String(120))
    place = Column(String(100))
    #Mac = Column(String(100))
    #IP = Column(String(100))
    Notes  = Column(String(120))
    show = Column(Boolean)
    Date = Column(String(100))

