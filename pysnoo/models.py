"""PySnoo Data Models."""
import logging
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, date, timedelta, timezone
from enum import Enum

from .const import DATETIME_FMT_AGGREGATED_SESSION

_LOGGER = logging.getLogger(__name__)

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


def dt_to_dt_str(dt_value: datetime) -> str:
    """Convert datetime object to ISO-8601 datetime string object."""
    if dt_value is None:
        return None

    return dt_value.isoformat(timespec='milliseconds').replace('+00:00', 'Z')


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

    def to_dict(self):
        """Return dict from Object"""
        return {
            "email": self.email,
            "givenName": self.given_name,
            "region": self.region,
            "surname": self.surname,
            "userId": self.user_id
        }


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

    def to_dict(self):
        """Return dict from Object"""
        return {
            "name": self.name,
            "updatedAt": dt_to_dt_str(self.updated_at)
        }


@dataclass(frozen=True)
class Device:
    """Object holding Snoo device information."""
    baby: str  # ID of baby
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

    def to_dict(self):
        """Return dict from Object"""
        return {
            "baby": self.baby,
            "createdAt": dt_to_dt_str(self.created_at),
            "firmwareUpdateDate": dt_to_dt_str(self.firmware_update_date),
            "firmwareVersion": self.firmware_version,
            "lastProvisionSuccess": dt_to_dt_str(self.last_provision_success),
            "lastSSID": self.last_ssid.to_dict(),
            "serialNumber": self.serial_number,
            "timezone": self.timezone,
            "updatedAt": dt_to_dt_str(self.updated_at)
        }


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

    def to_dict(self):
        """Return dict from Object"""
        return {
            "id": self.id,
            "mime": self.mime,
            "encoded": self.encoded,
            "updatedAt": dt_to_dt_str(self.updated_at)
        }


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
    minimal_level_volume: MinimalLevelVolume
    soothing_level_volume: SoothingLevelVolume
    minimal_level: MinimalLevel
    motion_limiter: bool
    weaning: bool
    car_ride_mode: bool
    offline_lock: bool
    # App restriction is 5-12 (am)
    daytime_start: int
    sticky_white_noise_timeout: int

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
            daytime_start=data.get("daytimeStart", 7),
            sticky_white_noise_timeout=data.get("stickyWhiteNoiseTimeout", 0)
        )

    def to_dict(self):
        """Return dict from Object"""
        return {
            "responsivenessLevel": self.responsiveness_level.value,
            "minimalLevelVolume": self.minimal_level_volume.value,
            "soothingLevelVolume": self.soothing_level_volume.value,
            "minimalLevel": self.minimal_level.value,
            "motionLimiter": self.motion_limiter,
            "weaning": self.weaning,
            "carRideMode": self.car_ride_mode,
            "offlineLock": self.offline_lock,
            "daytimeStart": self.daytime_start,
            "stickyWhiteNoiseTimeout": self.sticky_white_noise_timeout
        }


@dataclass(frozen=True)
class Baby:
    """Object for Snoo Baby information."""

    baby: str  # ID of baby
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
            baby=data.get("_id", ""),
            baby_name=data.get("babyName", ""),
            birth_date=birth_date,
            created_at=dt_str_to_dt(data.get("createdAt", None)),
            disabled_limiter=data.get("disabledLimiter", False),
            pictures=[Picture.from_dict(p) for p in data.get("pictures", [])],
            settings=Settings.from_dict(data.get("settings", {})),
            preemie=data.get("preemie"),
            sex=data.get("sex"),
            updated_at=dt_str_to_dt(data.get("updatedAt", None)),
            updated_by_user_at=dt_str_to_dt(data.get("updatedByUserAt", None)),
        )

    def to_dict(self):
        """Return dict from Object"""
        birth_date = self.birth_date
        if birth_date is not None:
            birth_date = birth_date.isoformat()

        return {
            "baby": self.baby,
            "babyName": self.baby_name,
            "birthDate": birth_date,
            "createdAt": dt_to_dt_str(self.created_at),
            "disabledLimiter": self.disabled_limiter,
            "pictures": [item.to_dict() for item in self.pictures],
            "settings": self.settings.to_dict(),
            "preemie": self.preemie,
            "sex": self.sex,
            "updatedAt": dt_to_dt_str(self.updated_at),
            "updatedByUserAt": dt_to_dt_str(self.updated_by_user_at),
        }


