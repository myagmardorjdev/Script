#New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' -Name '6.0retailv3---' -Value 'D:\Scripts\pos_res.vbs' -PropertyType "String"

#region SALBARIIN POS IP BOLON BAAZIIN ner vvd 
$databaselist = "10.1.1.5 Sansar1RetailPOS
10.32.1.5 Sansar32RetailPOS
10.34.1.5 Sansar34RetailPOS
10.13.1.5 Sansar13RetailPOS
10.21.1.5 Sansar21RetailPOS
10.6.1.5 Sansar6RetailPOS 
10.1.30.5 Sansar9RetailPOS
10.8.1.5 Sansar8RetailPOS
10.39.1.5 Sansar39RetailPOS
10.34.1.6 Sansar341RetailPOS
10.26.1.5 Sansar26RetailPOS 
10.26.1.6 OlimpRetailPOS 
10.6.1.6 Sansar61RetailPOS
10.32.1.6 Sansar321RetailPOS 
10.1.1.6 Sansar11RetailPOS 
10.8.1.6 Sansar81RetailPOS
10.13.1.6 Sansar132RetailPOS 
10.22.1.6 Sansar22RetailPOS 
10.22.1.5 Sansar221RetailPOS 
10.21.1.6 Sansar211RetailPOS 
10.39.1.3 Nemelt39RetailPOS 
10.40.1.6 Sansar401RetailPOS 
10.40.1.5 Sansar40RetailPOS 
10.12.1.5 Sansar42RetailPOS 234567
10.82.1.11 SansartestRetailPOS 1234567
10.90.1.5 ShangrilaRetailPOS 456789
10.21.1.7 Sansar212RetailPOS 987645
10.38.1.5 Sansar38RetailPOS 111111
10.1.1.15 EshopRetailPOS 222222
10.40.1.7 Sansar402RetailPOS 
10.38.1.7 Sansar381RetailPOS 
10.16.1.6 Sansar161RetailPOS 
10.16.1.5 Sansar16RetailPOS 
10.34.1.7 Sansar342RetailPOS 
10.39.1.13 Sansar392RetailPOS 
10.12.1.7 Sansar421RetailPOS 
10.15.1.5 Sansar15RetailPOS 
10.15.1.6 Sansar151RetailPOS 
10.25.1.5 Sansar25RetailPOS 
10.25.1.6 Sansar251RetailPOS 
10.62.1.7 Sansar62RetailPOS 
10.62.1.6 Sansar621RetailPOS 
10.62.1.5 Sansar622RetailPOS 
10.22.1.30 Sansar222RetailPOS
10.61.1.6 Sansar61RetailPOS
10.61.1.5 Sansar612RetailPOS 
10.61.1.7 Sansar613RetailPOS 
10.22.1.31 Sansar223RetailPOS 
10.17.1.5 Sansar171RetailPOS 
10.17.1.6 Sansar172RetailPOS 
"
#endregion
#region үндсэн тоxиргооны кодууд -----------------------------------------------------------------------------------------------------------------
$poslist= $databaselist -split "\n"
$ecr = 'D:\IBI\WILDFLY\welcome-content\DBIS Files\POS\ECRTerminalLog'
$soc = 'D:\IBI\WILDFLY\welcome-content\DBIS Files\POS\SocialPayLog'
$log = 'D:\IBI\WILDFLY\standalone\log'
 #'not equal -ne !=''-equal -eq  ==''greater -qt  >''lower -lt <     '
