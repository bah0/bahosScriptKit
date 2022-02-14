#
# This script checks every mailbox for send as delegation from account relay@*  
# and adds the same send as delegation to test@example.com
#

$mailboxes = Get-EXOMailbox -ResultSize Unlimited
$relay1 = @();


foreach ($u in $mailboxes) {
    $relay1 += Get-RecipientPermission -Identity $u.UserPrincipalName | Where {$_.Trustee -like "relay@*"} | Add-RecipientPermission -Identity $u.UserPrincipalName -Trustee "test@example.com" -Confirm:$false
}


echo $relay1