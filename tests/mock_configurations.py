import json
def mock_configurations()-> json:
# Economical Charging (default)
    return {
        "EM_RE_ENABLE_MICROGRID": False,
        "NVM_PfcIsFixedCosPhiActive": 0,
        "NVM_PfcFixedCosPhi": 0.8,
        "IC_BatteryModules": 2,
        "EM_ToU_Schedule": [],
        "DE_Software":"1.14.5",
        "EM_USER_INPUT_TIME_ONE": 0,
        "NVM_PfcIsFixedCosPhiLagging": 0,
        "EM_Prognosis_Charging": 1,
        "EM_USOC": 20,
        "EM_USER_INPUT_TIME_TWO": 0,
        "EM_OperatingMode": "2",
        "SH_HeaterTemperatureMax": 80,
        "SH_HeaterOperatingMode": 0,
        "IC_InverterMaxPower_w": 5000,
        "SH_HeaterTemperatureMin": 0 ,
        "CM_MarketingModuleCapacity": 5000,
        "EM_USER_INPUT_TIME_THREE": 0,
        "CN_CascadingRole": "none",
        "EM_US_GEN_POWER_SET_POINT": 0
    }