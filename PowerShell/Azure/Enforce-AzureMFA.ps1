# usage ./script samaccountname

$samaccountname = $args[0]

$enforcedMFA = New-Object -TypeName Microsoft.Online.Administration.StrongAuthenticationRequirement
$enforcedMFA.RelyingParty = "*"
$enforcedMFA.State = "Enforced"
$sar = @($enforcedMFA)


$userExists = Get-ADUser $samaccountname

if($userExists) {
    $msoluser = Get-MsolUser -UserPrincipalName $userExists.UserPrincipalName
    if ($msoluser){
        Write-Host "User found:" $userExists.Name
        Write-Host "MFA State:" $msoluser.StrongAuthenticationRequirements.State
        if($msoluser.StrongAuthenticationRequirements.State -ne "Enforced"){
            Write-Host -ForegroundColor yellow "Setting MFA to Enforced for User " $userExists.Name
        Set-MsolUser -UserPrincipalName $userExists.UserPrincipalName -StrongAuthenticationRequirements $sar
        } else {
            Write-Host -ForegroundColor red "User has already MFA enforced. Quitting..."
        }

    }
    else {
        Write-Host -ForegroundColor red "User not found in Azure AD. Wait for sync and try again later."
    }
}
else {
    Write-Host -ForegroundColor red "User not found in AD."
}



#$enforcedMFA = New-Object -TypeName Microsoft.Online.Administration.StrongAuthenticationRequirement
#$enforcedMFA.RelyingParty = "*"
#$enforcedMFA.State = "Enforced"
#$sar = @($enforcedMFA)
#Set-MsolUser -UserPrincipalName $user -StrongAuthenticationRequirements $sar