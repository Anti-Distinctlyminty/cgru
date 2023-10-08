@echo off

call %CGRU_LOCATION%\software_setup\setup_lightwave.cmd

start "Modeler" "%APP_DIR%\bin\Modeler.exe" %*
