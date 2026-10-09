"""Domain 2 - Implement and manage storage (15-20%)."""
from qlib import mc, multi, hot, yn, dd, code
import cases  # noqa: F401

A = "Configure access to storage"
S = "Configure and manage storage accounts"
F = "Configure Azure Files and Azure Blob Storage"

L = "https://learn.microsoft.com/en-us/azure/storage/"
FW = L + "common/storage-network-security"
TRUSTED = L + "common/storage-network-security-trusted-azure-services"
SAS = L + "common/storage-sas-overview"
UDSAS = L + "blobs/storage-blob-user-delegation-sas-create-cli"
SAP = L + "common/storage-stored-access-policy-define-dotnet"
SAP_REST = "https://learn.microsoft.com/en-us/rest/api/storageservices/define-stored-access-policy"
ACCT_SAS = "https://learn.microsoft.com/en-us/rest/api/storageservices/create-account-sas"
KEYS = L + "common/storage-account-keys-manage"
SHAREDKEY = L + "common/shared-key-authorization-prevent"
FILES_ID = L + "files/storage-files-active-directory-overview"
FILES_ADDS = L + "files/storage-files-identity-ad-ds-enable"
FILES_SHARE_PERM = L + "files/storage-files-identity-assign-share-level-permissions"
FILES_KERB = L + "files/storage-files-identity-auth-hybrid-identities-enable"
FILES_445 = "https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/connectivity/files-troubleshoot"
REDUND = L + "common/storage-redundancy"
CHANGE_REDUND = L + "common/redundancy-migration"
OBJREP = L + "blobs/object-replication-overview"
CMK = L + "common/customer-managed-keys-overview"
INFRA = L + "common/infrastructure-encryption-enable"
SCOPES = L + "blobs/encryption-scope-overview"
ENC = L + "common/storage-service-encryption"
AZCOPY = L + "common/storage-use-azcopy-v10"
AZCOPY_SYNC = L + "common/storage-use-azcopy-blobs-synchronize"
EXPLORER = "https://learn.microsoft.com/en-us/azure/vs-azure-tools-storage-manage-with-storage-explorer"
ACCT = L + "common/storage-account-overview"
ACCT_CREATE = L + "common/storage-account-create"
FAILOVER = L + "common/storage-disaster-recovery-guidance"
LIFECYCLE = L + "blobs/lifecycle-management-overview"
TIERS = L + "blobs/access-tiers-overview"
REHYDRATE = L + "blobs/archive-rehydrate-overview"
BLOB_SD = L + "blobs/soft-delete-blob-overview"
CONT_SD = L + "blobs/soft-delete-container-overview"
VERSIONING = L + "blobs/versioning-overview"
PITR = L + "blobs/point-in-time-restore-overview"
FILES_SNAP = L + "files/storage-snapshots-files"
FILES_SD = L + "files/storage-files-prevent-file-share-deletion"
ANON = L + "blobs/anonymous-read-access-configure"
IMMUT = L + "blobs/immutable-storage-overview"
FILES_PLAN = L + "files/storage-files-planning"
FILES_CREATE = L + "files/create-classic-file-share"

