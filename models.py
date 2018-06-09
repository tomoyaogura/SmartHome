import enum

from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import db
from scheduler import get_jobs

class DeviceType(enum.Enum):
    RF = 1
    LIGHT = 2
    FAN = 3 

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    time_off = db.Column(db.DateTime, unique=True)
    device_type = db.Column(db.Enum(DeviceType), nullable=False)
    state = db.Column(db.Boolean, default=False)
    on_code = db.Column(db.String(10))
    off_code = db.Column(db.String(10))

    def __repr__(self):
        return '<Device %r>' % self.name

    @hybrid_property
    def schedules(self):
        return get_jobs(self)

    @hybrid_property
    def schedules_count(self):
        return len(get_jobs(self))

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)

