# Networking Notes

From The Roads and The Keep. Lab network: `172.16.10.0/24` on Hyper-V switch `mavlab`, NAT gateway `172.16.10.1`, DC1 (DNS) `172.16.10.10`, SRV2 `.20`, Linux1 `.30`. Azure: `mavnetwork` `10.0.0.0/16`, `mars1` `10.0.1.0/24`, `AzureBastionSubnet` `10.0.0.0/26`.

Older notes using `172.31.x` addresses come from the Hyper-V Default Switch, before the `mavlab` network existed.

## Troubleshooting order

| Step | Linux | Windows |
| --- | --- | --- |
| 1. Local link | `ping -c 4 172.16.10.10` | `Test-NetConnection 172.16.10.30` |
| 2. Gateway | `ping -c 4 172.16.10.1` | `Get-NetRoute -DestinationPrefix 0.0.0.0/0` |
| 3. Internet by IP | `ping -c 4 8.8.8.8` | `Test-NetConnection 8.8.8.8` |
| 4. DNS service | `nslookup google.com 172.16.10.10` | `Get-NetUDPEndpoint -LocalPort 53` |
| 5. External DNS | `resolvectl status` | `Resolve-DnsName google.com -Server 1.1.1.1` |

If step 3 works and step 5 doesn't, it's DNS. If ping fails, test the actual service port before deciding the path is down:

```powershell
Test-NetConnection 172.16.10.10 -Port 53
```

## Hyper-V NAT

```powershell
Get-VMSwitch; Get-NetAdapter     # confirm the mavlab switch and its vEthernet adapter
New-NetIPAddress -IPAddress 172.16.10.1 -PrefixLength 24 -InterfaceAlias "vEthernet (mavlab)"
New-NetNat -Name "MavLabNAT" -InternalIPInterfaceAddressPrefix "172.16.10.0/24"
Get-NetNat
```

## Windows routing and DNS

```powershell
New-NetRoute -InterfaceAlias "Ethernet" -DestinationPrefix "0.0.0.0/0" -NextHop "172.16.10.1"
Get-DnsServerForwarder
Remove-DnsServerForwarder -IPAddress <old> -Force
Add-DnsServerForwarder -IPAddress 1.1.1.1 -PassThru
Get-NetFirewallProfile | Select-Object Name, Enabled
```

A forwarder pointing at an address the server can't reach breaks external resolution for every client that uses the server.

## Same subnet but no traffic

Check in this order: virtual switch membership, ARP (`ip neigh`, `Get-NetNeighbor`), routes (`ip route get <ip>`), the host firewall, then whether the service is listening.

## Azure

- NSG default rules deny inbound internet traffic. Explicit rules make the allowed path visible in code.
- Allow RDP or SSH only from the Bastion subnet, not `*`.
- Leave unused address space in the VNet. `10.0.0.0/24` was reserved, later used for Bastion.
- VNets, subnets, and NICs are bound to one region.
