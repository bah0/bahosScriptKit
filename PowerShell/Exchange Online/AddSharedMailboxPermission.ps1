try {
# usage ./this_script.ps1 "user" "shared mailbox"



$user = $args[0]
$sharedMailbox = $args[1]
$confirm = $args[2]
echo $confirm

if($args.Count -ge 2){
    if ($args.Count -gt 3){
        if($confirm -eq $false){
            $confirm = $false
        }
        else {
            $confirm = $true
        }
    }
    else {
        $confirm = $true
    }

}
else {
    Write-Host -ForegroundColor Yellow  "Usage: ./script user shared_mailbox"
    Write-Host -ForegroundColor Red  "Too few arguments. Skipping..."
    exit
}



#$adminbahadir = Import-Clixml ./pso365Cred.cred
#Connect-ExchangeOnline -Credential $adminbahadir

   
    Write-Host ""
	Write-Host "User:"
	$upn = (Get-EXOMailbox $user)
    Write-Host $upn.UserPrincipalName
    Write-Host ""

    if($upn.RecipientTypeDetails -ne "UserMailbox")
    {
        Write-Host -ForegroundColor Red  "User does not have type UserMailbox in RecipientTypeDetails. Skipping..."
        exit
    }

	Write-Host "Mailbox:"
	$mbx = (Get-EXOMailbox $sharedMailbox)
    Write-Host $mbx.PrimarySmtpAddress 
    Write-Host ""

    if($mbx.RecipientTypeDetails -ne "SharedMailbox")
    {
        Write-Host -ForegroundColor Red "Mailbox does not have type SharedMailbox in RecipientTypeDetails. Skipping..."
        exit
    }

	Write-Host "checking if user has already permission..."	
	$x = Get-EXOMailboxPermission -Identity $sharedMailbox | Where {$_.User -like "*@*"}

    $x | ForEach-Object {
        if( $upn.UserPrincipalName -eq $_.User){
            Write-Host -ForegroundColor Red "User already exists here. Skipping..."
            exit
        }
        #Write-Host $_.User
    }
    Write-Host "User doesn't have permission yet"

    Write-Host ""

	Write-Host ""
	Write-Host "adding $user to Mailbox $sharedMailbox..."
	Add-MailboxPermission -Identity $sharedMailbox -User $user -AccessRights FullAccess -InheritanceType all -Confirm:$confirm
	Add-RecipientPermission -Identity $sharedMailbox -Trustee $user -AccessRights SendAs -Confirm:$confirm
	Write-Host "erledigt."

    Write-Host ""
}

catch {
	Write-Host "Fehler abgefangen`r`n $_.Exception.Message"
	
}