
$starthour = 22
$startminute = 30
$enddate =24
$maxendhour = 1
#label 3 duusax on sar baixgvi
$label3 = 4067, 4071, 4040, 61, 47, 45, 46, 44, 4054, 176, 67, 62, 63, 3177, 3183, 2255, 3176, 3137, 3138, 3140, 3136, 2028, 3135, 3131, 3133, 3130, 3132, 3144, 3175, 3178, 3141, 3179, 3142, 2066, 6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6010, 6011, 6012, 6013, 6014, 6015, 6016, 6017, 6018, 6019, 6020, 6021, 6022, 6023, 1550, 1523, 192, 129, 207, 241, 316, 328, 2012, 2083, 2098, 2137, 3155, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2280, 2324, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 3127, 3070, 4007, 4002, 4003, 4004, 4005, 4001, 4008, 4006, 4009, 4010, 4011, 4012, 4013, 4014, 4015, 4016, 4017, 4018, 4019, 4020, 4021, 4022, 4023, 4024, 4025, 4026, 4027, 4028, 4029, 4030, 4031, 4032, 4033, 4034, 4035, 4036, 4037, 4038, 4039, 4041, 4044, 4045, 4046, 4042, 4043, 4048, 4047, 4050, 4049, 4052, 4061, 4051, 4060, 4054, 4057, 4053, 4056, 4062, 4063, 4064, 4055, 4058, 4059, 4213, 4209, 4211, 4210, 4212, 4208, 4066, 4069, 4071, 4065, 4068, 4070, 4073, 4077, 4080, 4085, 4082, 4081, 4197, 4196, 4087, 4086, 4090, 4089, 4088, 4091, 4092, 4094, 4093, 4095, 4096, 4097, 4099, 4098, 4202, 4203, 4204, 4205, 4206, 4112, 4113, 4114, 4116, 4117, 4118, 4119, 4120, 4121, 4115, 4122, 4124, 4125, 4126, 4214, 4215, 4216, 4217, 4218, 4219, 4220, 4221, 4222, 4223, 4224, 4225, 4226, 4227, 4228, 4229, 4230, 4231, 4123, 4127, 4128, 4129, 4130, 4131, 4132, 4133, 4134, 4135, 4136, 4137, 4138, 4139, 4140, 4141, 4142, 4143, 4144, 4186, 4201, 4187, 4198, 4199, 4200, 4147, 4153, 4158, 4159, 4160, 4161, 4162, 4163, 4164, 4165, 4166, 4167, 4168, 4169, 4191, 4192, 4193, 4188, 4184, 4185, 4195, 4240 # duusax on sar baixgvi
# yamar ch on sargvi
$label2 = 2081, 2179, 4060, 4054, 4071,2414 # ogt on sargvi 
#ortsgvi baraaanuud tom label dr garax
Import-Module importexcel 
#0                                         1                                        2                                           3                                   4                                       5           6                                               7                                                       8                               9

$sleeptime = 40;
$logfile = "B:\Scripts\scalelog.txt"
(Get-Date).ToString() + " Script Started." | out-file -FilePath $logfile -append

