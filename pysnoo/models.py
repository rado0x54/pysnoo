# coding: utf-8
"""PySnoo Data Models."""
from typing import List
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from enum import Enum


# from: https://github.com/ctalkington/python-sonarr/blob/master/sonarr/models.py
def dt_str_to_dt(dt_str: str) -> datetime:
    """Convert ISO-8601 datetime string to datetime object."""
    if dt_str is None:
        return None

    utc = False

    if "Z" in dt_str:
        utc = True
        dt_str = dt_str[:-1]

    if "." in dt_str:
        # Python doesn't support long microsecond values
        ts_bits = dt_str.split(".", 1)
        dt_str = "{}.{}".format(ts_bits[0], ts_bits[1][:3])
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
    else:
        fmt = "%Y-%m-%dT%H:%M:%S"

    if utc:
        dt_str += "Z"
        fmt += "%z"

    return datetime.strptime(dt_str, fmt)


@dataclass(frozen=True)
class User:
    """Object holding the user information from Snoo."""

    email: str
    given_name: str
    region: str
    surname: str
    user_id: str

    @staticmethod
    def from_dict(data: dict):
        """Return user object from dict."""
        return User(
            email=data.get("email", ""),
            given_name=data.get("givenName", ""),
            region=data.get("region", ""),
            surname=data.get("surname", ""),
            user_id=data.get("userId", ""),
        )


@dataclass(frozen=True)
class SSID:
    """Object holding ssid information."""

    name: str
    updated_at: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return SSID object from dict."""
        return SSID(
            name=data.get("name", ""),
            updated_at=dt_str_to_dt(data.get("updatedAt", None))
        )


@dataclass(frozen=True)
class Device:
    """Object holding Snoo device information."""
    baby: str
    created_at: datetime
    firmware_update_date: datetime
    firmware_version: str
    last_provision_success: datetime
    last_ssid: SSID
    serial_number: str
    timezone: str
    updated_at: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return device object from dict."""
        return Device(
            baby=data.get("baby", ""),
            created_at=dt_str_to_dt(data.get("createdAt", None)),
            firmware_update_date=dt_str_to_dt(data.get("firmwareUpdateDate", None)),
            firmware_version=data.get("firmwareVersion", ""),
            last_provision_success=dt_str_to_dt(data.get("lastProvisionSuccess", None)),
            last_ssid=SSID.from_dict(data.get("lastSSID", {})),
            serial_number=data.get("serialNumber", ""),
            timezone=data.get("timezone", ""),
            updated_at=dt_str_to_dt(data.get("updatedAt", None)),
        )


@dataclass(frozen=True)
class Picture:
    """Object holding picture information."""

    id: str  # pylint: disable=invalid-name
    mime: str
    encoded: bool
    updated_at: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return picture object from dict."""
        return Picture(
            id=data.get("id", ""),
            mime=data.get("mime", ""),
            encoded=data.get("encoded", False),
            updated_at=dt_str_to_dt(data.get("updatedAt", None)),
        )


class ResponsivenessLevel(Enum):
    """Enum for ResponsivenessLevel"""
    VERY_LOW = 'lvl-2'
    LOW = 'lvl-1'
    NORMAL = 'lvl0'
    HIGH = 'lvl+1'
    VERY_HIGH = 'lvl+2'


class MinimalLevelVolume(Enum):
    """Enum for MinimalLevelVolume"""
    VERY_LOW = 'lvl-2'
    LOW = 'lvl-1'
    NORMAL = 'lvl0'
    HIGH = 'lvl+1'
    VERY_HIGH = 'lvl+2'


class SoothingLevelVolume(Enum):
    """Enum for SoothingLevelVolume"""
    NORMAL = 'lvl0'
    HIGH = 'lvl+1'
    VERY_HIGH = 'lvl+2'


class MinimalLevel(Enum):
    """Enum for MinimalLevel"""
    BASELINE = 'baseline'
    LEVEL1 = 'level1'
    LEVEL2 = 'level2'


class Sex(Enum):
    """Enum for Sex"""
    MALE = 'Male'
    FEMALE = 'Female'


@dataclass(frozen=True)
class Settings:
    """Object holding Snoo Settings information."""

    responsiveness_level: ResponsivenessLevel
    minimal_level_volume: str
    soothing_level_volume: str
    minimal_level: str
    motion_limiter: bool
    weaning: bool
    car_ride_mode: bool
    offline_lock: bool
    # App restriction is 5-12 (am)
    daytime_start: int

    @staticmethod
    def from_dict(data: dict):
        """Return device object from dict."""
        return Settings(
            responsiveness_level=ResponsivenessLevel(data.get("responsivenessLevel", "lvl0")),
            minimal_level_volume=MinimalLevelVolume(data.get("minimalLevelVolume", "lvl0")),
            soothing_level_volume=SoothingLevelVolume(data.get("soothingLevelVolume", "lvl0")),
            minimal_level=MinimalLevel(data.get("minimalLevel", "baseline")),
            motion_limiter=data.get("motionLimiter", False),
            weaning=data.get("weaning", False),
            car_ride_mode=data.get("carRideMode", False),
            offline_lock=data.get("offlineLock", False),
            daytime_start=data.get("daytimeStart", 7)
        )


@dataclass(frozen=True)
class Baby:
    """Return baby object from dict."""

    baby_name: str
    birth_date: date
    created_at: datetime
    disabled_limiter: bool
    pictures: List[Picture]
    # Can be None
    preemie: int
    settings: Settings
    # Can be None
    sex: Sex
    updated_at: datetime
    updated_by_user_at: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return baby object from dict."""
        birth_date = dt_str_to_dt(data.get("birthDate", None))
        if birth_date is not None:
            birth_date = birth_date.date()

        return Baby(
            baby_name=data.get("babyName", ""),
            birth_date=birth_date,
            created_at=dt_str_to_dt(data.get("createdAt", None)),
            disabled_limiter=data.get("disabledLimiter", False),
            pictures=[Picture.from_dict(p) for p in data.get("pictures", [])],
            settings=Settings.from_dict(data.get("settings", {})),
            preemie=data.get("preemie", None),
            sex=data.get("sex", None),
            updated_at=dt_str_to_dt(data.get("updatedAt", None)),
            updated_by_user_at=dt_str_to_dt(data.get("updatedByUserAt", None)),
        )


class SessionLevel(Enum):
    """Enum for SessionLevel"""
    ONLINE = 'ONLINE'
    BASELINE = 'BASELINE'
    LEVEL1 = 'LEVEL1'
    LEVEL2 = 'LEVEL2'
    LEVEL3 = 'LEVEL3'
    LEVEL4 = 'LEVEL4'


@dataclass(frozen=True)
class LastSession:
    """Return LastSession object from dict."""

    end_time: datetime
    levels: List[SessionLevel]
    start_time: datetime

    @property
    def duration(self) -> timedelta:
        """Return the duration of the last session"""
        return self.end_time - self.start_time

    @staticmethod
    def from_dict(data: dict):
        """Return LastSession object from dict."""
        return LastSession(
            end_time=dt_str_to_dt(data.get("endTime", None)),
            levels=[SessionLevel(item['level']) for item in data.get("levels", [])],
            start_time=dt_str_to_dt(data.get("startTime", None)),
        )
