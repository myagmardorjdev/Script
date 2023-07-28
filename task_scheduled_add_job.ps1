$action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument "D:\scripts\pos_res.vbs"
$trigger =  New-ScheduledTaskTrigger -AtLogOn 
$Settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "POSLOG" -Settings $Settings