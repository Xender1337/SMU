# -*- coding: utf-8 -*-
import pyvisa
import time
import sys
import requests
import base64
import re
from decimal import Decimal

#Commande note for ANDO 1135E
#O for auto offset
#W1250 for wavelengt

# -------------------------- README ----------------------------------------- #
'''
                            !!! WARNING !!!
To abort a test due to observed hazard the PSU need to be shutdown with the 
main switch on the front panel.
!!! All data will be lost due to communication failure. !!!

Requirements : 
    - IO Librairy Suite : (available on sharepoint)
                            KM_OPP02465\Project\5_R&D\53_Electronics\537_TestSoftware\Source\IOLibSuite_18_2_28229.exe
    - Python 3.9 (use spyder to execute the script)
    - pyvisa (pip install pyvisa)
    - pyperclip (pip install pyperclip)
    - progress ( pip install progress)
    - Install NI Visa (https://www.ni.com/fr-fr/support/downloads/drivers/download/packaged.ni-visa.460225.html)

'''

# -------------------------- Brief ------------------------------------------ #
# - Parameter description
'''
starting_current    : Set the starting current for the first iteration of measurement
max_current         : Set the last current applied on the DUT for measurement
step_current        : Set the step of test measurement

compliance_voltage  : Set the maximum voltage applied on the LED
photodiode_IW       : Set the Current / Power ratio to calculate the power measured.

delay               : Set the delay between two measurement to let cool down the DUT
settling_time       : Set the delay between the application of current on the 
                        DUT and the measurement of the DMM to measure receive power
'''

# -------------------------- How to use ------------------------------------- #
'''
In order to proceed measurement the PSU and DMM neet to be power-on and connected through GPIB.
The address of each gear is already setup (ADDR : 2 for PSU and ADDR : 16 for DMM).

After execution of the script the test result will be saved in clipboard and 
can be paste directly in Excel with Ctrl + V.
'''
# PSU ADDR 2 // KEITHLEY 237
smu_addr = 16

# Init of communication
rm = pyvisa.ResourceManager()
smu = rm.open_resource('GPIB0::{}::INSTR'.format(smu_addr))
# =============================================================================
# 
# print(smu.query('F0,1X'))
# print(smu.query('G5,0,0X'))
# print(smu.query('B5,2,0X'))
# 
# print(smu.query('Q4,2,8,2,2,100,100X'))
# time.sleep(10)
# print(smu.query('H0X'))
# =============================================================================


# =============================================================================
# 
# print(smu.query('F0,1X'))
# print(smu.query('B1,2,0X'))
# print(smu.query('Q4,1,10,1,2,500,1000X'))
# print(smu.query('R1X'))
# print(smu.query('N1X'))
# print(smu.query('H0X'))
# print(smu.query('G4,2,2X'))
# =============================================================================

# print(smu.query('R1X'))
# print(smu.query('N1X'))
# print(smu.query('Q0,10,10,100,20X'))
# time.sleep(2)
# print(smu.query('H0X'))
# time.sleep(2)
# print(smu.query('G4,2,2X'))
# print(smu.query('N0X'))

# print(smu.query('F0,0X'))
# print(smu.query('R1X'))
# print(smu.query('N1X'))
# print(smu.query('H0X'))

pattern = r"(?P<smu_source_parameter>[A-Z]*).(?P<set_value>\d*.\d*).(?P<set_exponent>.\d*).(?P<smu_measure_parameter>[A-Z]*).(?P<measure_value>\d*.\d*..\d*)"

try:
    while True:
        try:
            result = smu.query('G5,0,0X')
        except:
            continue
        print(result)
        match = re.search(pattern, result)
        print(match.groups())
        print(match.group(5))
        value = float(match.group(5))
        send_value = f"{value:.14f}"
        print(send_value)
        time.sleep(2)
        
        USER_ID = 991863
        API_KEY = "glc_eyJvIjoiODU3ODA5IiwibiI6InRlc3Qtc211IiwiayI6IjlZdDFpdzQ1MDRUaDM5UmlBMGo0bU1jTCIsIm0iOnsiciI6InByb2QtZXUtd2VzdC0yIn19"
        
        body = 'test,bar_label=test_smu,source=grafana_cloud_docs metric={}'.format(send_value)
        print(body)
        
        try:
            response = requests.post('https://influx-prod-24-prod-eu-west-2.grafana.net/api/v1/push/influx/write', 
                                     headers = {
                                       'Content-Type': 'text/plain',
                                     },
                                     data = str(body),
                                     auth = (USER_ID, API_KEY)
            )
            
            status_code = response.status_code
        except:
            continue
        print(status_code)
        
except KeyboardInterrupt:
    print('out')