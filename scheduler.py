from tzlocal import get_localzone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
import os

FILE_PATH =  os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'scheduler.db'
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///' + os.path.join(FILE_PATH, DB_NAME))
}

scheduler = BackgroundScheduler(jobstores=jobstores, timezone=get_localzone())

def timer(device, func, time_delta):
    scheduler.add_job(func, 'date', args=[device.device_id], next_run_time= datetime.now() + time_delta, id=get_new_id(device))

def get_jobs(device):
    jobs = [j for j in scheduler.get_jobs() if j.id.split('-')[0] == device.name]
    return jobs

def get_new_id(device):
    jobs = get_jobs(device)
    used_ids = [int(job.id.split('-')[1]) for job in jobs]

    def find_available_id(ids):
        new_id = 1
        for id in sorted(ids):
            if new_id != id:
                return new_id
            else:
                new_id += 1
        return new_id

    return '{}-{}'.format(device.name, find_available_id(used_ids))
