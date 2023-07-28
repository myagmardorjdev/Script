#Function to Upload Large File to SharePoint Online Library
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
 
#Connect to SharePoint Online site
Connect-PnPOnline "https://altanjoloogroupmn.sharepoint.com/sites/it77" 
$Ctx = Get-PnPContext
 
#Call the function to Upload File
Upload-LargeFile -FilePath "D:\sharepoint_sync\data.dat" -LibraryName "Document" 

$Source = "Shared Documents/Drawing2.vsdx"
$Target ="Shared Documents/Backups/Drawing2.vsdx"
Move-PnPFile $Source -TargetUrl $Target -Force