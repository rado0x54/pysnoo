"""TestClass for all Snoo Models"""

import json
from unittest import TestCase
from datetime import datetime, timedelta

from pysnoo import (User, Device, Baby, LastSession,
                    ResponsivenessLevel,
                    MinimalLevelVolume,
                    SoothingLevelVolume,
                    MinimalLevel,
                    SessionLevel,
                    AggregatedSession,
                    SessionItemType,
                    AggregatedSessionAvg)


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

    def test_device_mapping(self):
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

    def test_baby_mapping(self):
        """Test successful mapping from json payload"""
        baby_payload = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        baby = Baby.from_dict(baby_payload)

        self.assertEqual(baby.baby, baby_payload['_id'])
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

    def test_last_session_mapping(self):
        """Test successful mapping from json payload"""
        last_session_payload = json.loads(load_fixture('', 'ss_v2_sessions_last__get_200.json'))
        last_session = LastSession.from_dict(last_session_payload)

        self.assertEqual(last_session.start_time,
                         datetime.strptime(last_session_payload['startTime'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(last_session.end_time,
                         datetime.strptime(last_session_payload['endTime'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(last_session.duration, timedelta(seconds=36, milliseconds=729))
        self.assertEqual(last_session.levels, [
            SessionLevel.BASELINE,
            SessionLevel.LEVEL1,
            SessionLevel.LEVEL2,
            SessionLevel.LEVEL2,
            SessionLevel.LEVEL2,
            SessionLevel.LEVEL3,
            SessionLevel.LEVEL4,
            SessionLevel.ONLINE
        ])

    def test_aggregated_session_mapping(self):
        """Test successful mapping from json payload"""
        aggregated_session_payload = json.loads(load_fixture('', 'ss_v2_sessions_aggregated__get_200.json'))
        aggregated_session = AggregatedSession.from_dict(aggregated_session_payload)

        self.assertEqual(aggregated_session.day_sleep, timedelta(seconds=aggregated_session_payload['daySleep']))
        self.assertEqual(aggregated_session.longest_sleep,
                         timedelta(seconds=aggregated_session_payload['longestSleep']))
        self.assertEqual(aggregated_session.naps, aggregated_session_payload['naps'])
        self.assertEqual(aggregated_session.night_sleep, timedelta(seconds=aggregated_session_payload['nightSleep']))
        self.assertEqual(aggregated_session.night_wakings, aggregated_session_payload['nightWakings'])
        self.assertEqual(aggregated_session.timezone, aggregated_session_payload['timezone'])
        self.assertEqual(aggregated_session.total_sleep, timedelta(seconds=aggregated_session_payload['totalSleep']))

        # Levels:
        self.assertEqual(len(aggregated_session.levels), len(aggregated_session_payload['levels']))
        for session_item, session_item_payload in zip(aggregated_session.levels, aggregated_session_payload['levels']):
            self.assertEqual(session_item.is_active, session_item_payload['isActive'])
            self.assertEqual(session_item.session_id, session_item_payload['sessionId'])
            self.assertEqual(session_item.start_time,
                             datetime.strptime(session_item_payload['startTime'], "%Y-%m-%d %H:%M:%S.%f"))
            self.assertEqual(session_item.state_duration, timedelta(seconds=session_item_payload['stateDuration']))
            self.assertEqual(session_item.type, SessionItemType(session_item_payload['type']))

    def test_aggregated_session_avg_mapping(self):
        """Test successful mapping from json payload"""
        aggregated_session_avg_payload = json.loads(
            load_fixture('', 'ss_v2_babies_sessions_aggregated_avg__get_200.json'))
        aggregated_session_avg = AggregatedSessionAvg.from_dict(aggregated_session_avg_payload)

        self.assertEqual(aggregated_session_avg.total_sleep_avg,
                         timedelta(seconds=aggregated_session_avg_payload['totalSleepAVG']))
        self.assertEqual(aggregated_session_avg.day_sleep_avg,
                         timedelta(seconds=aggregated_session_avg_payload['daySleepAVG']))
        self.assertEqual(aggregated_session_avg.night_sleep_avg,
                         timedelta(seconds=aggregated_session_avg_payload['nightSleepAVG']))
        self.assertEqual(aggregated_session_avg.longest_sleep_avg,
                         timedelta(seconds=aggregated_session_avg_payload['longestSleepAVG']))
        self.assertEqual(aggregated_session_avg.night_wakings_avg,
                         aggregated_session_avg_payload['nightWakingsAVG'])
        self.assertIsNotNone(aggregated_session_avg.days)
        self.assertEqual(aggregated_session_avg.days.total_sleep,
                         [timedelta(seconds=item) for item in aggregated_session_avg_payload['days']['totalSleep']])
        self.assertEqual(aggregated_session_avg.days.day_sleep,
                         [timedelta(seconds=item) for item in aggregated_session_avg_payload['days']['daySleep']])
        self.assertEqual(aggregated_session_avg.days.night_sleep,
                         [timedelta(seconds=item) for item in aggregated_session_avg_payload['days']['nightSleep']])
        self.assertEqual(aggregated_session_avg.days.longest_sleep,
                         [timedelta(seconds=item) for item in aggregated_session_avg_payload['days']['longestSleep']])
        self.assertEqual(aggregated_session_avg.days.night_wakings,
                         aggregated_session_avg_payload['days']['nightWakings'])
