
$loopstatus = 0
$backstatus = 0
$jobstart_hour = 7 # 22
$jobstart_min = 0 # 33
$jobend_hour = 18
$startleepduration = 50
$price_check_row_limit = 250
$scalezerostatus = 7
$scalezerostatusmin = 0
$isrun = 'B:\Scripts\zabbix_scale\isrunmon.txt'
$logfilemain = "B:\Scripts\scalelogv3.txt"
$carrefour = @{c88 = 'B:\Scripts\scalepricelist\file88.xlsx','B:\Scripts\plu88.csv', "" , 'B:\Scripts\zabbix_scale\Scale88.txt' ,'10.88.1.240';
               c21 = 'B:\Scripts\scalepricelist\file21.xlsx','B:\Scripts\plu21.csv', "" , 'B:\Scripts\zabbix_scale\Scale21.txt' ,'10.21.1.240'; 
            }
#hamgiin bagadaa 2 ip address zooj ogoxiig anxaarna uu
$ipdevices = @{c88 = '10.88.1.240';
               c21 = '10.21.1.240', '10.21.1.241','10.21.1.242','10.21.1.243'
            }

$onsargvi = @(4028,4071,4061,4054,4066,4060,4052,4248,4246,4246)
$nofiltered = @("Сироп 10л Cola, Sprite","Өндөг /хоол/","Огурцы 1кг")
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
function deletefolder($v1, $v2){
    $logfolder = Get-ChildItem $v1 -Directory
    foreach($f in $logfolder){
        $ts =  New-TimeSpan -Start $f.CreationTime -end (Get-Date)
        if($ts.Days -gt $v2){
            $tp = $v1 + $f.Name
            Remove-item $tp -Recurse
        }
    }
}

$query_zksoftbackup = "BACKUP DATABASE [ZKSoft] TO  DISK = N'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\Backup\ZKSoft.bak' 
WITH NOFORMAT, NOINIT,  NAME = N'ZKSoft-Full Database Backup', SKIP, NOREWIND, NOUNLOAD,  STATS = 10
"

