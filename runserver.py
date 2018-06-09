"""
MAIN APP
"""
import os 

from app import create_app
from scheduler import scheduler

app_env = os.getenv('ENVIRONMENT', 'development')
app = create_app(app_env)

if __name__ == "__main__":
  scheduler.start()
  if app_env == 'deployment':
    app.run(host='0.0.0.0')
  else:
    app.run(host='0.0.0.0')