$current_date = Get-Date;
$SqlServer    = "192.168.0.25" # SQL Server instance (HostName\InstanceName for named instance)
$Database     = "msdb"      # SQL database to connect to 
$Ajtsi = "AltanJolooTradeSystemInfo";
net use "\\it.ajnets.com\itid\11. ServerPOS" /Persistent:yes /USER:"pos@altanjoloo.com" "Aa1234" 
$ComputerN    =  HOSTNAME.EXE;  
$SqlAuthLogin = "sa"          # SQL Authentication login
$SqlAuthPass  = "SpawnGG"     # SQL Authentication login password
$Username = "pos@altanjoloo.com"
$Password = ConvertTo-SecureString D:\Scripts\secure.txt -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($Username, $Password)
$serverzam = "\\it.ajnets.com\itid\11. ServerPOS\log_deleter\"
$serverzampkid = "\\it.ajnets.com\itid\11. ServerPOS\pkid\"
$default_printer = Get-WMIObject -Query " SELECT * FROM Win32_Printer WHERE Default=$true"
$printername = $default_printer.name
$printerjobs = Get-PrintJob -PrinterName $printername
$locallog = "D:\Scripts\Backup\querytest.txt" 
$ipaddress=(Get-WmiObject -Class Win32_NetworkAdapterConfiguration | where {$_.DHCPEnabled -ne $null -and $_.DefaultIPGateway -ne $null}).IPAddress | Select-Object -First 1;
#endregion
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< POS script PS file updatelog >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
$externallog = $serverzam + $ipaddress + ".txt"
$ps_script_udpate = (Get-Item "D:\Scripts\pos_restarter_Service.ps1").LastWriteTime
(Get-Date).ToString() + " ps_file last update:" + $ps_script_udpate | out-file -FilePath $externallog -append 
(Get-Date).ToString() + " Powershell Version: " + $PSVersionTable.PSVersion | Out-File -FilePath $externallog -Append

#########################################################################################################
for($i= 0 ; $i -lt $poslist.Length-1; $i++){
    $temp=$poslist[$i].Split(" ")
    $temp1=$poslist[$i].Split(" ")
    Write-Output $temp1
    if($ipaddress -eq $temp[0]){
        $DatabasePos = $temp[1]  # databaselist-c posiin neriig salgaj awc bna
        break;
    }
}
$DatabasePos -replace " ",""
Copy-Item "\\it.ajnets.com\itid\11. ServerPOS\posrestarter.bat" -Destination  "D:\Scripts" -Recurse
#region Сарын сүүлийн 1 дэxь өдөрийг олоx -------------------------------------------------------------------------------------------------
$last_day = [DateTime]::DaysInMonth($current_date.Year, $current_date.Month)
$last_day_date = $current_date.AddDays($last_day-$current_date.Day)
for ($i = 1; $i -lt 8; $i++) {
    Write-Output $last_day_date.DayOfWeek;
    if($last_day_date.DayOfWeek -eq 'Monday'){
        $dargiin_odor = $last_day_date.Day;
        break;
    }
    $last_day_date = $last_day_date.AddDays(-1);
}
Write-Output $dargiin_odor;
$deleting_day = $current_date.AddDays(-$current_date.Day);
$deleting_day = $deleting_day.ToString("yyyyMMdd")
$saveday = $dargiin_odor
$current_date.ToString() + " Computer Deleting day is:" + $deleting_day + " Gej tootsoolj bna" | out-file -FilePath $externallog -append
$current_date.ToString() + " Computer Last_monday_in_month is:" + $dargiin_odor + " Gej tootsoolj bna" | out-file -FilePath $externallog -append
#endregion
#region ECR LOG delete ---------------------------------------------------------------------------------------------------------------
$today_date = Get-Date
if($dargiin_odor -eq $current_date.Day){
    $ecr1 = Get-ChildItem $ecr -name # нэр нүүд байна
    $ecr_len = $ecr1.Count-1 

for($i=0; $i -le $ecr_len; $i++){
    $path1 = $ecr + '\' + $ecr1[$i]
    $tempdate = (Get-Item $path1).CreationTime
    $ans = (NEW-TIMESPAN -Start $tempdate -End $today_date).TotalDays
    $ans = [math]::ceiling($ans) ;
    if($ans -gt $saveday){    # 10 
        Remove-Item -Path $path1    
    }
}
}

#--------------------- Social Log delete ----------------------------------------
if($dargiin_odor -eq $current_date.Day){
    $soc1 = Get-ChildItem $soc -name # нэр нүүд байна
    $soc_len = $soc1.Count-1 
    
    for($i=1; $i -le $soc_len; $i++){
        $path1 = $soc + '\' + $soc1[$i]
        $tempdate = (Get-Item $path1).CreationTime
        $ans = (NEW-TIMESPAN -Start $tempdate -End $today_date).TotalDays
        $ans = [math]::ceiling($ans);
        if($ans -gt $saveday){
            Remove-Item -Path $path1   
        }
    
    }
}

