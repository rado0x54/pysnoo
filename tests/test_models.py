"""TestClass for all Snoo Models"""

import json
from unittest import TestCase
from datetime import datetime, timedelta, timezone

from pysnoo import (User, Device, Baby, LastSession,
                    ResponsivenessLevel,
                    MinimalLevelVolume,
                    SoothingLevelVolume,
                    MinimalLevel,
                    SessionLevel,
                    AggregatedSession,
                    SessionItemType,
                    AggregatedSessionAvg,
                    ActivityState)


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

        # Check to_dict()
        self.assertEqual(user.to_dict(), user_payload)

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

        # Check to_dict()
        self.assertEqual(device.to_dict(), device_payload)

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

        # Check to_dict()
        baby_to_dict_payload = baby_payload
        baby_to_dict_payload['baby'] = baby_payload['_id']
        baby_to_dict_payload['birthDate'] = baby_to_dict_payload['birthDate'][:10]  # Remove time from ISO
        baby_to_dict_payload['preemie'] = None
        del baby_to_dict_payload['_id']
        self.assertEqual(baby.to_dict(), baby_to_dict_payload)

    def test_last_session_mapping(self):
        """Test successful mapping from json payload"""
        last_session_payload = json.loads(load_fixture('', 'ss_v2_sessions_last__get_200.json'))
        last_session = LastSession.from_dict(last_session_payload)

        self.assertEqual(last_session.start_time,
                         datetime.strptime(last_session_payload['startTime'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(last_session.end_time,
                         datetime.strptime(last_session_payload['endTime'], "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.assertEqual(last_session.current_status, SessionItemType.AWAKE)
        # Maybe update to mock datetime.now() for cleaner test.
        self.assertLessEqual(last_session.current_status_duration, datetime.now(timezone.utc) - last_session.end_time)
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

        # Check to_dict()
        last_session_to_dict_payload = last_session_payload
        last_session_to_dict_payload['levels'] = [item['level'] for item in last_session_to_dict_payload['levels']]
        last_session_to_dict_payload['currentStatus'] = last_session.current_status.value

        last_session_to_dict = last_session.to_dict()
        # Hacky, solution for not mocking datetime.now().
        last_session_to_dict_payload['currentStatusDuration'] = last_session_to_dict['currentStatusDuration']
        self.assertEqual(last_session_to_dict, last_session_to_dict_payload)

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

        # Check to_dict()
        aggregated_session_to_dict_payload = aggregated_session_payload
        aggregated_session_to_dict_payload['daySleep'] = str(
            timedelta(seconds=aggregated_session_to_dict_payload['daySleep']))
        aggregated_session_to_dict_payload['levels'] = [{
            'isActive': item['isActive'],
            'sessionId': item['sessionId'],
            'startTime': item['startTime'].replace(' ', 'T'),
            'stateDuration': str(timedelta(seconds=item['stateDuration'])),
            'type': item['type'],
        } for item in aggregated_session_to_dict_payload['levels']]
        aggregated_session_to_dict_payload['longestSleep'] = str(
            timedelta(seconds=aggregated_session_to_dict_payload['longestSleep']))
        aggregated_session_to_dict_payload['nightSleep'] = str(
            timedelta(seconds=aggregated_session_to_dict_payload['nightSleep']))
        aggregated_session_to_dict_payload['totalSleep'] = str(
            timedelta(seconds=aggregated_session_to_dict_payload['totalSleep']))
        self.assertEqual(aggregated_session.to_dict(), aggregated_session_to_dict_payload)

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

        # Check to_dict()
        aggregated_session_avg_to_dict_payload = aggregated_session_avg_payload
        aggregated_session_avg_to_dict_payload['daySleepAVG'] = str(
            timedelta(seconds=aggregated_session_avg_to_dict_payload['daySleepAVG']))
        aggregated_session_avg_to_dict_payload['totalSleepAVG'] = str(
            timedelta(seconds=aggregated_session_avg_to_dict_payload['totalSleepAVG']))
        aggregated_session_avg_to_dict_payload['nightSleepAVG'] = str(
            timedelta(seconds=aggregated_session_avg_to_dict_payload['nightSleepAVG']))
        aggregated_session_avg_to_dict_payload['longestSleepAVG'] = str(
            timedelta(seconds=aggregated_session_avg_to_dict_payload['longestSleepAVG']))

        aggregated_session_avg_to_dict_payload['days']['daySleep'] = [
            str(timedelta(seconds=item)) for item in aggregated_session_avg_to_dict_payload['days']['daySleep']
        ]
        aggregated_session_avg_to_dict_payload['days']['totalSleep'] = [
            str(timedelta(seconds=item)) for item in aggregated_session_avg_to_dict_payload['days']['totalSleep']
        ]
        aggregated_session_avg_to_dict_payload['days']['nightSleep'] = [
            str(timedelta(seconds=item)) for item in aggregated_session_avg_to_dict_payload['days']['nightSleep']
        ]
        aggregated_session_avg_to_dict_payload['days']['longestSleep'] = [
            str(timedelta(seconds=item)) for item in aggregated_session_avg_to_dict_payload['days']['longestSleep']
        ]
        self.assertEqual(aggregated_session_avg.to_dict(), aggregated_session_avg_to_dict_payload)

    def test_activity_signal_mapping(self):
        """Test successful mapping from json payload"""
        activity_state_msg_payload = json.loads(
            load_fixture('', 'pubnub_message_ActivityState.json'))
        activity_state = ActivityState.from_dict(activity_state_msg_payload)

        self.assertEqual(activity_state.left_safety_clip, activity_state_msg_payload['left_safety_clip'])
        self.assertIsNotNone(activity_state.rx_signal)
        self.assertEqual(activity_state.rx_signal.rssi, activity_state_msg_payload['rx_signal']['rssi'])
        self.assertEqual(activity_state.rx_signal.strength, activity_state_msg_payload['rx_signal']['strength'])
        self.assertEqual(activity_state.right_safety_clip, activity_state_msg_payload['right_safety_clip'])
        self.assertEqual(activity_state.sw_version, activity_state_msg_payload['sw_version'])
        self.assertEqual(activity_state.event_time.timestamp() * 1000, activity_state_msg_payload['event_time_ms'])
        self.assertIsNotNone(activity_state.state_machine)
        self.assertEqual(activity_state.state_machine.up_transition.value,
                         activity_state_msg_payload['state_machine']['up_transition'])
        self.assertEqual(activity_state.state_machine.since_session_start.total_seconds() * 1000,
                         activity_state_msg_payload['state_machine']['since_session_start_ms'])
        self.assertEqual(activity_state.state_machine.sticky_white_noise,
                         activity_state_msg_payload['state_machine']['sticky_white_noise'] == 'on')
        self.assertEqual(activity_state.state_machine.weaning,
                         activity_state_msg_payload['state_machine']['weaning'] == 'on')
        self.assertEqual(activity_state.state_machine.time_left, None)
        self.assertEqual(activity_state.state_machine.session_id,
                         activity_state_msg_payload['state_machine']['session_id'])
        self.assertEqual(activity_state.state_machine.state.value, activity_state_msg_payload['state_machine']['state'])
        self.assertEqual(activity_state.state_machine.is_active_session,
                         activity_state_msg_payload['state_machine']['is_active_session'] == 'true')
        self.assertEqual(activity_state.state_machine.down_transition.value,
                         activity_state_msg_payload['state_machine']['down_transition'])
        self.assertEqual(activity_state.state_machine.hold, activity_state_msg_payload['state_machine']['hold'] == 'on')
        self.assertEqual(activity_state.state_machine.audio,
                         activity_state_msg_payload['state_machine']['audio'] == 'on')
        self.assertEqual(activity_state.system_state, activity_state_msg_payload['system_state'])
        self.assertEqual(activity_state.event.value, activity_state_msg_payload['event'])

        # Check to_dict()
        activity_state_msg_to_dict_payload = activity_state_msg_payload
        activity_state_msg_to_dict_payload['event_time'] = datetime.fromtimestamp(
            activity_state_msg_to_dict_payload['event_time_ms'] / 1000, timezone.utc
        ).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        del activity_state_msg_to_dict_payload['event_time_ms']
        activity_state_msg_to_dict_payload['left_safety_clip'] = bool(
            activity_state_msg_to_dict_payload['left_safety_clip'])
        activity_state_msg_to_dict_payload['right_safety_clip'] = bool(
            activity_state_msg_to_dict_payload['right_safety_clip'])
        activity_state_msg_to_dict_payload['state_machine']['audio'] = \
            activity_state_msg_to_dict_payload['state_machine']['audio'] == 'on'
        activity_state_msg_to_dict_payload['state_machine']['hold'] = \
            activity_state_msg_to_dict_payload['state_machine']['hold'] == 'on'
        activity_state_msg_to_dict_payload['state_machine']['is_active_session'] = \
            activity_state_msg_to_dict_payload['state_machine']['is_active_session'] == 'true'
        activity_state_msg_to_dict_payload['state_machine']['sticky_white_noise'] = \
            activity_state_msg_to_dict_payload['state_machine']['sticky_white_noise'] == 'on'
        activity_state_msg_to_dict_payload['state_machine']['weaning'] = \
            activity_state_msg_to_dict_payload['state_machine']['weaning'] == 'on'
        activity_state_msg_to_dict_payload['state_machine']['time_left'] = None
        activity_state_msg_to_dict_payload['state_machine']['since_session_start'] = str(timedelta(
            milliseconds=activity_state_msg_to_dict_payload['state_machine']['since_session_start_ms']
        ))
        del activity_state_msg_to_dict_payload['state_machine']['since_session_start_ms']
        self.assertEqual(activity_state.to_dict(), activity_state_msg_to_dict_payload)

    def test_session_level(self):
        """Test SessionLevel Enum"""
        self.assertTrue(SessionLevel.BASELINE.is_active_level())
        self.assertTrue(SessionLevel.WEANING_BASELINE.is_active_level())
        self.assertTrue(SessionLevel.LEVEL1.is_active_level())
        self.assertTrue(SessionLevel.LEVEL2.is_active_level())
        self.assertTrue(SessionLevel.LEVEL3.is_active_level())
        self.assertTrue(SessionLevel.LEVEL4.is_active_level())
        self.assertFalse(SessionLevel.ONLINE.is_active_level())
        self.assertFalse(SessionLevel.NONE.is_active_level())
        self.assertFalse(SessionLevel.PRETIMEOUT.is_active_level())
