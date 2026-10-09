"""Domain 3 - Deploy and manage Azure compute resources (20-25%)."""
from qlib import mc, multi, hot, yn, dd, code
import cases  # noqa: F401

T = "Automate deployment of resources by using ARM templates or Bicep files"
V = "Create and configure virtual machines"
C = "Provision and manage containers in the Azure portal"
P = "Create and configure Azure App Service"

L = "https://learn.microsoft.com/en-us/azure/"
MODES = L + "azure-resource-manager/templates/deployment-modes"
SYNTAX = L + "azure-resource-manager/templates/syntax"
DECOMPILE = L + "azure-resource-manager/bicep/decompile"
EXPORT = L + "azure-resource-manager/templates/export-template-portal"
BICEP_PS = L + "azure-resource-manager/bicep/deploy-powershell"
BICEP_SUB = L + "azure-resource-manager/bicep/deploy-to-subscription"
KV_PARAM = L + "azure-resource-manager/templates/key-vault-parameter"
DEPENDS = L + "azure-resource-manager/templates/resource-dependency"
WHATIF = L + "azure-resource-manager/templates/deploy-what-if"
EXISTING = L + "azure-resource-manager/bicep/existing-resource"
LOOPS = L + "azure-resource-manager/bicep/loops"
BICEP_PARAMS = L + "azure-resource-manager/bicep/parameters"
BICEP_FILE = L + "azure-resource-manager/bicep/file"
EAH = L + "virtual-machines/disks-enable-host-based-encryption-portal"
DISK_ENC = L + "virtual-machines/disk-encryption-overview"
MOVER = L + "resource-mover/tutorial-move-region-virtual-machines"
VM_MOVE = L + "azure-resource-manager/management/move-limitations/virtual-machines-move-limitations"
RESIZE = L + "virtual-machines/sizes/resize-vm"
AVAIL = L + "virtual-machines/availability"
AVSET = L + "virtual-machines/availability-set-overview"
DISKS = L + "virtual-machines/disks-types"
SHARED = L + "virtual-machines/disks-shared"
EXPAND = L + "virtual-machines/windows/expand-disks"
SCALEIN = L + "virtual-machine-scale-sets/virtual-machine-scale-sets-scale-in-policy"
UPGRADE = L + "virtual-machine-scale-sets/virtual-machine-scale-sets-upgrade-policy"
ORCH = L + "virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes"
CSE = L + "virtual-machines/extensions/custom-script-windows"
VMSS_AUTO = L + "virtual-machine-scale-sets/virtual-machine-scale-sets-autoscale-overview"
ACR_SKU = L + "container-registry/container-registry-skus"
ACR_ROLES = L + "container-registry/container-registry-rbac-built-in-roles-overview"
ACR_AUTH = L + "container-registry/container-registry-authentication"
ACI_GROUPS = L + "container-instances/container-instances-container-groups"
ACI_RESTART = L + "container-instances/container-instances-restart-policy"
ACI_FILES = L + "container-instances/container-instances-volume-azure-files"
ACI_UPDATE = L + "container-instances/container-instances-update"
ACA_SCALE = L + "container-apps/scale-app"
ACA_REV = L + "container-apps/revisions"
ACA_COMPARE = L + "container-apps/compare-options"
PLANS = L + "app-service/overview-hosting-plans"
SLOTS = L + "app-service/deploy-staging-slots"
DOMAIN = L + "app-service/app-service-web-tutorial-custom-domain"
CERT = L + "app-service/configure-ssl-certificate"
BIND = L + "app-service/configure-ssl-bindings"
VNETINT = L + "app-service/overview-vnet-integration"
NETFEAT = L + "app-service/networking-features"
BACKUP = L + "app-service/manage-backup"
SCALEUP = L + "app-service/manage-scale-up"
AUTOSCALE = L + "azure-monitor/autoscale/autoscale-get-started"
IPRESTRICT = L + "app-service/app-service-ip-restrictions"
LIMITS = L + "azure-resource-manager/management/azure-subscription-service-limits"