#-------------------- SERVER LOG delete ------------------------------------------
if($dargiin_odor -eq $current_date.Day){
    $log1 = Get-ChildItem $log -name # нэр нүүд байна
    $log_len = $log1.Count-1 

    for($i=1; $i -le $log_len; $i++){
    $path1 = $log + '\' + $log1[$i]
    $tempdate = (Get-Item $path1).CreationTime
    $ans = (NEW-TIMESPAN -Start $tempdate -End $today_date).TotalDays
    $ans = [math]::ceiling($ans);
    if($ans -gt $saveday){
        Remove-Item -Path $path1   
    }
}
}

#region----------- TEMP CLEAR --------------------------------------------------------
$a = $env:UserName
$b = 'C:\Users\' + $a + '\AppData\Local\Temp\*'
$c = 'C:\Users\' + $a + '\AppData\Local\Microsoft\Windows\Caches\*'
$d = 'C:\Users\' + $a + '\AppData\Local\Microsoft\Internet Explorer\*'
$f = 'C:\Users\' + $a + '\AppData\Local\Microsoft\Excel\*'
$e = 'C:\Users\' + $a + '\AppData\Local\Microsoft\OneDrive\*'
$g = 'C:\Users\' + $a + '\AppData\Local\Microsoft\Terminal Server Client\Cache\*'
$g1 = 'C:\Users\' + $a + '\AppData\Local\Microsoft\*'
$g2 = 'C:\Users\' + $a +' \AppData\Local\Microsoft\UserScanProfiles\*'
$g3 = 'C:\Users\' + $a +' \AppData\Local\OneDrive'
$g4 = 'C:\Users\' + $a +' \AppData\Local\Package Cache\*'
$g5 = 'C:\Users\' + $a +' \AppData\Local\Packages\*'
$g6 = 'C:\Users\' + $a +' \AppData\LocalLow\Intel\ShaderCache\*'
$g7 = 'C:\Users\' + $a +' \AppData\LocalLow\Microsoft\Internet Explorer\*'
#endregion=================================================================================#
Remove-Item $b -Recurse -Force
Remove-Item $c -Recurse -Force
Remove-Item $d -Recurse -Force
Remove-Item $f -Recurse -Force
Remove-Item $e -Recurse -Force
Remove-Item $g -Recurse -Force
Remove-Item $g1 -Recurse -Force
Remove-Item $g2 -Recurse -Force
Remove-Item $g3 -Recurse -Force
Remove-Item $g4 -Recurse -Force
Remove-Item $g5 -Recurse -Force
Remove-Item $g6 -Recurse -Force
Remove-Item $g7 -Recurse -Force
#endregion 
#region FUNCTION #------------------------------------------------------------------------------------------------------------------------- 
function EXECUTER($v1, $v2,$v3){
    $value = 0
    $SqlAuthLogin = "sa"          # SQL Authentication login
    $SqlAuthPass  = "SpawnGG" 
    $connString = "Data Source=$v1;Database=$v2;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
    $conn = New-Object System.Data.SqlClient.SqlConnection $connString
    $conn.Open()
    $sqlcmd = $conn.CreateCommand()
    $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
    $sqlcmd.Connection = $conn
    $sqlcmd.CommandText = $v3
    $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
    $data = New-Object System.Data.DataSet
    $adp.Fill($data) | Out-Null
    $value = $data.Tables
    $conn.Close();
    return $value
}

#endregion 
#region  QUERy ZONE------------------------------------------------------------------------------------------------------------------------
$Query_pos_backup = "DECLARE @STR varchar(35) = '" + $DatabasePos + "';
DECLARE @str2 varchar(100) = Concat('N',@STR,'-Full Database Backup');
DECLARE @FileName varchar(1000)
SELECT @FileName = (SELECT 'D:\IBI\WILDFLY\standalone\log\Backup_' + convert(varchar(500), GetDate(),112) + '.bak')
Backup Database @STR To disk = @FileName with noformat, noinit, name = @str2, SKIP, NOREWIND, NOUNLOAD, STATS = 10";
$Query = "SELECT TOP 1 run_status,run_date
FROM [msdb].[dbo].[sysjobhistory2] 
WHERE step_name = '"+ $ipaddress + "'
and convert(varchar, getdate(), 112) = run_date" #convert(varchar, getdate(), 112)

