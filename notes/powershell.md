# PowerShell Notes

Patterns from The Forge, The Keep, and the Azure scripts.

## Script skeleton

```powershell
<#
.SYNOPSIS
    One line on what it does.
.DESCRIPTION
    What it changes, what it never touches, and whether it's safe to re-run.
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$ResourceGroupName
)
$ErrorActionPreference = 'Stop'

if ($PSCmdlet.ShouldProcess($ResourceGroupName, "Apply baseline")) {
    # change
}
# read back and verify
```

`SupportsShouldProcess` gives you `-WhatIf` and `-Confirm` for free.

## Idempotency

Check, then act. From `New-LabDepartment` in [MavLabTools](https://github.com/Lglass510/The_Forge/blob/main/Modules/MavLabTools/MavLabTools.psm1):

```powershell
try {
    Get-ADOrganizationalUnit -Identity $DepartmentOU -ErrorAction Stop
    Write-Host "Department '$Department' already exists under '$ParentOU'."
}
catch {
    New-ADOrganizationalUnit -Name $Department -Path $ParentOUPath
}
```

Or use an operation that's idempotent by design (HTTP PUT, `Set-*`). POST and `New-*` usually need the check.

## Secrets

Never put a password in a script:

```powershell
$Password = Read-Host "Initial password" -AsSecureString
```

## Modules

```text
Modules\
└── MavLabTools\
    ├── MavLabTools.psd1   # manifest (still to add in The Forge)
    └── MavLabTools.psm1
```

```powershell
$env:PSModulePath -split ';'          # where PowerShell looks
Import-Module MavLabTools
Get-Command -Module MavLabTools
```

## Remoting

```powershell
$s = New-PSSession -VMName "DC1" -Credential (Get-Credential)   # PowerShell Direct from the Hyper-V host
Copy-Item -Path .\Modules\MavLabTools\MavLabTools.psm1 `
    -Destination "C:\Users\Administrator\Documents\WindowsPowerShell\Modules\MavLabTools" -ToSession $s -Force
Invoke-Command -Session $s { Import-Module MavLabTools; Get-LabUsers }
Enter-PSSession $s   # interactive only
```

## CSV-driven Active Directory work

```powershell
Import-Csv .\mavlab_employees.csv | ForEach-Object {
    New-ADUser -Name "$($_.FirstName) $($_.LastName)" -SamAccountName $_.Username `
        -Path "OU=$($_.Department),$BaseOU" -AccountPassword $Password -ChangePasswordAtLogon $true -Enabled $true
}
```

Keep source data, OU placement, manager mapping, and group membership as separate steps. Each is easier to check alone. Source: [The Keep ActiveDirectory](https://github.com/Lglass510/The_Keep/tree/main/ActiveDirectory)

## Syntax traps

| Trap | What happens |
| --- | --- |
| Anything after a line-continuation backtick | Statement ends early and runs half-built |
| `-AddressPrefix subnet.AddressPrefix` (no `$`) | Passes the literal text |
| Misspelled parameter | Error, no fuzzy matching |
| Ignoring a cmdlet's return value | Works only if it happens to modify in place |
| Command not recognized | Check `$PSVersionTable`, then `Get-Command`, then the module |
| Splatting: `@params` not `$params` | `$params` passes one hashtable as a positional argument |
