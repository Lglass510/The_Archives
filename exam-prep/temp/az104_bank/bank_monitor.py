"""Domain 5 - Monitor and maintain Azure resources (10-15%)."""
from qlib import mc, multi, hot, yn, dd, code
import cases  # noqa: F401

M = "Monitor resources in Azure"
B = "Implement backup and recovery"

L = "https://learn.microsoft.com/en-us/azure/"
METRICS = L + "azure-monitor/metrics/data-platform-metrics"
DIAG = L + "azure-monitor/data-collection/diagnostic-settings"
ACTLOG = L + "azure-monitor/fundamentals/activity-log"
KQL_START = L + "azure-monitor/logs/get-started-queries"
KQL_SUMM = "https://learn.microsoft.com/en-us/kusto/query/summarize-operator"
ALERT_TYPES = L + "azure-monitor/alerts/alerts-types"
AG = L + "azure-monitor/alerts/action-groups"
APR = L + "azure-monitor/alerts/alerts-processing-rules"
VMI = L + "azure-monitor/vm/monitor-vm"
AMA = L + "azure-monitor/agents/azure-monitor-agent-overview"
DCR = L + "azure-monitor/vm/data-collection"
STI = L + "storage/common/storage-insights-overview"
IPFLOW = L + "network-watcher/ip-flow-verify-overview"
CONNMON = L + "network-watcher/connection-monitor-overview"
VNETFLOW = L + "network-watcher/vnet-flow-logs-overview"
NSGFLOW_MIG = L + "network-watcher/nsg-flow-logs-migrate"
PCAP = L + "network-watcher/packet-capture-overview"
VM_BACKUP = L + "backup/backup-azure-arm-vms-prepare"
ENHANCED = L + "backup/backup-azure-vms-enhanced-policy"
ASR_ENABLE = L + "site-recovery/azure-to-azure-tutorial-enable-replication"
ASR_DRILL = L + "site-recovery/azure-to-azure-tutorial-dr-drill"
ASR_FAILOVER = L + "site-recovery/azure-to-azure-tutorial-failover-failback"
BV = L + "backup/backup-vault-overview"
DISK_BACKUP = L + "backup/disk-backup-overview"
FILE_RECOVERY = L + "backup/backup-azure-restore-files-from-vm"
RSV_CREATE = L + "backup/backup-create-recovery-services-vault"
BACKUP_FAQ = L + "backup/backup-azure-backup-faq"
SOFTDEL = L + "backup/secure-by-default"
REPORTS = L + "backup/configure-reports"
BK_ALERTS = L + "backup/monitoring-and-alerts-overview"
RESTORE_VM = L + "backup/backup-azure-arm-restore-vms"

