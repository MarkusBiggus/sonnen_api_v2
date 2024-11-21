import json
def mock_powermeter()-> json:
    return [
        {
            'a_l1': 2.4730000495910645, 'a_l2': 0,
            'a_l3': 0,
            'channel': 1,
            'deviceid': 4,
            'direction': 'production',
            'error': 0,
            'kwh_exported': 0,
            'kwh_imported': 3969.800048828125,
            'v_l1_l2': 0,
            'v_l1_n': 246.60000610351562,
            'v_l2_l3': 0,
            'v_l2_n': 0,
            'v_l3_l1': 0,
            'v_l3_n': 0,
            'va_total': 609.5,
            'var_total': 0,
            'w_l1': 609.5,
            'w_l2': 0,
            'w_l3': 0,
            'w_total': 609.5
        },
        {
            'a_l1': 2.0929999351501465,
            'a_l2': 0,
            'a_l3': 0,
            'channel': 2,
            'deviceid': 4,
            'direction': 'consumption',
            'error': 0,
            'kwh_exported': 0,
            'kwh_imported': 816.5,
            'v_l1_l2': 0,
            'v_l1_n': 246.6999969482422,
            'v_l2_l3': 0,
            'v_l2_n': 0,
            'v_l3_l1': 0,
            'v_l3_n': 0,
            'va_total': 516.2000122070312,
            'var_total': -512.7999877929688,
            'w_l1': 59.29999923706055,
            'w_l2': 0,
            'w_l3': 0,
            'w_total': 59.29999923706055
        }
    ]