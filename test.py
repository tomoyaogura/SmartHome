import unittest
import os
import json
from app import create_app
from database import db
from scheduler import scheduler
from models import Device, DeviceType

class APITestCase(unittest.TestCase):
    def setUp(self):
        scheduler.start()
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.devices = {'name': 'test'}
        with self.app.app_context():
            db.create_all()
            db.session.add(Device(name='Test Fan', device_id='L-20', device_type=DeviceType.FAN))
            db.session.add(Device(name='Test RF', device_id='101-1', device_type=DeviceType.RF))
            db.session.commit()

    def test_get_devices(self):
        """ Test API can list devices """
        response = self.client().get('/api/v1/devices/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Fan', response.data)
        self.assertIn('Test RF', response.data)

    def test_get_device(self):
        """ Test API can get specific device """
        response = self.client().get('/api/v1/devices/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Fan', response.data)
        
        response = self.client().get('/api/v1/devices/404')
        self.assertEqual(response.status_code, 404)

    def test_post_device(self):
        """ Test API can enable devices """
        response = self.client().get('/api/v1/devices/1')
        resp_json = json.loads(response.data)
        self.assertEqual(resp_json['state'], False)

        response = self.client().post('/api/v1/devices/1', data=json.dumps({'state': True}), 
                                      content_type='application/json')
        
        response = self.client().get('/api/v1/devices/1')
        resp_json = json.loads(response.data)
        self.assertEqual(resp_json['state'], True)

    def tearDown(self):
        scheduler.shutdown()
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__== "__main__":
    unittest.main()