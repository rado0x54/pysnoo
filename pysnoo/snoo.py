"""The main API class"""
from typing import List, Optional
from datetime import date, datetime, timedelta

from .const import (SNOO_ME_ENDPOINT,
                    SNOO_DEVICES_ENDPOINT,
                    SNOO_BABY_ENDPOINT,
                    SNOO_SESSIONS_LAST_ENDPOINT,
                    SNOO_SESSIONS_AGGREGATED_ENDPOINT,
                    SNOO_SESSIONS_AGGREGATED_AVG_ENDPOINT,
                    SNOO_SESSIONS_TOTAL_TIME_ENDPOINT,
                    DATETIME_FMT_AGGREGATED_SESSION)
from .auth_session import SnooAuthSession
from .models import (User, Device, Baby, Sex,
                     MinimalLevel,
                     MinimalLevelVolume,
                     ResponsivenessLevel,
                     SoothingLevelVolume,
                     LastSession,
                     AggregatedSession,
                     AggregatedSessionAvg,
                     AggregatedSessionInterval)


class Snoo:
    """A Python Abstraction object to Snoo Smart Sleeper Bassinett."""
    def __init__(self, auth: SnooAuthSession):
        """Initialize the Snoo object."""
        self.auth = auth

    async def get_me(self) -> User:
        """Return Information about the current User"""
        async with self.auth.get(SNOO_ME_ENDPOINT) as resp:
            assert resp.status == 200
            return User.from_dict(await resp.json())

    async def get_devices(self) -> List[Device]:
        """Return Information about the configured devices"""
        async with self.auth.get(SNOO_DEVICES_ENDPOINT) as resp:
            assert resp.status == 200
            resp_json = await resp.json()
            return [Device.from_dict(d) for d in resp_json]

    async def get_baby(self) -> Baby:
        """Return Information about the current User"""
        async with self.auth.get(SNOO_BABY_ENDPOINT) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def get_last_session(self) -> LastSession:
        """Return Information about the last session"""
        async with self.auth.get(SNOO_SESSIONS_LAST_ENDPOINT) as resp:
            assert resp.status == 200
            return LastSession.from_dict(await resp.json())

    async def get_aggregated_session(self, start_time: datetime) -> AggregatedSession:
        """Return Information about the aggregated session

        This function returns information about the next 24h segment beginning from start_time.
        Note, start_time does not contain or respect a timezone property, but it will assume the
        timezone that is configured server-side.
        """
        url_params = {
            'startTime': start_time.strftime(DATETIME_FMT_AGGREGATED_SESSION)[:-3]
        }
        async with self.auth.get(SNOO_SESSIONS_AGGREGATED_ENDPOINT,
                                 params=url_params) as resp:
            assert resp.status == 200
            return AggregatedSession.from_dict(await resp.json())

    async def get_aggregated_session_avg(self,
                                         baby: str,
                                         start_time: datetime,
                                         interval: AggregatedSessionInterval = AggregatedSessionInterval.WEEK,
                                         days: bool = True) -> AggregatedSessionAvg:
        """Return Information about the aggregated session averages

        :param baby: ID of baby to get average for
        :param start_time: start_time of the interval (time is ignored)
        :param interval: week/month calculate average for a week or month interval
        :param days: true/false Include value for each day in response payload
        :return:
        """
        url_params = {
            'startTime': start_time.strftime(DATETIME_FMT_AGGREGATED_SESSION)[:-3],
            'interval': interval.value,
            'days': str(days).lower(),
        }
        async with self.auth.get(SNOO_SESSIONS_AGGREGATED_AVG_ENDPOINT.format(baby),
                                 params=url_params) as resp:
            assert resp.status == 200
            return AggregatedSessionAvg.from_dict(await resp.json())

    async def get_session_total_time(self,
                                     baby: str) -> timedelta:
        """Return Information about the total usage of a Snoo

        :param baby: ID of baby to get the total time for
        :return:
        """
        async with self.auth.get(SNOO_SESSIONS_TOTAL_TIME_ENDPOINT.format(baby)) as resp:
            assert resp.status == 200
            resp_json = await resp.json()
            return timedelta(seconds=resp_json.get('totalTime', 0))

    async def set_baby_info(self,
                            baby_name: str,
                            birth_date: date,
                            preemie: Optional[int],
                            sex: Optional[Sex]) -> Baby:
        """Updates and returns baby-related information"""

        if sex is not None:
            sex = sex.value
        request_payload = {
            'babyName': baby_name,
            'birthDate': birth_date.isoformat(),
            'preemie': preemie,
            'sex': sex
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def set_minimal_level(self,
                                minimal_level: MinimalLevel) -> Baby:
        """Updates minimal_level setting and returns baby-related information"""
        request_payload = {
            'settings': {
                'minimalLevel': minimal_level.value
            }
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def set_minimal_level_volume(self,
                                       minimal_level_volume: MinimalLevelVolume) -> Baby:
        """Updates minimal_level_volume setting and returns baby-related information"""
        request_payload = {
            'settings': {
                'minimalLevelVolume': minimal_level_volume.value
            }
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def set_responsiveness_level(self,
                                       responsiveness_level: ResponsivenessLevel) -> Baby:
        """Updates responsiveness_level setting and returns baby-related information"""
        request_payload = {
            'settings': {
                'responsivenessLevel': responsiveness_level.value
            }
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def set_soothing_level_volume(self,
                                        soothing_level_volume: SoothingLevelVolume) -> Baby:
        """Updates soothing_level_volume setting and returns baby-related information"""
        request_payload = {
            'settings': {
                'soothingLevelVolume': soothing_level_volume.value
            }
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def set_motion_limiter(self,
                                 motion_limiter: bool) -> Baby:
        """Updates motion_limiter setting and returns baby-related information"""
        request_payload = {
            'settings': {
                'motionLimiter': motion_limiter
            }
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())

    async def set_weaning(self,
                          weaning: bool) -> Baby:
        """Updates weaning setting and returns baby-related information"""
        request_payload = {
            'settings': {
                'weaning': weaning
            }
        }

        async with self.auth.patch(SNOO_BABY_ENDPOINT, json=request_payload) as resp:
            assert resp.status == 200
            return Baby.from_dict(await resp.json())