$Query_get_locationPkId = "SELECT VALUE FROM "+$DatabasePos+".dbo.PosConfiguration WHERE ID like '%LocationPkID%'";
$Query_shrink_db = "USE ["+ $DatabasePos + "]
DBCC SHRINKDATABASE(N'" + $DatabasePos + "' )
USE [" + $DatabasePos + "] 
DBCC SHRINKFILE (N'" + $DatabasePos + "_Data' , 255)" # бодитоор 219MB log file үүсэж байна
$Query_delete_price_table_sale = "DELETE FROM "+ $DatabasePos +".[dbo].[ItemSalePrice];"
$Query_delete_price_table_saleboon = "DELETE FROM "+ $DatabasePos +".[dbo].[ItemSaleWholePrice]";
$Query_insert_into = "INSERT INTO "+$DatabasePos+ ".dbo.ItemSalePrice (PkId,Type,BeginDate,ItemPkID,BarcodePkID,LocationPkId,SalePrice,BalanceString,Status,HealthPrice,HealthDiscountPrice,PackagePkId,PackageBarCodePkId,PackageBalanceString,NextSalePrice,NextBeginDate,IsEndPrice,ContractMapPkId) VALUES "
$Query_pos_delete = "DELETE FROM " + $DatabasePos + ".dbo.BillDtl WHERE BillDate <= '" + $deleting_day + "';
                     DELETE FROM " + $DatabasePos + ".dbo.Billhdr WHERE BillDate <= '" + $deleting_day + "';
                     DELETE FROM " + $DatabasePos + ".dbo.logbillaction WHERE CreatedDate <= '" + $deleting_day + "';
                     DELETE FROM " + $DatabasePos + ".dbo.logvatps WHERE CreatedDate <= '" + $deleting_day + "';
                     DELETE FROM " + $DatabasePos + ".dbo.logvatpsarchive WHERE CreatedDate <= '" + $deleting_day + "';"; 
$Query_236 = "SELECT lvl1,run_date FROM msdb.dbo.sysjobhistory2 WHERE step_name = '192.168.0.236' and run_date=convert(varchar, getdate(), 112)"
$Query_price_update_failed = "INSERT INTO [msdb].[dbo].[sysjobhistory2] (step_name, run_status,run_date,run_time) VALUES ('"+$ipaddress+"',0, convert(varchar, getdate(), 112),convert(varchar, getdate(), 108))"
$Query_price_update_success = "IF EXISTS (SELECT 1 FROM [msdb].[dbo].[sysjobhistory2] WHERE run_date = convert(varchar, getdate(), 112) and step_name = '"+$ipaddress+"')
BEGIN
UPDATE [msdb].[dbo].[sysjobhistory2]
SET run_status = 1 ,run_time = convert(varchar, getdate(),108)
WHERE run_date = convert(varchar, getdate(), 112) and step_name = '"+$ipaddress+"';
END
"
$Query_price_update_succ_fail = "IF EXISTS (SELECT 1 FROM [msdb].[dbo].[sysjobhistory2] WHERE run_date = convert(varchar, getdate(), 112) and step_name = '"+$ipaddress+"')
BEGIN
UPDATE [msdb].[dbo].[sysjobhistory2]
SET run_status = 1 ,run_time = convert(varchar, getdate(),108)
WHERE run_date = convert(varchar, getdate(), 112) and step_name = '"+$ipaddress+"';
END
ELSE
BEGIN
	INSERT INTO [msdb].[dbo].[sysjobhistory2] (step_name, run_status,run_date,run_time) VALUES ('"+$ipaddress+"',1, convert(varchar, getdate(), 112),convert(varchar, getdate(), 108))
