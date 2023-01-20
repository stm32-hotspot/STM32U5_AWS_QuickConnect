::******************************************************************************
::* @file    awsConfig.bat
::* @author  MCD Application Team
::* @brief   Configures AWS CLI for STM32U5_AWS_QuickConnect
::******************************************************************************
:: * Copyright (c) 2022 STMicroelectronics.
::
:: * All rights reserved.
::
:: * This software component is licensed by ST under BSD 3-Clause license,
:: * the "License"; You may not use this file except in compliance with the
:: * License. You may obtain a copy of the License at:
:: *                        opensource.org/licenses/BSD-3-Clause
:: *
:: ******************************************************************************

@echo off

cd %HOMEPATH%\.aws

if exist config (
    echo config file found

    if exist config.bak (
        echo backup config file found
        echo Deleting config file
        del config
    ) else (
        echo creating backup config file
        ren config   config.bak
    )
)

if exist credentials (
    echo credentials file found

    if exist credentials.bak (
        echo backup credentials file found
        echo Deleting credentials file
        del credentials
    ) else (
        echo creating backup credentials file
        ren credentials   credentials.bak
    )
)

::Setting provision profile credentials 
set provision_accessKey=
set provision_secretKey=
set provision_profile=default

::Setting dashboard profile credentials 
set dashboard_accessKey=
set dashboard_secretKey=
set dashboard_profile=dashboard

set region=us-east-1
set outputForm=json


::Configures aws cli for prod account
(echo %provision_accessKey% && echo %provision_secretKey% && echo %region% && echo %outputForm%) | (aws configure --profile %provision_profile%)

(echo %dashboard_accessKey% && echo %dashboard_secretKey% && echo %region% && echo %outputForm%) | (aws configure --profile %dashboard_profile%)

@echo on
