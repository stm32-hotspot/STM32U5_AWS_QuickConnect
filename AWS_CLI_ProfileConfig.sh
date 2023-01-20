#!/bin/bash

# ******************************************************************************
# * @file    AWS_CLI_ProfileConfig.sh
# * @author  MCD Application Team
# * @brief   Configures AWS CLI for STM32U5_AWS_QuickConnect
# ******************************************************************************
# * Copyright (c) 2022 STMicroelectronics.
#
# * All rights reserved.
#
# * This software component is licensed by ST under BSD 3-Clause license,
# * the "License"; You may not use this file except in compliance with the
# * License. You may obtain a copy of the License at:
# *                        opensource.org/licenses/BSD-3-Clause
# *
# ******************************************************************************

# Setting provision profile credentials 
provision_accessKey=''
provision_secretKey=''
provision_profile='default'

# Setting dashboard profile credentials 
dashboard_accessKey=''
dashboard_secretKey=''
dashboard_profile='dashboard'

region='us-east-1'
outputForm='json'


# Configures aws cli for default and  dashboard accounts used in the workshop

#backup the config file
file=$HOME/.aws/config.bak
if [ ! -f $file ]; then
  file=$HOME/.aws/config
  if [ -f $file ]; then
    mv $HOME/.aws/config $HOME/.aws/config.bak
  fi
fi

#delete current config file
rm -rf $HOME/.aws/config

#create new config file
cat << EOF >> $HOME/.aws/config
[$provision_profile]
region = $region
output = $outputForm
[profile $dashboard_profile]
region = $region
output = $outputForm
EOF

#backup the credentials file
file=$HOME/.aws/credentials.bak
if [ ! -f $file ]; then
  file=$HOME/.aws/credentials
  if [ -f $file ]; then
    mv $HOME/.aws/credentials $HOME/.aws/credentials.bak
  fi
fi

#delete current credentials file
rm -rf $HOME/.aws/credentials

#create new credentials file
cat << EOF >> $HOME/.aws/credentials
[$provision_profile]
aws_access_key_id = $provision_accessKey
aws_secret_access_key = $provision_secretKey
[$dashboard_profile]
aws_access_key_id = $dashboard_accessKey
aws_secret_access_key = $dashboard_secretKey
EOF