END"
$Query_price_update_to_025 = "EXEC msdb.dbo.sp_help_jobactivity @job_name = 'LastPriceImport'"
#endregion
$sleeptime = 3;
$backup_delete_status = 0
$uptime_tsag = 23
$loop_status = 0;  # price update-iig zogsoox 
$insert_sql_0 = 0; # SQL 00:00 tsagt 0 utga ogj bbna
$re_price_update_if = 0; # ogloo pos asaxad 0 utgatai pos baiwal daxin updatelsniii daraa loop zogsono
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< RESTART ZONE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while(1 -eq 1){
    #region manual stop_computer zone
    $current_date = Get-Date;
    $bootuptime = (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime
    $uptime = $current_date - $bootuptime
    if($uptime.TotalHours -gt $uptime_tsag){
        $current_date.ToString() + " Shutdown on Uptime Limit."| out-file -FilePath $externallog -append
        Stop-Computer -Force
    }elseif($current_date.Hour -eq 5 -and $current_date.Minute -lt 2){
        $current_date.ToString() + " Shutdown on Time Limit."| out-file -FilePath $externallog -append
        Stop-Computer -Force
    }
	#sql-d 0 insert nemj bna
    if($current_date.Hour -eq 0 -and (get-date).Minute -gt 5 -and $insert_sql_0 -eq 0){
        EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query_price_update_failed;
		$current_date.ToString() + " 0 stats to sented 236"| out-file -FilePath $externallog -append
        "0" | out-file -FilePath "D:\Scripts\price_status.txt"
		$re_price_update_if = 0;
        $insert_sql_0 = 1
    }
    #endregion
    #region LOCAL SQL query WORKING ZONE ******************************************************************************************>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    if($dargiin_odor -eq $current_date.Day -and $current_date.Hour -eq 0 -and $backup_delete_status -eq 0){ #backup авсан үгүй болон даргын өдөр зэрэг таарч байгаа үгүйг шалгаж байна. 
        #----------------------BACKUP ZONE -------------------------------------------------------------------------------- 
        (Get-Date).ToString() + " Last_monday_loop ajillax gej bna"| out-file -FilePath $externallog -append
        $connString = "Data Source=$ComputerN;Database=$DatabasePos;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
        $conn = New-Object System.Data.SqlClient.SqlConnection $connString
        $conn.Open()
        #----------------------BEFORE SHRINK ---------------------------------------------------
		$temp1 = "D:\IBI\Database\"+$DatabasePos+".mdf"
        $sqlfilesize = ((Get-Item $temp1).Length/1MB)
        $temp2 = "D:\IBI\Database\"+$DatabasePos+"_Log.ldf"
        $sqlfilesizelog = ((Get-Item $temp2).Length/1MB)
        (Get-Date).ToString() + " Before database size: DBsize_" + $sqlfilesize + "MB DBLog_" +$sqlfilesizelog+ "MB.txt" | out-file -FilePath $externallog -append
		#------------------- DELETING ZONE ---------------------------------------------------------------------------
        $sqlcmd = $conn.CreateCommand()
        $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
        $sqlcmd.Connection = $conn
        $sqlcmd.CommandText = $Query_pos_delete
        $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
        $adp.SelectCommand.CommandTimeout=90
        $data = New-Object System.Data.DataSet
        $adp.Fill($data) | Out-Null
        $data.Tables | format-table 
        #------------------- SHRINKE FILE ZONE ---------------------------------------------------------------------
        $sqlcmd = $conn.CreateCommand()
        $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
        $sqlcmd.Connection = $conn
        $sqlcmd.CommandText = $Query_shrink_db
        $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
        $adp.SelectCommand.CommandTimeout=50
        $data = New-Object System.Data.DataSet
        $adp.Fill($data) | Out-Null
        $data.Tables | format-table 
        $temp = "D:\IBI\Database\"+$DatabasePos+".mdf"
        $sqlfilesize = ((Get-Item $temp).Length/1MB)
        $temp = "D:\IBI\Database\"+$DatabasePos+"_Log.ldf"
        $sqlfilesizelog = ((Get-Item $temp).Length/1MB)
        (Get-Date).ToString() + " Shrinkle After database size: DBsize_" + $sqlfilesize + "MB DBLog_" +$sqlfilesizelog+ "MB.txt" | out-file -FilePath $externallog -append
        
        $conn.Close()    
		$backup_delete_status = 1
    }
    #endregion
    #region PRINTER QUEUE RESTART ZONE ******************************************************************************************>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    $printerjobs = Get-PrintJob -PrinterName $printername
    if($printerjobs.Length -gt 3){
        Write-Output 'bna'
        Restart-PrintJob -PrinterName $printername -ID 3
        Restart-PrintJob -PrinterName $printername -ID 1
        Restart-PrintJob -PrinterName $printername -ID 2
        Restart-PrintJob -PrinterName $printername -ID 4
        (Get-Date).ToString() + " printer queue vvsej, restart xiij bna" | out-file -FilePath $externallog -append
    }
    #endregion    
    #region POS PRICE UPDATE ZONE ******************************************************************************************>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    $tempminute = (New-Timespan -Hours $current_date.Hour -Minutes $current_date.Minute).TotalMinutes
    if($current_date.Hour -lt 3 -and $tempminute -gt 12 -and $loop_status -eq 0){ #0 -s baga
        $code_93 = 0 # price table
        $code_221 = 0; # boon Price table
        $code_236 = 0;
        $code_97 = 0 # price success
        $code_98 = 0 # price Boon sucess
        if(Test-Connection -IPAddress $SqlServer -Quiet){
            $atime = get-date;    
            # get locationPKID zone
            $location = (EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_get_locationPkId).Value
            if ($location.Length -gt 1){
                (Get-Date).ToString() + " LocationPkid created success" | out-file -FilePath $externallog -append
            }       
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Sale price 
            $temppat = $serverzampkid+ $location+'.csv'
            $tempzam = $serverzampkid+ $location+'B.csv'
            if(Test-Path -Path $temppat -PathType Leaf){
                try {Copy-Item -Path $temppat -Destination "D:\Scripts\" -Recurse 
                    (Get-Date).ToString() + " CSV file copied" | out-file -FilePath $externallog -append}
                catch {$code_93 = 1}
                $tempday = (get-date).ToString("yyyyMMdd");
                $code_236 = EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query_236
                $job_stat_20to25 = (EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query_price_update_to_025).run_status
                if($code_93 -eq 0 -and $code_236.lvl1 -eq 1 -and $tempday -eq $code_236.run_date -and $job_stat_20to25 -eq 1){
                    #Remove-Item $temppat # access nexeed baigaaa
                    try { EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_delete_price_table_sale;
                    (Get-Date).ToString() + " ItemSalePrice table delete SUCCESS" | out-file -FilePath $externallog -append
                    }catch {Write-Output 'failed'}
                    $Query_bulk_insert = "
                    BULK INSERT "+$DatabasePos+".dbo.ItemSalePrice
                    FROM 'D:\Scripts\"+$location+".csv'
                    WITH (FIRSTROW = 2
                    ,DATAFILETYPE='widechar'
                    ,FIELDTERMINATOR = ',' 
                    , ROWTERMINATOR ='\n'
                    )"    
                    try { EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_bulk_insert;
                        (Get-Date).ToString() + " ItemSalePrice BULK Insert SUCCESS" | out-file -FilePath $externallog -append
                        $code_97 = 1;
                    }catch {Write-Output 'FAILED'}
                }
            }else{
                (Get-Date).ToString() + " ItemSalePrice csv_file not created or other condition error" | out-file -FilePath $externallog -append
            }
            # boonii vne update
            if(Test-Path -Path $tempzam -PathType Leaf){
                try {Copy-Item -Path $tempzam -Destination "D:\Scripts\" -Recurse }
                catch {$code_221 = 1}
                if($code_221 -eq 0 -and $code_236.lvl1 -eq 1 -and $code_236.run_date -eq $tempday){
                    (Get-date).ToString() + " ItemSaleWholePrice CSV file copied." | out-file -FilePath $externallog -append
                    try {EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_delete_price_table_saleboon;
                        (Get-Date).ToString() + " ItemSaleWholePrice table delete SUCCESS" | out-file -FilePath $externallog -append}
                    catch {Write-Output 'ALdaa ogc bna'}
                    $Query_bulk_insert = "
                    BULK INSERT "+$DatabasePos+".dbo.[ItemSaleWholePrice]
                    FROM 'D:\Scripts\"+$location+"B.csv'
                    WITH (FIRSTROW = 2
                    ,DATAFILETYPE='widechar'
                    ,FIELDTERMINATOR = ',' 
                    , ROWTERMINATOR ='\n'
                    )"

                    try {EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_bulk_insert;
                    (Get-Date).ToString() + " ItemSaleWholePrice Bulk insert SUCCESS" | out-file -FilePath $externallog -append
                    $code_98=1;}
                    catch {Write-Output 'FAILED'}
                
                }
            }else{
                (Get-Date).ToString() + " ItemSaleWholePrice csv_file not created" | out-file -FilePath $externallog -append
            }
            $ctime = New-TimeSpan -Start $atime -End (Get-Date);
            if($code_97 -eq 1 -and $code_98 -eq 1){
                $loop_status = 1;
                (Get-Date).ToString() + " Bulk baaz update " + $ctime.Minutes +":"+$ctime.Seconds + " xugatsaand duuslaa" | out-file -FilePath $externallog -append
                1 | out-file -FilePath "D:\Scripts\price_status.txt"
                EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query_price_update_success;
            }
            
        }
        
    }
    #endregion <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #region POS SHUTDOWN ZONE #############################################################################################################
    if($current_date.Hour -lt 5){
        $sleeptime = 10;
		$current_date = Get-Date; #цаг 00 руу шилжихэд сервер компьютерүүд зөрүү үүсж магадгүй тул. 
        $connString = "Data Source=$SqlServer;Database=$Database;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
        #Create a SQL connection object
        $conn = New-Object System.Data.SqlClient.SqlConnection $connString
        $conn.Open()
        
        $sqlcmd = $conn.CreateCommand()
        $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
        $sqlcmd.Connection = $conn
        $sqlcmd.CommandText = $query
        $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd 
        $data = New-Object System.Data.DataSet
        $adp.Fill($data) | Out-Null
        $data.Tables | format-table 
        $conn.Close()
        if($data.Tables.run_status -eq $null){
            Write-Output "null bna"
        }else{
			$tempday = (get-date).ToString("yyyyMMdd");
            Write-Output "Утга байна"
            $tempminute = (New-Timespan -Hours $current_date.Hour -Minutes $current_date.Minute).TotalMinutes
            if($data.Tables.run_status -eq 1 -and $tempday -eq $data.Tables.run_date -and $tempminute -gt 26){
                #Тухайн салбарын ажилчид 12 цагаас хойш кассаа хаах тохиолдол байдаг тул 15 minutaas эхлэн унтарч эхлэнэ
                (Get-Date).ToString() + " sql.1 status shutdown" | out-file -FilePath $externallog -append
				Start-Sleep -Seconds 1
                Stop-Computer -Force 
            }       
        }
    }else{
        $sleeptime = 7;
    }
    #endregion
    #region ALWAySUP RESTARTER ZONE ##########################################################################################################
    # $deployment = 'D:\IBI\WILDFLY\standalone\deployments'
    # $dep_files = Get-ChildItem $deployment -Name
    # for ($i = 0; $i -lt $dep_files.Count; $i++) {
    #     $def_extension = (Split-Path -Path $dep_files[$i] -Leaf).Split(".")[2];
    #     if($def_extension -eq "undeployed"){
    #         (Get-Date).ToString() + " undeployed ear file ustgalaa" | out-file -FilePath $externallog -append
    #         $tmp = $deployment + "\" + $dep_files[$i]
    #         Remove-Item -Path $tmp -Force
    #     }
    # }
    #endregion
    #region POS wakeup check zone 
    $job_stat = (EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query).run_status
    if($job_stat -eq 0 -or $job_stat -eq $null){
		if($re_price_update_if -eq 0 -and $current_date.Hour -lt 18 -and $current_date.Hour -ge 6){ #6-10 tsag dotor 
        (Get-Date).ToString() + " baaz re update zone, do nothing" | out-file -FilePath $externallog -append
        Write-Output 'xello 1'
        
		$code_93 = 0 # price table
        $code_221 = 0; # boon Price table
        $code_236 = 0;
        $code_97 = 0 # price success
        $code_98 = 0 # price Boon sucess
        if(Test-Connection -IPAddress $SqlServer -Quiet){
            $atime = get-date;    
            # get locationPKID zone
            $location = (EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_get_locationPkId).Value
            if ($location.Length -gt 1){
                (Get-Date).ToString() + " LocationPkid created success" | out-file -FilePath $externallog -append
            }       
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Sale price 
            $temppat = $serverzampkid+ $location+'.csv'
            $tempzam = $serverzampkid+ $location+'B.csv'
            if(Test-Path -Path $temppat -PathType Leaf){
                try {Copy-Item -Path $temppat -Destination "D:\Scripts\" -Recurse 
                    (Get-Date).ToString() + " CSV file copied" | out-file -FilePath $externallog -append}
                catch {$code_93 = 1}
                $tempday = (get-date).ToString("yyyyMMdd");
                $code_236 = EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query_236
                if($code_93 -eq 0 -and $code_236.lvl1 -eq 1 -and $tempday -eq $code_236.run_date){
                    #Remove-Item $temppat # access nexeed baigaaa
                    try { EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_delete_price_table_sale;
                    (Get-Date).ToString() + " ItemSalePrice table delete SUCCESS" | out-file -FilePath $externallog -append
                    }catch {Write-Output 'failed'}
                    $Query_bulk_insert = "
                    BULK INSERT "+$DatabasePos+".dbo.ItemSalePrice
                    FROM 'D:\Scripts\"+$location+".csv'
                    WITH (FIRSTROW = 2
                    ,DATAFILETYPE='widechar'
                    ,FIELDTERMINATOR = ',' 
                    , ROWTERMINATOR ='\n'
                    )"    
                    try { EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_bulk_insert;
                        (Get-Date).ToString() + " ItemSalePrice BULK Insert SUCCESS" | out-file -FilePath $externallog -append
                        $code_97 = 1;
                    }catch {Write-Output 'FAILED'}
                }
            }else{
                (Get-Date).ToString() + " ItemSalePrice csv_file not created" | out-file -FilePath $externallog -append
            }
            # boonii vne update
            if(Test-Path -Path $tempzam -PathType Leaf){
                try {Copy-Item -Path $tempzam -Destination "D:\Scripts\" -Recurse }
                catch {$code_221 = 1}
                if($code_221 -eq 0 -and $code_236.lvl1 -eq 1 -and $code_236.run_date -eq $tempday){
                    (Get-date).ToString() + " ItemSaleWholePrice CSV file copied." | out-file -FilePath $externallog -append
                    try {EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_delete_price_table_saleboon;
                        (Get-Date).ToString() + " ItemSaleWholePrice table delete SUCCESS" | out-file -FilePath $externallog -append}
                    catch {Write-Output 'ALdaa ogc bna'}
                    $Query_bulk_insert = "
                    BULK INSERT "+$DatabasePos+".dbo.[ItemSaleWholePrice]
                    FROM 'D:\Scripts\"+$location+"B.csv'
                    WITH (FIRSTROW = 2
                    ,DATAFILETYPE='widechar'
                    ,FIELDTERMINATOR = ',' 
                    , ROWTERMINATOR ='\n'
                    )"

                    try {EXECUTER -v1 $ComputerN -v2 $DatabasePos -v3 $Query_bulk_insert;
                    (Get-Date).ToString() + " ItemSaleWholePrice Bulk insert SUCCESS" | out-file -FilePath $externallog -append
                    $code_98=1;}
                    catch {Write-Output 'FAILED'}
                
                }
            }else{
                (Get-Date).ToString() + " ItemSaleWholePrice csv_file not created" | out-file -FilePath $externallog -append
            }
            $ctime = New-TimeSpan -Start $atime -End (Get-Date);
            if($code_97 -eq 1 -and $code_98 -eq 1){
                $loop_status = 1;
                (Get-Date).ToString() + " Bulk baaz update " + $ctime.Minutes +":"+$ctime.Seconds + " xugatsaand duuslaa" | out-file -FilePath $externallog -append
                EXECUTER -v1 $SqlServer -v2 $Database -v3 $Query_price_update_succ_fail;
                $re_price_update_if = 1;
                1 | out-file -FilePath "D:\Scripts\price_status.txt"
            }
            
        }
		}
    }
    #endregion 
    if(((Get-Date).Minute/5).GetType().Name -eq "Int32"){
        try {
            if(((w32tm /query /status)[0]).Substring(18,10) -eq 'no warning' -and (Get-Service -Name W32Time).Status -eq 'Running') {
            1 | out-file -FilePath 'D:\Scripts\time_status.txt' }
            else{
            0 | out-file -FilePath 'D:\Scripts\time_status.txt'        }
        }
        catch {
            0 | out-file -FilePath 'D:\Scripts\time_status.txt'        
        }
    }
    
    Start-Sleep -Seconds $sleeptime
	stop-service DoSvc
	stop-service wuauserv
}

