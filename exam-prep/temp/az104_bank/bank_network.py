"""Domain 4 - Implement and manage virtual networking (15-20%)."""
from qlib import mc, multi, hot, yn, dd, code
import cases  # noqa: F401

N = "Configure and manage virtual networks in Azure"
S = "Configure secure access to virtual networks"
D = "Configure name resolution and load balancing"

L = "https://learn.microsoft.com/en-us/azure/"
PEER = L + "virtual-network/virtual-network-peering-overview"
PEER_PS = L + "virtual-network/tutorial-connect-virtual-networks-powershell"
PEER_ADDR = L + "virtual-network/update-virtual-network-peering-address-space"
VNET_FAQ = L + "virtual-network/virtual-networks-faq"
TRANSIT = L + "vpn-gateway/vpn-gateway-peering-gateway-transit"
HUBSPOKE = L + "architecture/networking/architecture/hub-spoke"
PIP = L + "virtual-network/ip-services/public-ip-addresses"
PIP_PREFIX = L + "virtual-network/ip-services/public-ip-address-prefix"
UDR = L + "virtual-network/virtual-networks-udr-overview"
UDR_TUT = L + "virtual-network/tutorial-create-route-table"
NEXTHOP = L + "network-watcher/next-hop-overview"
CONN_TS = L + "network-watcher/connection-troubleshoot-overview"
DEFAULT_OUT = L + "virtual-network/ip-services/default-outbound-access"
NAT = L + "nat-gateway/nat-overview"
NSG = L + "virtual-network/network-security-groups-overview"
NSG_WORKS = L + "virtual-network/network-security-group-how-it-works"
ASG = L + "virtual-network/application-security-groups"
BAS_CFG = L + "bastion/configuration-settings"
BAS_SKU = L + "bastion/bastion-sku-comparison"
BAS_NATIVE = L + "bastion/native-client"
BAS_PEER = L + "bastion/vnet-peering"
BAS_REC = L + "bastion/session-recording"
SE = L + "virtual-network/virtual-network-service-endpoints-overview"
PE = L + "private-link/private-endpoint-overview"
PE_DNS = L + "private-link/private-endpoint-dns"
DNS_DELEG = L + "dns/dns-delegate-domain-azure-dns"
DNS_AUTOREG = L + "dns/private-dns-autoregistration"
DNS_ALIAS = L + "dns/dns-alias"
PDNS = L + "dns/private-dns-overview"
LB = L + "load-balancer/load-balancer-overview"
LB_COMP = L + "load-balancer/components"
LB_DIST = L + "load-balancer/distribution-mode-concepts"
LB_NAT = L + "load-balancer/inbound-nat-rules"
LB_PROBE = L + "load-balancer/load-balancer-custom-probe-overview"
LB_TS = "https://learn.microsoft.com/en-us/troubleshoot/azure/load-balancer/troubleshoot-common-problems/load-balancer-troubleshoot"
LB_HA = L + "load-balancer/load-balancer-ha-ports-overview"
LB_OUT = L + "load-balancer/outbound-rules"
LB_CHOICE = L + "architecture/guide/technology-choices/load-balancing-overview"
APPGW = L + "application-gateway/overview"

