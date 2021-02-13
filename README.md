# pysnoo
[![Coverage Status](https://coveralls.io/repos/github/rado0x54/pysnoo/badge.svg?branch=develop)](https://coveralls.io/github/rado0x54/pysnoo?branch=develop)
![Python package](https://github.com/rado0x54/pysnoo/workflows/Python%20package/badge.svg)

pysnoo is a python library to interact with the SNOO Smart Sleeper Bassinet

## Disclaimer
Please use this library at your own risk and make sure that you do not violate the
[Terms of Service of HappiestBaby](https://www.happiestbaby.com/pages/terms-of-service).

## Installation
```shell
pip install pysnoo
```

## Programmatic Usage
Programatically, the project provides two main class inferfaces. The Snoo API Client interface
[snoo.py](./pysnoo/snoo.py) and the Snoo PubNub interface [pubnub.py](./pysnoo/pubnub.py).

Here's a short example to setup both. It uses the Snoo API Interface to get the Snoo serial number,
and access token, which are required to initialize the PubNub interface. More usage examples can be
found by looking at the [CLI Tool](./scripts/snoo) or the [unit tests](./tests).

```python
async with SnooAuthSession(token, token_updater) as auth:

    if not auth.authorized:
        # Init Auth
        new_token = await auth.fetch_token(username, password)
        token_updater(new_token)

    # Snoo API Interface
    snoo = Snoo(auth)
    devices = await snoo.get_devices()
    if not devices:
        # No devices
        print('There is no Snoo connected to that account!')
    else:
        # Snoo PubNub Interface
        pubnub = SnooPubNub(snoo.auth.access_token,
                          devices[0].serial_number,
                          f'pn-pysnoo-{devices[0].serial_number}',
                          callback)
    
        last_activity_state = (await pubnub.history())[0]
        if last_activity_state.state_machine.state == SessionLevel.ONLINE:
            # Start
            await pubnub.publish_start()
        else:
            # Stop
            await pubnub.publish_goto_state(SessionLevel.ONLINE)
    
        await pubnub.stop()
    

```

## CLI Usage
The pysnoo package contains the `snoo` CLI tool:

```shell
# snoo -h
Snoo Smart Bassinett

positional arguments:
  {user,device,baby,last_session,status,sessions,session_avg,total,monitor,history,toggle,toggle_hold,up,down}

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        username for Snoo account
  -p PASSWORD, --password PASSWORD
                        username for Snoo account
  -t file, --token_file file
                        Cached token file to read and write an existing OAuth Token to.
  -d DATETIME, --datetime DATETIME
                        Datetime in ISO8601 fromat. Used for some commands.
```

### Credentials / Token / First Run
If the tool cannot find a valid oauth token in `--token_file` (`./.snoo_token.txt` by default), it will automatically query for
a username and password on the first run. After a successful authentication a token will be placed in the specified
file. Subsequent calls that have access to the token will not query for credentials any longer.

```shell
# snoo status
Username: snoo-user@gmail.com
Password: 
awake (since: 0:34:54.891556)
# ls .snoo_token.txt
.snoo_token.txt
# snoo status
awake (since: 0:36:27.266366)
.snoo_token.txt
```
### Snoo CLI Commands

#### status
`snoo status` returns the current status of the snoo.

#### monitor
`snoo monitor` monitors the live events emited by the Snoo Bassinet. Monitoring can be cancelled
via `CTRL-C`. The command always returns the last historic event when launching.
```shell
# snoo monitor
{'event': 'activity',
 'event_time': '2021-02-13T16:02:40.628Z',
 'left_safety_clip': True,
 'right_safety_clip': True,
 'rx_signal': {'rssi': -45, 'strength': 100},
 'state_machine': {'audio': True,
                   'down_transition': 'NONE',
                   'hold': False,
                   'is_active_session': False,
                   'session_id': '0',
                   'since_session_start': None,
                   'state': 'ONLINE',
                   'sticky_white_noise': False,
                   'time_left': None,
                   'up_transition': 'NONE',
                   'weaning': False},
 'sw_version': 'v1.14.12',
 'system_state': 'normal'}
```

#### toggle
`snoo toggle` toggle the Snoo Bassinet between an active and a paused state.

#### toggle_hold
`snoo toggle_hold` will toggle the hold option on or off.

#### up
`snoo up` will transition the Snoo Bassinet one level up (if available)

#### down
`snoo down` will transition the Snoo Bassinet one level down (if available)

#### history
`snoo history` will return the last 100 events from the Snoo Bassinet.

```shell
# snoo history
{'event': 'cry',
 'event_time': '2021-02-13T16:02:23.025Z',
 'left_safety_clip': True,
 'right_safety_clip': True,
 'rx_signal': {'rssi': -45, 'strength': 100},
 'state_machine': {'audio': True,
                   'down_transition': 'LEVEL1',
                   'hold': False,
                   'is_active_session': True,
                   'session_id': '1696520262',
                   'since_session_start': '1:01:40.420000',
                   'state': 'LEVEL2',
                   'sticky_white_noise': False,
                   'time_left': '0:06:00',
                   'up_transition': 'LEVEL3',
                   'weaning': False},
 'sw_version': 'v1.14.12',
 'system_state': 'normal'}
{'event': 'activity',
 'event_time': '2021-02-13T16:02:40.628Z',
 'left_safety_clip': True,
 'right_safety_clip': True,
 'rx_signal': {'rssi': -45, 'strength': 100},
 'state_machine': {'audio': True,
                   'down_transition': 'NONE',
                   'hold': False,
                   'is_active_session': False,
                   'session_id': '0',
                   'since_session_start': None,
                   'state': 'ONLINE',
                   'sticky_white_noise': False,
                   'time_left': None,
                   'up_transition': 'NONE',
                   'weaning': False},
 'sw_version': 'v1.14.12',
 'system_state': 'normal'}
 ...
```

#### baby
`snoo baby` returns data about the baby and the settings of the linked Snoo Bassinet.

```shell
{'baby': 'ID',
 'babyName': 'BABY_NAME',
 'birthDate': '2021-01-17',
 'createdAt': '2020-11-18T16:12:08.064Z',
 'disabledLimiter': False,
 'pictures': [{'encoded': False,
               'id': 'PICTURE_ID',
               'mime': 'image/png',
               'updatedAt': '2021-01-21T10:45:07.542Z'}],
 'preemie': None,
 'settings': {'carRideMode': False,
              'daytimeStart': 7,
              'minimalLevel': 'baseline',
              'minimalLevelVolume': 'lvl-1',
              'motionLimiter': True,
              'offlineLock': False,
              'responsivenessLevel': 'lvl0',
              'soothingLevelVolume': 'lvl0',
              'weaning': False},
 'sex': 'Male',
 'updatedAt': '2021-02-02T22:23:10.770Z',
 'updatedByUserAt': '2021-02-02T21:35:45.665Z'}
```
Some of these settings can be upgraded programmatically.

#### device
`snoo device` returns information around the linked Snoo Bassinet:
```shell
{'baby': 'BABY_ID',
 'createdAt': '2019-02-19T19:03:13.544Z',
 'firmwareUpdateDate': '2021-01-14T17:36:51.149Z',
 'firmwareVersion': 'v1.14.12',
 'lastProvisionSuccess': '2020-11-18T16:25:57.973Z',
 'lastSSID': {'name': 'SSID-Network', 'updatedAt': '2021-01-28T22:04:21.151Z'},
 'serialNumber': 'SERIAL_NUMBER',
 'timezone': 'America/New_York',
 'updatedAt': '2021-02-13T16:50:16.685Z'}
```

#### user
`snoo user` returns account related information:
```shell
{'email': 'EMAIL',
 'givenName': 'GIVEN_NAME',
 'region': 'US',
 'surname': 'SURNAME',
 'userId': 'USER_ID'}
```

#### last_session
`snoo last_session` returns information around the last or currently active session.
```shell
{'currentStatus': 'awake',
 'currentStatusDuration': '0:51:04.121661',
 'endTime': '2021-02-13T16:02:40.635Z',
 'levels': ['BASELINE', 'LEVEL1', 'LEVEL2', 'ONLINE'],
 'startTime': '2021-02-13T15:00:42.604Z'}
```

#### sessions
`snoo sessions -d DATETIME` returns all sessions within a `24h` segement AFTER `DATETIME` in ISO8601
format. Note `DATETIME` does not respect any timezone information, but assumes the local timezone
that is that up within the account. If not specified `DATETIME` is the timestamp 24h before.

```shell
# snoo sessions -d 2021-01-30T07:00:00
{'daySleep': '4:46:18',
 'levels': [{'isActive': False,
             'sessionId': '1538910189',
             'startTime': '2021-01-30T07:00:00.000',
             'stateDuration': '0:23:18',
             'type': 'asleep'},
            ...
            {'isActive': False,
             'sessionId': '1010439060',
             'startTime': '2021-01-31T05:35:16.214',
             'stateDuration': '1:24:44',
             'type': 'asleep'}],
 'longestSleep': '3:25:44',
 'naps': 5,
 'nightSleep': '8:12:50',
 'nightWakings': 4,
 'timezone': None,
 'totalSleep': '12:59:08'}
```

#### session_avg
`snoo session_avg -d DATETIME` returns the average values for the week starting from `DATETIME`.

```shell
# snoo session_avg -d 2021-01-30T07:00:00
{'daySleepAVG': '5:38:43',
 'days': {'daySleep': ['4:46:18',
                       '5:06:47',
                       '5:32:30',
                       '7:41:16',
                       '6:15:46',
                       '5:39:27',
                       '4:28:57'],
          'longestSleep': ['3:25:44',
                           '3:35:49',
                           '3:32:16',
                           '3:56:58',
                           '3:11:14',
                           '4:02:54',
                           '3:12:44'],
          'nightSleep': ['8:12:50',
                         '8:30:22',
                         '6:40:29',
                         '6:42:13',
                         '8:46:07',
                         '6:24:24',
                         '8:14:42'],
          'nightWakings': [4, 3, 6, 5, 4, 3, 3],
          'totalSleep': ['12:59:08',
                         '13:37:09',
                         '12:12:59',
                         '14:23:29',
                         '15:01:53',
                         '12:03:51',
                         '12:43:39']},
 'longestSleepAVG': '3:33:57',
 'nightSleepAVG': '7:38:44',
 'nightWakingsAVG': 4,
 'totalSleepAVG': '13:17:27'}
```

#### total
`snoo total` returns the total time the Snoo Bassinet has been in operation.
```shell
# snoo total
11 days, 9:13:32
```



