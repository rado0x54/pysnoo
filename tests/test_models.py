"""TestClass for all Snoo Models"""

import json
from unittest import TestCase
from datetime import datetime

from pysnoo import (User,
                    Device,
                    Baby,
                    ResponsivenessLevel,
                    MinimalLevelVolume,
                    SoothingLevelVolume,
                    MinimalLevel)


from .helpers import load_fixture


class TestSnooModels(TestCase):
    """Snoo Models Test class"""

    def test_user_model_mapping(self):
        """Test successful mapping from json payload"""
        user_payload = json.loads(load_fixture('', 'us_me__get_200.json'))
        user = User.from_dict(user_payload)

        self.assertEqual(user.email, user_payload['email'])
        self.assertEqual(user.given_name, user_payload['givenName'])
        self.assertEqual(user.region, user_payload['region'])
        self.assertEqual(user.surname, user_payload['surname'])
        self.assertEqual(user.user_id, user_payload['userId'])

    def test_user_device_mapping(self):
        """Test successful mapping from json payload"""
        device_payload = json.loads(load_fixture('', 'ds_me_devices__get_200.json'))[0]
        device = Device.from_dict(device_payload)

        self.assertEqual(device.baby, device_payload['baby'])
        self.assertEqual(device.created_at, datetime.strptime(device_payload['createdAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(device.firmware_update_date,
                         datetime.strptime(device_payload['firmwareUpdateDate'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(device.firmware_version, device_payload['firmwareVersion'])
        self.assertEqual(device.last_provision_success,
                         datetime.strptime(device_payload['lastProvisionSuccess'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(device.last_ssid.name, device_payload['lastSSID']['name'])
        self.assertEqual(device.last_ssid.updated_at,
                         datetime.strptime(device_payload['lastSSID']['updatedAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(device.serial_number, device_payload['serialNumber'])
        self.assertEqual(device.updated_at, datetime.strptime(device_payload['updatedAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))

    def test_user_baby_mapping(self):
        """Test successful mapping from json payload"""
        baby_payload = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        baby = Baby.from_dict(baby_payload)

        self.assertEqual(baby.baby_name, baby_payload['babyName'])
        self.assertEqual(baby.birth_date, datetime.strptime(baby_payload['birthDate'], "%Y-%m-%dT%H:%M:%S.%f%z").date())
        self.assertEqual(baby.created_at, datetime.strptime(baby_payload['createdAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(baby.disabled_limiter, baby_payload['disabledLimiter'])
        self.assertEqual(len(baby.pictures), 1)
        self.assertEqual(baby.pictures[0].id, baby_payload['pictures'][0]['id'])
        self.assertEqual(baby.pictures[0].mime, baby_payload['pictures'][0]['mime'])
        self.assertEqual(baby.pictures[0].encoded, baby_payload['pictures'][0]['encoded'])
        self.assertEqual(baby.pictures[0].updated_at,
                         datetime.strptime(baby_payload['pictures'][0]['updatedAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(baby.settings.responsiveness_level,
                         ResponsivenessLevel(baby_payload['settings']['responsivenessLevel']))
        self.assertEqual(baby.settings.minimal_level_volume,
                         MinimalLevelVolume(baby_payload['settings']['minimalLevelVolume']))
        self.assertEqual(baby.settings.soothing_level_volume,
                         SoothingLevelVolume(baby_payload['settings']['soothingLevelVolume']))
        self.assertEqual(baby.settings.minimal_level, MinimalLevel(baby_payload['settings']['minimalLevel']))
        self.assertEqual(baby.settings.motion_limiter, baby_payload['settings']['motionLimiter'])
        self.assertEqual(baby.settings.weaning, baby_payload['settings']['weaning'])
        self.assertEqual(baby.settings.car_ride_mode, baby_payload['settings']['carRideMode'])
        self.assertEqual(baby.settings.offline_lock, baby_payload['settings']['offlineLock'])
        self.assertEqual(baby.settings.daytime_start, baby_payload['settings']['daytimeStart'])
        self.assertEqual(baby.sex, baby_payload['sex'])
        self.assertEqual(baby.updated_at, datetime.strptime(baby_payload['updatedAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(baby.updated_by_user_at,
                         datetime.strptime(baby_payload['updatedByUserAt'], "%Y-%m-%dT%H:%M:%S.%f%z"))
