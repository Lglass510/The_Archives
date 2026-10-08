# Azure Notes

Az PowerShell and Bicep patterns used in The Sky Hold, The Roads, and The Ascent.

## Before deploying anything

```powershell
Connect-AzAccount
Get-AzContext                                  # which subscription and tenant am I in?
Set-AzContext -Subscription "<name-or-id>"
```

Put a guard at the top of scripts:

```powershell
$ErrorActionPreference = 'Stop'
if (-not (Get-AzContext)) { throw "Not signed in. Run Connect-AzAccount." }
```

## Virtual networks

Build the subnet first and pass it to the VNet create. One call, nothing relies on side effects:

```powershell
$subnet = New-AzVirtualNetworkSubnetConfig -Name "mars1" -AddressPrefix "10.0.1.0/24"
New-AzVirtualNetwork -Name "mavnetwork" -ResourceGroupName $rg -Location "northcentralus" `
    -AddressPrefix "10.0.0.0/16" -Subnet $subnet
```

Add a subnet to an existing VNet. Capture the return value both times:

```powershell
$vnet = Get-AzVirtualNetwork -Name "mavnetwork" -ResourceGroupName $rg
$vnet = Add-AzVirtualNetworkSubnetConfig -Name "AzureBastionSubnet" -AddressPrefix "10.0.0.0/26" -VirtualNetwork $vnet
$vnet = $vnet | Set-AzVirtualNetwork
```

- `*Config` cmdlets only change a local object. Nothing reaches Azure until `Set-AzVirtualNetwork`.
- Bastion needs a subnet named exactly `AzureBastionSubnet`, `/26` or larger.
- A NIC must be in the same region as its VNet. A resource group's location doesn't decide that.

Source: [The Roads networkbuild.md](https://github.com/Lglass510/The_Roads/blob/main/networkbuild.md)

## NSGs

```powershell
$rule = New-AzNetworkSecurityRuleConfig -Name "Allow-RDP-From-Bastion" -Priority 100 `
    -Direction Inbound -Access Allow -Protocol Tcp `
    -SourceAddressPrefix "10.0.0.0/26" -SourcePortRange "*" `
    -DestinationAddressPrefix "*" -DestinationPortRange 3389
New-AzNetworkSecurityGroup -Name "mars1-nsg" -ResourceGroupName $rg -Location "northcentralus" `
    -SecurityRules $rule -Force   # -Force: confirmed management-port rule, narrow source
```

Default rules (priority 65000+) already deny inbound internet traffic. An explicit rule documents what's allowed.

## Storage baseline

```powershell
Set-AzStorageAccount -ResourceGroupName $rg -Name $name `
    -EnableHttpsTrafficOnly $true -MinimumTlsVersion TLS1_2 -AllowBlobPublicAccess $false
```

Denying public network access can break existing clients, so treat it as a separate, reviewed change. Infrastructure encryption can only be set when the account is created. Source: [The Sky Hold Storage](https://github.com/Lglass510/The_Sky_Hold/tree/main/Storage)

## Calling APIs that have no cmdlet

```powershell
$r = Invoke-AzRestMethod -Method PUT -Path "/providers/microsoft.aadiam/diagnosticSettings/<name>?api-version=2017-04-01" -Payload $json
if ($r.StatusCode -ge 300) { throw $r.Content }
```

`Invoke-AzRestMethod` doesn't throw on HTTP errors. Check `StatusCode` yourself.

## Bicep

| Pattern | Why |
| --- | --- |
| `name: guid(law.id, 'T1098.003')` | Same name every deploy, so it updates instead of duplicating |
| `resource law '...' existing = { name: lawName }` | Reference something deployed elsewhere, such as in a module |
| `scope: law` | Extension resources (Sentinel, role assignments) attach to another resource |
| `loadTextContent('detection/x.kql')` | Keep the KQL in its own file |
| `principalType: 'ServicePrincipal'` | Avoids `PrincipalNotFound` while a new managed identity replicates |
| `dependsOn` | Only when there's no reference that sets the order |
| `.bicepparam` | One-command deploys with `-TemplateParameterFile` |

```powershell
New-AzResourceGroupDeployment -ResourceGroupName $rg -TemplateParameterFile ./main.bicepparam -WhatIf
New-AzResourceGroupDeployment -ResourceGroupName $rg -TemplateParameterFile ./main.bicepparam
```

Source: [The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel)

## Teardown

Remove Sentinel from a workspace before deleting it, or don't reuse the workspace name. Sentinel state can outlive the workspace.