ITEMS = [
# ------------------------------------------------------------------ monitoring
mc("MO", M,
   "<p>You must analyze the <em>Percentage CPU</em> platform metric of 30 VMs over the past 18 months and correlate it with log data.</p><p>What should you configure now so that the data is available in the future?</p>",
   "A diagnostic setting on each VM (or via Azure Policy) that sends platform metrics to a Log Analytics workspace with sufficient retention",
   "Platform metrics are kept in the metrics database for <strong>93 days</strong>. To keep them longer and query them alongside logs, route them with <strong>diagnostic settings</strong> to a Log Analytics workspace (AzureMetrics table) and set the workspace retention as needed.",
   [("Increase the metrics retention period in Metrics Explorer to 18 months", "platform metric retention isn't configurable."),
    ("Pin the Metrics Explorer chart to a dashboard", "pinning doesn't extend retention."),
    ("Create a metric alert rule for each VM", "alerts evaluate signals and don't archive them.")],
   [METRICS, DIAG], 88),

mc("MO", M,
   "<p>Auditors need two years of history of who created, modified or deleted resources in subscription <em>Sub-Fin</em>, queryable with KQL.</p><p>What should you configure?</p>",
   "A diagnostic setting on the subscription's Activity log that sends data to a Log Analytics workspace with two-year retention",
   "The Activity log keeps events for <strong>90 days</strong>. A subscription-level <strong>diagnostic setting</strong> exports it to a Log Analytics workspace (AzureActivity table), where you set retention and query with KQL.",
   [("Nothing, because the Activity log keeps events for two years by default", "default retention is 90 days."),
    ("A resource lock on Sub-Fin", "locks prevent changes and don't record them."),
    ("Microsoft Entra audit logs", "these record directory changes such as users and groups, not Azure resource operations.")],
   [ACTLOG, DIAG], 93),

mc("MO", M,
   "<p>VMs send heartbeat data to a Log Analytics workspace. You need a query that lists computers that haven't sent a heartbeat in the last 15 minutes.</p><p>Which query should you use?</p>",
   "Heartbeat | summarize LastSeen = max(TimeGenerated) by Computer | where LastSeen < ago(15m)",
   "Group by computer and take the latest heartbeat with <code>summarize max(TimeGenerated)</code>, then keep only computers whose last heartbeat is older than 15 minutes.",
   [("Heartbeat | where TimeGenerated > ago(15m) | distinct Computer", "lists computers that <em>did</em> send heartbeats recently."),
    ("Heartbeat | where TimeGenerated < ago(15m) | distinct Computer", "returns almost every computer, because all have old heartbeats too."),
    ("Heartbeat | count by Computer | where count_ == 0", "computers with no rows never appear in the results, and the syntax is invalid.")],
   [KQL_START, KQL_SUMM], 90),

hot("MO", M,
   "<p>You need a time chart of average CPU per computer in 5-minute intervals over the last day. Complete the KQL query.</p>"
   + code("""Perf
| [Box 1] TimeGenerated > ago(1d) and CounterName == "% Processor Time"
| [Box 2] avg(CounterValue) by Computer, [Box 3](TimeGenerated, 5m)
| render timechart""", "kusto"),
   [("Box 1", ["where", "project", "extend", "summarize"], "where", "<code>where</code> filters rows."),
    ("Box 2", ["summarize", "where", "join", "top"], "summarize", "<code>summarize</code> aggregates rows by the group-by columns."),
    ("Box 3", ["bin", "ago", "count", "make_list"], "bin", "<code>bin()</code> rounds timestamps into fixed 5-minute buckets.")],
   "The pattern is filter (<code>where</code>), aggregate (<code>summarize ... by bin()</code>), then visualize (<code>render</code>).",
   [KQL_START, KQL_SUMM], 95),

mc("MO", M,
   "<p>Operations must be notified within minutes when <strong>Percentage CPU</strong> on VM <em>vm-web1</em> averages more than 85% over 15 minutes.</p><p>Which alert rule type is most appropriate?</p>",
   "Metric alert",
   "<strong>Metric alerts</strong> evaluate platform or custom metrics at regular intervals with low latency. They're the right choice for a threshold on a numeric metric such as Percentage CPU.",
   [("Activity log alert", "fires on control-plane events such as delete operations, not metric values."),
    ("Log search alert on the Event table", "the Event table holds Windows events, not CPU metrics, and log alerts have more latency."),
    ("Resource Health alert", "fires on platform health status changes, not utilization.")],
   [ALERT_TYPES], 94),

mc("MO", M,
   "<p>Security wants an alert when more than 20 failed sign-in attempts (Windows event ID 4625) are recorded on any server within 10 minutes. The events are collected into a Log Analytics workspace.</p><p>Which alert type should you create?</p>",
   "Log search alert with a KQL query on the security events, counted per server",
   "<strong>Log search alerts</strong> run a KQL query on a schedule and fire when the result meets a threshold, which is ideal for counting events in a time window.",
   [("Metric alert on Percentage CPU", "unrelated to sign-in events."),
    ("Activity log alert on Sign-in operations", "the Activity log records Azure control-plane operations, not OS logons."),
    ("Service Health alert", "reports Azure platform incidents.")],
   [ALERT_TYPES], 92),

mc("MO", M,
   "<p>You must be notified whenever anyone deletes a virtual machine in subscription <em>Sub-Prod</em>.</p><p>What should you create?</p>",
   "An activity log alert on the Delete Virtual Machine (Microsoft.Compute/virtualMachines/delete) operation",
   "Deleting a VM is a <strong>control-plane operation</strong> recorded in the Activity log. <strong>Activity log alerts</strong> fire on specific administrative operations.",
   [("A metric alert on VM availability", "would fire on any outage and doesn't identify deletes."),
    ("A log search alert on the Perf table", "Perf holds performance counters."),
    ("A budget alert", "monitors cost, not operations.")],
   [ALERT_TYPES, ACTLOG], 94),

mc("MO", M, "<p>Refer to the case study.</p><p>You need to meet the notification requirement for vmss-worker.</p><p>What should you configure?</p>",
   "A metric alert rule on average CPU > 80% over 10 minutes with an action group for SMS and email, plus an alert processing rule that suppresses notifications every Sunday 02:00–04:00",
   "An <strong>action group</strong> defines who's notified and how (SMS and email). An <strong>alert processing rule</strong> with a recurring schedule removes action groups from fired alerts during the maintenance window, without disabling the alert rule.",
   [("A metric alert with an action group, and disable the alert rule manually every Sunday", "this is manual and error-prone."),
    ("A log search alert with an action group that has only an email receiver", "SMS is required."),
    ("An alert processing rule that adds an action group, with no alert rule", "processing rules act on fired alerts and don't detect CPU conditions.")],
   [APR, AG], 92, case="litware"),

mc("MO", M,
   "<p>When a critical alert fires, a ticket must be created automatically in a third-party service desk that exposes a REST API accepting JSON payloads.</p><p>Which action group action type should you use?</p>",
   "Webhook",
   "A <strong>webhook</strong> action sends an HTTP POST with the alert payload (optionally the common alert schema) to any REST endpoint.",
   [("Email Azure Resource Manager role", "emails role members and doesn't create tickets."),
    ("Voice call", "notifies a phone number."),
    ("Azure app push notification", "sends to the Azure mobile app.")],
   [AG], 90),

mc("MO", M,
   "<p>You need to collect Windows event logs and guest OS performance counters from 50 Azure VMs into Log Analytics workspace <em>law-ops</em> and enable VM insights.</p><p>What should you deploy?</p>",
   "The Azure Monitor Agent on the VMs, with data collection rules that send the data to law-ops",
   "The <strong>Azure Monitor Agent (AMA)</strong> collects guest data, and <strong>data collection rules (DCRs)</strong> define what to collect and where to send it. VM insights uses AMA with a DCR.",
   [("The Log Analytics agent (MMA)", "it's retired and no longer supported."),
    ("A diagnostic setting on each VM resource", "collects host-level platform metrics, not guest event logs."),
    ("The Network Watcher extension", "enables network diagnostics, not guest log collection.")],
   [AMA, DCR, VMI], 92),

mc("MO", M,
   "<p>You manage 120 storage accounts and want one place to view capacity, transactions, latency and availability across all of them, with no setup.</p><p>What should you use?</p>",
   "Storage insights in Azure Monitor",
   "<strong>Storage insights</strong> gives a unified, at-scale view of capacity, performance, failures and availability for all storage accounts, based on platform metrics.",
   [("Azure Storage Explorer", "manages data and isn't a monitoring dashboard."),
    ("Microsoft Defender for Storage", "detects threats, not performance and capacity."),
    ("A Log Analytics workspace query on the StorageBlobLogs table", "requires diagnostic settings on every account and is more work.")],
   [STI], 90),

mc("MO", M,
   "<p>VM1 can't receive TCP 443 traffic from 198.51.100.10. You need to find out quickly whether an NSG rule blocks the flow and, if so, which rule.</p><p>Which Network Watcher tool should you use?</p>",
   "IP flow verify",
   "<strong>IP flow verify</strong> tests a specific 5-tuple against the effective NSG rules for a VM's NIC and returns <em>Allow</em> or <em>Deny</em> with the name of the matching rule.",
   [("Next hop", "diagnoses routing, not NSG filtering."),
    ("Packet capture", "captures traffic but doesn't name the NSG rule."),
    ("Topology", "visualizes resources and relationships.")],
   [IPFLOW], 95),

mc("MO", M,
   "<p>You need continuous monitoring of latency and packet loss between VM <em>vm-app</em> in Azure and an on-premises SQL Server endpoint, with alerts when thresholds are breached.</p><p>What should you configure?</p>",
   "Connection monitor in Network Watcher",
   "<strong>Connection monitor</strong> continuously tests reachability, latency and packet loss between endpoints (Azure or on-premises), stores results in Log Analytics, and supports alerts.",
   [("Connection troubleshoot", "runs a one-time, on-demand check."),
    ("IP flow verify", "evaluates NSG rules for a single flow."),
    ("VNet flow logs", "record flows but don't actively test latency or loss.")],
   [CONNMON], 93),

mc("MO", M,
   "<p>Security needs a record of IP traffic flowing through virtual network <em>VNet-Prod</em>, including allowed and denied flows, for traffic analytics. You're setting this up now.</p><p>What should you enable?</p>",
   "Virtual network flow logs for VNet-Prod",
   "<strong>VNet flow logs</strong> record IP traffic at the virtual network level and integrate with traffic analytics. <strong>NSG flow logs</strong> no longer support new creation (since June 30, 2025) and retire on September 30, 2027.",
   [("NSG flow logs on each NSG", "new NSG flow logs can't be created."),
    ("A packet capture session on every VM", "packet capture is short-lived and per VM, which doesn't scale."),
    ("Diagnostic settings for the virtual network's metrics", "metrics don't record individual flows.")],
   [VNETFLOW, NSGFLOW_MIG], 90),

mc("MO", M,
   "<p>An application on VM1 shows intermittent TLS handshake failures. You need the raw packets to and from VM1 for 10 minutes, filtered to TCP 443, saved to a storage account for Wireshark analysis.</p><p>What should you use?</p>",
   "Network Watcher packet capture",
   "<strong>Packet capture</strong> uses the Network Watcher VM extension to capture traffic with filters and time or size limits, and saves a .cap file to storage or the VM for analysis.",
   [("Connection monitor", "reports reachability and latency, not packet contents."),
    ("VNet flow logs", "record flow metadata, not payloads."),
    ("Azure Monitor metrics for the NIC", "shows aggregate byte and packet counts only.")],
   [PCAP], 93),

# ------------------------------------------------------------------ backup & recovery
mc("MO", B,
   "<p>You need to back up VM <em>vm-hr</em>, located in West Europe, by using Azure Backup. You plan to create a Recovery Services vault.</p><p>Where must the vault be created?</p>",
   "In West Europe",
   "For Azure VM backup, the Recovery Services vault must be in the <strong>same region</strong> as the VM. The vault can be in a different resource group, and in some cases a different subscription.",
   [("In the paired region North Europe", "backups are configured to a vault in the VM's region; geo-redundancy is a vault storage setting."),
    ("In any region, if the vault uses GRS", "GRS doesn't remove the same-region requirement."),
    ("In the same region as the resource group's metadata", "the resource group location doesn't matter.")],
   [VM_BACKUP, L + "backup/backup-support-matrix"], 93),

mc("MO", B, "<p>Refer to the case study.</p><p>You need to meet the backup requirement for vm-sql1 by using Azure VM backup.</p><p>What should you configure?</p>",
   "A Recovery Services vault with an Enhanced backup policy that uses an hourly schedule every 4 hours and daily retention of 30 days",
   "The <strong>Enhanced policy</strong> for Azure VM backup supports <strong>multiple backups per day</strong> (every 4, 6, 8 or 12 hours). The Standard policy allows only one backup per day.",
   [("A Recovery Services vault with a Standard policy and a daily backup", "Standard allows only one backup per day."),
    ("A Backup vault with an Azure Disk Backup policy for the OS disk only", "it wouldn't protect all disks consistently as a VM."),
    ("Azure Site Recovery with a 4-hour app-consistent snapshot frequency", "Site Recovery is disaster recovery replication, not backup with retention."),],
   [ENHANCED], 86, case="litware",
   conf_note="Application-consistent SQL backups might instead use the SQL Server in Azure VM workload backup; the item focuses on VM-level backup frequency."),

mc("MO", B, "<p>Refer to the case study.</p><p>You need to meet the regional recovery requirement for vm-sql1.</p><p>What should you implement?</p>",
   "Azure Site Recovery replication of vm-sql1 to West US by using a Recovery Services vault in West US",
   "<strong>Azure Site Recovery</strong> continuously replicates Azure VMs to another region, with RPOs typically measured in minutes, and supports failover and failback. The vault used for ASR must be in a region other than the source region (usually the target).",
   [("Azure Backup with Cross Region Restore enabled", "restores from the secondary region use backup recovery points that are hours old, not minutes."),
    ("Geo-redundant storage for vm-sql1's managed disks", "managed disks don't support GRS."),
    ("An availability set for vm-sql1", "protects within one datacenter, not against regional outages.")],
   [ASR_ENABLE], 92, case="litware"),

mc("MO", B,
   "<p>You need daily, snapshot-based operational backups of several Azure managed disks, with incremental snapshots kept in your own resource group.</p><p>Which vault type should you create?</p>",
   "Backup vault",
   "<strong>Azure Disk Backup</strong> is managed through a <strong>Backup vault</strong>, which handles newer workloads such as Azure Disks, Blobs and Azure Database for PostgreSQL. Recovery Services vaults handle Azure VMs, SQL/SAP HANA in VMs, Azure Files and MARS.",
   [("Recovery Services vault", "doesn't host the Azure Disk Backup workload."),
    ("Key vault", "stores secrets and keys, not backups."),
    ("Storage account with soft delete", "isn't a backup orchestration service.")],
   [BV, DISK_BACKUP, BACKUP_FAQ], 90),

mc("MO", B,
   "<p>A user deleted a single folder from a Windows VM that's backed up daily to a Recovery Services vault. You need to recover the folder without restoring the whole VM or its disks.</p><p>What should you do?</p>",
   "Use File Recovery: download and run the script for a recovery point to mount it as a drive, then copy the folder",
   "<strong>File Recovery</strong> generates a script that mounts the disks of a recovery point as local volumes (over iSCSI) so that you can copy individual files, then unmount.",
   [("Restore the VM to a new VM and copy the folder", "this works but is slower and costlier."),
    ("Replace the existing disks with the recovery point", "this overwrites all data changed since the backup."),
    ("Use Azure Site Recovery test failover", "ASR isn't configured, and it isn't a file restore tool.")],
   [FILE_RECOVERY], 92),

mc("MO", B,
   "<p>You created a Recovery Services vault with the default storage redundancy and have already protected 30 VMs. You now need to restore VMs in the secondary paired region if the primary region is unavailable.</p><p>Which statement is correct?</p>",
   "Cross Region Restore requires geo-redundant vault storage with CRR enabled; the redundancy type can't be changed after items are protected, unless you stop protection and reconfigure",
   "<strong>Cross Region Restore</strong> needs a <strong>GRS</strong> vault with CRR enabled. The vault's storage replication type can be modified only <strong>before</strong> any backups are stored. You can enable CRR on an existing GRS vault, but you can't switch LRS to GRS after protection starts.",
   [("Cross Region Restore works with any vault redundancy", "it needs GRS."),
    ("You can change the vault from LRS to GRS at any time", "replication type is locked once backups exist."),
    ("Cross Region Restore requires Azure Site Recovery", "they're separate features.")],
   [RSV_CREATE, L + "backup/backup-support-matrix"], 82,
   conf_note="Whether a default vault is GRS or LRS depends on the creation method; check the current portal default."),

dd("MO", B,
   "<p>Azure Site Recovery replicates VM <em>vm-erp</em> from East US to West US. You must validate DR without affecting production, then perform an actual failover and finalize it.</p><p>Which four actions should you perform in sequence?</p>",
   [("Run a test failover into an isolated virtual network in West US", "validates the recovery point without affecting replication or production."),
    ("Clean up the test failover", "removes the test VMs and records the results."),
    ("Run a failover to West US", "starts vm-erp in West US from a selected recovery point."),
    ("Commit the failover", "finalizes the failover and removes the other recovery points.")],
   [("Disable replication for vm-erp", "would remove protection and is unnecessary."),
    ("Re-protect before the failover", "re-protect is done after failover, to replicate back toward the original region.")],
   "The usual DR lifecycle is enable replication, test failover, clean up, failover, commit, re-protect, then fail back when ready.",
   [ASR_DRILL, ASR_FAILOVER], 90),

mc("MO", B,
   "<p>An administrator stopped backup for VM <em>vm-legacy</em> and deleted its backup data by mistake five days ago. Soft delete is enabled with default settings on the Recovery Services vault.</p><p>What can you do?</p>",
   "Undelete the backup item in the vault and resume protection",
   "<strong>Soft delete</strong> for Azure Backup keeps deleted backup data for <strong>14 days</strong> by default at no extra cost, so the item can be undeleted and protection resumed.",
   [("Nothing; deleted backup data can't be recovered", "soft delete keeps it for 14 days."),
    ("Restore from the VM's Activity log", "the Activity log doesn't contain backup data."),
    ("Open a support case to restore from geo-redundant storage", "you can recover yourself with undelete.")],
   [SOFTDEL], 90),

mc("MO", B,
   "<p>Management wants historical trends of backup jobs, storage consumed and policy adherence across several Recovery Services vaults, viewed in Backup reports.</p><p>What must you configure first?</p>",
   "Diagnostic settings on each vault that send backup data to a Log Analytics workspace",
   "<strong>Backup reports</strong> are built on Log Analytics. Each vault must send its backup diagnostic data (resource-specific tables) to a workspace through <strong>diagnostic settings</strong>, often at scale with Azure Policy.",
   [("Enable Cross Region Restore on every vault", "unrelated to reporting."),
    ("Create an alert processing rule", "manages alert notifications, not reports."),
    ("Export the Activity log to a storage account", "it doesn't contain backup job or storage details.")],
   [REPORTS], 90),

multi("MO", B,
   "<p>You need to restore an Azure VM from a Recovery Services vault recovery point.</p><p>Which three restore options does Azure Backup offer for Azure VMs?</p>",
   [("Create a new VM", "creates a VM from the recovery point with basic settings."),
    ("Restore disks", "restores managed disks (plus a template) that you can attach or use to customize a VM."),
    ("Replace existing", "replaces the existing VM's disks with the restored disks.")],
   "The three VM restore options are create new, restore disks, and replace existing. Cross-region and cross-subscription variants depend on vault settings.",
   [("Restore to an Azure App Service plan", "VM backups can't be restored as web apps."),
    ("Restore directly into an Azure Container Instances group", "not a supported target."),
    ("Restore the VM as a Bicep template only, with no disks", "a template alone isn't a restore option; Restore disks produces disks plus a template.")],
   [RESTORE_VM], 91),
]
