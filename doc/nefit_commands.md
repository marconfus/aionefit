## GET /ecus/rrc/uiStatus

```javascript
{'id': '/ecus/rrc/uiStatus',
 'recordable': 0,
 'type': 'uiUpdate',
 'value': {'ARS': 'init',
           'BAI': 'No',
           'BBE': 'false',
           'BLE': 'false',
           'BMR': 'false',
           'CPM': 'auto',
           'CSP': '14',
           'CTD': '2018-12-25T20:27:29+00:00 Tu',
           'CTR': 'room',
           'DAS': 'off',
           'DHW': 'on',
           'DOT': 'true',
           'ESI': 'off',
           'FAH': 'false',
           'FPA': 'off',
           'HED_DB': '',
           'HED_DEV': 'false',
           'HED_EN': 'false',
           'HMD': 'off',
           'IHS': 'ok',
           'IHT': '21.50',
           'MMT': '21.5',
           'PMR': 'false',
           'RS': 'off',
           'TAS': 'off',
           'TOD': '0',
           'TOR': 'off',
           'TOT': '17.0',
           'TSP': '21.5',
           'UMD': 'manual'},
 'writeable': 0}
```

| Key      | Description  |
|----------|--------------|
| ARS      |
| BAI      | boiler indicator "CH"=central heating; "HW"=hot water; "No"=off
| BBE      | boiler block
| BLE      | boiler lock
| BMR      | boiler maintainance
| CPM      | clock program
| CSP      | current switchpoint
| CTD      | current time and date
| CTR      | control
| DAS      | (to)day as sunday
| DHW      |
| DOT      |
| ESI      |
| FAH      |
| FPA      |
| HED_DB   |
| HED_DEV  | hed device at home
| HED_EN   | hed enabled
| HMD      | holiday mode
| IHS      | in house status
| IHT      | in house temp
| MMT      |
| PMR      |
| RS       |
| TAS      | tomorrow as sunday
| TOD      | temp override duration
| TOR      |
| TOT      | temp override
| TSP      | temp setpoint
| UMD      | user mode




temp manual:
self.put('/heatingCircuits/hc1/temperatureRoomManual', {'value': float(temperature)})
self.put('/heatingCircuits/hc1/manualTempOverride/status', {'value': 'on'})
self.put('/heatingCircuits/hc1/manualTempOverride/temperature', {'value': float(temperature)})


operation mode:
self._client.put("/heatingCircuits/hc1/usermode", {"value": "manual"})
self._client.put("/heatingCircuits/hc1/usermode", {"value": "clock"})


https://www.home-assistant.io/components/climate/