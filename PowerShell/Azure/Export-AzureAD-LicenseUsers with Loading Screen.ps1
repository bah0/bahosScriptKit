$admincred = Get-Credential

Connect-AzureAD -Credential $admincred

$SearchLicense = "POWER_BI_PRO"

$AzureADUsers = Get-AzureADUser -All $true
$Counter = 0

$Members = New-Object System.Collections.ArrayList


Write-Host "Vorgang dauert ca. 5 Minuten, bitte warten..."
foreach ($u in $AzureADUsers){
    $userPN = $u.UserPrincipalName
    $displayName = $u.DisplayName
    
    $Counter++
    Write-Progress -Activity "Ladevorgang" -Percentcomplete (($Counter*100)/$AzureADUsers.count) -Status "Aktuell bei User $($AzureADUsers[$Counter].UserPrincipalName)"
    
    $PBIAssigned = Get-AzureADUserLicenseDetail -ObjectId $userPN | Select SkuPartNumber 
    
    if($PBIAssigned.SkuPartNumber -ne $null){
        foreach($license in $PBIAssigned.SkuPartNumber){
            $temp = New-Object System.Object
            $temp | Add-Member -MemberType NoteProperty -Name "DisplayName" -Value $displayName
            $temp | Add-Member -MemberType NoteProperty -Name "UserPrincipalName" -Value $userPN
            $temp | Add-Member -MemberType NoteProperty -Name "AssignedLicences" -Value $license
            $Members.Add($temp) | Out-Null
        }
    }
} 
Write-Host "Schleife durch, exportiere Datei output.csv"
$Members | Export-Csv "output.csv"