ITEMS = [
# ------------------------------------------------------------------ access
mc("ST", A, "<p>Refer to the case study.</p><p>You need to configure contosodata01 to meet the network access requirement.</p><p>Which configuration should you use?</p>",
   "Enable the Microsoft.Storage service endpoint on the App subnet; set public network access to Enabled from selected networks; add a virtual network rule for VNet-Sea/App and an IP rule for 203.0.113.0/27",
   "The storage firewall's <strong>selected networks</strong> mode combines <strong>virtual network rules</strong> (which need the Microsoft.Storage service endpoint on the subnet) and <strong>IP network rules</strong> for public ranges such as the office range. All other traffic is denied.",
   [("Set public network access to Disabled and add an IP rule for 203.0.113.0/27", "with public network access disabled, IP rules aren't evaluated, so the office would be blocked."),
    ("Enable the service endpoint on the App subnet and assign Storage Blob Data Reader to the subnet", "RBAC roles are assigned to identities, not subnets, and the firewall stays open to all networks."),
    ("Add the Seattle range 203.0.113.0/27 as an address prefix of the App subnet", "a public range can't stand in for an Azure subnet, and it doesn't configure the storage firewall.")],
   [FW], 90, case="contoso"),

mc("ST", A,
   "<p>A storage account's firewall allows only selected virtual networks. Azure Backup now can't back up Azure file shares in the account.</p><p>What should you configure on the storage account with the least effort?</p>",
   "Enable the exception that allows Azure services on the trusted services list to access the storage account",
   "The <strong>trusted Microsoft services</strong> exception lets specific first-party services, including Azure Backup, reach the account through the firewall by using strong authentication. You don't need to manage Microsoft IP ranges.",
   [("Add an IP rule for every Azure Backup public IP address", "Microsoft doesn't support allow-listing service IPs this way, and the ranges change."),
    ("Set public network access to Enabled from all networks", "this removes the firewall protection completely."),
    ("Rotate the storage account access keys", "key rotation has nothing to do with network rules.")],
   [TRUSTED, FW], 88),

mc("ST", A,
   "<p>A developer needs to give a partner time-limited read access to a single blob. Security requires that the token is signed with Microsoft Entra credentials rather than the storage account key.</p><p>Which type of SAS should the developer create?</p>",
   "User delegation SAS",
   "A <strong>user delegation SAS</strong> is signed with a user delegation key obtained with Entra ID credentials. It's the recommended, most secure SAS type, and it works only for Blob Storage (including Data Lake Storage).",
   [("Service SAS", "is signed with the storage account key."),
    ("Account SAS", "is signed with the account key and can grant access to several services."),
    ("Ad hoc SAS with a stored access policy", "stored access policies apply to service SAS, which is still key-signed.")],
   [SAS, UDSAS], 95),

mc("ST", A,
   "<p>You issued 200 service SAS tokens for container <em>invoices</em>. All of them reference a stored access policy named <em>partner-read</em>. A partner's tokens have leaked.</p><p>What should you do to revoke all 200 tokens with the least impact on other applications?</p>",
   "Delete or change the expiry of the partner-read stored access policy",
   "A service SAS associated with a <strong>stored access policy</strong> inherits its start time, expiry and permissions from the policy. Deleting the policy, or changing its identifier or expiry, immediately invalidates every SAS that references it, without touching the account keys that other apps use.",
   [("Regenerate both storage account access keys", "this revokes the tokens but also breaks every other app and SAS that relies on those keys."),
    ("Delete the invoices container", "this is destructive and unnecessary."),
    ("Enable soft delete for blobs", "soft delete protects data and doesn't affect SAS validity.")],
   [SAP, SAS], 94),

mc("ST", A,
   "<p>An account SAS signed with <em>key1</em> was accidentally published. No stored access policy was used.</p><p>How can you invalidate the SAS?</p>",
   "Regenerate key1",
   "An ad hoc SAS can't be revoked individually. The only way to invalidate it before it expires is to <strong>regenerate the key that signed it</strong>. Apps using key1 must switch to key2 first to avoid an outage.",
   [("Create a stored access policy with the same name as the SAS", "account SAS tokens can't be linked to stored access policies."),
    ("Delete the SAS from the storage account's Shared access signature page", "SAS tokens aren't stored in Azure, so there's nothing to delete."),
    ("Change the storage account's default access tier", "the access tier doesn't affect authorization.")],
   [SAS, KEYS], 93),

yn("ST", A, "<p>Evaluate each statement about shared access signatures (SAS) and stored access policies.</p>",
   [("An account SAS can grant access to resources in more than one storage service, such as Blob and Queue.", "Yes",
     "The <code>ss</code> field of an account SAS lists the services, for example <code>ss=bq</code>."),
    ("A user delegation SAS can grant access to an Azure Files share.", "No",
     "User delegation SAS is supported only for Blob Storage and Data Lake Storage."),
    ("A container can have up to five stored access policies at a time.", "Yes",
     "A container, share, queue or table supports a maximum of five stored access policies.")],
   "Know which SAS types exist, what signs each one, and the hard limits on stored access policies.",
   [SAS, SAP_REST, ACCT_SAS], 92),

hot("ST", A,
   "<p>A developer gives you this SAS token query string:</p>"
   + code("sv=2022-11-02&ss=b&srt=co&sp=rl&se=2026-12-31T23:00:00Z&spr=https&sig=...")
   + "<p>Select the correct answer for each row.</p>",
   [("Services the token can access", ["Blob only", "Blob and File", "All storage services"], "Blob only", "<code>ss=b</code> limits the account SAS to the Blob service."),
    ("Permissions granted", ["Read and list", "Read, write and list", "Read only"], "Read and list", "<code>sp=rl</code> means read (r) and list (l)."),
    ("Protocols allowed", ["HTTPS only", "HTTP and HTTPS", "HTTP only"], "HTTPS only", "<code>spr=https</code> rejects plain HTTP.")],
   "The presence of <code>ss</code> and <code>srt</code> identifies this as an account SAS. <code>srt=co</code> scopes it to container- and object-level APIs.",
   [ACCT_SAS, SAS], 93),

dd("ST", A,
   "<p>Application <em>App1</em> connects to storage account <em>st1</em> by using key1. You must rotate both keys without downtime.</p><p>Which three actions should you perform in sequence?</p>",
   [("Update App1 to use key2", "move the app off the key you're about to regenerate."),
    ("Regenerate key1", "key1 is now unused, so regenerating it causes no outage."),
    ("Update App1 to use the new key1, then regenerate key2", "completes the rotation so both keys are new.")],
   [("Regenerate both keys at the same time", "the app would lose access until it's reconfigured."),
    ("Disable shared key access on st1", "this blocks key-based access completely, so App1 would fail.")],
   "Two access keys exist precisely so that you can rotate one while the other is in use. Storing keys in Key Vault and using Entra ID or managed identities reduces how often you need to rotate.",
   [KEYS], 95),

mc("ST", A,
   "<p>Security requires that every request to storage account <em>stfin01</em> is authorized with Microsoft Entra ID. Requests that use account keys or SAS tokens signed with account keys must fail.</p><p>What should you configure?</p>",
   "Set Allow storage account key access to Disabled",
   "Disallowing <strong>Shared Key authorization</strong> (<code>AllowSharedKeyAccess = false</code>) makes the account reject requests signed with the account key, including account and service SAS. User delegation SAS still works because it's backed by Entra ID.",
   [("Set the minimum TLS version to 1.2", "this enforces transport security, not the authorization method."),
    ("Enable infrastructure encryption", "this adds a second encryption layer at rest and has nothing to do with authorization."),
    ("Disable anonymous blob access", "this blocks unauthenticated reads but still allows Shared Key.")],
   [SHAREDKEY], 92),

mc("ST", A,
   "<p>Contoso's users are synchronized from on-premises AD DS. Domain-joined Windows clients must mount an Azure file share by using their existing AD credentials, and NTFS permissions must be enforced.</p><p>What should you do first?</p>",
   "Enable AD DS authentication on the storage account by joining it to the on-premises domain",
   "For on-premises AD DS identities, you enable <strong>AD DS authentication</strong> for Azure Files (for example, with the AzFilesHybrid module), which creates a computer or service account for the storage account in AD. You then assign share-level RBAC roles and configure NTFS ACLs.",
   [("Assign the Storage Blob Data Contributor role to the users", "blob data roles don't apply to SMB access to Azure Files."),
    ("Generate a SAS token for the share and distribute it to users", "SMB mounts don't use SAS, and SAS doesn't enforce NTFS ACLs."),
    ("Enable Microsoft Entra Domain Services in a new forest", "possible in other designs, but unnecessary when on-premises AD DS already exists.")],
   [FILES_ADDS, FILES_ID], 90),

mc("ST", A,
   "<p>Identity-based authentication is configured for an Azure file share. Members of group <em>Finance</em> must read, write and delete files in the share, but must not change NTFS permissions.</p><p>Which share-level role should you assign?</p>",
   "Storage File Data SMB Share Contributor",
   "<strong>Storage File Data SMB Share Contributor</strong> allows read, write and delete over SMB. <em>Elevated Contributor</em> adds the right to modify Windows ACLs, which isn't wanted here.",
   [("Storage File Data SMB Share Elevated Contributor", "it also allows modifying NTFS permissions."),
    ("Storage File Data SMB Share Reader", "read-only, so writes and deletes fail."),
    ("Storage Account Contributor", "a control-plane role that doesn't grant SMB data access through identity auth.")],
   [FILES_SHARE_PERM], 93),

mc("ST", A,
   "<p>Remote users have hybrid identities and Microsoft Entra joined Windows 11 devices with no line of sight to domain controllers. They must access an Azure file share with their identities and Kerberos.</p><p>Which identity source should you enable for Azure Files?</p>",
   "Microsoft Entra Kerberos",
   "<strong>Microsoft Entra Kerberos</strong> lets Entra ID issue Kerberos tickets for Azure Files, so Entra joined clients can access shares without contacting a domain controller. It's designed for hybrid user identities.",
   [("On-premises AD DS authentication", "clients need line of sight to domain controllers to get Kerberos tickets."),
    ("Microsoft Entra Domain Services", "requires clients joined to the managed domain."),
    ("Storage account key with net use", "this is key-based, not identity-based.")],
   [FILES_KERB, FILES_ID], 84, conf_note="Support for cloud-only identities with Entra Kerberos has been changing; the item assumes hybrid identities as documented."),

mc("ST", A,
   "<p>Home-office users can't mount an Azure file share over SMB from their computers. Other HTTPS traffic to Azure works. Their ISP is known to filter some ports.</p><p>Which port is most likely blocked?</p>",
   "TCP 445",
   "SMB uses <strong>TCP 445</strong>. Many ISPs and organizations block outbound 445. Workarounds include point-to-site or site-to-site VPN, ExpressRoute, or Azure File Sync to a local server.",
   [("TCP 443", "HTTPS works, so 443 isn't blocked; REST access to Files uses 443, but SMB mounts don't."),
    ("TCP 3389", "this is RDP and unrelated to SMB."),
    ("UDP 137", "NetBIOS name service isn't used to mount Azure file shares.")],
   [FILES_445], 93),

# ------------------------------------------------------------------ accounts
mc("ST", S,
   "<p>A storage account must keep data available if an availability zone fails, keep a copy in a secondary region, and let applications <strong>read</strong> from the secondary region even before a failover.</p><p>Which redundancy option should you choose?</p>",
   "Read-access geo-zone-redundant storage (RA-GZRS)",
   "<strong>RA-GZRS</strong> replicates synchronously across three zones in the primary region (zone resilience), asynchronously to a secondary region, and exposes a read-only secondary endpoint at all times.",
   [("Geo-redundant storage (GRS)", "the primary uses LRS, so a zone failure can affect it, and the secondary isn't readable before failover."),
    ("Zone-redundant storage (ZRS)", "has no secondary region."),
    ("Read-access geo-redundant storage (RA-GRS)", "the secondary is readable, but the primary is LRS, so it isn't zone resilient.")],
   [REDUND], 96),

mc("ST", S,
   "<p>A log-processing workload needs its storage account to survive the failure of a single datacenter (zone) in the region. Geographic replication isn't required, and cost must be minimized.</p><p>Which redundancy option should you choose?</p>",
   "Zone-redundant storage (ZRS)",
   "<strong>ZRS</strong> synchronously copies data across three availability zones in one region. That's the cheapest option that survives a zone failure.",
   [("Locally redundant storage (LRS)", "keeps three copies in a single datacenter, so a zone failure can make data unavailable."),
    ("Geo-zone-redundant storage (GZRS)", "meets the requirement but adds secondary-region cost that isn't needed."),
    ("Geo-redundant storage (GRS)", "adds a secondary region but still uses LRS in the primary.")],
   [REDUND], 95),

hot("ST", S, "<p>For each redundancy option, select the correct value.</p>",
   [("Number of copies of the data kept by LRS", ["3", "6", "2"], "3", "LRS stores three copies within a single datacenter in the primary region."),
    ("Total number of copies kept by GRS", ["6", "3", "9"], "6", "Three copies with LRS in the primary region plus three with LRS in the secondary region."),
    ("ZRS distributes its copies across", ["Three availability zones", "Two regions", "Three racks in one datacenter"], "Three availability zones", "ZRS replicates synchronously across three zones in the primary region.")],
   "Remembering 3 copies per region and where they live answers most redundancy questions.",
   [REDUND], 94),

mc("ST", S,
   "<p>An existing StorageV2 account in a region that supports availability zones uses LRS. You must change it to ZRS with minimal administrative effort and no application changes.</p><p>What should you do?</p>",
   "Request a conversion to ZRS from the account's Redundancy settings (customer-initiated conversion)",
   "Azure supports <strong>customer-initiated conversion</strong> from LRS to ZRS for supported accounts. The account name, endpoints and keys stay the same, so applications don't change.",
   [("Create a new ZRS account and copy the data with AzCopy", "this works but changes endpoints and adds effort; it's a fallback when conversion isn't supported."),
    ("Enable object replication to a ZRS account", "this copies blobs to another account; it doesn't change this account's redundancy."),
    ("Change the access tier from Hot to Cool", "the access tier is unrelated to redundancy.")],
   [CHANGE_REDUND], 80, conf_note="Conversion support depends on account type, region and features in use; check the current redundancy migration guidance."),

mc("ST", S,
   "<p>A compliance team plans to move rarely read blobs to the <strong>Archive</strong> tier. You're creating the storage account now.</p><p>Which redundancy setting supports the Archive tier?</p>",
   "Geo-redundant storage (GRS)",
   "The Archive tier is supported for <strong>LRS, GRS and RA-GRS</strong> accounts. It isn't supported for ZRS, GZRS or RA-GZRS.",
   [("Zone-redundant storage (ZRS)", "Archive isn't supported on ZRS."),
    ("Geo-zone-redundant storage (GZRS)", "Archive isn't supported on GZRS."),
    ("Read-access geo-zone-redundant storage (RA-GZRS)", "Archive isn't supported on RA-GZRS.")],
   [TIERS], 88),

mc("ST", S,
   "<p>You plan to configure object replication from storage account <em>stsrc</em> (East US) to <em>stdst</em> (West US).</p><p>Which configuration is required?</p>",
   "Blob versioning on both accounts, and change feed on the source account",
   "Object replication requires <strong>blob versioning</strong> on the source and destination accounts and <strong>blob change feed</strong> on the source account. Replication is asynchronous and works for block blobs.",
   [("Geo-redundant storage on both accounts", "redundancy setting isn't a prerequisite."),
    ("A private endpoint on the destination account", "network isolation isn't required for object replication."),
    ("Hierarchical namespace on both accounts", "object replication isn't supported when hierarchical namespace is enabled.")],
   [OBJREP], 92),

mc("ST", S,
   "<p>You configure a storage account to encrypt data with a customer-managed key stored in Azure Key Vault <em>kv-cmk</em>. The configuration fails validation.</p><p>Which Key Vault setting is most likely missing?</p>",
   "Soft delete and purge protection",
   "Customer-managed keys for Azure Storage require the key vault (or managed HSM) to have <strong>soft delete and purge protection</strong> enabled. This prevents the key from being permanently deleted, which would make the data unreadable.",
   [("A private endpoint for the key vault", "useful for network isolation but not required for CMK."),
    ("The Premium SKU of Key Vault", "Standard vaults support software-protected RSA keys for CMK."),
    ("An access policy that grants the Storage Account Contributor role", "the storage account's managed identity needs key permissions such as get, wrapKey and unwrapKey, not this role.")],
   [CMK], 91),

mc("ST", S,
   "<p>Regulations require two layers of encryption at rest for a new storage account, using two different algorithms and keys.</p><p>When must you enable infrastructure encryption?</p>",
   "When you create the storage account",
   "<strong>Infrastructure encryption</strong> adds a second layer of 256-bit AES encryption at the infrastructure level. It can be enabled <strong>only at account creation</strong> and can't be turned on later.",
   [("At any time from the Encryption page", "it can't be enabled after creation."),
    ("After you switch to customer-managed keys", "infrastructure encryption is independent of the key type."),
    ("Only when the account uses the Premium performance tier", "it's supported on Standard general-purpose v2 accounts too.")],
   [INFRA], 93),

mc("ST", S,
   "<p>A multitenant SaaS application stores each customer's blobs in a separate container in one storage account. Each customer's data must be encrypted with a different key.</p><p>What should you use?</p>",
   "Encryption scopes assigned per container",
   "<strong>Encryption scopes</strong> let you encrypt at the container or blob level with different keys (Microsoft-managed or customer-managed) in the same account.",
   [("A separate customer-managed key for the whole account per customer", "an account can use only one account-level key."),
    ("Infrastructure encryption", "adds a second encryption layer but doesn't provide per-container keys."),
    ("Stored access policies on each container", "these control SAS authorization, not encryption keys.")],
   [SCOPES, ENC], 92),

mc("ST", S,
   "<p>Each night you must copy only new and changed files from <code>D:\\Exports</code> on a server to container <em>exports</em>, and delete blobs whose source files were deleted.</p><p>Which AzCopy command should you use?</p>",
   "azcopy sync \"D:\\Exports\" \"https://st1.blob.core.windows.net/exports?<SAS>\" --delete-destination=true",
   "<code>azcopy sync</code> compares the source and destination by last-modified time and transfers only differences. <code>--delete-destination=true</code> removes destination blobs that no longer exist at the source.",
   [("azcopy copy \"D:\\Exports\" \"https://st1.blob.core.windows.net/exports?<SAS>\" --recursive", "copies everything every time and never deletes destination blobs."),
    ("azcopy remove \"https://st1.blob.core.windows.net/exports?<SAS>\" --recursive", "deletes data and doesn't upload anything."),
    ("azcopy make \"https://st1.blob.core.windows.net/exports?<SAS>\"", "creates a container and doesn't transfer files.")],
   [AZCOPY_SYNC, AZCOPY], 92),

mc("ST", S,
   "<p>An external auditor uses Azure Storage Explorer. The auditor must be able to view and download blobs in one container for seven days, with no access to anything else in the account and no Entra account in your tenant.</p><p>What should you give the auditor?</p>",
   "A SAS URL for the container with read and list permissions that expires in seven days",
   "Storage Explorer can attach to a resource with a <strong>SAS URL</strong>. A container-scoped SAS with <code>rl</code> permissions and a seven-day expiry gives exactly the required access and expires on its own.",
   [("The storage account access key", "grants full access to the whole account and never expires."),
    ("The connection string for the storage account", "contains the account key, so it's the same problem."),
    ("Reader role on the storage account", "it's control-plane only, and the auditor has no identity in your tenant.")],
   [EXPLORER, SAS], 92),

mc("ST", S,
   "<p>You need Azure file shares that provide consistent low latency and provisioned IOPS on SSD storage for a database workload that uses SMB.</p><p>Which storage account type should you create?</p>",
   "Premium FileStorage account",
   "Premium (SSD) file shares are hosted in the <strong>FileStorage</strong> account kind with the Premium performance tier.",
   [("Standard general-purpose v2 account", "provides HDD-based standard file shares."),
    ("Premium BlockBlobStorage account", "designed for premium block blobs, not file shares."),
    ("Premium page blobs account", "used for page blobs such as unmanaged disks.")],
   [FILES_PLAN, ACCT], 92),

mc("ST", S,
   "<p>You're creating a new storage account with Azure PowerShell.</p><p>Which name is valid?</p>",
   "contosologs2026",
   "Storage account names must be <strong>3–24 characters</strong>, contain <strong>only lowercase letters and numbers</strong>, and be globally unique because they form the endpoint DNS name.",
   [("Contoso-Logs-2026", "contains uppercase letters and hyphens."),
    ("contoso_logs", "underscores aren't allowed."),
    ("contosologsarchiveprimary2026", "it's 29 characters, which is longer than the 24-character limit.")],
   [ACCT_CREATE, ACCT], 96),

mc("ST", S,
   "<p>A GRS storage account's primary region has a prolonged outage, and you start a customer-managed (unplanned) failover to the secondary region.</p><p>After the failover completes, what is the redundancy of the account?</p>",
   "Locally redundant storage (LRS) in the new primary region",
   "After an unplanned failover, the former secondary becomes the primary and the account is <strong>LRS</strong>. You must reconfigure geo-redundancy to protect it again.",
   [("GRS, with the original primary as the new secondary", "geo-replication isn't automatically restored after an unplanned failover."),
    ("ZRS in the new primary region", "failover doesn't change the account to ZRS."),
    ("RA-GRS with read access to the original region", "the original region isn't serving as a secondary.")],
   [FAILOVER], 82, conf_note="Planned failovers behave differently (redundancy is kept). This item covers unplanned failover only."),

# ------------------------------------------------------------------ files & blob
hot("ST", F,
   "<p>You need a lifecycle management rule for block blobs under the <code>logs/</code> prefix. Blobs move to Cool 30 days after last modification, move to Archive after 90 days, and are deleted after 365 days. Complete the policy.</p>"
   + code('''{
  "rules": [{
    "name": "logs-retention",
    "enabled": true,
    "type": "Lifecycle",
    "definition": {
      "filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["logs/"] },
      "actions": {
        "baseBlob": {
          "[Box 1]": { "daysAfterModificationGreaterThan": 30 },
          "[Box 2]": { "daysAfterModificationGreaterThan": 90 },
          "[Box 3]": { "daysAfterModificationGreaterThan": 365 }
        }
      }
    }
  }]
}''', "json"),
   [("Box 1", ["tierToCool", "tierToArchive", "delete", "enableAutoTierToHotFromCool"], "tierToCool", "Moves blobs to the Cool tier at 30 days."),
    ("Box 2", ["tierToCool", "tierToArchive", "delete", "enableAutoTierToHotFromCool"], "tierToArchive", "Moves blobs to the Archive tier at 90 days."),
    ("Box 3", ["tierToCool", "tierToArchive", "delete", "enableAutoTierToHotFromCool"], "delete", "Deletes blobs at 365 days.")],
   "Lifecycle actions under <code>baseBlob</code> are tierToCool, tierToCold, tierToArchive and delete, each with an age condition. Filters narrow the rule by blob type and prefix.",
   [LIFECYCLE], 94),

mc("ST", F,
   "<p>You want a lifecycle rule that moves blobs to Cool when they haven't been <strong>read</strong> for 60 days, regardless of when they were last modified. The rule is accepted, but nothing ever moves.</p><p>What should you enable?</p>",
   "Last access time tracking on the storage account",
   "Conditions based on <code>daysAfterLastAccessTimeGreaterThan</code> require <strong>last access time tracking</strong> to be enabled on the account. Without it, Azure doesn't record read times.",
   [("Blob versioning", "versioning keeps previous versions and doesn't record access times."),
    ("Change feed", "records changes, not reads."),
    ("Hierarchical namespace", "isn't related to lifecycle access-time conditions.")],
   [LIFECYCLE], 90),

mc("ST", F,
   "<p>A 2 GB blob in the Archive tier is needed for a legal request within the next hour.</p><p>What should you do?</p>",
   "Change the blob's tier to Hot with the rehydrate priority set to High",
   "Archived blobs are offline. <strong>Rehydration</strong> by changing the tier (or copying to an online tier) is required. <strong>High</strong> priority can complete in under an hour for objects smaller than 10 GB, while Standard priority can take up to 15 hours.",
   [("Download the blob directly from the Archive tier", "archived data can't be read until it's rehydrated."),
    ("Change the blob's tier to Cool with Standard priority", "standard rehydration can take up to 15 hours."),
    ("Create a snapshot of the archived blob and read the snapshot", "snapshots of archived blobs are also offline.")],
   [REHYDRATE], 92),

mc("ST", F,
   "<p>A blob was moved to the Archive tier and then deleted 60 days later.</p><p>What happens from a billing perspective?</p>",
   "An early deletion charge applies for the remaining 120 days of the 180-day minimum",
   "The Archive tier has a <strong>180-day</strong> minimum storage duration (Cool is 30 days and Cold is 90). Deleting or moving the blob earlier incurs a prorated early deletion charge for the remaining days.",
   [("No charge, because Archive storage is billed per read", "Archive is billed for storage, with retrieval costs as well."),
    ("A charge for the remaining 30 days of a 90-day minimum", "these numbers belong to the Cold tier and don't apply here."),
    ("The deletion is blocked until 180 days have passed", "early deletion is allowed; it's charged, not blocked.")],
   [TIERS], 92),

mc("ST", F,
   "<p>An application sometimes overwrites blobs with corrupt data. You must be able to restore the previous state of any blob after an overwrite. The fix should be automatic, with no application changes.</p><p>What should you enable?</p>",
   "Blob versioning",
   "With <strong>blob versioning</strong>, every write creates a new version and the previous version is kept automatically. You can promote an earlier version to restore the data.",
   [("Container soft delete", "protects against container deletion, not blob overwrites."),
    ("A time-based immutability policy", "would block the application's legitimate writes."),
    ("Last access time tracking", "only records reads.")],
   [VERSIONING, BLOB_SD], 92),

mc("ST", F,
   "<p>An administrator accidentally deleted container <em>contracts</em> four days ago. Container soft delete is enabled with a 14-day retention period.</p><p>What should you do?</p>",
   "Restore the container from the list of deleted containers in the portal or by using the Restore container API",
   "With <strong>container soft delete</strong>, a deleted container and its contents are kept for the retention period and can be restored. Restoring brings back the container and all its blobs.",
   [("Restore each blob with the Undelete Blob operation", "blob soft delete doesn't cover blobs inside a deleted container."),
    ("Recover the container from the account's object replication destination", "no replication is mentioned, and it isn't a restore feature."),
    ("Open a support case; deleted containers can't be restored", "restoration is possible because soft delete was enabled.")],
   [CONT_SD], 93),

yn("ST", F, "<p>You protect Azure file share <em>finance</em> by using share snapshots and soft delete. Evaluate each statement.</p>",
   [("Share snapshots are read-only, incremental copies of the share.", "Yes", "Snapshots capture the share at a point in time and store only changed data."),
    ("Soft delete for Azure file shares is configured at the storage account level and applies to all file shares in the account.", "Yes", "The setting and its retention period are configured per storage account."),
    ("You can restore an individual file from a share snapshot.", "Yes", "Individual files or the whole share can be restored from a snapshot, including through Previous Versions in Windows.")],
   "Snapshots protect against corruption and accidental changes. Soft delete protects against deletion of the whole share.",
   [FILES_SNAP, FILES_SD], 88),

mc("ST", F,
   "<p>A marketing site must let anonymous users read individual images in container <em>public-img</em> by URL. Anonymous users must <strong>not</strong> be able to list the container's contents. Anonymous access is currently disallowed on the storage account.</p><p>What should you do?</p>",
   "Allow blob anonymous access on the storage account, then set the container's access level to Blob",
   "Anonymous access must first be <strong>allowed at the account level</strong>. The container access level <strong>Blob</strong> allows anonymous reads of blobs, while <strong>Container</strong> would also allow listing.",
   [("Set the container's access level to Container", "this also allows anonymous listing."),
    ("Set the container's access level to Private", "this blocks all anonymous access."),
    ("Create a stored access policy with read permissions", "SAS tokens require a signed token in the URL, which isn't anonymous access.")],
   [ANON], 93),

mc("ST", F,
   "<p>Financial records in container <em>ledger</em> must not be modified or deleted for seven years after they're written, and even account administrators must not be able to shorten that period once it's locked.</p><p>What should you configure?</p>",
   "A locked time-based retention immutability policy of seven years on the container",
   "A <strong>time-based retention policy</strong> puts blobs in a WORM (write once, read many) state for the specified interval. Once <strong>locked</strong>, the policy's retention period can't be shortened, which meets SEC-style compliance requirements.",
   [("A legal hold on the container", "legal holds have no time period and are cleared manually."),
    ("A CanNotDelete resource lock on the storage account", "management-plane locks don't stop data-plane writes or deletes of blobs."),
    ("Blob soft delete with 365-day retention", "soft delete allows modification and has a maximum retention of 365 days.")],
   [IMMUT], 92),

multi("ST", F,
   "<p>You need to enable point-in-time restore for block blobs in storage account <em>st-orders</em>.</p><p>Which three features must be enabled?</p>",
   [("Blob soft delete", "required because restore relies on soft-deleted data."),
    ("Blob versioning", "required to track blob changes."),
    ("Blob change feed", "required to know which changes to reverse.")],
   "Point-in-time restore needs soft delete, versioning and change feed. The restore retention period must be shorter than the soft delete retention period.",
   [("Container soft delete", "useful, but not a prerequisite for point-in-time restore."),
    ("Hierarchical namespace", "point-in-time restore isn't supported on accounts with hierarchical namespace."),
    ("Geo-redundant storage", "redundancy isn't a prerequisite.")],
   [PITR], 91),

mc("ST", F,
   "<p>You need to create a 2 TiB SMB file share named <em>projects</em> in storage account <em>stcorp</em> by using Azure PowerShell.</p><p>Which cmdlet should you use?</p>",
   "New-AzRmStorageShare -ResourceGroupName rg1 -StorageAccountName stcorp -Name projects -QuotaGiB 2048",
   "<code>New-AzRmStorageShare</code> creates a file share through the Azure Resource Manager (Microsoft.Storage) provider. <code>-QuotaGiB</code> sets the share size.",
   [("New-AzStorageContainer -Name projects -Context $ctx", "creates a blob container, not a file share."),
    ("New-AzStorageAccount -Name projects -Kind FileStorage", "creates a storage account, not a share."),
    ("New-AzStorageQueue -Name projects -Context $ctx", "creates a queue.")],
   [FILES_CREATE, "https://learn.microsoft.com/en-us/powershell/module/az.storage/new-azrmstorageshare"], 90),

mc("ST", F,
   "<p>Users report that a 30 GB file share named <em>scans</em> on a standard (pay-as-you-go) account returns 'disk full' errors. Usage is at 30 GiB.</p><p>What should you do?</p>",
   "Increase the share's quota",
   "Standard file shares enforce the configured <strong>quota</strong> as the maximum size. Raising the quota, up to the account's limit, immediately adds capacity, and you pay only for used capacity on pay-as-you-go standard shares.",
   [("Change the storage account redundancy to ZRS", "redundancy doesn't change capacity."),
    ("Enable large file shares on the storage account and change the share to Premium", "a standard share can't be converted to Premium in place, and the issue is just the quota."),
    ("Create a share snapshot", "snapshots don't add capacity.")],
   [FILES_CREATE, FILES_PLAN], 86),
]
