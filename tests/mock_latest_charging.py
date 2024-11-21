import json
def latest_charging()-> json:
    return {
        'FullChargeCapacity': 20683.490,
        'GridFeedIn_W': 0,
        'Production_W': 2972,
        'Consumption_W': 1578,
        'Pac_total_W': -1394,
        'RSOC': 98,
        'SetPoint_W': -145,
        'Timestamp': '2022-04-30 17:00:58',
        'USOC': 98,
        'UTC_Offet': 2,
        'ic_status': {
            'DC Shutdown Reason': {
                'Critical BMS Alarm': False,
                'Electrolyte Leakage': False,
                'Error condition in BMS initialization': False,
                'HW_Shutdown': False,
                'HardWire Over Voltage': False,
                'HardWired Dry Signal A': False,
                'HardWired Under Voltage': False,
                'Holding Circuit Error': False,
                'Initialization Timeout': False,
                'Initialization of AC contactor failed': False,
                'Initialization of BMS hardware failed': False,
                'Initialization of DC contactor failed': False,
                'Initialization of Inverter failed': False,
                'Invalid or no SystemType was set': False,
                'Inverter Over Temperature': False,
                'Inverter Under Voltage': False,
                'Inverter Version Too Low For Dc-Module': False,
                'Manual shutdown by user': False,
                'Minimum rSOC of System reached': False,
                'Modules voltage out of range': False,
                'No Setpoint received by HC': False,
                'Odd number of battery modules': False,
                'One single module detected and module voltage is out of range': False,
                'Only one single module detected': False,
                'Shutdown Timer started': False,
                'System Validation failed': False,
                'Voltage Monitor Changed': False
            },
            'Eclipse Led': {
                'Blinking Red': False,
                'Pulsing Green': False,
                'Pulsing Orange': False,
                'Pulsing White': True,
                'Solid Red': False
            },
            'MISC Status Bits': {
                'Discharge not allowed': False,
                'F1 open': False,
                'Min System SOC': False,
                'Min User SOC': False,
                'Setpoint Timeout': False
            },
            'Microgrid Status': {
                'Continious Power Violation': False,
                'Discharge Current Limit Violation': False,
                'Low Temperature': False,
                'Max System SOC': False,
                'Max User SOC': False,
                'Microgrid Enabled': False,
                'Min System SOC': False,
                'Min User SOC': False,
                'Over Charge Current': False,
                'Over Discharge Current': False,
                'Peak Power Violation': False,
                'Protect is activated': False,
                'Transition to Ongrid Pending': False
            },
            'Setpoint Priority': {
                'BMS': False,
                'Energy Manager': True,
                'Full Charge Request': False,
                'Inverter': False,
                'Min User SOC': False,
                'Trickle Charge': False
            },
            'System Validation': {
                'Country Code Set status flag 1': False,
                'Country Code Set status flag 2': False,
                'Self test Error DC Wiring': False,
                'Self test Postponed': False,
                'Self test Precondition not met': False,
                'Self test Running': False,
                'Self test successful finished': False
            },
            'nrbatterymodules': 4,
            'secondssincefullcharge': 3720,
            'statebms': 'ready',
            'statecorecontrolmodule': 'ongrid',
            'stateinverter': 'running',
            'timestamp': 'Sat Apr 30 17:00:57 2022'
        }
    }