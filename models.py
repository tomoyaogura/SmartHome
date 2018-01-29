import enum

from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import db
from scheduler import get_jobs

class DeviceType(enum.Enum):
    rf_outlet = 1
    fan = 2

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    time_off = db.Column(db.DateTime, unique=True)
    device_type = db.Enum(DeviceType)
    device_id = db.Column(db.String(120), unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)

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

