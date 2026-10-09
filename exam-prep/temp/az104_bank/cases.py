"""Shared case studies (original, fictitious organizations)."""
from qlib import scenario

CONTOSO = scenario("contoso", "Contoso, Ltd.", """
<p><strong>Overview.</strong> Contoso, Ltd. is a manufacturing company with offices in Seattle and Amsterdam. It is consolidating its on-premises workloads into Azure. All Azure resources are in a single Microsoft Entra tenant named contoso.com.</p>
<p><strong>Existing environment.</strong></p>
<table>
<tr><th>Item</th><th>Configuration</th></tr>
<tr><td>Management groups</td><td>Tenant Root Group › MG-Contoso › MG-Prod and MG-Dev</td></tr>
<tr><td>Subscriptions</td><td>Sub-Prod (in MG-Prod), Sub-Dev (in MG-Dev)</td></tr>
<tr><td>VNet-Sea</td><td>East US, address space 10.10.0.0/16, subnets Web (10.10.1.0/24), App (10.10.2.0/24), in Sub-Prod</td></tr>
<tr><td>VNet-Ams</td><td>West Europe, address space 10.20.0.0/16, subnet Ops (10.20.1.0/24), in Sub-Prod</td></tr>
<tr><td>contosodata01</td><td>StorageV2 account, East US, GRS, public network access enabled from all networks</td></tr>
<tr><td>Group: Eng-Ops</td><td>Security group, assigned membership, 40 members</td></tr>
</table>
<p><strong>Requirements.</strong></p>
<ul>
<li>Production resources may be deployed only to East US and West Europe. Development resources are not restricted.</li>
<li>VMs in VNet-Ams must reach VMs in VNet-Sea by using private IP addresses across the Microsoft backbone.</li>
<li>contosodata01 must accept connections only from the App subnet of VNet-Sea and from the Seattle office public IP range 203.0.113.0/27.</li>
<li>Members of Eng-Ops must be able to restart and resize every VM in Sub-Prod, but must not be able to delete VMs or change networking.</li>
<li>Administrative effort and the number of assignments must be minimized.</li>
</ul>""")

LITWARE = scenario("litware", "Litware, Inc.", """
<p><strong>Overview.</strong> Litware, Inc. runs an online ordering platform. The platform is hosted in the East US Azure region in a subscription named Sub-Orders.</p>
<p><strong>Existing environment.</strong></p>
<table>
<tr><th>Resource</th><th>Configuration</th></tr>
<tr><td>plan-orders</td><td>App Service plan, Standard S1, 2 instances, Windows</td></tr>
<tr><td>app-orders</td><td>Web app hosted on plan-orders; one deployment slot named staging</td></tr>
<tr><td>vmss-worker</td><td>Virtual Machine Scale Set, Flexible orchestration, 3 instances, Ubuntu</td></tr>
<tr><td>vm-sql1</td><td>Windows Server VM running SQL Server, Premium SSD managed disks, no backup configured</td></tr>
<tr><td>law-litware</td><td>Log Analytics workspace, East US</td></tr>
</table>
<p><strong>Requirements.</strong></p>
<ul>
<li>app-orders must scale out automatically during sales events to as many as 15 instances.</li>
<li>Code changes must be validated in staging and promoted to production with no downtime; the staging slot's database connection string must never move to production.</li>
<li>vm-sql1 must be backed up every four hours, and recovery points must be retained for 30 days.</li>
<li>If East US becomes unavailable, vm-sql1 must be recoverable in West US with a recovery point objective (RPO) measured in minutes.</li>
<li>The operations team must receive an SMS and an email when average CPU of vmss-worker exceeds 80% for 10 minutes, except during the Sunday 02:00–04:00 maintenance window.</li>
</ul>""")