class SessionLevel(Enum):
    """Enum for SessionLevel"""
    ONLINE = 'ONLINE'
    BASELINE = 'BASELINE'
    WEANING_BASELINE = 'WEANING_BASELINE'
    LEVEL1 = 'LEVEL1'
    LEVEL2 = 'LEVEL2'
    LEVEL3 = 'LEVEL3'
    LEVEL4 = 'LEVEL4'
    NONE = 'NONE'
    PRETIMEOUT = 'PRETIMEOUT'
    TIMEOUT = 'TIMEOUT'

    def is_active_level(self):
        """Returns true if the Enum value represents an active level."""
        return self in [SessionLevel.BASELINE,
                        SessionLevel.WEANING_BASELINE,
                        SessionLevel.LEVEL1,
                        SessionLevel.LEVEL2,
                        SessionLevel.LEVEL3,
                        SessionLevel.LEVEL4]


class SessionItemType(Enum):
    """Enum for SessionItemType"""
    ASLEEP = 'asleep'
    SOOTHING = 'soothing'
    AWAKE = 'awake'


@dataclass(frozen=True)
class LastSession:
    """Object for Snoo LastSession information."""

    end_time: datetime
    levels: List[SessionLevel]
    start_time: datetime

    @property
    def current_status_duration(self) -> timedelta:
        """Return the duration spent in current status"""
        if self.end_time:
            return datetime.now(timezone.utc) - self.end_time

        return datetime.now(timezone.utc) - self.start_time

    @property
    def current_status(self) -> SessionItemType:
        """Return the current status"""
        if self.end_time:
            return SessionItemType.AWAKE

        if self.levels[-1] in [SessionLevel.BASELINE, SessionLevel.WEANING_BASELINE]:
            return SessionItemType.ASLEEP

        return SessionItemType.SOOTHING

    @staticmethod
    def from_dict(data: dict):
        """Return LastSession object from dict."""
        return LastSession(
            end_time=dt_str_to_dt(data.get("endTime", None)),
            levels=[SessionLevel(item['level']) for item in data.get("levels", [])],
            start_time=dt_str_to_dt(data.get("startTime", None)),
        )

    def to_dict(self):
        """Return dict from Object"""

        return {
            "endTime": dt_to_dt_str(self.end_time),
            "levels": [item.value for item in self.levels],
            "startTime": dt_to_dt_str(self.start_time),
            "currentStatus": self.current_status.value,
            "currentStatusDuration": str(self.current_status_duration)
        }


@dataclass(frozen=True)
class AggregatedSessionItem:
    """Object for Snoo AggregatedSessionItem information."""

    is_active: bool
    session_id: str
    start_time: datetime
    state_duration: timedelta
    type: SessionItemType

    @staticmethod
    def from_dict(data: dict):
        """Return AggregatedSessionItem object from dict."""

        start_time = data.get("startTime")
        if start_time is not None:
            start_time = datetime.strptime(start_time, DATETIME_FMT_AGGREGATED_SESSION)

        return AggregatedSessionItem(
            is_active=data.get("isActive", False),
            session_id=data.get("sessionId", ""),
            start_time=start_time,
            state_duration=timedelta(seconds=data.get("stateDuration", 0)),
            type=SessionItemType(data.get("type"))
        )

    def to_dict(self):
        """Return dict from Object"""
        return {
            "isActive": self.is_active,
            "sessionId": self.session_id,
            "startTime": dt_to_dt_str(self.start_time),
            "stateDuration": str(self.state_duration),
            "type": self.type.value
        }


