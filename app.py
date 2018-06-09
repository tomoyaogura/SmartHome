import os

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField

from database import db
from models import Device
from scheduler import timer
from datetime import timedelta
from config import app_config
from control import turn_on, turn_off


class DeviceUpdate(FlaskForm):
    state = BooleanField('on')

class ScheduleUpdate(FlaskForm):
    state = BooleanField('on')

def create_app(app_env):
    app = Flask(__name__)
    app.config.from_object(app_config[app_env])
    bootstrap = Bootstrap(app)
    db.init_app(app)

    @app.route("/api/v1/devices/", methods=['GET'])
    def devices_api():
        devices = Device.query.all()
        results = []
        for device in devices:
            obj = {
                'id': device.id,
                'name': device.name,
                'device_type': device.device_type.name,
                'state': device.state
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route("/api/v1/devices/<int:id>", methods=['GET', 'POST'])
    def device_api(id):
        device = Device.query.filter_by(id=id).first()
        if not device:
            abort(404)
        if request.method == 'POST':
            if not request.json or 'state' not in request.json or not isinstance(request.json['state'], bool):
                abort(400)
            if request.json['state']:
                turn_on(device)
            else:
                turn_off(device)
            response = jsonify({'result': True})
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'id': device.id,
                'name': device.name,
                'device_type': device.device_type.name,
                'state': device.state
            })
            response.status_code = 200
            return response

    @app.route("/shutdown")
    def shutdown():
        devices = Device.query.filter_by(state=True)
        for device in devices:
            turn_off(device)
            Device.query.filter_by(id=device.id).update({'state': False})
        db.session.commit()
        return render_template("index.html", devices=devices)

    @app.route("/activate")
    def activate():
        devices = Device.query.filter_by(state=False)
        lights = ['LEDs', 'Living Room', 'Kitchen Light']
        for device in devices:
            if device.name in lights:
                turn_on(device)
                Device.query.filter_by(id=device.id).update({'state': True})
        db.session.commit()
        return render_template("index.html", devices=devices)

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
                        turn_on(device)
                    else:
                        state = False
                        turn_off(device)
                    Device.query.filter_by(id=device_id).update({'state': state})
                    db.session.commit()
                    return redirect(url_for('index'))
            else:
                return 'Device not found'

    return app