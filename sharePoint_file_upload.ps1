Function Upload-LargeFile($FilePath, $LibraryName, $FileChunkSize=10)
{
    Try {
        #Get File Name
        $FileName = [System.IO.Path]::GetFileName($FilePath)
        $UploadId = [GUID]::NewGuid()
 
        #Get the folder to upload
        $Library = $Ctx.Web.Lists.GetByTitle($LibraryName)
        $Ctx.Load($Library)
        $Ctx.Load($Library.RootFolder)
        $Ctx.ExecuteQuery()
 
        $BlockSize = $FileChunkSize * 1024 * 1024 
        $FileSize = (Get-Item $FilePath).length
        If($FileSize -le $BlockSize)
        {
            #Regular upload
            $FileStream = New-Object IO.FileStream($FilePath,[System.IO.FileMode]::Open)
            $FileCreationInfo = New-Object Microsoft.SharePoint.Client.FileCreationInformation
            $FileCreationInfo.Overwrite = $true
            $FileCreationInfo.ContentStream = $FileStream
            $FileCreationInfo.URL = $FileName
            $Upload = $Docs.RootFolder.Files.Add($FileCreationInfo)
            $ctx.Load($Upload)
            $ctx.ExecuteQuery()
        }
        Else
        {
            #Large File Upload in Chunks
            $ServerRelativeUrlOfRootFolder = $Library.RootFolder.ServerRelativeUrl
            [Microsoft.SharePoint.Client.File]$Upload
            $BytesUploaded = $null 
            $Filestream = $null
            $Filestream = [System.IO.File]::Open($FilePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
            $BinaryReader = New-Object System.IO.BinaryReader($Filestream)
            $Buffer = New-Object System.Byte[]($BlockSize)
            $LastBuffer = $null
            $Fileoffset = 0
            $TotalBytesRead = 0
            $BytesRead
            $First = $True
            $Last = $False
 
            #Read data from the file in blocks
            While(($BytesRead = $BinaryReader.Read($Buffer, 0, $Buffer.Length)) -gt 0)
            { 
                $TotalBytesRead = $TotalBytesRead + $BytesRead 
                If ($TotalBytesRead -eq $FileSize)
                { 
                    $Last = $True
                    $LastBuffer = New-Object System.Byte[]($BytesRead)
                    [Array]::Copy($Buffer, 0, $LastBuffer, 0, $BytesRead) 
                }
                If($First)
                { 
                    #Create the File in Target
                    $ContentStream = New-Object System.IO.MemoryStream
                    $FileCreationInfo = New-Object Microsoft.SharePoint.Client.FileCreationInformation
                    $FileCreationInfo.ContentStream = $ContentStream
                    $FileCreationInfo.Url = $FileName
                    $FileCreationInfo.Overwrite = $true
                    $Upload = $Library.RootFolder.Files.Add($FileCreationInfo)
                    $Ctx.Load($Upload)
 
                    #Start FIle upload by uploading the first slice
                    $s = new-object System.IO.MemoryStream(, $Buffer) 
                    $BytesUploaded = $Upload.StartUpload($UploadId, $s)
                    $Ctx.ExecuteQuery() 
                    $fileoffset = $BytesUploaded.Value 
                    $First = $False 
                } 
                Else
                { 
                    #Get the File Reference
                    $Upload = $ctx.Web.GetFileByServerRelativeUrl($Library.RootFolder.ServerRelativeUrl + [System.IO.Path]::AltDirectorySeparatorChar + $FileName);
                    If($Last)
                    {
                        $s = [System.IO.MemoryStream]::new($LastBuffer)
                        $Upload = $Upload.FinishUpload($UploadId, $fileoffset, $s)
                        $Ctx.ExecuteQuery()
                        Write-Host "File Upload completed!" -f Green                       
                    }
                    Else
                    {
                        #Update fileoffset for the next slice
                        $s = [System.IO.MemoryStream]::new($buffer)
                        $BytesUploaded = $Upload.ContinueUpload($UploadId, $fileoffset, $s)
                        $Ctx.ExecuteQuery()
                        $fileoffset = $BytesUploaded.Value
                    }
                }
            }
        }
    }
    Catch {
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
    Finally {
        If($Filestream -ne $null)
        {
            $Filestream.Dispose()
        }
    }
}


$URL = "https://altanjoloogroupmn.sharepoint.com/sites/it77"
$TargetFolderRelativeURL ="Shared Documents/Backups/AJT 5.0"
$sourceFolder = "D:\"
$logout = 'D:\sharepointlog.txt'
#CREDENTIAL
$AdminAccount = "enkhtur@altanjoloo.mn"
$AdminPass = "Yanjika123$"
$SecPwd = $(ConvertTo-SecureString $AdminPass -asplaintext -force) 
$Cred = New-Object System.Management.Automation.PSCredential ($AdminAccount, $SecPwd)

Import-Module SharePointPnPPowerShellOnline
Connect-PnPOnline -url $URL -Credentials ($cred)
$Ctx = Get-PnPContext

#subfolders create
$File = Get-ChildItem -Path $sourceFolder -Recurse -Directory -Force -ErrorAction SilentlyContinue | Select-Object FullName
foreach($f in $File) {
    Write-Output $f 
    $f = $f.FullName
    $ve = ($f -split "\\").Length
    $foldername = ($F -split "\\")[$ve-1] 
    if($f.IndexOf("\") -eq $f.LastIndexOf("\")){
        $folderdirectory = $TargetFolderRelativeURL
        Add-PnPFolder -Name $foldername -Folder $folderdirectory
    }else{
        $folderdirectory = $f.Substring(3)
        $urldirectory=$folderdirectory.Substring(0,$folderdirectory.Length-$foldername.Length-1)
        $urldirectory=$urldirectory.Replace("\","/")
        $urldirectory = $TargetFolderRelativeURL+"/"+$urldirectory
        Write-Output "folder: " $foldername
        Write-Output "url: "$urldirectory
        Add-PnPFolder -Name $foldername -Folder $urldirectory
    }
}

$counter = 0;
$Files = Get-ChildItem $sourceFolder -Recurse | % { $_.FullName }
foreach($File in $Files) {
    $begindate = (get-date)
    $tempdate = (Get-Item $File).CreationTime
    $lastdate = (Get-Item $File).LastWriteTime
    $tmp1 = ($File -split "\\")[-1]
    #if((Get-Date).Day -eq $tempdate.Day -or (get-date).day -eq $lastdate.day){
            $tmp2 = $File.Substring($sourceFolder.Length)
            $tmp2 = $tmp2.Substring(0,$tmp2.LastIndexOf("\"))
            $tmp2 = $tmp2.Replace('\','/')
            $target = $TargetFolderRelativeURL +"/"+ $tmp2  # subfolders url path
            if(Test-Path -Path $File -PathType Leaf){
                $filesize = (Get-Item -Path $File).Length/1MB
                if($filesize -lt 100){ # 100 MB aas baga zone
                try {
                    
                    Add-PnPFile -Path $File -Folder $target   #CREATING SUB FOLDERS
                    Write-Output $tmp1+" file uploaded" -f Green
                    $counter++;
                    (Get-Date).ToString() + "File uploaded: " + $file +" Counter: "+ $counter | out-file -FilePath $logout -append
                }
                catch {
                    Write-Output $File "failed"
                    (Get-Date).ToString() + "File failed: " + $file +" Counter: "+ $counter | out-file -FilePath $logout -append
                }}
                else{ # LARGE FILE COPy ZONE
                    try {
                        Upload-LargeFile -FilePath $File -LibraryName "Documents" 
                        $counter++;
                        (Get-Date).ToString() + "Large file uploaded: " + $file +" Counter: "+ $counter | out-file -FilePath $logout -append
                    }
                    catch {
                        (Get-Date).ToString() + "Large file failed: " + $file +" Counter: "+ $counter | out-file -FilePath $logout -append
                    }
                    $tmp3 = $File.Substring($sourceFolder.length)
                    $tmp3 = $tmp3.replace("\","/")
                
                $file_name_only = ($file -split "\\")[($file -split "\\").Length-1]
                $subfolders_only = $tmp3.Replace($file_name_only,""); $subfolders_only = $subfolders_only.Replace("\","/")   ; $subfolders_only=$subfolders_only.Substring(0,$subfolders_only.Length-1)
                $Source = "/Shared Documents/" + (Split-Path $file -Leaf)

                $Target = $TargetFolderRelativeURL +"/"+$tmp3

                    Move-PnPFile $Source -TargetUrl $Target -Force
                    (Get-Date).ToString() + "Large file moved: " + $file +" Counter: "+ $counter  + " Moved target name: " +$target | out-file -FilePath $logout -append 
                }
                
            }
             
#    }
}
#endregion