@dataclass(frozen=True)
class AggregatedSession:
    """Object for Snoo AggregatedSession information."""

    day_sleep: timedelta
    levels: List[AggregatedSessionItem]
    longest_sleep: timedelta
    naps: int
    night_sleep: timedelta
    night_wakings: int
    timezone: str
    total_sleep: timedelta

    @staticmethod
    def from_dict(data: dict):
        """Return AggregatedSession object from dict."""
        return AggregatedSession(
            day_sleep=timedelta(seconds=data.get("daySleep", 0)),
            levels=[AggregatedSessionItem.from_dict(item) for item in data.get("levels", [])],
            longest_sleep=timedelta(seconds=data.get("longestSleep", 0)),
            naps=data.get("naps", 0),
            night_sleep=timedelta(seconds=data.get("nightSleep", 0)),
            night_wakings=data.get("nightWakings", 0),
            timezone=data.get("timezone"),
            total_sleep=timedelta(seconds=data.get("totalSleep", 0)),
        )

    def to_dict(self):
        """Return dict from Object"""
        return {
            "daySleep": str(self.day_sleep),
            "levels": [item.to_dict() for item in self.levels],
            "longestSleep": str(self.longest_sleep),
            "naps": self.naps,
            "nightSleep": str(self.night_sleep),
            "nightWakings": self.night_wakings,
            "timezone": self.timezone,
            "totalSleep": str(self.total_sleep),
        }


class AggregatedSessionInterval(Enum):
    """Enum for AggregatedSessionInterval"""
    WEEK = 'week'
    MONTH = 'month'


@dataclass(frozen=True)
class AggregatedDays:
    """Object for Snoo AggregatedDays information."""
    total_sleep: List[timedelta]
    day_sleep: List[timedelta]
    night_sleep: List[timedelta]
    longest_sleep: List[timedelta]
    night_wakings: List[int]

    @staticmethod
    def from_dict(data: dict):
        """Return AggregatedDays object from dict."""
        if data is None:
            return None

        return AggregatedDays(
            total_sleep=[timedelta(seconds=item) for item in data.get("totalSleep", [])],
            day_sleep=[timedelta(seconds=item) for item in data.get("daySleep", [])],
            night_sleep=[timedelta(seconds=item) for item in data.get("nightSleep", [])],
            longest_sleep=[timedelta(seconds=item) for item in data.get("longestSleep", [])],
            night_wakings=data.get("nightWakings", [])
        )

    def to_dict(self):
        """Return dict from Object"""
        return {
            "totalSleep": [str(item) for item in self.total_sleep],
            "daySleep": [str(item) for item in self.day_sleep],
            "nightSleep": [str(item) for item in self.night_sleep],
            "longestSleep": [str(item) for item in self.longest_sleep],
            "nightWakings": self.night_wakings,
        }


@dataclass(frozen=True)
class AggregatedSessionAvg:
    """Object for Snoo AggregatedSessionAvg information."""

    total_sleep_avg: timedelta
    day_sleep_avg: timedelta
    night_sleep_avg: timedelta
    longest_sleep_avg: timedelta
    night_wakings_avg: float
    days: Optional[AggregatedDays]

    @staticmethod
    def from_dict(data: dict):
        """Return AggregatedSessionAvg object from dict."""
        return AggregatedSessionAvg(
            total_sleep_avg=timedelta(seconds=data.get("totalSleepAVG", 0)),
            day_sleep_avg=timedelta(seconds=data.get("daySleepAVG", 0)),
            night_sleep_avg=timedelta(seconds=data.get("nightSleepAVG", 0)),
            longest_sleep_avg=timedelta(seconds=data.get("longestSleepAVG", 0)),
            night_wakings_avg=data.get("nightWakingsAVG", 0.0),
            days=AggregatedDays.from_dict(data.get("days")),
        )

    def to_dict(self):
        """Return dict from Object"""
        days = self.days
        if days is not None:
            days = days.to_dict()

        return {
            "totalSleepAVG": str(self.total_sleep_avg),
            "daySleepAVG": str(self.day_sleep_avg),
            "nightSleepAVG": str(self.night_sleep_avg),
            "longestSleepAVG": str(self.longest_sleep_avg),
            "nightWakingsAVG": self.night_wakings_avg,
            "days": days
        }


@dataclass(frozen=True)
class Signal:
    """Object for Snoo Signal information."""
    rssi: int
    strength: int

    @staticmethod
    def from_dict(data: dict):
        """Return AggregatedSessionAvg object from dict."""
        return Signal(**data)

    def to_dict(self):
        """Return dict from Object"""
        return vars(self)


