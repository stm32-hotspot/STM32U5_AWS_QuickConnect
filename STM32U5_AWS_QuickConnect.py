#******************************************************************************
# * @file           : STM32U5_AWS_QuickConnect.py
# * @brief          : Automatically registers new thing to AWS associated with connected STM32.
# ******************************************************************************
# * @attention
# *
# * <h2><center>&copy; Copyright (c) 2022 STMicroelectronics.
# * All rights reserved.</center></h2>
# *
# * This software component is licensed by ST under BSD 3-Clause license,
# * the "License"; You may not use this file except in compliance with the
# * License. You may obtain a copy of the License at:
# *                        opensource.org/licenses/BSD-3-Clause
# ******************************************************************************
from ast import Interactive
import sys
import subprocess
from tokenize import Name
from utils.getDeviceName import *
import getopt
import getpass
import platform
from halo import Halo

VERSION = "1.3.1"

SSID = 'st_iot_demo'
PSWD = 'stm32u585'

DUMMY_SSID = '0'
DUMMY_PSWD = '0'

DASHBOARD_URL        = 'https://main.d3mkj47qkab3qo.amplifyapp.com'

AWS_CLI_DASHBOARD_PROFILE = 'dashboard'
AWS_CLI_PROVISION_PROFILE = 'default'

if platform.system() == 'Windows': 
    BIN_FILE = '.\\firmware\\Projects\\b_u585i_iot02a_ntz\\Debug\\b_u585i_iot02a_ntz.bin'
else:
    BIN_FILE = './firmware/Projects/b_u585i_iot02a_ntz/Debug/b_u585i_iot02a_ntz.bin'

HELP = ['openDashboard.py options:', 
        '\n\t-h or --help for help',
        '\n\t-i for interactive mode',
        '\n\t--ssid=[WiFi SSID]',
        '\n\t--password=[WiFi Password]', 
        '\n\t--dashboard-profile=[aws cli dashboard profile]',
        '\n\t--provision-profile=[aws cli provision profile]',
        '\n\t--dashboard-url=[dashboard url]',
        '\n\t--version for the file version']

# Run path in command line and output it to output.txt if logging level is greater than debug
def cmd(path: list):
    proc = subprocess.Popen(path)
    proc.communicate()
    retState = proc.poll()

    if retState != 0:
        print('Error: ' + path[1])
        sys.exit(1)

################################
def getParam(curParam, label):
    param = input(label + " [" + curParam + "]: ").strip()

    if param:
        return param
    else:
        return curParam

################################
def getHiddenParam(curParam, label):
    hidden = '*' * len(curParam)
    param = getpass.getpass(prompt=label + " [" + hidden + "]: ").strip()

    if param:
        return param
    else:
        return curParam

################################
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi", ["help", "interactive", "ssid=", "password=", "dashboard-profile=", "provision-profile=", "dashboard-url="])
    except getopt.GetoptError:
        print("Parameter Error")
        sys.exit(1)

    name = get_name()
    ssid = SSID
    pswd = PSWD
    aws_dashboard_profile=AWS_CLI_DASHBOARD_PROFILE
    aws_provision_profile=AWS_CLI_PROVISION_PROFILE
    dashboard_url=DASHBOARD_URL
    interactiveMode = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(HELP)
            sys.exit(1)

        elif opt in ("--ssid"):
            ssid  = arg

        elif opt in ("--password"):
            pswd = arg

        elif opt in ("--dashboard-profile"):
            aws_dashboard_profile = arg    

        elif opt in ("--provision-profile"):
            aws_provision_profile = arg  

        elif opt in ("--dashboard-url"):
            dashboard_url = arg  

        elif opt in ("-i", "--interactive"):
            interactiveMode = True
        
        elif opt in ("--version"):
            print("STM32U5_AWS_QuickConnect.py version: " + VERSION)
            sys.exit(1)

    if interactiveMode:
        ssid = getParam(ssid, "Wi-Fi SSID")
        pswd = getParam(pswd, "Wi-Fi Password")
        aws_provision_profile = getParam(aws_provision_profile, "AWS_CLI_PROVISION_PROFILE")
        #aws_dashboard_profile = getParam(aws_dashboard_profile, "AWS_CLI_DASHBOARD_PROFILE")
        aws_dashboard_profile = getParam(aws_dashboard_profile, "AWS_CLI_PROVISION_PROFILE")
        dashboard_url = getParam(dashboard_url, "DASHBOARD_URL")

    spinner = Halo(text='', spinner='dots')

    print("Flashing Firmware")
    spinner.start()
    cmd(['python', 'utils/flash.py', '--bin-file='+BIN_FILE])
    spinner.stop()

    print("Setting Wi-Fi parameters")
    spinner.start()
    cmd(['python', 'utils/setWiFiParam.py', '--ssid=' + DUMMY_SSID, '--password='+ DUMMY_PSWD])
    spinner.stop()

    print("Privisionong STM32 with AWS")
    cmd(['python', 'utils/provision.py', '--thing-name=' + name, '--wifi-ssid=' +  ssid, '--wifi-credential=' + pswd, '--aws-profile=' + aws_provision_profile])

    #cmd(['python', 'utils/getConfig.py', '--device-id='+ name, '--profile='+aws_provision_profile, '--wifi-ssid=' +  ssid, '--wifi-credential=' + pswd])

    print("Waiting for STM32 to connect to AWS")
    spinner.start()
    cmd(['python', 'utils/readSerial.py'])
    spinner.stop()
    print("Connected to AWS")

    print("Opening Dashboard")
    spinner.start()
    cmd(['python', 'utils/openDashboard.py', '--device-id='+ name, '--dashboard-profile='+aws_dashboard_profile,   '--dashboard-url='+ dashboard_url])
    spinner.stop()


################################
if __name__ == "__main__":
    main(sys.argv[1:])

 #************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/           