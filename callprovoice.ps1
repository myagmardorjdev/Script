$ftpServer = "ftp://192.168.0.65"
$ftpUsername = "callpro"
$ftpPassword = "VNa9cT9h"


$remoteFilePath = "/SNSRSPR/2023/11/20/14/2023-11-20_14-42-33_503_SNSRSPR_97677557755_99965891_99965891_srv03b.callpro.mn-1700462553.1420152.wav"

 #the downloaded file
$localDirectory = "D:"
$remoteDirectory = "/SNSRSPR"
# Create FTP request
# Create FTP request
$ftpRequest = [System.Net.FtpWebRequest]::Create("$ftpServer$remoteDirectory")
$ftpRequest.Credentials = New-Object System.Net.NetworkCredential($ftpUsername, $ftpPassword)
$ftpRequest.Method = [System.Net.WebRequestMethods+Ftp]::ListDirectoryDetails

# Get FTP response
$ftpResponse = $ftpRequest.GetResponse()

# Get the list of files and subdirectories from the response stream
$reader = New-Object System.IO.StreamReader($ftpResponse.GetResponseStream())
$listing = $reader.ReadToEnd()

# Display the list of files and subdirectories
Write-Output $listing
#768364 Nov 20 15:00 2023-11-20_14-42-33_503_SNSRSPR_97677557755_99965891_99965891_srv03b.callpro.mn-1700462553.1420152.wav
# Close the response stream
$reader.Close()
$ftpResponse.Close()

$webClient = New-Object System.Net.WebClient
$webClient.Credentials = New-Object System.Net.NetworkCredential($ftpUsername, $ftpPassword)

$filename = '1700462553.1420152.wav'
$webClient.DownloadFile("$ftpServer$remoteFilePath", $localDirectory+'\'+$filename)


$webClient.Dispose()