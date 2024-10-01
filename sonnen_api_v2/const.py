# API latestdata System-Status Groups
IC_STATUS = 'ic_status'

# API Item keys
STATUS_CONSUMPTION_W = 'Consumption_W'
STATUS_CONSUMPTION_AVG = 'Consumption_Avg'
STATUS_PRODUCTION_W = 'Production_W'
STATUS_BACKUPBUFFER = "BackupBuffer"
STATUS_GRIDFEEDIN_W = 'GridFeedIn_W'
STATUS_BATTERY_CHARGING = 'BatteryCharging'
STATUS_BATTERY_DISCHARGING = 'BatteryDischarging'
STATUS_REMAININGCAPACITY_WH = 'RemainingCapacity_Wh'
STATUS_FLOW_CONSUMPTION_BATTERY = 'FlowConsumptionBattery'
STATUS_FLOW_CONSUMPTION_GRID = 'FlowConsumptionGrid'
STATUS_FLOW_CONSUMPTION_PRODUCTION = 'FlowConsumptionProduction'
STATUS_FLOW_GRID_BATTERY = 'FlowGridBattery'
STATUS_FLOW_PRODUCTION_BATTERY = 'FlowProductionBattery'
STATUS_FLOW_PRODUCTION_GRID = 'FlowProductionGrid'
STATUS_GRID_FEED_IN_W = 'GridFeedIn_W'
STATUS_APPARENT_OUTPUT = 'Apparent_output'
STATUS_PAC_TOTAL_W = 'Pac_total_W'
STATUS_MODULES_INSTALLED = 'nrbatterymodules'
STATUS_DISCHARGE_NOT_ALLOWED = 'dischargeNotAllowed'
USOC_KEY = 'USOC'
RSOC_KEY = 'RSOC'
DETAIL_FULL_CHARGE_CAPACITY = 'FullChargeCapacity'
DETAIL_STATE_CORECONTROL_MODULE = "statecorecontrolmodule"
DETAIL_PAC_TOTAL_W = 'Pac_total_W'
DETAIL_PRODUCTION_W = 'Production_W'
DETAIL_SECONDS_SINCE_FULLCHARGE = 'secondssincefullcharge'
BATTERY_CYCLE_COUNT = 'cyclecount'
BATTERY_FULL_CHARGE_CAPACITY_AH = 'fullchargecapacity'
BATTERY_FULL_CHARGE_CAPACITY_WH = 'fullchargecapacitywh'
BATTERY_REMAINING_CAPACITY = 'remainingcapacity'
BATTERY_MAX_CELL_TEMP = 'maximumcelltemperature'
BATTERY_MAX_CELL_VOLTAGE = 'maximumcellvoltage'
BATTERY_MAX_MODULE_CURRENT = 'maximummodulecurrent'
BATTERY_MAX_MODULE_VOLTAGE = 'maximummoduledcvoltage'
BATTERY_MAX_MODULE_TEMP = 'maximummoduletemperature'
BATTERY_MIN_CELL_TEMP = 'minimumcelltemperature'
BATTERY_MIN_CELL_VOLTAGE = 'minimumcellvoltage'
BATTERY_MIN_MODULE_CURRENT = 'minimummodulecurrent'
BATTERY_MIN_MODULE_VOLTAGE = 'minimummoduledcvoltage'
BATTERY_MIN_MODULE_TEMP = 'minimummoduletemperature'
BATTERY_RSOC = 'relativestateofcharge'
BATTERY_USABLE_REMAINING_CAPACITY = 'usableremainingcapacity'
BATTERY_SYSTEM_CURRENT = 'systemcurrent'
BATTERY_SYSTEM_VOLTAGE = 'systemdcvoltage'
POWERMETER_KWH_CONSUMED = 'kwh_imported'
POWERMETER_KWH_PRODUCED = 'kwh_imported'
CONFIGURATION_EM_OPERATINGMODE = "EM_OperatingMode"
CONFIGURATION_EM_USOC = "EM_USOC"
CONFIGURATION_DE_SOFTWARE = "DE_Software"
IC_ECLIPSE_LED = "Eclipse Led"

_EM_OPERATINGMODE = {
     "1": 'Manual',
     "2": 'Automatic - Self Consumption',
     "6": 'Battery-Module-Extension (30%)',
    "10": 'Time-Of-Use'
}
# default timeout
TIMEOUT = 20
TIMEOUT_CONNECT=0
TIMEOUT_REQUEST=1