@dataclass(frozen=True)
class StateMachine:
    """Object for Snoo StateMachine information."""

    up_transition: SessionLevel
    since_session_start: timedelta
    sticky_white_noise: bool
    weaning: bool
    time_left: timedelta
    session_id: str
    state: SessionLevel
    is_active_session: bool
    down_transition: SessionLevel
    hold: bool
    audio: bool

    @staticmethod
    def from_dict(data: dict):
        """Return StateMachine object from dict."""
        time_left = data.get("time_left")
        if time_left and time_left >= 0:
            time_left = timedelta(seconds=time_left)
        else:
            time_left = None

        since_session_start = data.get("since_session_start_ms")
        if since_session_start and since_session_start >= 0:
            since_session_start = timedelta(milliseconds=since_session_start)
        else:
            since_session_start = None

        return StateMachine(
            up_transition=SessionLevel(data.get("up_transition", SessionLevel.NONE.value)),
            since_session_start=since_session_start,
            sticky_white_noise=data.get("sticky_white_noise") == 'on',
            weaning=data.get("weaning") == 'on',
            time_left=time_left,
            session_id=data.get("session_id"),
            state=SessionLevel(data.get("state", SessionLevel.NONE.value)),
            is_active_session=data.get("is_active_session") == 'true',
            down_transition=SessionLevel(data.get("down_transition", SessionLevel.NONE.value)),
            hold=data.get("hold") == 'on',
            audio=data.get("audio") == 'on'
        )

    def to_dict(self):
        """Return dict from Object"""
        return {
            'up_transition': self.up_transition.value,
            'since_session_start': None if self.since_session_start is None else str(self.since_session_start),
            'sticky_white_noise': self.sticky_white_noise,
            'weaning': self.weaning,
            'time_left': None if self.time_left is None else str(self.time_left),
            'session_id': self.session_id,
            'state': self.state.value,
            'is_active_session': self.is_active_session,
            'down_transition': self.down_transition.value,
            'hold': self.hold,
            'audio': self.audio
        }


class EventType(Enum):
    """Enum for EventType"""
    UNKNOWN = 'unknown'
    ACTIVITY = 'activity'
    CRY = 'cry'
    TIMER = 'timer'
    COMMAND = 'command'
    SAFETY_CLIP = 'safety_clip'
    STICKY_WHITE_NOISE_UPDATED = 'sticky_white_noise_updated'
    LONG_ACTIVITY_PRESS = 'long_activity_press'
    STATUS_REQUESTED = 'status_requested'
    RESTART = 'restart'

    @staticmethod
    def try_parse(val):
        try: 
            return EventType(val)
        except ValueError:
            _LOGGER.warn("Unknown EventType '%s'", val)
            return EventType.UNKNOWN


@dataclass(frozen=True)
class ActivityState:
    """Return AggregatedSessionAvg object from dict."""

    left_safety_clip: bool
    rx_signal: Signal
    right_safety_clip: bool
    sw_version: str
    event_time: datetime
    state_machine: StateMachine
    system_state: str
    event: EventType

    @staticmethod
    def from_dict(data: dict):
        """Return ActivityState object from dict."""
        return ActivityState(
            left_safety_clip=bool(data.get("left_safety_clip")),
            rx_signal=Signal.from_dict(data.get("rx_signal", {})),
            right_safety_clip=bool(data.get("right_safety_clip")),
            sw_version=data.get("sw_version"),
            event_time=datetime.utcfromtimestamp(data.get("event_time_ms") / 1000).replace(tzinfo=timezone.utc),
            state_machine=StateMachine.from_dict(data.get("state_machine", {})),
            system_state=data.get("system_state"),
            event=EventType.try_parse(data.get("event", EventType.ACTIVITY.value)),
        )

    def to_dict(self):
        """Return dict from Object"""
        return {
            "left_safety_clip": self.left_safety_clip,
            "rx_signal": self.rx_signal.to_dict(),
            "right_safety_clip": self.right_safety_clip,
            "sw_version": self.sw_version,
            "event_time": dt_to_dt_str(self.event_time),
            "state_machine": self.state_machine.to_dict(),
            "system_state": self.system_state,
            "event": self.event.value,
        }