while(1 -eq 1){

    if((Get-Date).Hour -ge $jobstart_hour -and (Get-Date).Hour -le $jobend_hour -and (get-date).Minute -ge $jobstart_min -and $loopstatus -eq 0){
        $loopstatus = 1
        foreach ($z in $carrefour.GetEnumerator()){
            $counter=0
            $ingred = @();
            $plu0uall = Import-Csv -Path 'B:\Scripts\plu0uallsource.csv' -Delimiter "," 
            Import-Module importexcel 
            $orig = Import-Excel -Path $z.Value[0]
            $orig = $orig | Sort-Object -Property 'Code on Scale' # scale code oor ni sort hiij bna
            For($i=0; $i -lt $orig.Count ; $i++){
                if($orig[$i].'Code on Scale' -ne $null -and $orig[$i].'Code on Scale' -ne '0') {
                    $plu0uall[$counter].1 = $orig[$i].'Code on Scale'
                    $temp = $orig[$i].'Code on Scale' + "000000"
                    $plu0uall[$counter].24 =$temp
                    $plu0uall[$counter].19 = $orig[$i].'Product Price' 
                    $plu0uall[$counter].52 = $orig[$i].'Code on Scale' # ingredint шошго
                    $plu0uall[$counter].8 = 1; #sell by time
                    $plu0uall[$counter].9 = 1  #sell by time 
                    $plu0uall[$counter].16 = 1 # PLU price change
                    $plu0uall[$counter].15 = 1  # unit price override
                    if($orig[$i].Unit -eq "Kg"){
                        $plu0uall[$counter].3 = 0
                    }else{
                        $plu0uall[$counter].3 = 1
                    }
                    $temp = $null
                    #region
                    for($j=0; $j -lt ($orig[$i].'Product Name').Length; $j++){
                        if($orig[$i].'Product Name'[$j] -eq 'У' -and $orig[$i].'Product Name'[$j] -cmatch "^[У]*$"){
                            $temp = $temp + 'Ó'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'р' -and $orig[$i].'Product Name'[$j] -cmatch "^[р]*$"){
                            $temp = $temp + 'ð'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Р' -and $orig[$i].'Product Name'[$j] -cmatch "^[Р]*$"){
                            $temp = $temp + 'Ð'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'т' -and $orig[$i].'Product Name'[$j] -cmatch "^[т]*$"){
                            $temp = $temp + 'ò'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ц' -and $orig[$i].'Product Name'[$j] -cmatch "^[ц]*$"){
                            $temp = $temp + 'ö'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ц' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ц]*$"){
                            $temp = $temp + 'Ö'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'а' -and $orig[$i].'Product Name'[$j] -cmatch "^[а]*$"){
                            $temp = $temp + 'à'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'г' -and $orig[$i].'Product Name'[$j] -cmatch "^[г]*$"){
                            $temp = $temp + 'ã'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Г' -and $orig[$i].'Product Name'[$j] -cmatch "^[Г]*$"){
                            $temp = $temp + 'Ã'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'н' -and $orig[$i].'Product Name'[$j] -cmatch "^[н]*$"){
                            $temp = $temp + 'í'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Н' -and $orig[$i].'Product Name'[$j] -cmatch "^[Н]*$"){
                            $temp = $temp + 'Í'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'м' -and $orig[$i].'Product Name'[$j] -cmatch "^[м]*$"){
                            $temp = $temp + 'ì'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'М' -and $orig[$i].'Product Name'[$j] -cmatch "^[М]*$"){
                            $temp = $temp + 'Ì'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ө' -and $orig[$i].'Product Name'[$j] -cmatch "^[ө]*$"){
                            $temp = $temp + 'ù'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ө' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ө]*$"){
                            $temp = $temp + 'Ù'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ш' -and $orig[$i].'Product Name'[$j] -cmatch "^[ш]*$"){
                            $temp = $temp + 'ø'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ш' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ш]*$"){
                            $temp = $temp + 'Ø'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ч' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ч]*$"){
                            $temp = $temp + '×'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'д' -and $orig[$i].'Product Name'[$j] -cmatch "^[д]*$"){
                            $temp = $temp + 'ä'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Б' -and $orig[$i].'Product Name'[$j] -cmatch "^[Б]*$"){
                            $temp = $temp + 'Á'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'я' -and $orig[$i].'Product Name'[$j] -cmatch "^[я]*$"){
                            $temp = $temp + 'ÿ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'я' -and $orig[$i].'Product Name'[$j] -cmatch "^[Я]*$"){
                            $temp = $temp + 'ß'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'с' -and $orig[$i].'Product Name'[$j] -cmatch "^[с]*$"){
                            $temp = $temp + 'ñ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'л'-and $orig[$i].'Product Name'[$j] -cmatch "^[л]*$"){
                            $temp = $temp + 'ë'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Л'-and $orig[$i].'Product Name'[$j] -cmatch "^[Л]*$"){
                            $temp = $temp + 'Ë'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ү' -and $orig[$i].'Product Name'[$j] -cmatch "^[ү]*$"){
                            $temp = $temp + 'ú'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ү' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ү]*$"){
                            $temp = $temp + 'Y'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'х' -and $orig[$i].'Product Name'[$j] -cmatch "^[х]*$"){
                            $temp = $temp + 'õ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Х' -and $orig[$i].'Product Name'[$j] -cmatch "^[Х]*$"){
                            $temp = $temp + 'Õ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'и' -and $orig[$i].'Product Name'[$j] -cmatch "^[и]*$"){
                            $temp = $temp + 'è'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'И' -and $orig[$i].'Product Name'[$j] -cmatch "^[И]*$"){
                            $temp = $temp + 'È'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'й'){
                            $temp = $temp + 'é'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'э' -and $orig[$i].'Product Name'[$j] -cmatch "^[э]*$"){
                            $temp = $temp + 'ý'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'к' -and $orig[$i].'Product Name'[$j] -cmatch "^[к]*$"){
                            $temp = $temp + 'ê'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'б' -and $orig[$i].'Product Name'[$j] -cmatch "^[б]*$"){
                            $temp = $temp + 'á'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'п' -and $orig[$i].'Product Name'[$j] -cmatch "^[п]*$"){
                            $temp = $temp + 'ï'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'П' -and $orig[$i].'Product Name'[$j] -cmatch "^[П]*$"){
                            $temp = $temp + 'Ï'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'у' -and $orig[$i].'Product Name'[$j] -cmatch "^[у]*$"){
                            $temp = $temp + 'ó'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'в' -and $orig[$i].'Product Name'[$j] -cmatch "^[в]*$"){
                            $temp = $temp + 'â'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'В' -and $orig[$i].'Product Name'[$j] -cmatch "^[В]*$"){
                            $temp = $temp + 'Â'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'о' -and $orig[$i].'Product Name'[$j] -cmatch "^[о]*$"){
                            $temp = $temp + 'î'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'О' -and $orig[$i].'Product Name'[$j] -cmatch "^[О]*$"){
                            $temp = $temp + 'Î'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'з' -and $orig[$i].'Product Name'[$j] -cmatch "^[з]*$"){
                            $temp = $temp + 'ç'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'З' -and $orig[$i].'Product Name'[$j] -cmatch "^[З]*$"){
                            $temp = $temp + 'Ç'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'К' -and $orig[$i].'Product Name'[$j] -cmatch "^[К]*$"){
                            $temp = $temp + 'Ê'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ж' -and $orig[$i].'Product Name'[$j] -cmatch "^[ж]*$"){
                            $temp = $temp + 'æ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ж' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ж]*$"){
                            $temp = $temp + 'Æ'
                        }elseif($orig[$i].'Product Name'[$j] -eq ' '){
                            $temp = $temp + ' '
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ы'){
                            $temp = $temp + 'û'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ё' -and $orig[$i].'Product Name'[$j] -cmatch "^[ё]*$"){
                            $temp = $temp + '¸'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ё' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ё]*$"){
                            $temp = $temp + '¨'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ь'){
                            $temp = $temp + 'ü'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Т' -and $orig[$i].'Product Name'[$j] -cmatch "^[Т]*$"){
                            $temp = $temp + 'Ò'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ч' -and $orig[$i].'Product Name'[$j] -cmatch "^[ч]*$"){
                            $temp = $temp + '÷'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'А' -and $orig[$i].'Product Name'[$j] -cmatch "^[А]*$"){
                            $temp = $temp + 'À'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'С' -and $orig[$i].'Product Name'[$j] -cmatch "^[С]*$"){
                            $temp = $temp + 'Ñ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Э' -and $orig[$i].'Product Name'[$j] -cmatch "^[Э]*$"){
                            $temp = $temp + 'Ý'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Д' -and $orig[$i].'Product Name'[$j] -cmatch "^[Д]*$"){
                            $temp = $temp + 'Ä'
                        }elseif($orig[$i].'Product Name'[$j] -eq '1'){
                            $temp = $temp + '1'
                        }elseif($orig[$i].'Product Name'[$j] -eq '2'){
                            $temp = $temp + '2'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'd' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'd'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'D' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'D'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'b' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'b'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'c' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'c'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'C' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'C'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'E' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'E'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'O' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'O'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'l' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'l'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'L' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'L'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'B' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'B'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'e' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'e'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'f' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'f'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'F' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'F'
                        }elseif($orig[$i].'Product Name'[$j] -eq 's' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 's'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'a' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'a'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'A' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'A'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'n' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'n'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'N' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'N'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'k' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'k'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'K' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'K'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'S' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'S'
                        }elseif($orig[$i].'Product Name'[$j] -eq 't' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 't'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'T' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'T'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'k' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'k'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'm' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'm'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'M' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'M'
                        }elseif($orig[$i].'Product Name'[$j] -eq 't' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 't'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'h' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'h'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'H' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'H'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'i' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'i'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'I' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'I'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'u' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'u'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'U' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'U'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'o' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'o'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'p' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'p'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'P' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'P'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'J' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'J'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'j' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'j'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'z' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'z'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Z' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'Z'
                        }elseif($orig[$i].'Product Name'[$j] -eq '3'){
                            $temp = $temp + '3'
                        }elseif($orig[$i].'Product Name'[$j] -eq '4'){
                            $temp = $temp + '4'
                        }elseif($orig[$i].'Product Name'[$j] -eq '5'){
                            $temp = $temp + '5'
                        }elseif($orig[$i].'Product Name'[$j] -eq '6'){
                            $temp = $temp + '6'
                        }elseif($orig[$i].'Product Name'[$j] -eq '7'){
                            $temp = $temp + '7'
                        }elseif($orig[$i].'Product Name'[$j] -eq '8'){
                            $temp = $temp + '8'
                        }elseif($orig[$i].'Product Name'[$j] -eq '9'){
                            $temp = $temp + '9'
                        }elseif($orig[$i].'Product Name'[$j] -eq '0'){
                            $temp = $temp + '0'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'е' -and $orig[$i].'Product Name'[$j] -cmatch "^[е]*$"){
                            $temp = $temp + 'å'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Е' -and $orig[$i].'Product Name'[$j] -cmatch "^[Е]*$"){
                            $temp = $temp + 'Å'
                        }elseif($orig[$i].'Product Name'[$j] -eq ','){
                            $temp = $temp + ''
                        }elseif($orig[$i].'Product Name'[$j] -eq 'q' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'q'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Q' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'Q'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'w' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'w'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'W' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'W'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'r' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'r'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'R' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'R'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'y' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'y'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Y' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'Y'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'g' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'g'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'G' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'G'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'x' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'x'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'X' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'X'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'v' -and $orig[$i].'Product Name'[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'v'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'V' -and $orig[$i].'Product Name'[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'V'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ю' -and $orig[$i].'Product Name'[$j] -cmatch "^[ю]*$" ){
                            $temp = $temp + 'þ'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ю' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ю]*$" ){
                            $temp = $temp + 'Þ'
                        }elseif($orig[$i].'Product Name'[$j] -eq '%'){
                            $temp = $temp + '%'
                        }elseif($orig[$i].'Product Name'[$j] -eq '/'){
                            $temp = $temp + '/'
                        }elseif($orig[$i].'Product Name'[$j] -eq '-'){
                            $temp = $temp + '-'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'ф' -and $orig[$i].'Product Name'[$j] -cmatch "^[ф]*$"){
                            $temp = $temp + 'ô'
                        }elseif($orig[$i].'Product Name'[$j] -eq 'Ф' -and $orig[$i].'Product Name'[$j] -cmatch "^[Ф]*$"){
                            $temp = $temp + 'Ô'
                        }
                    }
                    #endregion
                # $temp = $orig[$i].'Product Name'.Replace(",","-")
                if($temp.Length -gt 30){
                        $temp = $temp.Substring(0,30)
                }
                    
                    $plu0uall[$counter].103 = $temp    # барааны нэрийг тайрч байна
                    $plu0uall[$counter].33 = $orig[$i].'Expiration Days'
                    $plu0uall[$counter].105 = ""
                    try {
                        $cod = $orig[$i].'Product Code'[0] + $orig[$i].'Product Code'[1]
                        $cod2 = $orig[$i].'Product Code'[0] + $origitg[$i].'Product Code'[1] + $orig[$i].'Product Code'[2]
                    }
                    catch {
                        <#Do this if a terminating exception happens#>
                    }
                    If($cod -eq '22'){ # jims nogoo duusax ognoo arilgax
                        $plu0uall[$counter].5 = 1 #sawlasan ognoooo
                        $plu0uall[$counter].7 = 0 #duusax ognooo
                        
                    }else{
                        $plu0uall[$counter].5 = 1
                        $plu0uall[$counter].7 = 1
                    }
                    If($cod2 -eq '245'){ #xoldooson бүтээгдэхүүн arilgax
                        $plu0uall[$counter].5 = 1
                        $plu0uall[$counter].7 = 0
                    }
                    if($orig[$i].'Expiration Days' -eq 0 -or $orig[$i].'Expiration Days' -eq $null -or $orig[$i].'Expiration Days' -eq -1){
                        $plu0uall[$counter].7 = 0 #duuuuax on sar odor
                        $plu0uall[$counter].9 = 0 #dsuuax time
                    }
                    
                    for($m = 0; $m -lt $onsargvi.Length ; $m++){  # duusax bolon exlex on sar
                        if($onsargvi[$m] -eq $orig[$i].'Code on Scale'){
                            $plu0uall[$counter].5 = 0
                            $plu0uall[$counter].7 = 0
                            $plu0uall[$counter].8 = 0; #sell by time
                            $plu0uall[$counter].9 = 0 
                            $m = $onsargvi.Length + 1
                        }         
                    }
                    $cod = $null
                    
                    $counter++;
                }
            }
            
            #ingredient array
            For($i=0; $i -lt $orig.Count ; $i++){
                if($orig[$i].'Code on Scale' -ne $null -and $orig[$i].'Code on Scale' -ne '0' -and ($orig[$i].'Ingredient List').Length -gt 0) {
                    $temp = $null ;$word = $null
                    #region
                    $word = "Орц: " + $orig[$i].'Ingredient List'
                    for($j=0; $j -lt $word.Length; $j++){
                        if($word[$j] -eq 'У' -and $word[$j] -cmatch "^[У]*$"){
                            $temp = $temp + 'Ó'
                        }elseif($word[$j] -eq 'р' -and $word[$j] -cmatch "^[р]*$"){
                            $temp = $temp + 'ð'
                        }elseif($word[$j] -eq 'т' -and $word[$j] -cmatch "^[т]*$"){
                            $temp = $temp + 'ò'
                        }elseif($word[$j] -eq 'ф' -and $word[$j] -cmatch "^[ф]*$"){
                            $temp = $temp + 'ô'
                        }elseif($word[$j] -eq 'Ф' -and $word[$j] -cmatch "^[Ф]*$"){
                            $temp = $temp + 'Ô'
                        }elseif($word[$j] -eq 'ц' -and $word[$j] -cmatch "^[ц]*$"){
                            $temp = $temp + 'ö'
                        }elseif($word[$j] -eq 'Ц' -and $word[$j] -cmatch "^[Ц]*$"){
                            $temp = $temp + 'Ö'
                        }elseif($word[$j] -eq 'а' -and $word[$j] -cmatch "^[а]*$"){
                            $temp = $temp + 'à'
                        }elseif($word[$j] -eq 'г' -and $word[$j] -cmatch "^[г]*$"){
                            $temp = $temp + 'ã'
                        }elseif($word[$j] -eq 'Г' -and $word[$j] -cmatch "^[Г]*$"){
                            $temp = $temp + 'Ã'
                        }elseif($word[$j] -eq 'н' -and $word[$j] -cmatch "^[н]*$"){
                            $temp = $temp + 'í'
                        }elseif($word[$j] -eq 'Н' -and $word[$j] -cmatch "^[Н]*$"){
                            $temp = $temp + 'Í'
                        }elseif($word[$j] -eq 'м' -and $word[$j] -cmatch "^[м]*$"){
                            $temp = $temp + 'ì'
                        }elseif($word[$j] -eq 'М' -and $word[$j] -cmatch "^[М]*$"){
                            $temp = $temp + 'Ì'
                        }elseif($word[$j] -eq 'ө' -and $word[$j] -cmatch "^[ө]*$"){
                            $temp = $temp + 'ù'
                        }elseif($word[$j] -eq 'Ө' -and $word[$j] -cmatch "^[Ө]*$"){
                            $temp = $temp + 'Ù'
                        }elseif($word[$j] -eq 'ш' -and $word[$j] -cmatch "^[ш]*$"){
                            $temp = $temp + 'ø'
                        }elseif($word[$j] -eq 'Ш' -and $word[$j] -cmatch "^[Ш]*$"){
                            $temp = $temp + 'Ø'
                        }elseif($word[$j] -eq 'Ч' -and $word[$j] -cmatch "^[Ч]*$"){
                            $temp = $temp + '×'
                        }elseif($word[$j] -eq 'д' -and $word[$j] -cmatch "^[д]*$"){
                            $temp = $temp + 'ä'
                        }elseif($word[$j] -eq 'Б' -and $word[$j] -cmatch "^[Б]*$"){
                            $temp = $temp + 'Á'
                        }elseif($word[$j] -eq 'я' -and $word[$j] -cmatch "^[я]*$"){
                            $temp = $temp + 'ÿ'
                        }elseif($word[$j] -eq 'я' -and $word[$j] -cmatch "^[Я]*$"){
                            $temp = $temp + 'ß'
                        }elseif($word[$j] -eq 'с' -and $word[$j] -cmatch "^[с]*$"){
                            $temp = $temp + 'ñ'
                        }elseif($word[$j] -eq 'л'-and $word[$j] -cmatch "^[л]*$"){
                            $temp = $temp + 'ë'
                        }elseif($word[$j] -eq 'Л'-and $word[$j] -cmatch "^[Л]*$"){
                            $temp = $temp + 'Ë'
                        }elseif($word[$j] -eq 'ү' -and $word[$j] -cmatch "^[ү]*$"){
                            $temp = $temp + 'ú'
                        }elseif($word[$j] -eq 'Ү' -and $word[$j] -cmatch "^[Ү]*$"){
                            $temp = $temp + 'Y'
                        }elseif($word[$j] -eq 'х' -and $word[$j] -cmatch "^[х]*$"){
                            $temp = $temp + 'õ'
                        }elseif($word[$j] -eq 'Х' -and $word[$j] -cmatch "^[Х]*$"){
                            $temp = $temp + 'Õ'
                        }elseif($word[$j] -eq 'р' -and $word[$j] -cmatch "^[р]*$"){
                            $temp = $temp + 'ð'
                        }elseif($word[$j] -eq 'Р' -and $word[$j] -cmatch "^[Р]*$"){
                            $temp = $temp + 'Ð'
                        }elseif($word[$j] -eq ':'){
                            $temp = $temp + ':'
                        }elseif($word[$j] -eq 'и' -and $word[$j] -cmatch "^[и]*$"){
                            $temp = $temp + 'è'
                        }elseif($word[$j] -eq 'И' -and $word[$j] -cmatch "^[И]*$"){
                            $temp = $temp + 'È'
                        }elseif($word[$j] -eq 'й'){
                            $temp = $temp + 'é'
                        }elseif($word[$j] -eq 'э' -and $word[$j] -cmatch "^[э]*$"){
                            $temp = $temp + 'ý'
                        }elseif($word[$j] -eq 'к' -and $word[$j] -cmatch "^[к]*$"){
                            $temp = $temp + 'ê'
                        }elseif($word[$j] -eq 'б' -and $word[$j] -cmatch "^[б]*$"){
                            $temp = $temp + 'á'
                        }elseif($word[$j] -eq 'п' -and $word[$j] -cmatch "^[п]*$"){
                            $temp = $temp + 'ï'
                        }elseif($word[$j] -eq 'П' -and $word[$j] -cmatch "^[П]*$"){
                            $temp = $temp + 'Ï'
                        }elseif($word[$j] -eq '%'){
                            $temp = $temp + '%'
                        }elseif($word[$j] -eq '/'){
                            $temp = $temp + '/'
                        }elseif($word[$j] -eq 'у' -and $word[$j] -cmatch "^[у]*$"){
                            $temp = $temp + 'ó'
                        }elseif($word[$j] -eq 'в' -and $word[$j] -cmatch "^[в]*$"){
                            $temp = $temp + 'â'
                        }elseif($word[$j] -eq 'В' -and $word[$j] -cmatch "^[В]*$"){
                            $temp = $temp + 'Â'
                        }elseif($word[$j] -eq 'о' -and $word[$j] -cmatch "^[о]*$"){
                            $temp = $temp + 'î'
                        }elseif($word[$j] -eq 'О' -and $word[$j] -cmatch "^[О]*$"){
                            $temp = $temp + 'Î'
                        }elseif($word[$j] -eq 'з' -and $word[$j] -cmatch "^[з]*$"){
                            $temp = $temp + 'ç'
                        }elseif($word[$j] -eq 'З' -and $word[$j] -cmatch "^[З]*$"){
                            $temp = $temp + 'Ç'
                        }elseif($word[$j] -eq 'К' -and $word[$j] -cmatch "^[К]*$"){
                            $temp = $temp + 'Ê'
                        }elseif($word[$j] -eq 'ж' -and $word[$j] -cmatch "^[ж]*$"){
                            $temp = $temp + 'æ'
                        }elseif($word[$j] -eq 'Ж' -and $word[$j] -cmatch "^[Ж]*$"){
                            $temp = $temp + 'Æ'
                        }elseif($word[$j] -eq ' '){
                            $temp = $temp + ' '
                        }elseif($word[$j] -eq 'ы'){
                            $temp = $temp + 'û'
                        }elseif($word[$j] -eq 'ё' -and $word[$j] -cmatch "^[ё]*$"){
                            $temp = $temp + '¸'
                        }elseif($word[$j] -eq 'Ё' -and $word[$j] -cmatch "^[Ё]*$"){
                            $temp = $temp + '¨'
                        }elseif($word[$j] -eq 'ь'){
                            $temp = $temp + 'ü'
                        }elseif($word[$j] -eq 'Т' -and $word[$j] -cmatch "^[Т]*$"){
                            $temp = $temp + 'Ò'
                        }elseif($word[$j] -eq 'ч' -and $word[$j] -cmatch "^[ч]*$"){
                            $temp = $temp + '÷'
                        }elseif($word[$j] -eq 'А' -and $word[$j] -cmatch "^[А]*$"){
                            $temp = $temp + 'À'
                        }elseif($word[$j] -eq 'С' -and $word[$j] -cmatch "^[С]*$"){
                            $temp = $temp + 'Ñ'
                        }elseif($word[$j] -eq 'Э' -and $word[$j] -cmatch "^[Э]*$"){
                            $temp = $temp + 'Ý'
                        }elseif($word[$j] -eq 'Д' -and $word[$j] -cmatch "^[Д]*$"){
                            $temp = $temp + 'Ä'
                        }elseif($word[$j] -eq '1'){
                            $temp = $temp + '1'
                        }elseif($word[$j] -eq '2'){
                            $temp = $temp + '2'
                        }elseif($word[$j] -eq 'd' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'd'
                        }elseif($word[$j] -eq 'D' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'D'
                        }elseif($word[$j] -eq 'b' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'b'
                        }elseif($word[$j] -eq 'c' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'c'
                        }elseif($word[$j] -eq 'C' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'C'
                        }elseif($word[$j] -eq 'E' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'E'
                        }elseif($word[$j] -eq 'O' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'O'
                        }elseif($word[$j] -eq 'l' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'l'
                        }elseif($word[$j] -eq 'L' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'L'
                        }elseif($word[$j] -eq 'B' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'B'
                        }elseif($word[$j] -eq 'e' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'e'
                        }elseif($word[$j] -eq 'f' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'f'
                        }elseif($word[$j] -eq 'F' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'F'
                        }elseif($word[$j] -eq 's' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 's'
                        }elseif($word[$j] -eq 'a' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'a'
                        }elseif($word[$j] -eq 'A' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'A'
                        }elseif($word[$j] -eq 'n' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'n'
                        }elseif($word[$j] -eq 'N' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'N'
                        }elseif($word[$j] -eq 'k' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'k'
                        }elseif($word[$j] -eq 'K' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'K'
                        }elseif($word[$j] -eq 'S' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'S'
                        }elseif($word[$j] -eq 't' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 't'
                        }elseif($word[$j] -eq 'T' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'T'
                        }elseif($word[$j] -eq 'k' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'k'
                        }elseif($word[$j] -eq 'm' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'm'
                        }elseif($word[$j] -eq 'M' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'M'
                        }elseif($word[$j] -eq 't' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 't'
                        }elseif($word[$j] -eq 'h' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'h'
                        }elseif($word[$j] -eq 'H' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'H'
                        }elseif($word[$j] -eq 'i' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'i'
                        }elseif($word[$j] -eq 'I' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'I'
                        }elseif($word[$j] -eq 'u' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'u'
                        }elseif($word[$j] -eq 'U' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'U'
                        }elseif($word[$j] -eq 'o' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'o'
                        }elseif($word[$j] -eq 'p' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'p'
                        }elseif($word[$j] -eq 'P' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'P'
                        }elseif($word[$j] -eq 'J' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'J'
                        }elseif($word[$j] -eq 'j' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'j'
                        }elseif($word[$j] -eq 'z' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'z'
                        }elseif($word[$j] -eq 'Z' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'Z'
                        }elseif($word[$j] -eq '3'){
                            $temp = $temp + '3'
                        }elseif($word[$j] -eq '4'){
                            $temp = $temp + '4'
                        }elseif($word[$j] -eq '5'){
                            $temp = $temp + '5'
                        }elseif($word[$j] -eq '6'){
                            $temp = $temp + '6'
                        }elseif($word[$j] -eq '7'){
                            $temp = $temp + '7'
                        }elseif($word[$j] -eq '8'){
                            $temp = $temp + '8'
                        }elseif($word[$j] -eq '9'){
                            $temp = $temp + '9'
                        }elseif($word[$j] -eq '0'){
                            $temp = $temp + '0'
                        }elseif($word[$j] -eq 'е'){
                            $temp = $temp + 'å'
                        }elseif($word[$j] -eq 'Е' -and $word[$j] -cmatch "^[Е]*$"){
                            $temp = $temp + 'Å'
                        }elseif($word[$j] -eq ','){
                            $temp = $temp + ','
                        }elseif($word[$j] -eq 'q' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'q'
                        }elseif($word[$j] -eq 'Q' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'Q'
                        }elseif($word[$j] -eq 'w' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'w'
                        }elseif($word[$j] -eq 'W' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'W'
                        }elseif($word[$j] -eq 'r' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'r'
                        }elseif($word[$j] -eq 'R' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'R'
                        }elseif($word[$j] -eq 'y' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'y'
                        }elseif($word[$j] -eq 'Y' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'Y'
                        }elseif($word[$j] -eq 'g' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'g'
                        }elseif($word[$j] -eq 'G' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'G'
                        }elseif($word[$j] -eq 'x' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'x'
                        }elseif($word[$j] -eq 'X' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'X'
                        }elseif($word[$j] -eq 'v' -and $word[$j] -cmatch "^[a-z]*$"){
                            $temp = $temp + 'v'
                        }elseif($word[$j] -eq 'V' -and $word[$j] -cmatch "^[A-Z]*$"){
                            $temp = $temp + 'V'
                        }elseif($word[$j] -eq 'ю' -and $word[$j] -cmatch "^[ю]*$" ){
                            $temp = $temp + 'þ'
                        }elseif($word[$j] -eq 'Ю' -and $word[$j] -cmatch "^[Ю]*$" ){
                            $temp = $temp + 'Þ'
                        }elseif($word[$j] -eq '-'){
                            $temp = $temp + '-'
                        }
                    }
                    #endregion
                    #scale code 0 arilgalt   0083 >> 83 bolgono
                    $scalecode = $null
                    if($orig[$i].'Code on Scale'[0] -eq '0'){
                        $scalecode = $orig[$i].'Code on Scale'.Substring(1,3)
                        if($orig[$i].'Code on Scale'[1] -eq '0'){
                            $scalecode = $orig[$i].'Code on Scale'.Substring(2,2)
                            if($orig[$i].'Code on Scale'[2] -eq '0'){
                                $scalecode = $orig[$i].'Code on Scale'.Substring(3,1)
                            }
                        }
                    }else{
                        $scalecode = $orig[$i].'Code on Scale'
                    }     
                    $ingcollimit = 50
                    if($temp.Length -gt $ingcollimit ){
                        $linecounter = 1
                        $sum= 0
                        for($k=0 ; $k -lt $temp.Length/$ingcollimit ; $k++ , $linecounter++){
                            try {
                                $t2 = "|" + $temp.Substring($sum,$ingcollimit) + "|"
                                $ingred+=@(,($scalecode,$linecounter,'',3,$t2))
                            }
                            catch {
                                $t2 = "|" + $temp.Substring($sum,$temp.Length-$sum) + "|"
                                $ingred+=@(,($scalecode,$linecounter,'',3,$t2))
                            }
                            $sum += $ingcollimit 
                        }
                        
                    }else{
                        $t2 = "|" + $temp + "|"
                        $ingred+=@(,($scalecode,1,'',3,$t2))
                    }
                    
                    $temp = $null
                }
            }
            #Remove-Item 'B:\Scripts\plu0uall2.csv'
            $plu0uall | ConvertTo-Csv -delimiter "," -NoTypeInformation | %{$_ -replace '"',''} > 'B:\Scripts\plu0uall2.csv'
            $Resultingred = @()
            #Convert Array to object
                ForEach ($Item in $ingred)
                    {
                        $Resultingred+=[pscustomobject]@{
                            1 = $item[0] 
                            2 = $item[1]
                            3 = $item[2]
                            4 = $item[3]
                            5 = $item[4]
                        }
                    }

            $Resultingred | ConvertTo-Csv -Delimiter "," -NoTypeInformation | ForEach-Object {
                $line = $_ -replace '"', ''  # First replacement
            
                $line | ForEach-Object {
                    $_ -replace '\|', '"'  # Second replacement
                }
            } | Out-File -FilePath 'B:\Scripts\ing0uall2.csv'
            
                        
            Add-Type -Path "B:\Scripts\chilkatdotnet47-9.5.0-x64\ChilkatDotNet47.dll"
            $sb = New-Object Chilkat.StringBuilder
            $sbing = New-Object Chilkat.StringBuilder

            $success = $sb.LoadFile('B:\Scripts\plu0uall2.csv',"utf-8")
            $ing = $sbing.LoadFile('B:\Scripts\ing0uall2.csv',"utf-8")
            
            $success = $sb.WriteFile('B:\Scripts\plu0uall.csv',"windows-1252",$false)
            $ing =  $sbing.WriteFile('B:\Scripts\ing0uall.csv',"windows-1252",$false)
            $ingred = $null
            Start-Sleep -Seconds 1
            try {
                if($ipdevices.($z.Key).GetType().Name -eq "String"){
                    $len = 1
                }else{
                    $len = $ipdevices.($z.Key).Length
                }
                for($i = 0; $i -lt $len; $i++){
                    if($len -eq 1){   # ip device 1 baiwal 
                        $logcontent = Get-Content $z.Value[3] # 0 1 iig shalgaj bna txt ees 
                        if($logcontent -eq 0){
                            cmd.exe /c 'pluimport.bat' $ipdevices.($z.Key)
                            1 | out-file -FilePath $z.Value[3]
                            $testping = $null
                            $testping = Test-Connection -ComputerName $ipdevices.($z.Key) -Count 2 -Quiet  # svljeetei vgvig shalgaj bna
                            if(!$testping){
                                if((Get-Date).Hour -ge 8 -and (Get-Date).Hour -le 18){
                                    Write-Output "88 jin svljeegvi bnashdee"
                                    $loopstatus = 0
                                    0 | out-file -FilePath $z.Value[3]
                                }  
                            }

                        }else{
                            Write-Output "88 jin shinechilsen bna"
                        }
                    }else{ # ipdevices 2 ba olon baiwal 
                        $sliceoflife = 'B:\Scripts\zabbix_scale\' + $ipdevices.($z.Key)[$i] + '.txt'

                        $logcontent = Get-Content $sliceoflife
                        if($logcontent -eq 0){
                            cmd.exe /c 'pluimport.bat' $ipdevices.($z.Key)[$i]
                            1 | out-file -FilePath $sliceoflife
                            $testping = $null
                            $testping = Test-Connection -ComputerName $ipdevices.($z.Key)[$i] -Count 2 -Quiet
                            if(!$testping){
                                if((Get-Date).Hour -ge 8 -and (Get-Date).Hour -le 18){
                                    Write-Output "21 jin svljeegvi bnashdee"
                                    $loopstatus = 0
                                    
                                    0 | out-file -FilePath $sliceoflife
                                }  
                            }
                            #$tempfname = "B:\Scripts\zabbix_scale\" + (Get-Date -Format "yyyyMMddhhmmss") + "." + $ipdevices.($z.Key)[$i]
                            #New-Item -ItemType Directory -Path $tempfname
                            #copy-item "B:\Scripts\plu0uall.csv" -Destination $tempfname
                        }else{
                            Write-Output "21 jin shinechilsen bna"
                        }    
                    }
                }
            }
            catch {
                #0 | out-file -FilePath $z.Value[3]
            }
        Remove-Item $z.Value[1];
        Copy-Item "B:\Scripts\plu0uall.csv" -Destination $z.Value[1];
        Remove-Item "B:\Scripts\plu0uall.csv"
        } # for leep end
    } # dict loop end
    
    # RESET ALL SCALES 0 status
    if((get-date).Hour -eq $scalezerostatus -and (get-date).Minute -le $scalezerostatusmin){
        $loopstatus = 0
        $backstatus = 0
        0 | out-file -FilePath 'B:\Scripts\zabbix_scale\Scale88.txt'

        for($i =0; $i -lt $ipdevices.($z.Key).Length; $i++){
            $logfile = 'B:\Scripts\zabbix_scale\' + $ipdevices.($z.Key)[$i] + '.txt'
            0 | Out-File -FilePath $logfile
        }

        (get-date).toString()+ "all digit scale 0 status" | out-file -FilePath $logfilemain -Append
    }
        
    
    #ZK time device baaz backup
    if((get-date).hour -eq 12 -and $backstatus -eq 0){
        EXECUTER -v1 "192.168.0.25" -v2 "ZKSoft" -v3 $query_zksoftbackup
        Copy-Item  "\\192.168.0.25\mssql\Backup\ZKSoft.bak" -Destination "\\10.0.99.40\Backups\ZkSfot" -Force
        Remove-Item "\\192.168.0.25\mssql\Backup\ZKSoft.bak"
        (get-date).toString() + "zk time device backup run" | out-file -FilePath $logfilemain -Append
        $backstatus = 1
    }

    # carrefour sport odorlogoos bolj loop daxin ajilluulj bna  # RESET ALL SCALES 0 status
    if((get-date).hour -eq 22 -and (get-date).minute -eq 32){
        $loopstatus = 0
        0 | out-file -FilePath 'B:\Scripts\zabbix_scale\Scale88.txt'

        for($i =0; $i -lt $ipdevices.($z.Key).Length; $i++){
            $logfile = 'B:\Scripts\zabbix_scale\' + $ipdevices.($z.Key)[$i] + '.txt'
            0 | Out-File -FilePath $logfile
        }

        (get-date).toString() + "all digit scale 0 status 22:30 d" | out-file -FilePath $logfilemain -Append
    }

    # price check zone, Жингийн PLU -г татаж эксел файлтай тулгалт хийж байна
    if($loopstatus -eq 1 -and (get-date).Hour -ge $jobstart_hour -and (get-date).hour -le $jobend_hour -and (get-date).minute -ge $jobstart_min){
        foreach ($z in $carrefour.GetEnumerator()){
            $origcheck = Import-Excel -Path $z.Value[0]
            $origcheck = $origcheck | Sort-Object -Property 'Code on Scale'
            $lfcodeindex = $origcheck.'Code on Scale' -as [string[]]
            cmd.exe /c 'B:\Scripts\zabbix_scale\yagjinplu\pluget.bat' $z.Value[4]
            $scaleplu = Import-Csv -Path 'B:\Scripts\plu0uall.csv' -Delimiter "," -Header 'lfcode','flagdelete','weight','col4','selldate','useddate','packeddate','selltime','packedtime','col10','col11','pricebased_per_unit','col13','nutritionprint','unit_price_override_15','PLU_price_change_16','col17','col18','unit_price'
            Start-sleep -seconds 1
            Remove-item 'B:\Scripts\plu0uall.csv'
            # 
            for($i=10; $i -lt $price_check_row_limit; $i++){
                if(($scaleplu[$i].'lfcode').Length -eq 1){
                    $tcode = "000" + $scaleplu[$i].'lfcode'
                }elseif(($scaleplu[$i].'lfcode').Length -eq 2){
                    $tcode = "00" + $scaleplu[$i].'lfcode'
                }elseif(($scaleplu[$i].'lfcode').Length -eq 3){
                    $tcode = "0" + $scaleplu[$i].'lfcode'
                }else{
                    $tcode = $scaleplu[$i].'lfcode'
                }
                $tindex = [array]::FindIndex($lfcodeindex,[Predicate[String]]{param($s)$s -eq $tcode})
                $produectname = $origcheck[$tindex].'Product Name'
                $ldfcode = $origcheck[$tindex].'Code on Scale'
                $scaleprice = $scaleplu[$i].'unit_price'
                $excelprice = $origcheck[$tindex].'Product Price'
                #Write-Output "scaleprice: $scaleprice excelprice: $excelprice"
                
                if($excelprice -ne $scaleprice -and $tindex -ne -1){
                    (get-date).toString() + " lfcode: $ldfcode product name: $produectname price: $scaleprice vs $excelprice" | out-file -FilePath $logfilemain -Append
                }
            }
        }
    }
    
    Write-Output "DIGI Scale Sleeping..."
    0 | Out-File -FilePath $isrun
    Start-Sleep -Seconds $startleepduration


}





