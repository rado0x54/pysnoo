"""The main API class"""
from typing import List, Optional
from datetime import date

from .const import (SNOO_ME_ENDPOINT,
                    SNOO_DEVICES_ENDPOINT,
                    SNOO_BABY_ENDPOINT,
                    SNOO_SESSIONS_LAST_ENDPOINT)
from .auth_session import SnooAuthSession
from .models import (User, Device, Baby, Sex,
                     MinimalLevel,
                     MinimalLevelVolume,
                     ResponsivenessLevel,
                     SoothingLevelVolume,
                     LastSession)


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

    async def get_devices(self) -> List[User]:
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
