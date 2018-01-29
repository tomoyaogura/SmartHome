import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField

from database import db
from models import Device
from scheduler import scheduler, timer
from datetime import timedelta

from control import turn_on, turn_off

""" APP SETTINGS """

FILE_PATH =  os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'smarthome.db'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(FILE_PATH, DB_NAME) 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'get_from_env'
    bootstrap = Bootstrap(app)
    db.init_app(app)
    scheduler.start()
    return app

app = create_app()

class DeviceUpdate(FlaskForm):
    state = BooleanField('on')

class ScheduleUpdate(FlaskForm):
    state = BooleanField('on')


@app.route("/debug")
def hello():
    return "Hello World"

@app.route("/")
def index():
    devices = Device.query.all()
    return render_template("index.html", devices=devices)

@app.route("/db")
def database():
    devices = [d.name for d in Device.query.all()]
    return str(devices)

@app.route("/schedules/")
def schedules_index():
    devices = Device.query.all()
    return render_template("schedule.html", devices=devices)

@app.route("/schedules/<device_id>", methods=['GET', 'POST'])
def schedule_update(device_id):
    form = ScheduleUpdate()
    device = Device.query.filter_by(id=device_id).first()
    if request.method == 'GET':
        if device:
            return render_template('add_schedule.html', form=form, device=device)
        else:
            return 'Device not found'
    elif request.method == 'POST':
        if device:
            if form.validate_on_submit():
                if request.form['on'] == 'on':
                    function = turn_on
                else:
                    function = turn_off
                second = int(request.form['second'])
                minute = int(request.form['minute'])
                hour = int(request.form['hour'])
                timer(device, function, timedelta(seconds=second, minutes=minute, hours=hour))
                return redirect(url_for('schedules_index'))
        else:
            return 'Device not found'



@app.route("/devices/<device_id>", methods=['GET', 'POST'])
def devices(device_id):
    form = DeviceUpdate()
    device = Device.query.filter_by(id=device_id).first()
    if request.method == 'GET':
        if device:
            return render_template('device.html', form=form, device=device)
        else:
            return 'Device not found'
    elif request.method == 'POST':
        if device:
            if form.validate_on_submit():
                if request.form['on'] == 'on':
                    state = True
                    turn_on(device.device_id)
                else:
                    state = False
                    turn_off(device.device_id)
                Device.query.filter_by(id=device_id).update({'state': state})
                db.session.commit()
                return redirect(url_for('index'))
        else:
            return 'Device not found'


"""
MAIN APP
"""
if __name__ == "__main__":
  if os.environ.get('DEBUG'):
    app.run()
  else:
    app.run(host='0.0.0.0')