function EXECUTER($v1, $v2, $v3) {
    $value = 0
    $SqlAuthLogin = "sa"          # SQL Authentication login
    $SqlAuthPass = "SpawnGG123" 
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
net use "\\192.168.0.236\Aclas LINK69" /Persistent:yes /USER:"pos@altanjoloo.com" "Aa1234" 
net use "\\10.21.1.45\aclassdk_log" /Persistent:yes /USER:"pos@altanjoloo.com" "Aa1234" 

$loopcount = 0
while (1 -eq 1) {
    $carrefour = @{       #0                                      1                                   2                                              3                                       4                                      5            6                                                    7                                        8                                     9
    c13 =            '"http://10.13.1.220/scale/products"', '"X-Odoo-dbfilter: CARREFOURS13_LIVE"', 'B:\Scripts\ScalePriceLIST\check\file13.xlsx', 'B:\Scripts\ScalePriceLIST\file13.xlsx', 'B:\Scripts\ScalePriceLIST\file13.csv', 's13scale', '\\192.168.0.236\Aclas LINK69\aclassdk_log\*.txt', '\\192.168.0.236\Aclas LINK69\Temp\*', '\\192.168.0.236\Scalelog\scale',         'B:\Scripts\zabbix_scale\scalecodeduplicated13.txt';
    c34            = '"http://10.34.1.220/scale/products"', '"X-Odoo-dbfilter: CARREFOURS34_LIVE"', 'B:\Scripts\ScalePriceLIST\check\file34.xlsx', 'B:\Scripts\ScalePriceLIST\file34.xlsx', 'B:\Scripts\ScalePriceLIST\file34.csv', 's34scale', 'C:\Program Files (x86)\Aclas LINK69\aclassdk_log\*.txt', 'C:\Program Files (x86)\Aclas LINK69\Temp\*', "B:\Scripts\zabbix_scale\scale", 'B:\Scripts\zabbix_scale\scalecodeduplicated34.txt';
    c88            = '"http://10.88.1.220/scale/products"', '"X-Odoo-dbfilter: CARREFOURS88_LIVE"', 'B:\Scripts\ScalePriceLIST\check\file88.xlsx', 'B:\Scripts\ScalePriceLIST\file88.xlsx', 'B:\Scripts\ScalePriceLIST\file88.csv', 's88scale', '',                                                  '',                                  '',                                    'B:\Scripts\zabbix_scale\scalecodeduplicated88.txt';
    c21            = '"http://10.21.1.220/scale/products"', '"X-Odoo-dbfilter: CARREFOURS21_LIVE"', 'B:\Scripts\ScalePriceLIST\check\file21.xlsx', 'B:\Scripts\ScalePriceLIST\file21.xlsx', 'B:\Scripts\ScalePriceLIST\file21.csv', 's21scale', '\\10.21.1.45\aclassdk_log\*.txt',                   '\\10.21.1.45\Temp\*',             "B:\Scripts\zabbix_scale\scale",           'B:\Scripts\zabbix_scale\scalecodeduplicated21.txt'
    } 
    $scaleipdevices = @{ip1 = '010.034.001.241'; ip2 = '010.034.001.242'; ip3 = '010.034.001.243'; ip4 = '010.034.001.244'; ip5 = '010.034.001.245'
    ip6 = '010.034.001.246'; ip7 = '010.034.001.247'; ip8 = '010.034.001.248'; ip9 = '010.034.001.249'
    }
    $scaleip13 = @{ip1 = '010.013.001.249'; ip2 = '010.013.001.250'; ip3 = '010.013.001.251'; ip4 = '010.013.001.252' };
    $scaleip21 = @{ip1 = '010.021.001.244'; ip2 = '010.021.001.245'};
    if((get-date).Hour -ge 0 -and (get-date).Hour -lt 12){    # vvsex file iin on sar odor onoodor bna uu , vgvi bol daxin tatax oroldlog hiiij bna
        foreach ($x in $carrefour.GetEnumerator()) {
            $filecheck = ((Get-ChildItem -Path $x.Value[2]).CreationTime).DayOfYear
            if($filecheck -ne (Get-Date).DayOfYear){
                $loopcount = 0
                (Get-Date).ToString() + " file iin odor oor baigaa tul loop daxin ajilluulj bna." + $x.Key | out-file -FilePath $logfile -append
            }
        }
    }
    if (((get-date).Hour -ge $starthour -or (get-date).Hour -le $maxendhour) -and $loopcount -eq 0 -and (get-date).Minute -ge $startminute) {
        (Get-Date).ToString() + " file creater daxin ajillaj bna." | out-file -FilePath $logfile -append
        foreach ($z in $carrefour.GetEnumerator()) {
            Remove-Item $z.Value[2];
            curl.exe $z.Value[0] -H $z.Value[1] -H "X-Odoo: sansar" --output $z.Value[2]
            try {
                $hashsourcefile = Import-Excel -Path $z.Value[2] | Select-Object 'Code on Scale', 'Product Code', 'Product Name', 'Product Price', 'Unit'
                $hashold = Import-Excel -Path $z.Value[3] | Select-Object 'Code on Scale', 'Product Code', 'Product Name', 'Product Price', 'Unit'
            }
            catch {
                <#Do this if a terminating exception happens#>
            }
            for ($i = 0; $i -ne $hashsourcefile.Length; $i++) {
                if ($hashold[$i].'Code On Scale' -ne $hashsourcefile[$i].'Code On Scale' -or $hashold[$i].'Product Code' -ne $hashsourcefile[$i].'Product Code' -or $hashold[$i].'Product Name' -ne $hashsourcefile[$i].'Product Name' -or $hashold[$i].'Product Price' -ne $hashsourcefile[$i].'Product Price' -or $hashold[$i].'Unit' -ne $hashsourcefile[$i].'Unit') {
                    (Get-Date).ToString() + " difference product revealed ." | out-file -FilePath $logfile -append
                    Write-Output "Yalgaatai baraaa bnna"
                    break
                }
            }
            
            if ($i -ne $hashsourcefile.Length) {  # ene filed oorchlolt orj uu vgvi yu gedgiig shalgaj baij daraagin vildlvvvdee hiij bna
                
                remove-item $z.Value[3]
                Copy-Item $z.Value[2] -Destination $z.Value[3] -Recurse
                (Get-Date).ToString() + " file-d oorchlolt orson bna." + $z.Key | out-file -FilePath $logfile -append
                try {
                    $ans1 = Import-Excel -Path $z.Value[3] | Select-Object 'Code on Scale', 'Product Code', 'Product Name', 'Barcode',
                    'Product short name', 'Product Price', 'Unit', 'Ingredient List', 'Expiration Days', @{n = 'LabelID'; e = { [String]('1') } }, @{n = 'UnitID'; e = { [String]('4') } }
                }
                catch {
                    <#Do this if a terminating exception happens#>
                }
                  
                (Get-Date).ToString() + " labelid." | out-file -FilePath $logfile -append    
                for ($j = 0; $j -ne $ans1.Count; $j++) {
                    $temp = $label3.IndexOf($ans1[$j].'Code on Scale')
                    Write-Output $temp
                    if ($label3.IndexOf([int]($ans1[$j].'Code On Scale')) -ne -1) {
                        $ans1[$j].LabelID = 3
                        Write-Output '3 bnadaaa'
                    }
                    if ($label2.IndexOf([int]($ans1[$j].'Code On Scale')) -ne -1) {
                        $ans1[$j].LabelID = 2
                    }
                }
                (Get-Date).ToString() + " labelid." | out-file -FilePath $logfile -append
                #scale code duplicates check >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                $temp = Import-Excel $z.Value[3]
                $temp = $temp | Group-Object 'Code on Scale' | Select-Object Name, Count | Where-Object Count -gt 1
                $temp = $temp | Where-Object Name -ne ''
                if ($temp -eq $null) {
                    0 | Out-File $z.Value[9]
                }
                else {
                    1 | Out-File $z.Value[9]
                } 
                # kg pcs toxiruulj bna>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                for ($i = 0; $i -ne $ans1.Count; $i++) {
                    if ($ans1[$i].'Unit' -eq 'Unit') {
                        Write-Output $ans1[$i].'Unit'
                        $ans1[$i].'Unit' = "PCS(kg)"
                        $ans1[$i].'UnitID' = 10
                        Write-Output $ans1[$i].'Unit'
                        Write-Output $ans1[$i].'UnitID'
                    }
                    elseif ($ans1[$i].'Unit' -eq 'Units') {
                        $ans1[$i].'Unit' = "PCS(kg)"
                        $ans1[$i].'UnitID' = 10
                    }
                    elseif ($ans1[$i].'Unit' -eq 'kg') {
                        $ans1[$i].'UnitID' = 4
                    }
                }
                for ($i = 0; $i -ne $ans1.Count; $i++) {
                    if ($ans1[$i].'Code on Scale' -eq $null) {
                        $ans1[$i].'Code on Scale' = 0
                    }
                }
                # ortsgvi baraaag label 4 tei bolgox
                for ($i = 0; $i -ne $ans1.Count; $i++) {
                    if ($ans1[$i].'Ingredient List' -eq $null) {
                        #$ans1[$i].LabelID = 4;
                    }
                }
                Remove-Item $z.Value[4]
                Write-Output "--------------------["
                Write-Output $z.Value[5];
                Write-Output $z.Value[4]
                $ans1 |  ConvertTo-Csv -delimiter ";" -NoTypeInformation | % { $_ -replace '"', '' } > $z.Value[4]
                $q1 = "DELETE FROM [electronjin].[dbo]." + $z.Value[5]
                $q2 = "BULK INSERT electronjin.dbo." + $z.Value[5] +
                " FROM '" + $z.Value[4] + "'
                WITH (FIRSTROW = 2
                ,DATAFILETYPE='widechar'
                ,FIELDTERMINATOR = ';' 
                , ROWTERMINATOR ='\n'
                )"
                EXECUTER -v1 "WIN-3RGEU5J9BNE" -v2 "electronjin" -v3 $q1
                EXECUTER -v1 "WIN-3RGEU5J9BNE" -v2 "electronjin" -v3 $q2
            }
        }
        Write-Output "Finished"
        $loopcount = 1
    }
    # omnox odriin link69 loguudiig ustgaj bna
    if ((get-date).Hour -eq $starthour -and (get-date).Minute -eq $startminute) {
        #jin0 bolgox
        foreach ($j in $scaleipdevices.GetEnumerator()) {
            $temp = $carrefour.Item('c34')[8] + $j.Value.Split('.')[3] + ".txt"
            0 | out-file -FilePath $temp
            Remove-Item -Recurse -Force  $carrefour.Item('c34')[7]
            Remove-Item -Recurse -Force  $carrefour.Item('c34')[6]
        }
        foreach ($j in $scaleip13.GetEnumerator()) {
            $temp = $carrefour.Item('c13')[8] + $j.Value.Split('.')[3] + ".txt"
            0 | out-file -FilePath $temp
            Remove-Item -Recurse -Force  $carrefour.Item('c13')[7]
            Remove-Item -Recurse -Force  $carrefour.Item('c13')[6]
        }
        foreach ($j in $scaleip21.GetEnumerator()) {
            $temp = $carrefour.Item('c21')[8] + $j.Value.Split('.')[3] + ".txt"
            0 | out-file -FilePath $temp
            Remove-Item -Recurse -Force  $carrefour.Item('c21')[7]
            Remove-Item -Recurse -Force  $carrefour.Item('c21')[6]
        }
    }

    
    if ((Get-date).Hour -ge $starthour) {
        Write-output "s34 log checck"
        # s34 log c34 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>34 34 34 34 34 34 34 34 34 3 43
        foreach ($i1 in $scaleipdevices.GetEnumerator()) {
            $temp = $carrefour.Item('c34')[8] + $i1.Value.Split('.')[3] + ".txt"
            if ((Get-Content $temp) -eq 0) {
                $filter = "*AutoPLU_" + $i1.Value + "*"
                $result = Get-ChildItem -Path "C:\Program Files (x86)\Aclas LINK69\aclassdk_log\" -Recurse -Filter $filter
                if ($result -eq $null) {
                    Write-Output ($i1.Value -split ".")
                    $temp = $carrefour.Item('c34')[8] + $i1.Value.Split('.')[3] + ".txt"
                    0 | out-file -FilePath $temp
                }
                else {
                    $temp = $carrefour.Item('c34')[8] + $i1.Value.Split('.')[3] + ".txt"
                    Write-Output "jin amjillttai shinechilj 1 utga awlaa"
                    1 | out-file -FilePath $temp
                }
                $result = $null
                
            }
            else {
                Write-Output "s34 Success."
            }
        }
        # s13 log c13 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>13 13 13 13 13- 13- 13- 13-13-131-1--3-31-
        foreach ($i2 in $scaleip13.GetEnumerator()) {
            $temp = $carrefour.Item('c13')[8] + $i2.Value.Split('.')[3] + ".txt"
            if ((Get-Content $temp) -eq 0) {
                $filter = "*AutoPLU_" + $i2.Value + "*"
                $temp2 = $carrefour.item('c13')[6].replace('*.txt', '')
                $result = Get-ChildItem -Path $temp2 -Recurse -Filter $filter
                if ($result -eq $null) {
                    Write-Output ($i2.Value -split ".")
                    $temp = $carrefour.Item('c13')[8] + $i2.Value.Split('.')[3] + ".txt"
                    0 | out-file -FilePath $temp
                }
                else {
                    $temp = $carrefour.Item('c13')[8] + $i2.Value.Split('.')[3] + ".txt"
                    Write-Output "s13 jin amjillttai shinechilj 1 utga awlaa"
                    1 | out-file -FilePath $temp
                }
                $result = $null
                
            }
            else {
                Write-Output "s13 Success."
            }
        }
        ### c21 iin 2 jin  c21 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        foreach ($i2 in $scaleip21.GetEnumerator()) {
            $temp = $carrefour.Item('c21')[8] +'c21'+ $i2.Value.Split('.')[3] + ".txt"  # omnox utgaa shalgaj bna
            if ((Get-Content $temp) -eq 0) {
                $filter = "*AutoPLU_" + $i2.Value + "*"
                $temp2 = $carrefour.item('c21')[6].replace('*.txt', '')
                $result = Get-ChildItem -Path $temp2 -Recurse -Filter $filter
                if ($result -eq $null) {
                    Write-Output ($i2.Value -split ".")
                    $temp = $carrefour.Item('c21')[8]+'c21'+ $i2.Value.Split('.')[3] + ".txt"
                    Write-Output "s21 jin FAILED"
                    0 | out-file -FilePath $temp
                }
                else {
                    $temp = $carrefour.Item('c21')[8] +'c21'+$i2.Value.Split('.')[3] + ".txt"
                    Write-Output "s21 jin amjillttai shinechilj 1 utga awlaa"
                    1 | out-file -FilePath $temp
                }
                $result = $null
                
            }
            else {
                Write-Output "s21 Success."
            }
        }
    }  

    if ((get-date).Hour -eq $starthour){
        $loopcount = 0
    }
    if((get-date).Hour -ge $starthour -and (Get-Date).Hour -le $enddate){
        $vallen = (Get-ChildItem "B:\Scripts\scalepricelist\check\").Length
        if($vallen -ne $carrefour.Count){
            $loopcount = 0
            (Get-Date).ToString() + " file bvgd vvseegvi baigaa tul loop iig daxin exlvvlew." + $x.Key | out-file -FilePath $logfile -append
        }
    }
    Write-Output "sleep...."
    Start-Sleep -Seconds $sleeptime;

}#while loop external

#$a = ((Get-Content -path 'C:\Program Files (x86)\Aclas LINK69\Config\ImportData.ini' -Raw) -replace 'ExecTime=12:00','ExecTime=12:14')  
#$a = $a.Trim()
#$a | Set-Content -Path 'C:\Program Files (x86)\Aclas LINK69\Config\ImportData.ini'