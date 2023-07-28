$locationPkid = @{c1=170327122911096938; c6=170406043146007079; c8=170324022223062632; 
    c15=210405095049125072; c16=200413064930688403;
    c17=210408023905809340; c22=180116104648397919;
   c25=210408043134292339;c26=171013040031087717;c32=170406042750095661;
   c34=170406042848021210;c38=200116052340975509;c39=170406042603125478;
   c40=181205124759015413;c42=190411023639162812;c61=210521091034372689;
   c61b=210617022521293295;c62=210325042508161356}
#region тоxиргооны xэсгүүд -------------------------------------------------------------------------------
$current_date = Get-Date;
$SqlServer = "192.168.0.25" # SQL Server instance (HostName\InstanceName for named instance)
$Database = "msdb"      # SQL database to connect to 
$Ajtsi = "AltanJolooTradeSystemInfo";
$SqlAuthLogin = "sa"          # SQL Authentication login
$SqlAuthPass = "SpawnGG"     # SQL Authentication login password
$Username = "pos@altanjoloo.mn";
$Password = "Aa1234";
$serverzam = "D:\itid\11. ServerPOS\log_deleter\"
$ipaddress = (Get-WmiObject -Class Win32_NetworkAdapterConfiguration | where { $_.DHCPEnabled -ne $null -and $_.DefaultIPGateway -ne $null }).IPAddress | Select-Object -First 1;
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< POS script PS file updatelog >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
$externallog = $serverzam + $ipaddress + ".txt"
$current_date.ToString() + " Script ajillaj exellee:" | out-file -FilePath $externallog -append
$pat1 = "D:\ITID\11. ServerPOS\pkid\"

#endregion 
#region Query zone <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
$querty_log_succ = "IF EXISTS (SELECT 1 FROM msdb.dbo.sysjobhistory2 WHERE step_name = '192.168.0.236' and run_date=convert(varchar, getdate(), 112))
BEGIN
UPDATE msdb.dbo.sysjobhistory2
SET end_status = 1
WHERE step_name = '192.168.0.236' and run_date = convert(varchar, getdate(), 112)
END
ELSE
BEGIN
INSERT INTO msdb.dbo.sysjobhistory2 (step_name,end_status,run_date,down_time)
VALUES ('192.168.0.236',1, convert(varchar, getdate(), 112),convert(varchar, getdate(),108));
END"
$querty_log_fail = "IF EXISTS (SELECT 1 FROM msdb.dbo.sysjobhistory2 WHERE step_name = '192.168.0.236' and run_date=convert(varchar, getdate(), 112))
BEGIN
UPDATE msdb.dbo.sysjobhistory2
SET end_status = 0
WHERE step_name = '192.168.0.236' and run_date = convert(varchar, getdate(), 112)
   END
       ELSE
       BEGIN
INSERT INTO msdb.dbo.sysjobhistory2 (step_name,end_status,run_date)
VALUES ('192.168.0.236',0, convert(varchar, getdate(), 112) );
END"
#endregion 
$query_dashboard = "SELECT * FROM [msdb].[dbo].[sysjobhistory2] WHERE run_date = convert(varchar, getdate(), 112)"
$sleeptime = 30;
$loop_status = 0;
$counter = 0;
$query_dash = 0
$success_count = 0;