ITEMS = [
# ------------------------------------------------------------------ VNets
mc("NW", N, "<p>Refer to the case study.</p><p>You need to meet the connectivity requirement between VNet-Ams and VNet-Sea.</p><p>What should you configure?</p>",
   "Global virtual network peering, created in both directions between VNet-Ams and VNet-Sea",
   "<strong>Global VNet peering</strong> connects VNets in different regions over the Microsoft backbone with private IPs. The address spaces (10.20.0.0/16 and 10.10.0.0/16) don't overlap, so peering is possible. A peering link must exist on each VNet before the state becomes <em>Connected</em>.",
   [("A site-to-site VPN between the two VNets over the internet", "this crosses the internet through VPN gateways and adds cost and latency."),
    ("Service endpoints on the Ops subnet for Microsoft.Network", "service endpoints secure PaaS access, not VNet-to-VNet traffic."),
    ("Global peering created only from VNet-Ams to VNet-Sea", "a one-sided peering stays in the Initiated state, and no traffic flows.")],
   [PEER], 94, case="contoso"),

mc("NW", N,
   "<p>You create subnet <em>snet-mgmt</em> with the prefix 10.0.5.0/28 in an Azure virtual network.</p><p>How many IP addresses are available for VMs in the subnet?</p>",
   "11",
   "A /28 has 16 addresses. Azure <strong>reserves 5</strong> in every subnet: the network address, the default gateway (.1), two for Azure DNS mapping (.2 and .3), and the broadcast address. That leaves 11.",
   [("16", "ignores the reserved addresses."),
    ("14", "subtracts only the network and broadcast addresses, as on traditional networks."),
    ("13", "Azure reserves five addresses, not three.")],
   [VNET_FAQ], 96),

mc("NW", N,
   "<p>In a hub-spoke design, Spoke1 and Spoke2 are each peered with the Hub VNet. VMs in Spoke1 can't reach VMs in Spoke2.</p><p>What should you do so that Spoke1 can reach Spoke2 without traffic inspection?</p>",
   "Create a direct peering between Spoke1 and Spoke2",
   "VNet peering <strong>isn't transitive</strong>. Spoke-to-spoke traffic needs either a direct peering or routing through an NVA or Azure Firewall in the hub (UDRs plus forwarding). With no inspection required, direct peering is simplest.",
   [("Enable Allow gateway transit on the hub peerings", "gateway transit shares a VPN or ExpressRoute gateway; it doesn't make peering transitive."),
    ("Enable Allow forwarded traffic on the hub peerings only", "forwarded traffic still needs something in the hub to forward it."),
    ("Add a service endpoint for Microsoft.Network on both spokes", "service endpoints aren't for VNet-to-VNet routing.")],
   [PEER, HUBSPOKE], 93),

mc("NW", N,
   "<p>You try to peer VNet-A (10.1.0.0/16) with VNet-B (10.1.128.0/17). The peering creation fails.</p><p>What is the cause?</p>",
   "The address spaces overlap",
   "Peered VNets <strong>can't have overlapping address spaces</strong>. 10.1.128.0/17 is inside 10.1.0.0/16. Re-address one VNet before peering.",
   [("The VNets are in different resource groups", "peering works across resource groups, subscriptions and even tenants."),
    ("The VNets use different subnet sizes", "subnet size doesn't matter."),
    ("Peering requires a VPN gateway in each VNet", "peering doesn't need gateways.")],
   [PEER], 96),

mc("NW", N,
   "<p>The Hub VNet has a VPN gateway connected to the on-premises network. Spoke VNet-App is peered with the Hub. VMs in VNet-App must reach on-premises through the hub's gateway.</p><p>How should you configure the peerings?</p>",
   "On the hub-to-spoke peering, enable Allow gateway transit; on the spoke-to-hub peering, enable Use remote gateways",
   "<strong>Gateway transit</strong> lets a peered VNet use another VNet's VPN or ExpressRoute gateway. The hub side allows it, and the spoke side uses it. The spoke must not have its own gateway.",
   [("Enable Use remote gateways on both peerings", "the hub must allow transit; it doesn't use remote gateways itself."),
    ("Deploy a second VPN gateway in VNet-App", "this duplicates cost, and a spoke with its own gateway can't use remote gateways."),
    ("Add a UDR in VNet-App with next hop Internet for the on-premises prefix", "that would send traffic to the internet, not the gateway.")],
   [TRANSIT, PEER], 93),

mc("NW", N,
   "<p>VNet-Core (10.0.0.0/16) is peered with three other VNets. You need to add the address space 10.5.0.0/16 to VNet-Core without deleting the peerings.</p><p>What should you do after adding the address space?</p>",
   "Sync the peering on each peered VNet so that the remote VNets learn the new address space",
   "Address space can be added to a peered VNet. Afterward, each peering shows that it needs to be <strong>synced</strong>. Running sync (for example, <code>Sync-AzVirtualNetworkPeering</code> or the portal's Sync) updates the remote VNets.",
   [("Delete and recreate all peerings", "this was required in the past but is no longer necessary."),
    ("Restart all VMs in the peered VNets", "routing updates don't require VM restarts."),
    ("Nothing, because peerings update automatically", "remote VNets must be synced to learn the change.")],
   [PEER_ADDR], 82, conf_note="The sync workflow is relatively recent. Older guidance required deleting and recreating peerings."),

mc("NW", N,
   "<p>VM1 has a Standard SKU public IP address and runs a web server on TCP 443. VM1's NIC and subnet have no network security group. Internet clients can't connect.</p><p>What should you do?</p>",
   "Associate an NSG with an inbound rule that allows TCP 443 with the NIC or subnet",
   "Standard SKU public IPs are <strong>secure by default</strong>: inbound traffic is denied unless an NSG explicitly allows it.",
   [("Change the public IP to dynamic allocation", "Standard public IPs are always static, and allocation doesn't affect filtering."),
    ("Downgrade the public IP to the Basic SKU", "Basic public IPs were retired on September 30, 2025, and this isn't the right fix."),
    ("Enable IP forwarding on the NIC", "IP forwarding is for routing appliances.")],
   [PIP], 92),

mc("NW", N,
   "<p>A partner will allow-list your outbound IP addresses. You plan to add up to 16 VMs with public IPs over time, and the partner wants a single contiguous range that won't change.</p><p>What should you create?</p>",
   "A public IP address prefix of /28 and allocate the VMs' public IPs from it",
   "A <strong>public IP prefix</strong> reserves a contiguous, static block of public IPs (a /28 has 16). Addresses created from it come from that known range, so the partner can allow-list one prefix.",
   [("16 individual Standard public IPs", "addresses won't be contiguous, and the partner would need 16 entries."),
    ("A NAT gateway with one public IP", "gives one outbound IP, which conflicts with the per-VM public IP plan."),
    ("A Basic SKU dynamic public IP for each VM", "Basic is retired, and dynamic IPs can change.")],
   [PIP_PREFIX], 88),

mc("NW", N,
   "<p>All internet-bound traffic from subnet <em>snet-app</em> must pass through a firewall NVA at 10.0.0.4 in subnet <em>snet-fw</em>. You create route table <em>rt-app</em>.</p><p>Which configuration completes the solution?</p>",
   "Add a route 0.0.0.0/0 with next hop type Virtual appliance and address 10.0.0.4, associate rt-app with snet-app, and enable IP forwarding on the NVA's NIC",
   "A <strong>user-defined route</strong> overrides the system default route, the route table must be <strong>associated with the source subnet</strong>, and the NVA's NIC needs <strong>IP forwarding</strong> to forward traffic not addressed to itself.",
   [("Add a route 0.0.0.0/0 with next hop type Internet and associate rt-app with snet-fw", "next hop Internet bypasses the NVA, and the table is on the wrong subnet."),
    ("Add a route 0.0.0.0/0 with next hop type Virtual network gateway and associate rt-app with snet-app", "sends traffic to a VPN gateway, not the NVA."),
    ("Add a route 10.0.0.4/32 with next hop type Virtual appliance and associate rt-app with snet-app", "this only routes traffic destined to the NVA itself.")],
   [UDR, UDR_TUT], 93),

hot("NW", N,
   "<p>Subnet <em>snet-web</em> has this effective route table:</p>"
   + code("""Source   Address prefix   Next hop type        Next hop IP
Default  10.0.0.0/16      Virtual network      -
User     10.0.2.0/24      Virtual appliance    10.0.9.4
User     10.0.2.128/25    None                 -
Default  0.0.0.0/0        Internet             -
User     0.0.0.0/0        Virtual appliance    10.0.9.4""")
   + "<p>For each destination, select the next hop that is used.</p>",
   [("10.0.1.10", ["Virtual network", "Virtual appliance 10.0.9.4", "None (dropped)", "Internet"], "Virtual network", "Only 10.0.0.0/16 matches, so it uses the system Virtual network route."),
    ("10.0.2.20", ["Virtual network", "Virtual appliance 10.0.9.4", "None (dropped)", "Internet"], "Virtual appliance 10.0.9.4", "10.0.2.0/24 is the longest match."),
    ("10.0.2.200", ["Virtual network", "Virtual appliance 10.0.9.4", "None (dropped)", "Internet"], "None (dropped)", "10.0.2.128/25 is longer than /24, and next hop None drops the packet."),
    ("8.8.8.8", ["Virtual network", "Virtual appliance 10.0.9.4", "None (dropped)", "Internet"], "Virtual appliance 10.0.9.4", "Both 0.0.0.0/0 routes match. For equal prefixes, a user route overrides the system route.")],
   "Azure picks the route with the <strong>longest prefix match</strong>. When prefixes tie, user-defined routes win over BGP routes, which win over system routes.",
   [UDR], 94),

mc("NW", N,
   "<p>VM1 in snet-a can't reach VM2 at 10.2.1.5 in a peered VNet. You suspect a route table is sending traffic somewhere unexpected.</p><p>Which tool shows the next hop type and the route table used for traffic from VM1 to 10.2.1.5?</p>",
   "Network Watcher Next hop",
   "<strong>Next hop</strong> returns the next hop type, IP address and route table ID for a packet from a VM to a destination, which reveals UDR or peering routing problems.",
   [("Network Watcher IP flow verify", "reports whether NSG rules allow or deny a flow, not routing."),
    ("Azure Advisor", "gives best-practice recommendations, not per-flow routing."),
    ("Activity log", "shows management operations, not packet routing.")],
   [NEXTHOP], 93),

mc("NW", N,
   "<p>You create a new virtual network in May 2026 by using the latest API version and deploy a VM with no public IP. The VM can't reach public endpoints such as Windows Update. No NSG blocks outbound traffic.</p><p>What should you do to provide predictable outbound internet access for the subnet?</p>",
   "Associate a NAT gateway with a public IP address with the subnet",
   "For API versions released after March 31, 2026, subnets in new VNets are <strong>private by default</strong> (<code>defaultOutboundAccess = false</code>), so VMs need an <strong>explicit outbound method</strong>. A NAT gateway is the recommended choice for subnet-wide, predictable egress.",
   [("Enable IP forwarding on the VM's NIC", "IP forwarding doesn't create internet egress."),
    ("Add a route 0.0.0.0/0 with next hop type None", "next hop None drops traffic."),
    ("Create a private endpoint for the internet", "private endpoints connect to specific Private Link services, not the internet.")],
   [DEFAULT_OUT, NAT], 85, conf_note="Behavior depends on the API version used to create the VNet; existing VNets keep default outbound access."),

dd("NW", N,
   "<p>You need to peer VNet1 and VNet2 (same subscription) by using Azure PowerShell and confirm that the peering works.</p><p>Which four actions should you perform in sequence?</p>",
   [("Get both VNet objects with Get-AzVirtualNetwork", "the peering cmdlets need the VNet objects or IDs."),
    ("Run Add-AzVirtualNetworkPeering on VNet1 with RemoteVirtualNetworkId set to VNet2's ID", "creates the VNet1-to-VNet2 link (state Initiated)."),
    ("Run Add-AzVirtualNetworkPeering on VNet2 with RemoteVirtualNetworkId set to VNet1's ID", "creates the reverse link, and both become Connected."),
    ("Check that PeeringState is Connected with Get-AzVirtualNetworkPeering", "confirms the peering before you test traffic.")],
   [("Run New-AzVirtualNetworkGateway in both VNets", "gateways aren't needed for peering."),
    ("Run Set-AzVirtualNetworkSubnetConfig to add a service endpoint", "service endpoints aren't part of peering.")],
   "Peering is two links, one on each VNet. Until both exist, the state is Initiated and no traffic flows.",
   [PEER_PS, PEER], 92),

# ------------------------------------------------------------------ secure access
mc("NW", S,
   "<p>An NSG associated with snet-admin has these inbound rules:</p>"
   + code("""Priority  Name            Port  Source          Action
100       Deny-RDP-All    3389  Internet        Deny
200       Allow-RDP-Admin 3389  203.0.113.5/32  Allow""")
   + "<p>An administrator at 203.0.113.5 can't RDP to a VM in the subnet. What should you do?</p>",
   "Change the priority of Allow-RDP-Admin to a number lower than 100",
   "NSG rules are processed in <strong>priority order, lowest number first</strong>, and processing stops at the first match. The admin's traffic matches rule 100 (source Internet) and is denied before rule 200 is evaluated.",
   [("Change the priority of Deny-RDP-All to 50", "this makes the deny rule match even earlier."),
    ("Add an outbound rule allowing 3389 to 203.0.113.5", "NSGs are stateful, and the inbound deny is the problem."),
    ("Change Allow-RDP-Admin's source to VirtualNetwork", "the admin connects from the internet, so this wouldn't match.")],
   [NSG, NSG_WORKS], 96),

yn("NW", S,
   "<p>VM1's NIC is associated with NSG-NIC and its subnet is associated with NSG-Subnet. NSG-Subnet allows inbound TCP 80 from the internet. NSG-NIC has only the default rules. Evaluate each statement.</p>",
   [("Inbound HTTP traffic from the internet reaches VM1.", "No", "Inbound traffic is evaluated by the subnet NSG and then the NIC NSG. NSG-NIC's default DenyAllInBound blocks it."),
    ("Outbound traffic from VM1 is evaluated by NSG-NIC first, then by NSG-Subnet.", "Yes", "Outbound order is NIC first, then subnet."),
    ("Return traffic for an allowed outbound connection needs an inbound allow rule.", "No", "NSGs are stateful; return traffic for allowed flows is permitted automatically.")],
   "When NSGs exist at both levels, traffic must be allowed by <strong>both</strong>. Use the Effective security rules view to see the combined result.",
   [NSG_WORKS], 95),

mc("NW", S,
   "<p>Web servers and database servers are in the same subnet, and their IP addresses change often. Only the web servers may connect to the database servers on TCP 1433. You want to avoid maintaining IP lists.</p><p>What should you use in the NSG rule?</p>",
   "Application security groups as the source and destination",
   "<strong>Application security groups</strong> let you group VM NICs by role (asg-web, asg-db) and write rules such as <em>asg-web → asg-db : 1433 Allow</em>. IP changes don't require rule updates. All NICs in an ASG must be in the same VNet.",
   [("Service tags such as VirtualNetwork", "VirtualNetwork includes every address in the VNet, which is too broad."),
    ("Separate route tables for web and database VMs", "routes direct traffic and don't filter it."),
    ("A private endpoint for each database VM", "private endpoints are for PaaS and Private Link services, not VM-to-VM filtering.")],
   [ASG], 95),

mc("NW", S,
   "<p>VMs in subnets snet-a and snet-b of the same VNet can communicate even though you created no NSG rules allowing it. Both subnets have NSGs with only default rules.</p><p>Which default rule allows the traffic?</p>",
   "AllowVnetInBound (priority 65000)",
   "Every NSG includes <strong>AllowVnetInBound</strong>, which allows traffic from the VirtualNetwork service tag. That tag covers the VNet, peered VNets and connected on-premises ranges. Add a higher-priority deny rule to block it.",
   [("AllowAzureLoadBalancerInBound (priority 65001)", "allows traffic from the Azure Load Balancer, including health probes."),
    ("DenyAllInBound (priority 65500)", "denies traffic and is evaluated last."),
    ("AllowInternetOutBound (priority 65001)", "an outbound rule for internet traffic.")],
   [NSG], 95),

mc("NW", S,
   "<p>You're deploying Azure Bastion (Standard SKU) into VNet-Hub.</p><p>Which subnet configuration is required?</p>",
   "A subnet named AzureBastionSubnet with a prefix of /26 or larger",
   "Dedicated Bastion deployments need a subnet named exactly <strong>AzureBastionSubnet</strong> of at least <strong>/26</strong>, which allows host scaling.",
   [("A subnet named BastionSubnet with a prefix of /29", "the name must be exact, and /29 is too small."),
    ("A subnet named AzureBastionSubnet with a prefix of /28", "dedicated SKUs require /26 or larger."),
    ("A subnet named GatewaySubnet with a prefix of /27", "GatewaySubnet is for VPN and ExpressRoute gateways.")],
   [BAS_CFG], 95),

mc("NW", S,
   "<p>Administrators want to connect to Azure VMs through Azure Bastion by using the native SSH and RDP clients on their workstations (for example, <code>az network bastion ssh</code>) instead of the browser. You must use the lowest-cost SKU that supports this.</p><p>Which SKU should you deploy?</p>",
   "Standard",
   "<strong>Native client support</strong> requires the <strong>Standard</strong> or Premium SKU. Standard is the cheaper of the two.",
   [("Developer", "browser-only, one VM at a time, and no native client support."),
    ("Basic", "browser-based connections only."),
    ("Basic with host scaling enabled", "host scaling isn't available on Basic, and it wouldn't add native client support.")],
   [BAS_NATIVE, BAS_SKU], 93),

mc("NW", S,
   "<p>Contoso has a hub VNet and four spoke VNets peered to it. Administrators must use Azure Bastion to reach VMs in every spoke while you minimize the number of Bastion deployments.</p><p>What should you do?</p>",
   "Deploy one Bastion host (Basic SKU or higher) in the hub VNet",
   "Basic, Standard and Premium Bastion support <strong>connections to VMs in peered VNets</strong>, so a single host in the hub can serve all spokes. The Developer SKU doesn't support peering.",
   [("Deploy the Developer SKU in the hub VNet", "Developer doesn't support peered VNets."),
    ("Deploy a Bastion host in each spoke", "this works but doesn't minimize deployments."),
    ("Deploy Bastion in one spoke and enable gateway transit", "gateway transit applies to VPN and ExpressRoute gateways, not Bastion.")],
   [BAS_PEER, BAS_SKU], 92),

mc("NW", S,
   "<p>Compliance requires that every Bastion session to production VMs is recorded for audit.</p><p>Which Azure Bastion SKU supports this?</p>",
   "Premium",
   "<strong>Session recording</strong> is available only in the <strong>Premium</strong> SKU, which also offers private-only deployment.",
   [("Standard", "lacks session recording."),
    ("Basic", "lacks session recording."),
    ("Developer", "lacks session recording.")],
   [BAS_REC, BAS_SKU], 94),

mc("NW", S,
   "<p>Applications on-premises reach Azure over a site-to-site VPN. They must access storage account <em>stfinance</em> by using a <strong>private IP address</strong> in your VNet, and the account's public endpoint must be disabled.</p><p>What should you implement?</p>",
   "A private endpoint for the blob service of stfinance",
   "A <strong>private endpoint</strong> gives the storage service a NIC with a private IP in your VNet, reachable from peered and on-premises networks. Public network access can then be disabled.",
   [("A service endpoint for Microsoft.Storage on the gateway subnet", "service endpoints keep the public endpoint, aren't usable from on-premises, and aren't supported on GatewaySubnet."),
    ("A storage firewall IP rule for the on-premises public IP", "traffic would still use the public endpoint."),
    ("VNet peering between the VNet and the storage account", "PaaS services can't be peered.")],
   [PE, SE], 94),

mc("NW", S,
   "<p>You enable the Microsoft.Storage service endpoint on subnet <em>snet-app</em>.</p><p>Which statement describes the effect?</p>",
   "Traffic from snet-app to Azure Storage uses the Azure backbone with the subnet's identity, so the storage firewall can allow the subnet; the storage account keeps its public IP",
   "<strong>Service endpoints</strong> extend the VNet's identity to the service. Traffic stays on the backbone and appears with private source IPs, so storage firewalls can use virtual network rules. The service is still reached at its public endpoint.",
   [("The storage account gets a private IP address in snet-app", "that's what a private endpoint does."),
    ("All storage accounts block traffic from snet-app until they're added to a firewall rule", "accounts without network rules still accept the traffic."),
    ("On-premises clients can now reach storage through the VPN", "service endpoints don't extend to on-premises.")],
   [SE], 92),

dd("NW", S,
   "<p>You need VMs in VNet1 to access blob storage account <em>stdocs</em> privately by name (stdocs.blob.core.windows.net), and to block all public access to the account.</p><p>Which three actions should you perform in sequence?</p>",
   [("Create a private endpoint for stdocs (sub-resource blob) in a subnet of VNet1", "provides a private IP for the blob service."),
    ("Integrate the endpoint with the private DNS zone privatelink.blob.core.windows.net linked to VNet1", "makes the public FQDN resolve to the private IP inside VNet1."),
    ("Set Public network access on stdocs to Disabled", "blocks traffic to the public endpoint after private access works.")],
   [("Enable the Microsoft.Storage service endpoint on the subnet", "not required when you use a private endpoint."),
    ("Create an A record for stdocs in a public DNS zone", "public DNS would expose a private IP, and the CNAME chain uses the privatelink zone.")],
   "Private endpoints need DNS that resolves the service's normal FQDN to the endpoint's private IP. The privatelink private DNS zone does this automatically.",
   [PE_DNS, PE], 93),

mc("NW", S,
   "<p>You created a private endpoint for a Key Vault in VNet1. From a VM in VNet1, <code>nslookup kv-app.vault.azure.net</code> still returns a public IP address.</p><p>What is the most likely cause?</p>",
   "The private DNS zone privatelink.vaultcore.azure.net isn't linked to VNet1, or it doesn't contain the endpoint's record",
   "Resolution through the privatelink CNAME needs the matching <strong>private DNS zone</strong> linked to the VNet (or equivalent custom DNS forwarding). Without it, clients resolve the public address.",
   [("The VM needs a public IP address", "public IPs aren't involved in private name resolution."),
    ("The Key Vault firewall must allow the VM's private IP", "the firewall doesn't affect DNS answers."),
    ("Private endpoints can be resolved only from on-premises", "they're resolvable inside the VNet when DNS is configured.")],
   [PE_DNS], 92),

yn("NW", S, "<p>Evaluate each statement about network security groups.</p>",
   [("One NSG can be associated with multiple subnets.", "Yes", "An NSG can be associated with many subnets and NICs, as long as they're in the same region."),
    ("An NSG must be in the same region as the VNet whose subnet it's associated with.", "Yes", "NSGs are regional resources."),
    ("You must create an outbound rule to allow response traffic for inbound connections that an NSG allows.", "No", "NSGs are stateful.")],
   "Associations are flexible within a region, and stateful rule processing means you only write rules for the initiating direction.",
   [NSG], 94),

# ------------------------------------------------------------------ DNS & load balancing
mc("NW", D,
   "<p>You bought the domain <em>fabrikamshop.com</em> from a third-party registrar and created a public DNS zone with the same name in Azure DNS. Records in the zone don't resolve on the internet.</p><p>What should you do?</p>",
   "At the registrar, set the domain's name servers to the four Azure DNS name servers listed for the zone",
   "<strong>Delegation</strong> happens at the parent zone through the registrar. The domain's NS records must point to the Azure DNS name servers assigned to your zone.",
   [("Create a CNAME record at the zone apex pointing to azure-dns.com", "CNAME records aren't allowed at the apex, and that doesn't delegate."),
    ("Link the zone to a virtual network", "VNet links apply to private DNS zones."),
    ("Add an SOA record for the registrar in Azure DNS", "the SOA is managed by Azure DNS and doesn't control delegation.")],
   [DNS_DELEG], 95),

mc("NW", D,
   "<p>VMs in VNet-App must be resolvable by host name (for example, vm-app1.corp.contoso.internal), and the DNS records must be created and removed automatically as VMs come and go.</p><p>What should you configure?</p>",
   "A private DNS zone named corp.contoso.internal with a virtual network link to VNet-App that has auto-registration enabled",
   "<strong>Auto-registration</strong> on a private DNS zone's VNet link automatically creates A records for VMs in the linked VNet and removes them when the VMs are deleted.",
   [("A public DNS zone with A records for each VM", "the records would be public and manual."),
    ("A private DNS zone linked to VNet-App without auto-registration", "resolution works, but records must be created manually."),
    ("Custom DNS servers set on the VNet pointing to 168.63.129.16", "this is Azure-provided DNS, which doesn't use a custom zone name.")],
   [DNS_AUTOREG, PDNS], 93),

mc("NW", D,
   "<p>The apex domain <em>contoso.com</em> must route to an Azure Traffic Manager profile. Azure DNS hosts the zone.</p><p>Which record should you create at the apex?</p>",
   "An alias record set of type A that targets the Traffic Manager profile",
   "<strong>Alias records</strong> can point the zone apex at Azure resources such as Traffic Manager profiles, public IPs and Front Door, which a CNAME can't do at the apex. They also update automatically when the target changes.",
   [("A CNAME record at the apex pointing to contoso.trafficmanager.net", "CNAME isn't allowed at the apex."),
    ("An A record with the Traffic Manager profile's IP address", "Traffic Manager is DNS-based and has no single IP."),
    ("An NS record delegating the apex to Traffic Manager", "Traffic Manager isn't a DNS hosting service for delegation.")],
   [DNS_ALIAS], 92),

mc("NW", D,
   "<p>A three-tier app has web VMs and app VMs in the same VNet. The web tier must distribute TCP 8080 traffic across the app VMs by using a private IP address that isn't reachable from the internet.</p><p>What should you deploy?</p>",
   "An internal Standard Load Balancer with a private frontend IP in the app subnet",
   "An <strong>internal load balancer</strong> has a private frontend IP and balances traffic inside the VNet or from connected networks, which is ideal between tiers.",
   [("A public Standard Load Balancer", "exposes a public frontend to the internet."),
    ("Azure Traffic Manager", "works by DNS for public endpoints and doesn't balance private traffic inside a VNet."),
    ("A NAT gateway", "provides outbound SNAT, not inbound load balancing.")],
   [LB, LB_COMP], 95),

mc("NW", D,
   "<p>A legacy app behind an Azure Load Balancer stores session state in memory, so each client must keep reaching the same backend VM for the duration of its session.</p><p>What should you configure on the load-balancing rule?</p>",
   "Session persistence set to Client IP",
   "<strong>Session persistence</strong> (source IP affinity) uses a 2-tuple (Client IP) or 3-tuple (Client IP and protocol) hash so that a client keeps reaching the same backend.",
   [("Session persistence set to None", "the default 5-tuple hash can send new connections from a client to different backends."),
    ("Floating IP (direct server return)", "used for specific scenarios such as SQL Always On listeners, not affinity."),
    ("An idle timeout of 30 minutes", "keeps idle connections open but doesn't pin new connections.")],
   [LB_DIST], 93),

mc("NW", D,
   "<p>Administrators must RDP to VM2, which sits behind public Standard Load Balancer <em>lb-web</em>, by connecting to lb-web's public IP on TCP 50002. VM2 has no public IP.</p><p>What should you create on lb-web?</p>",
   "An inbound NAT rule mapping frontend port 50002 to VM2 on port 3389",
   "<strong>Inbound NAT rules</strong> forward traffic arriving on a specific frontend IP and port to a specific backend instance and port. Allow 3389 on VM2's NSG too. Bastion is usually the more secure option.",
   [("A load-balancing rule for port 50002 to the whole backend pool", "this distributes RDP across all VMs instead of reaching VM2."),
    ("An outbound rule for port 3389", "outbound rules configure SNAT for outbound traffic."),
    ("A health probe on port 50002", "probes check health and don't forward traffic.")],
   [LB_NAT], 93),

mc("NW", D,
   "<p>Behind a public Standard Load Balancer, all backend VMs show as unhealthy, so no traffic is delivered. The website runs on port 8080 in IIS, and the health probe is configured as TCP 80. NSGs allow the AzureLoadBalancer service tag.</p><p>What should you do?</p>",
   "Change the health probe to TCP (or HTTP) port 8080",
   "The <strong>health probe</strong> must target a port where the application answers. A probe on 80 against a service listening on 8080 fails, so every backend is marked down. Probe traffic comes from 168.63.129.16, which the default NSG rule AllowAzureLoadBalancerInBound permits.",
   [("Add an NSG rule that allows the Internet service tag on port 80", "the probe source is the AzureLoadBalancer tag, which is already allowed, and the port is wrong anyway."),
    ("Enable session persistence", "affinity doesn't affect health."),
    ("Move the VMs to a Basic Load Balancer", "Basic Load Balancer is retired, and the issue is the probe configuration.")],
   [LB_PROBE, LB_TS], 93),

mc("NW", D,
   "<p>Two firewall NVAs in a hub VNet must receive all TCP and UDP flows on all ports from spoke VNets, with high availability.</p><p>Which load balancer configuration should you use?</p>",
   "An internal Standard Load Balancer with an HA ports load-balancing rule",
   "<strong>HA ports</strong> rules (protocol All, port 0) on an internal Standard Load Balancer balance every flow on every port. That's the standard pattern for NVA high availability.",
   [("A public Standard Load Balancer with one rule per port", "managing a rule per port is impractical, and the frontend should be internal."),
    ("Azure Application Gateway with multi-site listeners", "it's layer 7 HTTP(S) only."),
    ("Traffic Manager with priority routing", "DNS-based routing doesn't forward packets to NVAs.")],
   [LB_HA], 92),

mc("NW", D,
   "<p>VMs without public IPs are in the backend pool of an <strong>internal</strong> Standard Load Balancer. In a new private-by-default subnet, they can't reach the internet for OS updates.</p><p>What should you do?</p>",
   "Associate a NAT gateway with the backend subnet",
   "An internal Standard Load Balancer gives backends <strong>no outbound internet access</strong>. A <strong>NAT gateway</strong> on the subnet provides explicit, scalable outbound SNAT and takes precedence over other outbound methods.",
   [("Add an outbound rule to the internal load balancer", "outbound rules need a public frontend IP, so they don't apply to an internal-only load balancer."),
    ("Add an inbound NAT rule for port 443", "inbound NAT rules forward inbound traffic."),
    ("Increase the load balancer's idle timeout", "timeouts don't create internet access.")],
   [NAT, LB_OUT, DEFAULT_OUT], 90),

mc("NW", D,
   "<p>A regional web app needs layer 7 load balancing with URL path-based routing (/images/* to one pool, /api/* to another) and a web application firewall.</p><p>Which service should you use?</p>",
   "Azure Application Gateway with WAF",
   "<strong>Application Gateway</strong> is a regional layer 7 load balancer with path-based and multi-site routing, TLS termination and an integrated WAF.",
   [("Azure Load Balancer", "works at layer 4 and can't route by URL path."),
    ("Azure Traffic Manager", "routes by DNS and never sees URL paths."),
    ("A NAT gateway", "handles outbound connectivity only.")],
   [APPGW, LB_CHOICE], 93),

mc("NW", D,
   "<p>Users report that a public website behind a Standard Load Balancer is intermittently unreachable. You want to see the health probe status per backend instance over time.</p><p>Where should you look?</p>",
   "The Health Probe Status metric (DipAvailability) of the load balancer in Azure Monitor, split by backend IP address",
   "Load Balancer exposes the <strong>Health Probe Status</strong> and <strong>Data Path Availability</strong> metrics. Splitting by backend IP shows which instances fail probes and when.",
   [("The Activity log of the load balancer", "records configuration changes, not data-plane health."),
    ("Microsoft Entra sign-in logs", "unrelated to load balancer health."),
    ("Azure Advisor reliability recommendations", "gives general advice, not per-instance probe history.")],
   [LB_TS, L + "load-balancer/load-balancer-standard-diagnostics"], 90),
]