ITEMS = [
# ------------------------------------------------------------------ ARM / Bicep
mc("CO", T,
   "<p>Resource group <em>RG-App</em> contains VM1, VNet1 and a storage account. You deploy a template that defines only VNet1 and the storage account, by running:</p>"
   + code("New-AzResourceGroupDeployment -ResourceGroupName RG-App -TemplateFile .\\infra.json -Mode Complete", "powershell")
   + "<p>What happens to VM1?</p>",
   "VM1 is deleted because it isn't defined in the template",
   "In <strong>Complete</strong> mode, Resource Manager deletes resources in the resource group that aren't in the template. (Resources blocked by locks or with specific provider behaviors may survive, but by default VM1 is removed.)",
   [("VM1 is left unchanged", "that's the behavior of Incremental mode, the default."),
    ("VM1 is stopped but not deleted", "deployment modes never just stop resources."),
    ("The deployment fails because VM1 isn't in the template", "Complete mode doesn't fail for this; it deletes.")],
   [MODES], 94),

mc("CO", T,
   "<p>You redeploy an ARM template to an existing resource group without specifying a deployment mode. The template changes the SKU of an existing storage account and doesn't mention a VM that exists in the group.</p><p>What is the result?</p>",
   "The storage account is updated and the VM is left unchanged",
   "The default mode is <strong>Incremental</strong>: resources in the template are created or updated to match it, and resources not in the template are left as they are.",
   [("The storage account is updated and the VM is deleted", "this would happen only in Complete mode."),
    ("The deployment is skipped because the storage account already exists", "templates are idempotent and update existing resources."),
    ("The storage account is deleted and recreated with the new SKU", "Resource Manager updates in place where the property allows it.")],
   [MODES], 95),

hot("CO", T,
   "<p>You review this Bicep file, which is deployed to resource group <em>RG1</em> in West Europe with no parameter values supplied.</p>"
   + code("""param location string = resourceGroup().location

@allowed([
  'Standard_LRS'
  'Standard_GRS'
])
param skuName string = 'Standard_LRS'
param count int = 2

resource st 'Microsoft.Storage/storageAccounts@2023-05-01' = [for i in range(0, count): {
  name: 'st${uniqueString(resourceGroup().id)}${i}'
  location: location
  sku: { name: skuName }
  kind: 'StorageV2'
}]

output names array = [for i in range(0, count): st[i].name]""", "bicep")
   + "<p>Select the correct answer for each row.</p>",
   [("Number of storage accounts created", ["2", "1", "0", "3"], "2", "<code>range(0, count)</code> with the default <code>count = 2</code> loops twice."),
    ("Region of the storage accounts", ["West Europe", "East US", "The subscription's default region"], "West Europe", "<code>location</code> defaults to <code>resourceGroup().location</code>."),
    ("Result if you pass skuName = 'Premium_LRS'", ["The deployment fails validation", "Premium_LRS accounts are created", "Standard_LRS is used instead"], "The deployment fails validation", "<code>@allowed</code> restricts the parameter to the listed values, so validation rejects Premium_LRS.")],
   "Interpreting Bicep means reading parameter defaults, decorators, loops and functions such as <code>uniqueString()</code>, which produces a deterministic hash for the resource group.",
   [LOOPS, BICEP_PARAMS], 93),

mc("CO", T,
   "<p>Your team has an existing ARM template, <em>main.json</em>, and wants to maintain it as Bicep from now on.</p><p>What should you run?</p>",
   "bicep decompile main.json",
   "<strong>Decompile</strong> converts ARM JSON to a best-effort Bicep file (<code>bicep decompile</code> or <code>az bicep decompile --file main.json</code>). You then review and fix any warnings.",
   [("bicep build main.json", "<code>build</code> compiles Bicep to ARM JSON, which is the opposite direction."),
    ("Export-AzResourceGroup -ResourceGroupName rg1", "exports a resource group to ARM JSON, not Bicep."),
    ("New-AzResourceGroupDeployment -TemplateFile main.json -WhatIf", "previews a deployment and doesn't convert files.")],
   [DECOMPILE], 93),

mc("CO", T,
   "<p>An administrator built resource group <em>RG-Demo</em> manually in the portal. You need a template that captures the current configuration of all resources in RG-Demo so that the environment can be redeployed later.</p><p>What should you do?</p>",
   "Use Export template on RG-Demo",
   "<strong>Export template</strong> at the resource group (or <code>Export-AzResourceGroup</code>) generates an ARM template from current resource state. Review it before reuse because some properties and resource types can't be exported.",
   [("Open Deployments in RG-Demo and download the latest deployment template", "manually created resources may never have gone through one deployment, so it wouldn't contain everything."),
    ("Run bicep decompile against RG-Demo", "decompile needs an ARM JSON file as input."),
    ("Create a Recovery Services vault backup of RG-Demo", "backups protect data, not infrastructure definitions.")],
   [EXPORT], 90),

mc("CO", T,
   "<p>You need to deploy <em>main.bicep</em> and its parameter file to resource group <em>RG-Web</em> by using Azure PowerShell. The Bicep CLI is installed.</p><p>Which command should you run?</p>",
   "New-AzResourceGroupDeployment -ResourceGroupName RG-Web -TemplateFile .\\main.bicep -TemplateParameterFile .\\main.bicepparam",
   "Azure PowerShell deploys Bicep files directly with <code>New-AzResourceGroupDeployment</code>; it transpiles the file with the Bicep CLI behind the scenes.",
   [("New-AzSubscriptionDeployment -Location westeurope -TemplateFile .\\main.bicep", "targets the subscription scope, not a resource group."),
    ("New-AzResourceGroup -Name RG-Web -TemplateFile .\\main.bicep", "creates a resource group and doesn't accept a template."),
    ("Invoke-AzDeployment -File .\\main.bicep", "this cmdlet doesn't exist.")],
   [BICEP_PS], 90),

mc("CO", T,
   "<p>A Bicep file must create three resource groups and then deploy resources into each one in a single deployment.</p><p>How should you configure and deploy the file?</p>",
   "Set targetScope = 'subscription' and deploy with New-AzSubscriptionDeployment, using modules scoped to each resource group",
   "Resource groups are subscription-level resources. A file with <code>targetScope = 'subscription'</code> can create them and call <strong>modules</strong> with <code>scope: resourceGroup(...)</code> to deploy inside them. Subscription deployments use <code>New-AzSubscriptionDeployment</code> (alias <code>New-AzDeployment</code>).",
   [("Keep the default targetScope and deploy with New-AzResourceGroupDeployment", "a resource group deployment can't create resource groups."),
    ("Set targetScope = 'tenant' and deploy with New-AzTenantDeployment", "tenant scope is for management groups and tenant-level resources and needs extra permissions."),
    ("Create the resource groups with dependsOn in a resource group deployment", "dependsOn doesn't change the deployment scope.")],
   [BICEP_SUB], 90),

mc("CO", T,
   "<p>An ARM template deploys a VM. The local administrator password must come from secret <em>vmAdminPwd</em> in Key Vault <em>kv-ops</em> and must never appear in source control.</p><p>What should you do?</p>",
   "Reference the Key Vault secret in the parameter file and enable Azure Resource Manager for template deployment on kv-ops",
   "A parameter file can use a <strong>Key Vault reference</strong> (vault ID plus secret name) for a <code>securestring</code> parameter. The vault must have <code>enabledForTemplateDeployment</code> set, and the deploying user needs permission to deploy using the vault.",
   [("Store the password in a template variable", "variables are stored in plain text in the template."),
    ("Add the password to the template outputs", "outputs are visible in deployment history and expose the secret."),
    ("Use a parameter of type string with a defaultValue", "a default puts the secret in source control.")],
   [KV_PARAM], 92),

mc("CO", T,
   "<p>An ARM template deploys a network interface and a VM that uses it. Deployments fail intermittently because Resource Manager tries to create the VM before the NIC exists.</p><p>What should you add to the VM resource?</p>",
   "A dependsOn element that references the NIC's resourceId()",
   "<strong>dependsOn</strong> tells Resource Manager to deploy the listed resources first. Resources without dependencies are deployed in parallel.",
   [("A condition element", "<code>condition</code> controls whether a resource is deployed at all, not the order."),
    ("A copy loop with a batchSize of 1", "batching controls serial deployment within a loop, not between different resources."),
    ("An output that returns the NIC ID", "outputs are evaluated after deployment and don't create ordering.")],
   [DEPENDS], 94),

mc("CO", T,
   "<p>Before deploying an updated template to production, you want to see which resources will be created, modified or deleted, without making any changes.</p><p>What should you use?</p>",
   "The what-if operation (New-AzResourceGroupDeployment -WhatIf)",
   "<strong>What-if</strong> compares the template to current state and reports Create, Modify, Delete, NoChange and Ignore results before anything is deployed.",
   [("Test-AzResourceGroupDeployment", "validates template syntax and parameters but doesn't show resource-level changes."),
    ("Export template", "captures current state and doesn't compare it to a new template."),
    ("Deploy in Incremental mode", "this actually deploys the changes.")],
   [WHATIF], 92),

hot("CO", T, "<p>You're modifying an ARM template. For each requirement, select the template section you should use.</p>",
   [("A value that the deployer supplies at deployment time", ["parameters", "variables", "outputs", "resources"], "parameters", "Parameters accept input at deployment time."),
    ("A value built from other values and reused in several places", ["parameters", "variables", "outputs", "resources"], "variables", "Variables compute reusable values inside the template."),
    ("A value returned after deployment, such as a public IP address", ["parameters", "variables", "outputs", "resources"], "outputs", "Outputs return values from the deployment.")],
   "The main sections of an ARM template are <code>$schema</code>, <code>contentVersion</code>, <code>parameters</code>, <code>variables</code>, <code>functions</code>, <code>resources</code> and <code>outputs</code>. Only resources is required.",
   [SYNTAX], 96),

mc("CO", T,
   "<p>You're modifying a Bicep file to deploy a NIC into subnet <em>app</em> of an existing virtual network named <em>vnet-hub</em>. The VNet isn't managed by this file and must not be modified.</p><p>How should you reference the VNet?</p>",
   "Declare it with the existing keyword: resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' existing = { name: 'vnet-hub' }",
   "The <strong>existing</strong> keyword creates a symbolic reference to a deployed resource so that you can read properties (for example, <code>vnet.properties.subnets</code>, or use a child <code>existing</code> subnet) without redeploying it.",
   [("Redeclare the VNet with its full address space and subnets", "this would redeploy the VNet and could overwrite settings managed elsewhere."),
    ("Add the VNet to the outputs section", "outputs don't create references."),
    ("Use a module that deploys a new VNet named vnet-hub", "this would deploy, not reference, the VNet.")],
   [EXISTING], 92),

# ------------------------------------------------------------------ VMs
dd("CO", V,
   "<p>You need to enable encryption at host on an existing VM named <em>vm-app1</em>. Encryption at host has never been used in the subscription.</p><p>Which four actions should you perform in sequence?</p>",
   [("Register the EncryptionAtHost feature for Microsoft.Compute in the subscription", "this is a one-time subscription prerequisite."),
    ("Stop (deallocate) vm-app1", "the setting can be changed only while the VM is deallocated."),
    ("Update vm-app1 to set encryptionAtHost to true", "for example, with <code>Update-AzVM -VM $vm -EncryptionAtHost $true</code>."),
    ("Start vm-app1", "the VM comes back with temp disk and caches encrypted at the host.")],
   [("Enable Azure Disk Encryption with BitLocker", "a different, guest-OS-based technology that isn't needed for encryption at host."),
    ("Create a disk encryption set", "only needed when you use customer-managed keys, which isn't required here.")],
   "Encryption at host encrypts the temporary disk and OS/data disk caches at the VM host, and flows encrypted data to Storage. It complements server-side encryption.",
   [EAH, DISK_ENC], 88),

mc("CO", V,
   "<p>Server-side encryption already protects VM1's managed disks at rest. A security review finds that the <strong>temporary disk</strong> and the disk caches aren't encrypted.</p><p>What should you enable to fix this without installing anything in the guest OS?</p>",
   "Encryption at host",
   "<strong>Encryption at host</strong> encrypts data on the VM host, including temp disks and OS/data disk caches, with platform-managed or customer-managed keys. No guest agent or BitLocker/DM-Crypt is involved.",
   [("Azure Disk Encryption", "encrypts within the guest OS by using BitLocker or DM-Crypt, which is the in-guest approach the requirement excludes."),
    ("Infrastructure encryption on a storage account", "applies to storage accounts, not VM hosts."),
    ("Confidential disk encryption on a standard VM size", "requires confidential VM sizes and is for a different scenario.")],
   [DISK_ENC, EAH], 88),

mc("CO", V,
   "<p>You must move VM <em>vm-erp</em>, its disks, NIC, and NSG from East US to North Europe. You want a guided, orchestrated process that handles dependencies and lets you commit or discard the move.</p><p>What should you use?</p>",
   "Azure Resource Mover",
   "<strong>Azure Resource Mover</strong> orchestrates cross-region moves of VMs and related resources. It analyzes dependencies, prepares and initiates the move, and lets you commit or discard.",
   [("Move-AzResource with the target region as a parameter", "Move-AzResource moves between resource groups or subscriptions, not regions."),
    ("The Move to another subscription option in the portal", "changes the subscription, not the region."),
    ("Export template and redeploy in North Europe", "recreates infrastructure without moving data or orchestrating the cutover.")],
   [MOVER], 90),

mc("CO", V,
   "<p>You need to move VM <em>vm-db</em> (with managed disks and a NIC) from subscription <em>Sub-A</em> to <em>Sub-B</em> in the same Entra tenant.</p><p>Which statement is correct?</p>",
   "The VM must be moved together with its dependent resources, such as its managed disks",
   "Cross-subscription moves of a VM must include its dependent resources (for example, managed disks). Use the portal's move experience or <code>Move-AzResource</code> with all required resource IDs. The target subscription must have the needed resource providers registered.",
   [("The VM must be deleted and recreated because VMs can't change subscription", "VMs with managed disks can be moved between subscriptions."),
    ("Only the VM resource is moved; disks stay in Sub-A", "the VM and its disks must move together."),
    ("The subscriptions must be in different Entra tenants", "both subscriptions must be in the same tenant.")],
   [VM_MOVE, L + "azure-resource-manager/management/move-resource-group-and-subscription"], 84,
   conf_note="Move limitations vary by feature (for example, Marketplace plans, encryption and backup); the general rule tested is to move the VM with its dependencies."),

mc("CO", V,
   "<p>You want to resize VM <em>vm-calc</em> from D4s_v5 to a larger size, but the size you need isn't in the list of available sizes while the VM is running.</p><p>What should you do?</p>",
   "Stop (deallocate) the VM, then select the size",
   "The list of sizes for a running VM is limited to what the current hardware cluster supports. <strong>Deallocating</strong> the VM releases it from the cluster so that you can choose any size available in the region.",
   [("Restart the VM from within the guest OS", "the VM stays on the same cluster."),
    ("Redeploy the VM from the Redeploy + reapply page", "redeploy moves the VM to a new host but doesn't make you pick a new size."),
    ("Create a snapshot of the OS disk", "has no effect on size availability.")],
   [RESIZE], 90),

mc("CO", V,
   "<p>A two-tier application must achieve the highest VM connectivity SLA that Azure offers within a single region.</p><p>How should you deploy the VMs for each tier?</p>",
   "Two or more VMs per tier, distributed across two or more availability zones",
   "VMs deployed across <strong>availability zones</strong> carry the highest single-region VM SLA (99.99%). Availability sets give 99.95%, and a single VM with premium storage gives 99.9%.",
   [("Two or more VMs per tier in an availability set", "gives 99.95%, which is lower than zones."),
    ("One VM per tier with Premium SSD disks", "a single VM gives the lowest of these SLAs."),
    ("One VM per tier in a proximity placement group", "proximity placement groups reduce latency and don't add availability.")],
   [AVAIL], 92),

mc("CO", V,
   "<p>An availability set has 3 fault domains and 5 update domains. It contains 10 VMs.</p><p>During planned platform maintenance, what is the maximum number of VMs that will be rebooted at the same time?</p>",
   "2",
   "Planned maintenance reboots <strong>one update domain at a time</strong>. 10 VMs spread over 5 update domains puts 2 VMs in each, so at most 2 reboot together.",
   [("3", "3 is the number of fault domains, which relate to unplanned hardware failures, not planned updates."),
    ("5", "5 is the number of update domains, not the VMs per domain."),
    ("10", "maintenance doesn't reboot every VM simultaneously.")],
   [AVSET], 92),

mc("CO", V,
   "<p>VM <em>vm-web3</em> was created without an availability set. You now want to place it in availability set <em>avset-web</em>.</p><p>What should you do?</p>",
   "Recreate the VM in the availability set, reusing its existing disks",
   "A VM can be assigned to an availability set <strong>only at creation</strong>. To move an existing VM into one, delete the VM (keeping its disks) and recreate it in the set from those disks.",
   [("Edit the VM's Availability settings and select avset-web", "the setting can't be changed after creation."),
    ("Deallocate the VM and run Update-AzVM with the availability set ID", "the availability set property is immutable."),
    ("Move the VM into the resource group that contains avset-web", "moving resource groups doesn't change availability set membership.")],
   [AVSET], 92),

mc("CO", V,
   "<p>A data disk for a transactional database needs sub-millisecond latency and IOPS and throughput that you can change on the fly without resizing the disk.</p><p>Which disk type should you use?</p>",
   "Ultra Disk",
   "<strong>Ultra Disks</strong> deliver sub-millisecond latency and let you adjust IOPS and throughput independently of capacity without detaching the disk. They're supported as data disks only.",
   [("Premium SSD", "performance is tied to the disk size tier (with optional bursting), not independently adjustable."),
    ("Standard SSD", "designed for lighter workloads with lower, size-based performance."),
    ("Standard HDD", "for backup and noncritical workloads with the highest latency.")],
   [DISKS], 88, note="Premium SSD v2 also offers adjustable performance and is a valid answer in many real designs; it wasn't offered as an option here."),

mc("CO", V,
   "<p>You over-provisioned a 1 TiB Premium SSD data disk on VM1 and want to reduce it to 256 GiB to save money.</p><p>What should you do?</p>",
   "Create a new 256 GiB disk, copy the data to it, and replace the original disk",
   "Azure managed disks <strong>can't be shrunk</strong>. You can only increase size. To reduce cost, create a smaller disk, migrate the data inside the guest, and remove the larger disk.",
   [("Deallocate VM1 and set the disk size to 256 GiB", "decreasing size isn't supported, even when deallocated."),
    ("Change the disk performance tier to P15", "the tier can be raised for performance but can't go below the tier that matches the provisioned size, and capacity stays 1 TiB."),
    ("Take an incremental snapshot and restore it as 256 GiB", "a disk created from a snapshot can't be smaller than the source.")],
   [EXPAND, DISKS], 88),

mc("CO", V,
   "<p>Two VMs in a Windows Server Failover Cluster need simultaneous access to the same managed disk for clustered storage.</p><p>What should you configure?</p>",
   "Create a Premium SSD (or Ultra) disk with maxShares set to 2 and attach it to both VMs",
   "<strong>Shared disks</strong> are enabled with the <code>maxShares</code> property and support SCSI persistent reservations used by WSFC and Pacemaker.",
   [("Attach the same Standard HDD disk to both VMs", "Standard HDD doesn't support shared disks, and attaching requires maxShares."),
    ("Use an Azure Files share mounted as a data disk", "Azure Files isn't attached as a block disk."),
    ("Enable host caching ReadWrite on the disk", "caching doesn't enable multi-attach.")],
   [SHARED], 86),

mc("CO", V,
   "<p>A Virtual Machine Scale Set scales in after a sale ends. The application team wants the scale set to remove the <strong>oldest</strong> instances first, balanced across availability zones.</p><p>What should you configure?</p>",
   "Scale-in policy: OldestVM",
   "The <strong>scale-in policy</strong> determines which instances are removed: <em>Default</em> (balance across zones and fault domains, then delete the highest instance ID), <em>NewestVM</em>, or <em>OldestVM</em>. Both NewestVM and OldestVM still balance across zones.",
   [("Scale-in policy: NewestVM", "removes the newest instances, which is the opposite requirement."),
    ("Upgrade policy: Rolling", "controls how model updates are applied, not scale-in order."),
    ("Instance protection from scale-in on every instance", "would block scale-in entirely.")],
   [SCALEIN], 92),

mc("CO", V,
   "<p>You update the OS image reference of a Uniform scale set. The change must be applied automatically in batches while keeping most instances serving traffic, with health checks between batches.</p><p>Which upgrade policy should you use?</p>",
   "Rolling",
   "<strong>Rolling</strong> upgrades update instances in batches, honor health probe or Application Health extension signals, and pause between batches.",
   [("Manual", "you'd have to update each instance yourself."),
    ("Automatic", "updates all instances at once in an undefined order, with possible downtime."),
    ("Scale-in policy: Default", "isn't an upgrade policy.")],
   [UPGRADE], 90),

mc("CO", V,
   "<p>You're creating a new scale set. You want to manage instances with standard VM APIs, mix Spot and regular instances, and get fault domain spreading for high availability.</p><p>Which orchestration mode should you choose?</p>",
   "Flexible",
   "<strong>Flexible orchestration</strong> treats instances as standard VMs with full VM API support, allows mixing Spot and regular capacity, and spreads instances across fault domains and zones. It's the recommended mode for new scale sets.",
   [("Uniform", "uses scale-set-specific instance APIs and identical instances; fewer standard VM capabilities."),
    ("Availability set mode", "isn't a scale set orchestration mode."),
    ("Proximity placement mode", "isn't an orchestration mode; proximity placement groups are a separate feature.")],
   [ORCH], 84, conf_note="Feature differences between Flexible and Uniform continue to narrow; check the current orchestration comparison."),

mc("CO", V,
   "<p>After you deploy 20 Windows VMs from a Marketplace image, each VM must download and run a PowerShell script from a storage account to install an agent. You want to use a VM extension.</p><p>Which extension should you use?</p>",
   "Custom Script Extension",
   "The <strong>Custom Script Extension</strong> downloads scripts from storage or a URL and runs them on the VM. It's commonly used for post-deployment configuration.",
   [("Azure Monitor Agent extension", "installs the monitoring agent and doesn't run arbitrary scripts."),
    ("VMAccess extension", "resets admin credentials or SSH configuration."),
    ("Network Watcher Agent extension", "enables Network Watcher capabilities such as packet capture.")],
   [CSE], 92),

hot("CO", V,
   "<p>You configure autoscale for scale set <em>vmss-api</em>. Requirements:</p><ul><li>Always keep at least 2 instances and never exceed 10.</li><li>Add instances when average CPU is high, and remove them when it's low.</li></ul><p>Select the correct value for each setting.</p>",
   [("Minimum instance count", ["2", "1", "10", "0"], "2", "The autoscale profile's minimum enforces the floor of 2."),
    ("Maximum instance count", ["10", "2", "20", "100"], "10", "The maximum caps scale-out at 10."),
    ("Rule metric source", ["Percentage CPU of the scale set", "Activity log events", "Storage account transactions"], "Percentage CPU of the scale set", "Host metrics such as Percentage CPU are available for autoscale without an agent."),
    ("Rules required", ["One scale-out rule and one scale-in rule", "Only a scale-out rule", "Only a scheduled profile"], "One scale-out rule and one scale-in rule", "Without a scale-in rule the set would never shrink after scaling out.")],
   "Autoscale profiles combine instance limits with paired scale-out and scale-in rules. Make sure the thresholds don't flap.",
   [VMSS_AUTO, AUTOSCALE], 92),

yn("CO", V, "<p>You're planning VM deployments in a region that supports availability zones. Evaluate each statement.</p>",
   [("A VM can be placed in both an availability set and an availability zone.", "No", "Availability sets and zones are mutually exclusive placement choices for a VM."),
    ("Zonal VMs in different zones can use the same zone-redundant Standard public load balancer.", "Yes", "Standard Load Balancer frontends can be zone-redundant and serve backends in multiple zones."),
    ("A managed disk attached to a zonal VM must be in the same zone as the VM.", "Yes", "Zonal VMs use zonal disks in the same zone. ZRS disks can attach across zones, but a zonal disk is pinned.")],
   "Choose zones for datacenter-failure resilience and availability sets for rack-level resilience in regions without zones.",
   [AVAIL, L + "reliability/availability-zones-overview"], 84,
   conf_note="ZRS managed disks change the disk-zone rule in some scenarios; the statement covers zonal (LRS) disks."),

# ------------------------------------------------------------------ containers
mc("CO", C,
   "<p>Your container images must be replicated to registries in East US, West Europe and Southeast Asia so that each region pulls locally, while you manage a single registry.</p><p>Which Azure Container Registry SKU is required?</p>",
   "Premium",
   "<strong>Geo-replication</strong> is a <strong>Premium</strong> SKU feature. Premium also adds private endpoints and higher throughput limits.",
   [("Basic", "doesn't support geo-replication."),
    ("Standard", "doesn't support geo-replication."),
    ("Any SKU, if zone redundancy is enabled", "zone redundancy is in-region resilience, not geo-replication.")],
   [ACR_SKU], 95),

mc("CO", C,
   "<p>An Azure Container Instances container group uses a user-assigned managed identity to pull images from registry <em>acrprod</em>. You must follow least privilege.</p><p>Which role should you assign to the identity on acrprod?</p>",
   "AcrPull",
   "<strong>AcrPull</strong> grants pull-only access to images, which is all a runtime needs.",
   [("AcrPush", "also allows pushing images."),
    ("Contributor", "grants full management of the registry."),
    ("Owner", "grants full management and role assignment.")],
   [ACR_ROLES, ACR_AUTH], 93),

mc("CO", C,
   "<p>A web container and a log-shipping sidecar must run on the same host, share a lifecycle and local network (localhost), and mount the same volume. You're using Azure Container Instances.</p><p>What should you deploy?</p>",
   "A single container group that contains both containers",
   "A <strong>container group</strong> is the top-level ACI resource. Its containers are scheduled on the same host, share lifecycle, network namespace (IP and localhost) and volumes. It's similar to a Kubernetes pod.",
   [("Two separate container groups in the same resource group", "they'd have separate hosts, IPs and lifecycles."),
    ("Two container groups connected by VNet peering", "peering connects networks; it doesn't co-locate containers."),
    ("An Azure Container Registry task", "ACR tasks build images; they don't run applications.")],
   [ACI_GROUPS], 93),

mc("CO", C,
   "<p>An ACI container runs a nightly data-processing job that should exit when it's done. If the process fails with a non-zero exit code, ACI should restart it. If it succeeds, it must not run again.</p><p>Which restart policy should you set?</p>",
   "OnFailure",
   "<strong>OnFailure</strong> restarts containers only when they exit with an error, which suits run-to-completion tasks that should retry on failure.",
   [("Always", "the default; it restarts containers even after successful completion, rerunning the job."),
    ("Never", "won't retry after a failure."),
    ("Manual", "isn't an ACI restart policy value.")],
   [ACI_RESTART], 95),

mc("CO", C,
   "<p>Data written by an ACI container must survive container restarts and redeployments and be readable from other services.</p><p>What should you configure?</p>",
   "Mount an Azure Files share as a volume in the container group",
   "ACI containers are stateless by default. Mounting an <strong>Azure Files</strong> share as a volume persists data beyond the container lifecycle and makes it accessible to other clients.",
   [("An emptyDir volume", "is tied to the container group's lifetime and is lost when the group is deleted."),
    ("A gitRepo volume", "clones a repository and isn't for persisting output."),
    ("Increase the container's memory allocation", "memory isn't persistent storage.")],
   [ACI_FILES], 93),

mc("CO", C,
   "<p>An API must scale automatically on HTTP traffic from zero instances (no cost when idle) up to 50 replicas. You don't want to manage Kubernetes clusters.</p><p>Which service should you use?</p>",
   "Azure Container Apps",
   "<strong>Container Apps</strong> provides serverless containers with KEDA-based scaling, including HTTP scale rules and <strong>scale to zero</strong>, without cluster management.",
   [("Azure Container Instances", "has no built-in autoscaling; you'd have to create and delete groups yourself."),
    ("Azure Kubernetes Service", "requires cluster management, which the requirement rules out."),
    ("A single VM running Docker", "has no automatic scaling and costs money when idle.")],
   [ACA_COMPARE, ACA_SCALE], 93),

mc("CO", C,
   "<p>You deploy a background-processing container app with ingress <strong>disabled</strong> and no scale rules defined. After a while, the app stops processing and never starts again.</p><p>What should you do?</p>",
   "Set minReplicas to 1 or add a custom (KEDA) scale rule that matches the workload's event source",
   "With no rule, Container Apps applies the default HTTP rule (min 0, max 10). With ingress disabled there's no HTTP traffic to wake it, so it <strong>scales to zero and can't start</strong>. Set <code>minReplicas ≥ 1</code> or add a custom scale rule, such as a queue-length rule.",
   [("Increase maxReplicas to 30", "the problem is the minimum, not the maximum."),
    ("Switch the app to single revision mode", "revision mode doesn't affect scaling."),
    ("Add more CPU to the container", "resources don't prevent scale to zero.")],
   [ACA_SCALE], 92),

hot("CO", C, "<p>For each Azure Container Apps requirement, select the scale setting to use.</p>",
   [("Scale on the number of messages in an Azure Service Bus queue", ["Custom (KEDA) scale rule", "HTTP scale rule", "TCP scale rule", "minReplicas"], "Custom (KEDA) scale rule", "Event sources such as Service Bus use custom rules based on KEDA scalers."),
    ("Scale on concurrent HTTP requests per replica", ["Custom (KEDA) scale rule", "HTTP scale rule", "TCP scale rule", "minReplicas"], "HTTP scale rule", "HTTP rules scale on concurrent requests."),
    ("Always keep at least one replica running to avoid cold starts", ["Custom (KEDA) scale rule", "HTTP scale rule", "TCP scale rule", "minReplicas"], "minReplicas", "Setting minReplicas to 1 or more prevents scale to zero.")],
   "Container Apps scaling is defined by limits (min and max replicas) plus rules (HTTP, TCP or custom).",
   [ACA_SCALE], 93),

mc("CO", C,
   "<p>You want to send 20% of production traffic to a new version of a container app and 80% to the current version, then shift traffic gradually.</p><p>What should you configure?</p>",
   "Multiple revision mode with traffic weights on the two revisions",
   "In <strong>multiple revision mode</strong>, several revisions can be active at once and you assign <strong>traffic weights</strong> to each one, which enables canary and blue-green releases.",
   [("Single revision mode with two replicas", "only one revision receives traffic in single revision mode."),
    ("Two container apps behind Azure DNS round-robin", "DNS can't apply percentage weights reliably and adds management overhead."),
    ("A custom scale rule with a weight of 20", "scale rules control replica counts, not traffic distribution.")],
   [ACA_REV], 92),

mc("CO", C,
   "<p>A running ACI container group needs more memory. You want to change the memory allocation of its container.</p><p>What should you do?</p>",
   "Delete and redeploy the container group with the new resource request",
   "Many ACI container group properties, including resource requests, <strong>can't be updated in place</strong>. You redeploy the group, typically by deleting it and creating it again with the new configuration.",
   [("Scale the container group out to two instances", "ACI groups don't scale out."),
    ("Edit the memory value on the container's Properties page and save", "changing resources in place isn't supported."),
    ("Enable autoscale on the container group", "ACI has no autoscale.")],
   [ACI_UPDATE], 80, conf_note="Some properties can be updated by redeploying with the same name; the resource-request change still requires recreation according to current docs."),

# ------------------------------------------------------------------ App Service
mc("CO", P, "<p>Refer to the case study.</p><p>You need to meet the scaling requirement for app-orders. The solution must minimize cost.</p><p>What should you do?</p>",
   "Scale plan-orders up to Premium v3 and configure autoscale with a maximum of 15 instances",
   "Standard plans support autoscale but only up to <strong>10 instances</strong>. <strong>Premium v3</strong> supports up to 30 instances, so it's the lowest tier that meets 15. Autoscale rules then add instances during sales events.",
   [("Keep Standard S1 and configure autoscale with a maximum of 15", "Standard can't scale beyond 10 instances."),
    ("Scale up to Isolated v2", "it meets the requirement but costs far more than necessary."),
    ("Scale down to Basic B3 and add a manual scale-out to 15", "Basic supports at most 3 instances and has no autoscale.")],
   [PLANS, LIMITS], 88, case="litware"),

mc("CO", P, "<p>Refer to the case study.</p><p>You need to meet the deployment requirement for app-orders.</p><p>What should you do?</p>",
   "Mark the staging database connection string as a deployment slot setting, then swap staging into production",
   "A <strong>slot swap</strong> warms up the source slot and switches routing with no downtime. Settings marked as <strong>deployment slot settings</strong> are sticky: they stay with the slot, so staging's connection string never moves to production.",
   [("Deploy directly to production and restart the app", "causes downtime and skips validation in staging."),
    ("Swap the slots without changing any settings", "non-sticky connection strings move with the swap, sending staging's database setting to production."),
    ("Clone the staging slot to a new production web app", "creates a new app with a different hostname, which isn't a zero-downtime promotion.")],
   [SLOTS], 93, case="litware"),

mc("CO", P,
   "<p>You need to map the root (apex) domain <em>contoso.com</em> to web app <em>contoso-web</em>.</p><p>Which DNS records should you create at the DNS provider?</p>",
   "An A record pointing to the app's inbound IP address, and a TXT record named asuid with the app's domain verification ID",
   "Apex domains can't use CNAME records. Use an <strong>A record</strong> to the app's IP plus a <strong>TXT asuid</strong> record that proves domain ownership to App Service.",
   [("A CNAME record for contoso.com pointing to contoso-web.azurewebsites.net", "CNAME isn't allowed at the zone apex."),
    ("An MX record pointing to contoso-web.azurewebsites.net", "MX records route mail."),
    ("A TXT record only", "TXT proves ownership but doesn't route traffic.")],
   [DOMAIN], 92),

mc("CO", P,
   "<p>You need to secure <em>shop.contoso.com</em>, <em>api.contoso.com</em> and future subdomains on an App Service app with one certificate.</p><p>What should you use?</p>",
   "A wildcard certificate for *.contoso.com, imported from Key Vault or purchased as an App Service certificate",
   "A <strong>wildcard</strong> certificate covers all first-level subdomains. App Service <strong>managed certificates</strong> are free but don't support wildcard names, so import a wildcard certificate or buy one as an App Service certificate.",
   [("A free App Service managed certificate for *.contoso.com", "managed certificates don't support wildcards."),
    ("A self-signed certificate created on the App Service plan", "browsers won't trust it, so it isn't suitable for production."),
    ("Enable HTTPS Only without a certificate", "HTTPS Only redirects traffic but doesn't provide a certificate for custom domains.")],
   [CERT, BIND], 90),

mc("CO", P,
   "<p>All HTTP requests to web app <em>app-portal</em> must be redirected to HTTPS, and clients that only support TLS 1.0 or 1.1 must be rejected.</p><p>Which two settings should you configure?</p>",
   "Set HTTPS Only to On and set Minimum Inbound TLS Version to 1.2",
   "<strong>HTTPS Only</strong> issues redirects from HTTP to HTTPS, and the <strong>minimum TLS version</strong> setting rejects older protocol versions.",
   [("Add a TLS/SSL binding and enable client certificates", "client certificates authenticate clients and don't enforce redirection or TLS version."),
    ("Configure an access restriction rule for port 80", "access restrictions filter by source and don't redirect to HTTPS."),
    ("Enable ARR affinity and HTTP 2.0", "ARR affinity is session stickiness, and HTTP/2 doesn't enforce TLS versions.")],
   [BIND, L + "app-service/overview-tls"], 90),

hot("CO", P, "<p>For each requirement for web app <em>app-hr</em>, select the App Service networking feature to use.</p>",
   [("The app must call an API hosted on a VM in VNet1 by its private IP address", ["Virtual network integration", "Private endpoint", "Access restrictions", "Hybrid connection"], "Virtual network integration", "VNet integration handles outbound traffic from the app into a VNet."),
    ("Users on-premises must reach the app over the site-to-site VPN by using a private IP address", ["Virtual network integration", "Private endpoint", "Access restrictions", "Hybrid connection"], "Private endpoint", "A private endpoint provides private inbound access to the app."),
    ("Only requests from the 198.51.100.0/24 range may reach the app's public endpoint", ["Virtual network integration", "Private endpoint", "Access restrictions", "Hybrid connection"], "Access restrictions", "Access restrictions allow or deny inbound traffic by IP or service tag.")],
   "Remember the direction: VNet integration is outbound, a private endpoint is inbound and private, and access restrictions filter inbound traffic to the public endpoint.",
   [NETFEAT, VNETINT, IPRESTRICT], 93),

mc("CO", P,
   "<p>You need App Service backups of <em>app-crm</em> that you can download and store in your own storage account, on a schedule of every 12 hours, with 30-day retention.</p><p>What should you configure?</p>",
   "A custom scheduled backup that targets a storage account container",
   "<strong>Custom backups</strong> are written to a storage account you specify, so they can be downloaded, and you can schedule frequency and retention. Automatic backups are hourly, platform-stored and not downloadable.",
   [("Rely on automatic backups", "they're stored by the platform and can't be downloaded."),
    ("Add the app to a Recovery Services vault backup policy", "Azure Backup doesn't protect App Service apps this way."),
    ("Create a deployment slot and clone the app every 12 hours", "cloning isn't a backup and doesn't keep retention.")],
   [BACKUP], 90),

mc("CO", P,
   "<p>An app on a Standard App Service plan runs out of memory under load. CPU is low, and adding more instances doesn't help because each request needs a lot of memory.</p><p>What should you do?</p>",
   "Scale up the App Service plan to a tier or size with more memory per instance",
   "<strong>Scale up</strong> changes the instance size or tier (more CPU and memory per instance). <strong>Scale out</strong> adds instances, which doesn't help a per-request memory problem.",
   [("Scale out the plan to more instances", "every instance still has the same memory limit."),
    ("Add a deployment slot", "slots run on the same instances and add load."),
    ("Enable ARR affinity", "session affinity doesn't add memory.")],
   [SCALEUP], 92),

mc("CO", P,
   "<p>Three web apps share App Service plan <em>plan-shared</em>. One of them, <em>app-reports</em>, frequently consumes most of the CPU and slows down the others.</p><p>What should you do to isolate the other apps from app-reports?</p>",
   "Move app-reports to its own App Service plan",
   "All apps in a plan share its instances. Moving the noisy app to a <strong>separate plan</strong> gives it dedicated compute and protects the others.",
   [("Create a deployment slot for app-reports", "slots share the same plan instances."),
    ("Enable autoscale on plan-shared", "scaling adds instances for all apps but doesn't isolate them."),
    ("Configure access restrictions on app-reports", "access restrictions filter traffic and don't control resources.")],
   [PLANS], 92),

mc("CO", P,
   "<p>Before a full release, you want 10% of production users routed to the <em>beta</em> deployment slot of a Windows web app to test new features with real traffic.</p><p>What should you configure?</p>",
   "Set the beta slot's Traffic % to 10 in Deployment slots",
   "<strong>Testing in production</strong> lets you route a percentage of production traffic to a slot. Clients are pinned to the slot with a routing cookie.",
   [("Swap with preview", "applies the target slot's settings for validation before completing a swap, not percentage routing."),
    ("Auto swap", "swaps the slot into production after deployment, which sends 100% of traffic."),
    ("Configure autoscale to 10%", "autoscale affects instance count, not routing.")],
   [SLOTS], 92),

multi("CO", P,
   "<p>You plan an App Service plan for a production web app that needs a custom domain with TLS, autoscale, and deployment slots. You want the lowest-cost tier.</p><p>Which two statements are correct?</p>",
   [("Standard is the lowest tier that includes autoscale", "autoscale starts at Standard; Basic supports only manual scale-out."),
    ("All apps in the plan scale together when the plan scales", "scaling is performed at the plan level and affects every app in it.")],
   "Pick the tier by required features, then remember that scaling applies to the whole plan.",
   [("The Free tier supports custom TLS bindings", "Free doesn't support custom domains with TLS."),
    ("Each web app in a plan is billed separately for its instances", "dedicated tiers are billed per plan instance, not per app."),
    ("Deployment slots run on separate instances from the production slot", "slots share the plan's instances.")],
   [PLANS, SCALEUP], 86, conf_note="Tier feature sets (for example, slot availability on lower tiers) change periodically; check the current App Service limits."),
]
