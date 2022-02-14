$UserhomePath = "\\mzfs01\Userhome\"



$Userhome = $args[0]
$identity = "MOZOHOLDING\$Userhome"

$UserhomeDirPath = ($UserhomePath + $Userhome)


$FileSystemRights = "Modify"
$AccessType = "Allow"

Write-Host -ForegroundColor yellow "Checking if User $Userhome exists"
$userExists = Get-ADUser $Userhome
$userFolderExists = Test-Path $UserhomeDirPath

if ($userExists){
    Write-Host "User: $Userhome found in Active Directory."
    if($userFolderExists -eq $false){
        Write-Host "Creating Userhome directory: $UserhomeDirPath"
        
        mkdir $UserhomeDirPath | Out-Null
        Write-Host "Setting ACLs for Userhome directory: $UserhomeDirPath"

        $newACL = Get-Acl $UserhomeDirPath
        $fsUserAccessRuleArguments = $identity, $FileSystemRights,"ContainerInherit,ObjectInherit", "None", $AccessType
        $fsUserAccessRule = New-Object -TypeName System.Security.AccessControl.FileSystemAccessRule -ArgumentList $fsUserAccessRuleArguments
        $newACL.SetAccessRule($fsUserAccessRule)
        Set-Acl $UserhomeDirPath -AclObject $newACL
        Write-Host -ForegroundColor yellow "Done!"

    }
    else {
        Write-Host -ForegroundColor Red "Userhome directory for User $Userhome already exists. Quitting."
    }

}
else {
    Write-Host -ForegroundColor Red "User: $Userhome not found in Active Directory. Quitting."
}
<#
$newACL = Get-ACL -Path $UserhomeDirPath
# Create new rule
$fsUserAccessRuleArguments = $identity, $FileSystemRights,"ContainerInherit,ObjectInherit", "None", $AccessType
$fsUserAccessRule = New-Object -TypeName System.Security.AccessControl.FileSystemAccessRule -ArgumentList $fsUserAccessRuleArguments
$newACL.SetAccessRule($fsUserAccessRule)
Set-Acl $UserhomeDirPath -AclObject $newACL
#>