while(1 -eq 1){
$current_date = Get-Date; 
$tempminute = (New-Timespan -Hours $current_date.Hour -Minutes $current_date.Minute).TotalMinutes
if($current_date.Hour -lt 2 -and $tempminute -gt 4 -and $loop_status -eq 0){
   if(Test-Connection -IPAddress $SqlServer -Quiet){
       #ITEMSALEPRCICE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       #5 aas xoiш 5 minuted vvsj baigaa
       foreach ($i in $locationPkid.GetEnumerator()) {
           #region Query_to_csv---------------------------------------------------------------------------------------------------------
           $Query_to_csv = "SELECT main.PkId, main.Type, main.BeginDate, main.ItemPkId, main.BarcodePkId,
           main.LocationPkId, main.SalePrice, main.BalanceString, 1 as Status,
           0 as HealthPrice, 0 as HealthDiscountPrice,
           0 as PackagePkId,0 as PackageBarCodePkId,'null_null' PackageBalanceString,
           '' as NextSalePrice,'' as NextBeginDate,0 as IsEndPrice,main.ContractMapPkId
            FROM [AltanJolooTradeSystemInfo].[dbo].[itemsalepricenew1] as main
           where locationpkid = '"+$($i.Value)+ "'";
           #endregion
           #region SQL query zone----------------------------------------------------------------------------------------------------
           $connString = "Data Source=$SqlServer;Database=$Ajtsi;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
           $conn = New-Object System.Data.SqlClient.SqlConnection $connString
           $conn.Open()
           $sqlcmd = $conn.CreateCommand()
           $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
           $sqlcmd.Connection = $conn
           $sqlcmd.CommandText = $Query_to_csv
           $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
           $data = New-Object System.Data.DataSet
           #endregion 
           try {
           $adp.Fill($data) | Out-Null 
           $var = $pat1+$($i.Value) + '.csv'
           $data.Tables[0] | ConvertTo-Csv -delimiter "," -NoTypeInformation | %{$_ -replace '"',''} > $var
           $success_count = $success_count + 1;
               Write-Output $success_count
           }
           catch {Write-Output 'failed'}
           
           #$data.Tables | Format-Table
           $conn.Close();
       }    
       Write-Output "exnii step duuslaa"
       (Get-Date).ToString() + " ItemPriceTable_to_csv zone done." | out-file -FilePath $externallog -append
       #ItemSaleWholePrice >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       #2 minuted created
       foreach ($i in $locationPkid.GetEnumerator()) {
       
           #region QUERY querywhole
           $querywhole = "SELECT 
           main.PkId ,null as OrganizationPkId,
           main.Type ,main.BeginDate ,
           main.ItemPkId, main.BarcodePkId, 
           main.LocationPkId ,main.PriceType ,
           main.Quantity ,main.SalePrice ,
           main.BalanceString,
           1 as Status, 0 as IsEndPrice, main.ContractMapPkId
           from [AltanJolooTradeSystemInfo].[dbo].[itemsalewholeprice1] as main
           where main.locationpkid =   '" +$($i.Value) + "'"
           #endregion
               $connString = "Data Source=$SqlServer;Database=$Ajtsi;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
               $conn = New-Object System.Data.SqlClient.SqlConnection $connString
               $conn.Open()
               $sqlcmd = $conn.CreateCommand()
               $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
               $sqlcmd.Connection = $conn
               $sqlcmd.CommandText = $querywhole
               $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
               $data = New-Object System.Data.DataSet
               try {
                   $adp.Fill($data) | Out-Null 
                   $var = $pat1+$($i.Value) + 'B.csv'
                   $data.Tables[0] | ConvertTo-Csv -delimiter "," -NoTypeInformation | %{$_ -replace '"',''} > $var
                   $success_count = $success_count + 1;
                   Write-Output $success_count
               }catch {Write-Output 'failed'}
               
               $CSVSize = (Get-Item -Path $var).Length
               $CSVSize = ($CSVSize/1KB)

               $conn.Close();
               $counter=$counter+1;  
               if($counter -eq $locationPkid.Count -and $success_count/2 -eq $locationPkid.Count -and $CSVSize -ge 800){
                   Write-Output "loop stopped"
                       $loop_status = 1; # onoodoriin LOOPiig zogsooow
                       #region log bicij vldej bna--------------------------------------------------------------------------
                       $connString = "Data Source=$SqlServer;Database=$Database;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
                       $conn = New-Object System.Data.SqlClient.SqlConnection $connString
                       $conn.Open()
                       $sqlcmd = $conn.CreateCommand()
                       $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
                       $sqlcmd.Connection = $conn
                       $sqlcmd.CommandText = $querty_log_succ
                       $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
                       $data = New-Object System.Data.DataSet
                       $adp.Fill($data) | Out-Null 
                       $conn.close();
                       $success_count = 0;
                       $counter = 0;
                       #endregion 
                       (Get-Date).ToString() + " today loop successfully." | out-file -FilePath $externallog -append

               }elseif($counter -eq $locationPkid.Count){
                       #region query failed log vldeej bna --------------------------------------------------------------------
                       $connString = "Data Source=$SqlServer;Database=$Database;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
                       $conn = New-Object System.Data.SqlClient.SqlConnection $connString
                       $conn.Open()
                       $sqlcmd = $conn.CreateCommand()
                       $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
                       $sqlcmd.Connection = $conn
                       $sqlcmd.CommandText = $querty_log_fail
                       $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
                       $data = New-Object System.Data.DataSet
                       $adp.Fill($data) | Out-Null 
                       $conn.close();
                       #endregion
                       (Get-Date).ToString() + " success count: " + $success_count | out-file -FilePath $externallog -append
                       (Get-Date).ToString() + " counter: " + $counter | out-file -FilePath $externallog -append
                       (Get-Date).ToString() + " Error vvsej daxin loop ajillax gej bna" | out-file -FilePath $externallog -append
                       $success_count = 0;
                       $counter = 0;
               }    
       }
       #for loop end <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 
   }
   
}
#loop_status iig sergeej deed taliin looopiig ajilluulax 
if($current_date.Hour -eq 0 -and $current_date.Minute -eq 0){
   $loop_status = 0; # csv file daxin 0 bolloo
   (Get-Date).ToString() + " Loop Status daxin 0 bollooo." | out-file -FilePath $externallog -append
   $query_dash = 0 # mail report daxin 0 bolloo
} 
#pkid file-уудыг устгаж байна
if($current_date.Hour -eq 23 -and $current_date.Minute -eq 0){
   Remove-Item -Path 'D:\ITID\11. ServerPOS\pkid\*'
   (Get-Date).ToString() + " pkid csv file-yydiig ustgaj bna: " + (get-childitem 'D:\ITID\11. ServerPOS\pkid').Count | out-file -FilePath $externallog -append
}

if((Get-Date).Hour -eq 24 -and $query_dash -eq 0){
   $connString = "Data Source=$SqlServer;Database=$Database;User ID=$SqlAuthLogin;Password=$SqlAuthPass"
   $conn = New-Object System.Data.SqlClient.SqlConnection $connString
   $conn.Open()
   $sqlcmd = $conn.CreateCommand()
   $sqlcmd = New-Object System.Data.SqlClient.SqlCommand
   $sqlcmd.Connection = $conn
   $sqlcmd.CommandText = $query_dashboard
   $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
   $data = New-Object System.Data.DataSet
   $adp.Fill($data) | Out-Null 
   $conn.close();
   $var1 = $data.Tables.step_name
   $var2 = $data.Tables.run_status
   $var3 = $data.Tables.run_time
   $msg_body = "Good Morning `r` "
   for ($i = 0; $i -lt $data.Tables.step_name.Count; $i++) {
       $msg_body += "IP: "+ $var1[$i] + "`t`t run_status: "+$var2[$i]+"`t`t run_time:   " +$var3[$i] + " `r` "
       Write-Output $msg_body
   }

   $userName = 'zapataast@gmail.com'
   $To = 'myagmardorj@altanjoloo.mn'
   $password = 'ymsgfkzgzyvuljpz'    
   [SecureString]$securepassword = $password | ConvertTo-SecureString -AsPlainText -Force 
   $credential = New-Object System.Management.Automation.PSCredential -ArgumentList $username, $securepassword
   Send-MailMessage -SmtpServer smtp.office365.com -Port 587 -UseSsl -From $userName -To $To -Subject "POS Price update 0.236 report" -Body $msg_body -Credential $credential
   $query_dash = 1
}

Start-Sleep -Seconds $sleeptime
}
