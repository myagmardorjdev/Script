$acl = Get-Acl "D:\Scripts"

$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("NT Service\MSSQLSERVER","FullControl","Allow")

$acl.SetAccessRule($AccessRule)

$acl | Set-Acl "D:\Scripts"