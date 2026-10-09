"""Domain 1 - Manage Azure identities and governance (20-25%)."""
from qlib import mc, multi, hot, yn, dd, code
import cases  # noqa: F401  (registers case studies)

U = "Manage Microsoft Entra users and groups"
A = "Manage access to Azure resources"
G = "Manage Azure subscriptions and governance"

L = "https://learn.microsoft.com/en-us/"
DYN = L + "entra/identity/users/groups-dynamic-membership"
GBL = L + "entra/identity/users/licensing-groups-assign"
GBL_ADV = L + "entra/identity/users/licensing-group-advanced"
GBL_FIX = L + "entra/identity/users/licensing-groups-resolve-problems"
ROLE_GRP = L + "entra/identity/role-based-access-control/groups-concept"
B2B_ALLOW = L + "entra/external-id/allow-deny-list"
B2B_SET = L + "entra/external-id/external-collaboration-settings-configure"
SSPR_HOW = L + "entra/identity/authentication/concept-sspr-howitworks"
SSPR_POL = L + "entra/identity/authentication/concept-sspr-policy"
SSPR_WB = L + "entra/identity/authentication/concept-sspr-writeback"
RESTORE = L + "entra/fundamentals/users-restore"
AU = L + "entra/identity/role-based-access-control/administrative-units"
GROUPS = L + "entra/fundamentals/concept-learn-about-groups"
ENTRA_ROLES = L + "entra/identity/role-based-access-control/permissions-reference"
MGUSER = L + "powershell/module/microsoft.graph.users/update-mguser"
BUILTIN = L + "azure/role-based-access-control/built-in-roles"
RBAC = L + "azure/role-based-access-control/overview"
SCOPE = L + "azure/role-based-access-control/scope-overview"
CUSTOM = L + "azure/role-based-access-control/custom-roles"
CUSTOM_PS = L + "azure/role-based-access-control/custom-roles-powershell"
ELEVATE = L + "azure/role-based-access-control/elevate-access-global-admin"
LIST_PS = L + "azure/role-based-access-control/role-assignments-list-powershell"
RBAC_VS = L + "azure/role-based-access-control/rbac-and-directory-admin-roles"
CHECK = L + "azure/role-based-access-control/check-access"
BLOB_DATA = L + "azure/storage/blobs/assign-azure-role-data-access"
DENY = L + "azure/role-based-access-control/deny-assignments"
POLICY = L + "azure/governance/policy/overview"
EFFECTS = L + "azure/governance/policy/concepts/effect-basics"
REMEDIATE = L + "azure/governance/policy/how-to/remediate-resources"
ASSIGN = L + "azure/governance/policy/concepts/assignment-structure"
INITIATIVE = L + "azure/governance/policy/concepts/initiative-definition-structure"
LOCKS = L + "azure/azure-resource-manager/management/lock-resources"
TAGS = L + "azure/azure-resource-manager/management/tag-resources"
TAG_POL = L + "azure/azure-resource-manager/management/tag-policies"
MOVE = L + "azure/azure-resource-manager/management/move-resource-group-and-subscription"
RG = L + "azure/azure-resource-manager/management/manage-resource-groups-portal"
MG = L + "azure/governance/management-groups/overview"
MG_MANAGE = L + "azure/governance/management-groups/manage"
BUDGET = L + "azure/cost-management-billing/costs/tutorial-acm-create-budgets"
BUDGET_AUTO = L + "azure/cost-management-billing/manage/cost-management-budget-scenario"
ADVISOR_COST = L + "azure/advisor/advisor-cost-recommendations"
ADVISOR = L + "azure/advisor/advisor-overview"
TRANSFER = L + "azure/role-based-access-control/transfer-subscription"
COST_ALERTS = L + "azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending"
COST_GROUP = L + "azure/cost-management-billing/costs/group-filter"

ITEMS = [
# ------------------------------------------------------------------ users & groups
mc("ID", U,
   "<p>Fabrikam wants every user whose <code>department</code> attribute equals <em>Finance</em> to be added to and removed from a group automatically as HR updates user records. You create a new group in Microsoft Entra ID.</p><p>Which group configuration should you use?</p>",
   "Security group with the Dynamic User membership type",
   "A dynamic user group evaluates a membership rule such as <code>(user.department -eq \"Finance\")</code> and adds or removes members as attributes change, so HR updates drive membership with no admin action. Dynamic membership requires Microsoft Entra ID P1 (or higher) licensing for the users who are in scope.",
   [("Security group with the Assigned membership type", "assigned membership is static; an administrator must add and remove members manually, which fails the 'automatically' requirement."),
    ("Security group with the Dynamic Device membership type", "dynamic device rules evaluate device attributes (for example <code>device.deviceOSType</code>), not user attributes such as department."),
    ("Microsoft 365 group with the Assigned membership type", "the group type is not the problem; assigned membership is still manual.")],
   [DYN, GROUPS], 96),

mc("ID", U,
   "<p>Litware uses group-based licensing. A group named <em>Sales-Licensed</em> is assigned a Microsoft 365 E3 license. A new user is added to the group, but the portal shows the license assignment for the user in an error state.</p><p>Which user property is most likely missing?</p>",
   "Usage location",
   "Licenses can't be assigned to a user who has no <strong>usage location</strong>, because some services are not available in every country or region. Group-based licensing reports the failure on that user; once the usage location is set, the group license is reprocessed and applied.",
   [("Job title", "job title is informational and has no effect on license assignment."),
    ("Manager", "the manager attribute is used for org charts and some workflows, not licensing."),
    ("Employee ID", "employee ID is optional metadata and is not checked when assigning licenses.")],
   [GBL_FIX, GBL], 93),

mc("ID", U,
   "<p>You plan to manage licenses for 1,200 users by using groups. The licensing team suggests assigning a license to a group named <em>All-Staff</em> whose members are the groups <em>HR</em>, <em>Sales</em>, and <em>Ops</em> (nested groups).</p><p>What will happen to the users who are members of the nested groups?</p>",
   "They will not receive the license because group-based licensing applies only to direct members",
   "Group-based licensing evaluates the <strong>direct</strong> members of the licensed group. Nested group membership isn't expanded for licensing, so users in HR, Sales, and Ops receive nothing from All-Staff. Assign the license to each group directly, or make All-Staff a dynamic group that contains the users.",
   [("They will receive the license only after a manual reprocess", "reprocessing re-evaluates direct members; it doesn't make nested membership count."),
    ("They will receive the license because licensing is inherited through nesting", "this is the common misconception the question tests; nesting is not supported for licensing."),
    ("They will receive the license only if All-Staff is a Microsoft 365 group", "the group type doesn't change the direct-member rule.")],
   [GBL_ADV, GBL], 86, conf_note="Microsoft documents this as a current limitation; it could change in a future release."),

mc("ID", U,
   "<p>You need to create a group in Microsoft Entra ID that the security team can later assign the <em>Helpdesk Administrator</em> Entra role to. Membership will be managed manually.</p><p>Which setting must be configured when the group is created?</p>",
   "Set Microsoft Entra roles can be assigned to the group to Yes",
   "Only groups created with <code>isAssignableToRole = true</code> can receive Entra role assignments. The property can be set <strong>only when the group is created</strong> and can't be changed later, which protects role-assignable groups from being taken over by lower-privileged group admins.",
   [("Set the membership type to Dynamic User", "role-assignable groups can't use dynamic membership; membership must be assigned."),
    ("Create the group as a Microsoft 365 group", "both security and Microsoft 365 groups can be role-assignable; the type alone doesn't enable it."),
    ("Add the group to an administrative unit", "administrative units scope management; they don't make a group eligible for role assignment.")],
   [ROLE_GRP], 94),

mc("ID", U,
   "<p>Tailspin Toys partners with Fabrikam and Northwind. Users should be able to invite guests from <em>fabrikam.com</em> and <em>northwind.com</em> only; invitations to any other domain must be blocked.</p><p>What should you configure?</p>",
   "Collaboration restrictions in External collaboration settings, set to allow invitations only to the specified domains",
   "External collaboration settings include <strong>collaboration restrictions</strong>, where you choose <em>Allow invitations only to the specified domains (most restrictive)</em> and list the partner domains. Invitations to any other domain are blocked at invitation time.",
   [("A Conditional Access policy that targets guest users", "Conditional Access controls sign-in conditions; it doesn't control which domains can be invited."),
    ("Guest user access restrictions set to the most restrictive level", "this limits what guests can see in the directory, not who can be invited."),
    ("A dynamic group rule that filters on the user's mail domain", "groups don't govern B2B invitations.")],
   [B2B_ALLOW, B2B_SET], 92),

mc("ID", U,
   "<p>Your organization restricts guest invitations so that only administrators and users in specific admin roles can invite external users. A project manager named Ana must be able to invite guests. You must follow the principle of least privilege.</p><p>Which Microsoft Entra role should you assign to Ana?</p>",
   "Guest Inviter",
   "The <strong>Guest Inviter</strong> role grants exactly one capability: inviting guest users, regardless of the 'members can invite' setting. It grants no other directory permissions, so it satisfies least privilege.",
   [("User Administrator", "can invite guests but also create, delete and reset passwords for users, which is far more than required."),
    ("Global Reader", "is read-only and can't invite anyone."),
    ("Application Administrator", "manages app registrations and enterprise apps, not guest invitations.")],
   [ENTRA_ROLES, B2B_SET], 92),

mc("ID", U,
   "<p>You are enabling self-service password reset (SSPR) for all users. Security requires users to prove their identity with two different methods before they can reset a password.</p><p>Which SSPR setting addresses this requirement?</p>",
   "Number of methods required to reset = 2",
   "Under <strong>Password reset › Authentication methods</strong>, <em>Number of methods required to reset</em> can be 1 or 2. Setting it to 2 forces users to pass two separate verification gates. Users must also register at least that many methods.",
   [("Number of days before users are asked to reconfirm their authentication information = 2", "this controls re-registration frequency, not how many methods are required during a reset."),
    ("Require users to register when signing in = Yes", "this forces registration but doesn't define how many methods a reset requires."),
    ("Notify all admins when other admins reset their password = Yes", "this is a notification setting and has nothing to do with verification strength.")],
   [SSPR_HOW, L + "entra/identity/authentication/tutorial-enable-sspr"], 95),

yn("ID", U,
   "<p>You enable self-service password reset (SSPR) in Contoso's tenant for a group named <em>SSPR-Pilot</em>. Some users are synchronized from on-premises Active Directory by Microsoft Entra Connect.</p><p>Evaluate each statement.</p>",
   [("Administrator accounts are subject to a separate, Microsoft-defined SSPR policy that requires two verification methods regardless of your SSPR configuration.", "Yes",
     "Admin roles always use the strong 'two-gate' administrator reset policy; your SSPR scope and method choices don't weaken it."),
    ("SSPR can be scoped to a single selected group instead of all users.", "Yes",
     "The SSPR <em>Properties</em> page offers None, Selected (one group), or All."),
    ("Synchronized users can reset their on-premises password through SSPR without enabling password writeback.", "No",
     "Password writeback (Entra Connect or Cloud Sync) is required to write the new password back to on-premises AD for hybrid users.")],
   "SSPR scoping, admin policy and writeback are independent settings. The admin policy can't be loosened by tenant settings, while writeback is the bridge for hybrid identities.",
   [SSPR_POL, SSPR_WB, SSPR_HOW], 90),

mc("ID", U,
   "<p>A cloud-only user account was deleted 12 days ago. The user returns and must keep the same object ID, group memberships, and license assignments.</p><p>What should you do?</p>",
   "Restore the user from Deleted users in Microsoft Entra ID",
   "Deleted users stay in a soft-deleted state for <strong>30 days</strong>. Restoring within that window brings back the same object, including object ID, group memberships, and licenses where possible.",
   [("Create a new user with the same user principal name", "a new account gets a new object ID and none of the previous memberships."),
    ("Restore the user from the Microsoft Entra audit log", "audit logs record the deletion but can't restore objects."),
    ("Run Microsoft Entra Connect to resynchronize the user", "this applies only to synchronized users; the user is cloud-only.")],
   [RESTORE], 95),

mc("ID", U,
   "<p>Contoso has offices in Paris and Berlin. The Paris helpdesk must be able to reset passwords only for users who work in Paris. Least privilege is required.</p><p>What should you implement?</p>",
   "An administrative unit that contains the Paris users, with the Helpdesk Administrator role assigned to the Paris helpdesk scoped to that administrative unit",
   "<strong>Administrative units</strong> restrict the scope of Entra role assignments to a subset of users, groups, or devices. Assigning Helpdesk Administrator at the AU scope lets the Paris team reset passwords for Paris users only.",
   [("A security group of Paris users with the Helpdesk Administrator role assigned to that group", "assigning a role to a group gives its members the role; it doesn't limit which users they can manage."),
    ("A management group named Paris with the User Access Administrator role", "management groups organize Azure subscriptions; they don't scope Entra directory roles."),
    ("The Helpdesk Administrator role assigned at the tenant scope with a Conditional Access policy for Paris", "tenant scope covers every user; Conditional Access doesn't restrict which accounts an admin can manage.")],
   [AU, ENTRA_ROLES], 93),

mc("ID", U,
   "<p>You use Microsoft Graph PowerShell. You need to change the <em>Department</em> attribute of user <em>megan@contoso.com</em> to <em>Logistics</em>.</p><p>Which command should you run after <code>Connect-MgGraph -Scopes User.ReadWrite.All</code>?</p>",
   "Update-MgUser -UserId megan@contoso.com -Department \"Logistics\"",
   "<code>Update-MgUser</code> is the Microsoft Graph PowerShell cmdlet that modifies properties of an existing user. <code>-UserId</code> accepts the object ID or UPN.",
   [("Set-AzADUser -UserPrincipalName megan@contoso.com -Department \"Logistics\"", "the Az module's Entra cmdlets cover a limited property set; Microsoft Graph PowerShell is the supported tool for user attribute management."),
    ("New-MgUser -UserId megan@contoso.com -Department \"Logistics\"", "<code>New-MgUser</code> creates a user; it doesn't modify an existing one."),
    ("Set-MsolUser -UserPrincipalName megan@contoso.com -Department \"Logistics\"", "the MSOnline module is retired and shouldn't be used for new automation.")],
   [MGUSER], 88, note="MSOnline and AzureAD PowerShell modules are retired; Microsoft Graph PowerShell (Mg* cmdlets) is the replacement."),

hot("ID", U,
   "<p>Contoso needs two groups:</p><ul><li><strong>GroupA</strong>: grant Contributor on an Azure resource group to 15 engineers.</li><li><strong>GroupB</strong>: give the marketing team a shared mailbox, calendar, and SharePoint site.</li></ul><p>Which group type should you create for each?</p>",
   [("GroupA", ["Security group", "Microsoft 365 group", "Distribution group"], "Security group",
     "Security groups are the standard principal for Azure RBAC and resource access."),
    ("GroupB", ["Security group", "Microsoft 365 group", "Distribution group"], "Microsoft 365 group",
     "Microsoft 365 groups provision a shared mailbox, calendar, SharePoint site and planner for collaboration.")],
   "Pick the group type by purpose: security groups for access control, Microsoft 365 groups for collaboration workloads. Distribution groups only distribute email and can't be used for Azure RBAC.",
   [GROUPS], 90),

mc("ID", U,
   "<p>A user named Ravi is synchronized from on-premises Active Directory to Microsoft Entra ID by Microsoft Entra Connect. In the Entra admin center you try to delete Ravi's account, but the delete option fails.</p><p>Where must the account be deleted?</p>",
   "In on-premises Active Directory, then allow the next synchronization cycle to remove it from Entra ID",
   "For synchronized objects, the <strong>source of authority</strong> is on-premises AD. Most attributes and the object's lifecycle must be managed there; deletion flows to Entra ID on the next sync.",
   [("In the Microsoft 365 admin center", "it reads the same Entra object, and the same source-of-authority restriction applies."),
    ("In Microsoft Entra ID, after converting the user to a guest", "converting the user type doesn't change the source of authority."),
    ("In Azure Resource Manager by using Remove-AzResource", "users aren't ARM resources.")],
   [L + "entra/identity/hybrid/connect/how-to-connect-sync-whatis"], 90),

multi("ID", U,
   "<p>You need to create 300 new cloud-only users in Microsoft Entra ID from an HR export. You want to reduce manual effort.</p><p>Which two methods can you use?</p>",
   [("Bulk create users by uploading a CSV template in the Microsoft Entra admin center", "the portal's Bulk operations › Bulk create accepts a CSV template."),
    ("A Microsoft Graph PowerShell script that loops through the CSV and calls New-MgUser", "scripting New-MgUser against the CSV rows is a standard automation path.")],
   "Both options create native cloud users at scale from the HR data.",
   [("Invite the users as B2B guests by using Bulk invite", "bulk invite creates guest accounts, not member users from your organization."),
    ("Create a dynamic user group with a rule that matches the CSV", "dynamic groups only group existing users; they don't create accounts."),
    ("Add the users to an administrative unit", "administrative units scope management of existing objects; they don't create users.")],
   [L + "entra/identity/users/users-bulk-add", L + "powershell/module/microsoft.graph.users/new-mguser"], 92),

# ------------------------------------------------------------------ RBAC
mc("ID", A,
   "<p>Operators must be able to create, start, stop, and resize virtual machines in resource group <em>RG-App</em>. They must <strong>not</strong> be able to grant access to others. You must follow least privilege.</p><p>Which built-in role should you assign at RG-App?</p>",
   "Virtual Machine Contributor",
   "<strong>Virtual Machine Contributor</strong> allows managing virtual machines, but not access to them and not the virtual network or storage account they're connected to. It doesn't include <code>Microsoft.Authorization/*/write</code>, so operators can't grant access.",
   [("Owner", "includes full management plus role assignment, which violates the requirement."),
    ("Contributor", "works but grants every resource type in the group (networks, storage, key vaults), so it isn't least privilege."),
    ("Virtual Machine Administrator Login", "grants the right to sign in to a VM's OS with Entra credentials, not to manage the VM resource.")],
   [BUILTIN], 90),

mc("ID", A,
   "<p>A security engineer must manage who has access to Azure resources in subscription <em>Sub1</em>. The engineer must not be able to create, change or delete any resources.</p><p>Which role best meets the requirement?</p>",
   "User Access Administrator",
   "<strong>User Access Administrator</strong> can manage role assignments (<code>Microsoft.Authorization/*</code>) and read resources, but it can't change resources. That matches 'manage access only'.",
   [("Owner", "grants role assignment and full resource management, which is more than allowed."),
    ("Contributor", "can manage resources but can't assign roles, which is the opposite of the requirement."),
    ("Security Admin", "is a Microsoft Defender for Cloud role for security policies and alerts, not RBAC administration.")],
   [BUILTIN, RBAC], 90, note="The newer <em>Role Based Access Control Administrator</em> role is also designed for this and can be constrained with conditions; it wasn't offered as an option here."),

mc("ID", A,
   "<p>Dana has the Contributor role on subscription <em>Sub2</em>. Dana tries to give a colleague the Reader role on a resource group in Sub2, and the operation fails with an authorization error.</p><p>Why?</p>",
   "Contributor excludes the Microsoft.Authorization write and delete actions that are required to create role assignments",
   "Contributor's definition is <code>Actions: *</code> with <code>NotActions</code> that include <code>Microsoft.Authorization/*/Write</code> and <code>Delete</code>. Creating role assignments is therefore excluded, even though Contributor can manage resources.",
   [("Role assignments can be made only at the subscription scope", "role assignments can be made at management group, subscription, resource group, or resource scope."),
    ("Dana must first activate the role in Privileged Identity Management", "nothing in the scenario says the assignment is eligible-only; it's an active Contributor assignment."),
    ("A resource lock on the resource group blocks role assignments", "locks restrict control-plane changes to resources; this failure is explained by the role definition.")],
   [BUILTIN, CUSTOM], 93),

yn("ID", A,
   "<p>User1 has the following Azure role assignments:</p><ul><li>Reader at subscription <em>Sub1</em></li><li>Contributor at resource group <em>RG1</em> (in Sub1)</li><li>No assignment at resource group <em>RG2</em> (in Sub1)</li></ul><p>Evaluate each statement.</p>",
   [("User1 can create a storage account in RG1.", "Yes", "Contributor at RG1 allows creating resources there."),
    ("User1 can view the virtual machines in RG2.", "Yes", "Reader at Sub1 is inherited by every resource group in the subscription."),
    ("User1 can stop a virtual machine in RG2.", "No", "Stopping a VM requires an action that Reader doesn't include; Contributor applies only to RG1.")],
   "Azure RBAC is additive and inherited downward: effective permissions are the union of all assignments at the resource's scope and above.",
   [SCOPE, RBAC], 95),

mc("ID", A,
   "<p>Contoso has 40 subscriptions under the management group <em>MG-Corp</em>. The audit team must be able to read every resource in all current and future subscriptions under MG-Corp with the fewest role assignments.</p><p>Where should you assign the Reader role?</p>",
   "At the MG-Corp management group",
   "Role assignments are inherited by every child scope. One assignment at MG-Corp covers all 40 subscriptions and any subscription added under it later.",
   [("At each subscription", "this works but needs 40+ assignments and misses future subscriptions."),
    ("At the Tenant Root Group", "this grants access to subscriptions outside MG-Corp, which is broader than required."),
    ("At each resource group", "this needs many assignments and misses new resource groups.")],
   [SCOPE, MG], 95),

mc("ID", A,
   "<p>A custom role definition contains <code>\"Actions\": [\"Microsoft.Compute/*\"]</code> and <code>\"NotActions\": [\"Microsoft.Compute/virtualMachines/delete\"]</code>. A user has this custom role and the built-in <em>Virtual Machine Contributor</em> role on the same resource group.</p><p>Can the user delete a VM in that resource group?</p>",
   "Yes, because NotActions only removes permissions from that role and isn't a deny; Virtual Machine Contributor grants delete",
   "<code>NotActions</code> subtracts actions from the <em>same</em> role's <code>Actions</code>; it isn't a deny assignment. Effective permissions are the union across roles, so delete is allowed through Virtual Machine Contributor.",
   [("No, because NotActions in any assigned role denies the action", "this is the misconception being tested; only deny assignments block an action granted elsewhere."),
    ("No, because custom roles take precedence over built-in roles", "there's no precedence between roles; RBAC is additive."),
    ("Yes, but only if the custom role's AssignableScopes includes the subscription", "AssignableScopes controls where a role can be assigned, not how NotActions combines with other roles.")],
   [CUSTOM, DENY], 92),

mc("ID", A,
   "<p>You are a Global Administrator in Microsoft Entra ID. You can't see any subscriptions in the Azure portal, and you need temporary access to manage role assignments in every subscription in the tenant.</p><p>What should you do first?</p>",
   "Turn on Access management for Azure resources in the Entra ID properties",
   "Entra roles and Azure roles are separate. Enabling <strong>Access management for Azure resources</strong> elevates the Global Administrator to <strong>User Access Administrator at root scope (/)</strong>, from which they can assign roles in any subscription. Microsoft recommends removing the elevation afterward.",
   [("Assign yourself the Owner role at the Tenant Root Group from the subscription's Access control (IAM) page", "you can't assign roles before you have permission on any scope; you need to elevate first."),
    ("Activate the Global Administrator role in Privileged Identity Management", "Global Administrator is a directory role and doesn't grant Azure resource permissions by itself."),
    ("Add yourself to the Subscription Owners Microsoft 365 group", "no such built-in mechanism exists; Azure access is granted through RBAC assignments.")],
   [ELEVATE, RBAC_VS], 94),

mc("ID", A,
   "<p>You need a PowerShell command that lists all Azure role assignments for user <em>kai@contoso.com</em> in the current subscription, <strong>including</strong> assignments that the user receives through group membership.</p><p>Which command should you run?</p>",
   "Get-AzRoleAssignment -SignInName kai@contoso.com -ExpandPrincipalGroups",
   "<code>-ExpandPrincipalGroups</code> makes <code>Get-AzRoleAssignment</code> return assignments made directly to the user <em>and</em> to groups the user belongs to. Without it you see direct assignments only.",
   [("Get-AzRoleAssignment -SignInName kai@contoso.com", "returns direct assignments only and misses group-based access."),
    ("Get-AzRoleDefinition -Name kai@contoso.com", "returns role definitions, not assignments, and doesn't accept a user."),
    ("Get-MgUserMemberOf -UserId kai@contoso.com", "lists group memberships, not Azure RBAC assignments.")],
   [LIST_PS], 87),

mc("ID", A,
   "<p>An analyst has the <em>Reader</em> role on storage account <em>stdata01</em>. When the analyst opens a container in the portal by using Microsoft Entra authentication, the portal says they don't have permission to list blobs.</p><p>Which role assignment resolves the issue with least privilege?</p>",
   "Storage Blob Data Reader on the container or storage account",
   "Reader is a <strong>control-plane</strong> role: it shows the account but grants no <em>data-plane</em> actions. Reading blob data with Entra authentication requires a data role such as <strong>Storage Blob Data Reader</strong>.",
   [("Storage Account Contributor", "this is control-plane management and can list keys, which grants far more than read access to data."),
    ("Storage Blob Data Owner", "grants full data access plus POSIX ACL management, so it isn't least privilege."),
    ("Reader and Data Access", "works by letting the user read account keys, which is broader than reading blob data with Entra ID.")],
   [BLOB_DATA, BUILTIN], 90),

multi("ID", A,
   "<p>You are planning Azure RBAC assignments for resource group <em>RG-Data</em>.</p><p>Which three security principals can be assigned an Azure role?</p>",
   [("A Microsoft Entra user", "users are a primary security principal type."),
    ("A Microsoft Entra security group", "assigning to groups is the recommended way to manage access at scale."),
    ("A user-assigned managed identity", "managed identities are service principals and can be assigned roles.")],
   "Azure roles can be assigned to users, groups, service principals and managed identities.",
   [("An administrative unit", "an administrative unit is a container for scoping Entra roles, not a principal."),
    ("A mail-only distribution group", "distribution groups aren't security-enabled and can't be granted access."),
    ("A resource group", "a resource group is a scope, not a principal.")],
   [RBAC, L + "azure/role-based-access-control/role-assignments"], 92),

dd("ID", A,
   "<p>You need to create a custom role named <em>VM Operator</em>, based on Virtual Machine Contributor, that can only start, restart and deallocate VMs. You will then assign it to group <em>Ops</em> at subscription Sub1 by using Azure PowerShell.</p><p>Which four actions should you perform in sequence?</p>",
   [("Run Get-AzRoleDefinition \"Virtual Machine Contributor\" to retrieve a template object", "starting from an existing definition gives you the correct object shape."),
    ("Clear Id and set Name, Description, Actions and AssignableScopes (/subscriptions/<Sub1 ID>) on the object", "a custom role needs a new name, only the required actions, and at least one assignable scope."),
    ("Run New-AzRoleDefinition -Role $role", "creates the custom role in the tenant."),
    ("Run New-AzRoleAssignment -ObjectId <Ops group ID> -RoleDefinitionName \"VM Operator\" -Scope /subscriptions/<Sub1 ID>", "assigns the new role to the group at the required scope.")],
   [("Run Set-AzRoleDefinition -Role $role", "Set-AzRoleDefinition updates an existing custom role, so you'd only use it later to change VM Operator."),
    ("Run New-AzPolicyDefinition", "Azure Policy governs resource properties, not who can perform actions.")],
   "Custom roles are defined first (definition plus AssignableScopes) and only then assigned. The role can be assigned only within its AssignableScopes.",
   [CUSTOM_PS, CUSTOM], 88),

mc("ID", A,
   "<p>A web app with a system-assigned managed identity must read secrets from Key Vault <em>kv-app</em>. The vault uses the Azure RBAC permission model.</p><p>Which role should you assign to the managed identity on kv-app?</p>",
   "Key Vault Secrets User",
   "<strong>Key Vault Secrets User</strong> grants read access to secret contents (<code>secrets/getSecret</code>), which is exactly what an app needs to fetch a secret at runtime.",
   [("Key Vault Reader", "allows reading vault metadata, not secret values."),
    ("Key Vault Contributor", "manages the vault resource (control plane) and doesn't grant data-plane access to secrets."),
    ("Key Vault Secrets Officer", "can create, update and delete secrets as well, which exceeds the requirement.")],
   [BUILTIN, L + "azure/key-vault/general/rbac-guide"], 88),

mc("ID", A,
   "<p>A user says they can't delete a resource group, even though you believe they have enough rights. You want to see the user's effective permissions on that resource group without reading every assignment manually.</p><p>What should you use?</p>",
   "The Check access feature on the resource group's Access control (IAM) page",
   "<strong>Check access</strong> evaluates a specific principal's role assignments at the selected scope, including inherited ones, and shows the roles and deny assignments that apply.",
   [("The Azure Activity log for the resource group", "shows what operations happened, not what a user is allowed to do."),
    ("Azure Advisor security recommendations", "Advisor gives best-practice recommendations, not per-user permission analysis."),
    ("The Microsoft Entra sign-in logs", "show authentication events, not Azure resource authorization.")],
   [CHECK], 90),

mc("ID", A, "<p>Refer to the case study.</p><p>You need to meet the requirement for the members of Eng-Ops. The solution must minimize the number of role assignments.</p><p>What should you do?</p>",
   "Create a custom role with start, restart, deallocate and VM size write actions; assign it to Eng-Ops at Sub-Prod",
   "No built-in role allows restart and resize while also blocking delete. A <strong>custom role</strong> with only the needed <code>Microsoft.Compute/virtualMachines/*</code> actions (start, restart, deallocate, write for size changes), assigned once to the group at the subscription, covers every VM with one assignment and excludes delete and networking.",
   [("Assign Virtual Machine Contributor to Eng-Ops at Sub-Prod", "Virtual Machine Contributor includes VM delete, which violates the requirement."),
    ("Assign Contributor to each member of Eng-Ops on each VM", "Contributor allows delete and networking changes, and per-user, per-VM assignments maximize administration."),
    ("Assign Virtual Machine Contributor to Eng-Ops at Sub-Prod and add a CanNotDelete lock to every VM", "locks block delete for everyone, including legitimate administrators, and add per-resource administration.")],
   [CUSTOM, BUILTIN], 84, case="contoso",
   conf_note="Resizing requires the write action on virtualMachines. A real deployment would narrow the role further with careful testing."),

# ------------------------------------------------------------------ governance
mc("ID", G, "<p>Refer to the case study.</p><p>You need to enforce the deployment region requirement for production. The solution must minimize administrative effort and cover subscriptions added to production later.</p><p>What should you do?</p>",
   "Assign the built-in Allowed locations policy at MG-Prod with East US and West Europe as parameters",
   "Assigning <strong>Allowed locations</strong> (Deny effect) at <strong>MG-Prod</strong> applies it to Sub-Prod and any subscription later placed in MG-Prod, while MG-Dev stays unrestricted.",
   [("Assign the Allowed locations policy at MG-Contoso", "this would also restrict MG-Dev, but development must stay unrestricted."),
    ("Assign the Allowed locations policy to each resource group in Sub-Prod", "this misses new resource groups and subscriptions and adds administrative effort."),
    ("Create a ReadOnly lock on Sub-Prod", "locks block changes but can't allow specific regions, and they'd stop all deployments.")],
   [POLICY, ASSIGN], 95, case="contoso"),

mc("ID", G,
   "<p>Every resource must carry the <em>CostCenter</em> tag of its resource group. Many existing resources lack the tag. You assign the built-in policy <em>Inherit a tag from the resource group if missing</em> at the subscription.</p><p>What else must you do so that <strong>existing</strong> resources receive the tag?</p>",
   "Create a remediation task for the policy assignment",
   "The policy uses the <strong>Modify</strong> effect. Modify acts automatically on new or updated resources, but existing non-compliant resources are changed only by a <strong>remediation task</strong>, which uses the assignment's managed identity.",
   [("Change the policy effect to Audit", "Audit only reports non-compliance; it never adds tags."),
    ("Enable tag inheritance on the resource group", "tags aren't inherited automatically, and resource groups have no such switch."),
    ("Apply a CanNotDelete lock to the resource group", "locks don't affect tagging or compliance.")],
   [TAG_POL, REMEDIATE], 93),

mc("ID", G,
   "<p>Security requires that nobody can create a storage account that allows public blob access. Requests that violate the rule must fail when they're made.</p><p>Which Azure Policy effect should the policy definition use?</p>",
   "Deny",
   "<strong>Deny</strong> evaluates the request before Resource Manager processes it and rejects non-compliant creates or updates with a 403.",
   [("Audit", "allows the request and only marks the resource non-compliant."),
    ("AuditIfNotExists", "audits for a missing related resource after deployment; it doesn't block anything."),
    ("Append", "adds fields to a request; it doesn't reject the request.")],
   [EFFECTS, POLICY], 96),

yn("ID", G,
   "<p>You assign an Azure Policy initiative to subscription <em>Sub1</em>. Evaluate each statement.</p>",
   [("You can exclude a specific resource group from the assignment.", "Yes",
     "Assignments support <code>notScopes</code> (exclusions) for child scopes."),
    ("Existing resources that violate a Deny policy in the initiative are deleted automatically.", "No",
     "Deny blocks new or updated requests; existing resources are only reported as non-compliant."),
    ("An initiative groups several policy definitions so that they can be assigned and tracked as one unit.", "Yes",
     "That is the purpose of an initiative (policy set definition).")],
   "Policy never deletes resources. Exclusions and initiatives are the main tools for scoping and grouping governance at scale.",
   [ASSIGN, INITIATIVE, EFFECTS], 94),

mc("ID", G,
   "<p>You assign a policy that uses the <em>DeployIfNotExists</em> effect to deploy the Azure Monitor agent to VMs. The remediation task fails with an authorization error.</p><p>What is the most likely cause?</p>",
   "The policy assignment's managed identity lacks the required role assignment at the target scope",
   "DeployIfNotExists and Modify run deployments through the <strong>assignment's managed identity</strong>. That identity needs the roles listed in the definition's <code>roleDefinitionIds</code> at the scope where it deploys. A missing role causes authorization failures.",
   [("DeployIfNotExists policies can't be assigned at the subscription scope", "they can be assigned at management group, subscription, or resource group scope."),
    ("You must change the effect to Audit before you run remediation", "Audit has nothing to remediate."),
    ("The VMs must be deallocated before policy can evaluate them", "evaluation and remediation don't require deallocated VMs.")],
   [REMEDIATE], 92),

mc("ID", G,
   "<p>You apply a <strong>ReadOnly</strong> lock to storage account <em>stlogs01</em>. A developer then reports that the application can no longer get the account's access keys from Resource Manager.</p><p>Why?</p>",
   "Listing keys is a POST operation, and a ReadOnly lock blocks it",
   "A ReadOnly lock permits only read (GET) operations at the management plane. <code>listKeys</code> is a <strong>POST</strong> action, so it's blocked. The portal's storage browsing may also fail when it relies on account keys.",
   [("ReadOnly locks also block all data-plane reads", "locks don't apply to the data plane; blob reads with SAS or Entra ID still work."),
    ("Locks rotate the storage account keys", "locks never change keys."),
    ("ReadOnly locks remove all RBAC role assignments on the resource", "locks don't change role assignments; they constrain operations.")],
   [LOCKS], 90),

yn("ID", G,
   "<p>Resource group <em>RG-Prod</em> contains VM1. You apply a <strong>ReadOnly</strong> lock to RG-Prod. A user with the Owner role on RG-Prod attempts the following actions. Evaluate each statement.</p>",
   [("The user can view VM1's configuration in the portal.", "Yes", "Read (GET) operations are allowed under a ReadOnly lock."),
    ("The user can start VM1.", "No", "Starting a VM is a POST action, which a ReadOnly lock blocks."),
    ("The user can remove the lock.", "Yes", "Owner includes <code>Microsoft.Authorization/locks/*</code>, so they can remove it and then make changes.")],
   "Locks override RBAC permissions for the actions they block, but users with lock permissions (Owner, User Access Administrator) can remove the lock.",
   [LOCKS], 91),

mc("ID", G,
   "<p>A resource group named <em>RG-Shared</em> has a <strong>CanNotDelete</strong> lock. An administrator with the Contributor role tries to change the size of a VM in RG-Shared and then delete a disk.</p><p>What is the result?</p>",
   "The resize succeeds and the disk deletion fails",
   "<strong>CanNotDelete</strong> allows read and modify operations but blocks deletes on the scope and its child resources. The lock is inherited from the resource group.",
   [("Both operations fail", "CanNotDelete doesn't block modifications such as resizing."),
    ("Both operations succeed because Contributor overrides the lock", "locks apply to every user regardless of role."),
    ("The resize fails and the disk deletion succeeds", "this reverses how CanNotDelete works.")],
   [LOCKS], 95),

mc("ID", G,
   "<p>Resource group <em>RG-Web</em> has the tag <code>Environment=Production</code>. You create a new web app in RG-Web without specifying tags.</p><p>Which tags does the web app have?</p>",
   "No tags",
   "Tags <strong>aren't inherited</strong> from resource groups or subscriptions. To propagate them, use Azure Policy (for example <em>Inherit a tag from the resource group</em>) or set tags at deployment time.",
   [("Environment=Production, inherited from the resource group", "this is the common misconception; inheritance requires policy."),
    ("Environment=Production, but only after the next policy evaluation", "no policy is mentioned, so nothing would add the tag."),
    ("Only tags defined at the subscription level", "subscription tags aren't inherited either.")],
   [TAGS, TAG_POL], 96),

mc("ID", G,
   "<p>Finance wants to show monthly Azure costs broken down by the value of the <em>Department</em> tag in a chart they can save and share.</p><p>What should you use?</p>",
   "Cost analysis in Microsoft Cost Management, grouped by the Department tag",
   "Cost analysis can <strong>group by</strong> a tag key and save the view. Costs are attributed to the tags present on resources when the usage occurred.",
   [("Azure Advisor cost recommendations", "Advisor suggests savings and doesn't break down spend by tag."),
    ("Azure Resource Graph Explorer", "Resource Graph queries inventory, not cost data."),
    ("Azure Monitor metrics explorer", "metrics show resource performance telemetry, not billing.")],
   [COST_GROUP], 90),

mc("ID", G,
   "<p>You move VM <em>vm-api</em> and its dependent resources from resource group <em>RG-A</em> to <em>RG-B</em> in the same subscription.</p><p>Which statement is true after the move?</p>",
   "The resource IDs of the moved resources change to include RG-B",
   "A resource ID includes the resource group name (<code>/subscriptions/{id}/resourceGroups/{rg}/providers/...</code>), so moving resources changes their IDs. Scripts, policies or alerts that reference the old IDs must be updated.",
   [("The VM's region changes to match RG-B's region", "moving between resource groups never changes a resource's region."),
    ("The VM must be deallocated permanently after the move", "moving a VM between resource groups doesn't require it to stay stopped."),
    ("Role assignments made directly on the VM move with it", "role assignments on a moved resource aren't moved; they must be recreated.")],
   [MOVE], 90),

mc("ID", G,
   "<p>You try to delete resource group <em>RG-Old</em>. The deletion fails. RG-Old contains a storage account that has a <strong>CanNotDelete</strong> lock.</p><p>What must you do to delete RG-Old?</p>",
   "Remove the lock from the storage account, then delete the resource group",
   "Deleting a resource group deletes all of its resources, and a delete lock on any one of them blocks the whole operation. Remove the lock (which needs lock permissions such as Owner) and try again.",
   [("Move the storage account to another resource group first", "moving a locked resource is also blocked."),
    ("Add a ReadOnly lock to the resource group", "adding locks makes deletion more restrictive, not less."),
    ("Use Remove-AzResourceGroup -Force", "<code>-Force</code> skips the confirmation prompt; it doesn't override locks.")],
   [LOCKS, RG], 95),

mc("ID", G,
   "<p>You need to move subscription <em>Sub-Analytics</em> from management group <em>MG-Lab</em> to <em>MG-Prod</em>.</p><p>Which permissions do you need?</p>",
   "Owner on the subscription, plus Management Group Contributor (write) on both MG-Lab and MG-Prod",
   "Moving a subscription requires write access on the subscription (for example, Owner) and management group write permissions on <strong>both</strong> the current parent and the target parent management groups.",
   [("Reader on MG-Prod only", "Reader can't change hierarchy."),
    ("Contributor on the subscription only", "permissions are also needed on the source and target management groups."),
    ("Billing account owner on the enrollment", "billing roles control invoicing, not the management group hierarchy.")],
   [MG_MANAGE], 82, conf_note="Exact role requirements have changed over time (for example, whether target-only permission is enough when moving from the root). Verify current docs."),

mc("ID", G,
   "<p>Litware's lab subscription has a monthly budget of USD 2,000. When forecast spend reaches 90%, all VMs tagged <code>Env=Lab</code> must be shut down automatically.</p><p>What should you configure?</p>",
   "A budget alert condition at 90% of forecasted cost that triggers an action group running an Automation runbook or Logic App to stop the VMs",
   "Budgets <strong>don't stop resources</strong> by themselves; they send alerts. Attaching an <strong>action group</strong> to a budget threshold lets you start automation (runbook, Logic App or function) that deallocates the tagged VMs.",
   [("A budget with a hard spending cap that deallocates resources at 90%", "Azure budgets have no hard cap; spending limits exist only on specific offer types and aren't tag-aware."),
    ("An Azure Advisor recommendation to right-size VMs", "Advisor doesn't take automatic action based on spend."),
    ("A CanNotDelete lock on the lab resource group", "locks don't control cost or stop VMs.")],
   [BUDGET, BUDGET_AUTO], 90),

mc("ID", G,
   "<p>You need a list of virtual machines that have consistently low CPU and network utilization so that you can shut them down or resize them to save money.</p><p>Which tool provides this recommendation with no additional configuration?</p>",
   "Azure Advisor cost recommendations",
   "Advisor's <strong>Cost</strong> category identifies underutilized VMs from utilization telemetry and recommends shutting them down or resizing them.",
   [("Microsoft Defender for Cloud secure score", "secure score measures security posture, not utilization."),
    ("Azure Policy compliance dashboard", "shows compliance against policies, not utilization."),
    ("Cost Management anomaly alerts", "detect unusual spend patterns, not idle resources.")],
   [ADVISOR_COST, ADVISOR], 94),

mc("ID", G,
   "<p>You plan to transfer subscription <em>Sub-Acq</em> from the Fabrikam Entra tenant to the Contoso Entra tenant.</p><p>What happens to the existing Azure role assignments in Sub-Acq?</p>",
   "They are permanently deleted and must be recreated in the new tenant",
   "When a subscription moves to a different directory, all Azure role assignments, including those for managed identities, are <strong>permanently deleted</strong>. Plan to document and recreate them after the transfer.",
   [("They are converted to guest assignments for the original users", "no automatic conversion happens."),
    ("They remain unchanged because they're stored in the subscription", "assignments reference principals in the old tenant, so they are removed."),
    ("They are moved to the root management group of the new tenant", "assignments aren't relocated.")],
   [TRANSFER], 92),

multi("ID", G,
   "<p>You are creating a new resource group named <em>RG-Payments</em>.</p><p>Which two statements about resource groups are true?</p>",
   [("A resource group stores metadata about its resources in the region you choose for the group", "the resource group location is where its metadata is stored."),
    ("A resource can belong to only one resource group at a time", "resources are in exactly one group, and they can be moved.")],
   "Resource groups are logical containers. Their location only affects metadata, and each resource belongs to exactly one group.",
   [("All resources in a resource group must be in the same region as the group", "resources in a group can be in different regions."),
    ("Resource groups can be nested inside other resource groups", "resource groups can't be nested."),
    ("Deleting a resource group leaves its resources in place", "deleting a group deletes everything in it.")],
   [RG], 94),

mc("ID", G,
   "<p>You need to ensure that no one can change the configuration of ExpressRoute circuits in subscription <em>Sub-Net</em>, including subscription Owners, while still allowing them to view the circuits.</p><p>What should you apply?</p>",
   "A ReadOnly lock on the ExpressRoute circuit resources",
   "A <strong>ReadOnly</strong> lock blocks all modify and delete operations for every user, including Owners, while still allowing reads. Owners could remove the lock, which is an intentional, auditable two-step action.",
   [("A CanNotDelete lock", "prevents deletion but still allows configuration changes."),
    ("An Azure Policy with the Audit effect", "Audit only reports and never blocks changes."),
    ("The Reader role for all users", "Owners keep their Owner assignment; adding Reader doesn't remove permissions.")],
   [LOCKS], 92),

mc("ID", G,
   "<p>You want every subscription that the company creates to automatically be placed under the <em>MG-Sandbox</em> management group instead of the root management group.</p><p>What should you configure?</p>",
   "The default management group setting in the management group hierarchy settings",
   "Hierarchy settings let you define a <strong>default management group</strong> for new subscriptions, so they land under MG-Sandbox (and its policies) instead of the root.",
   [("An Azure Policy assigned at the root that uses the Modify effect on subscriptions", "policy can't move subscriptions between management groups."),
    ("A tag on MG-Sandbox named Default=True", "tags don't change hierarchy behavior."),
    ("A ReadOnly lock on the Tenant Root Group", "management groups don't support locks, and a lock wouldn't redirect subscriptions.")],
   [MG_MANAGE, MG], 86),

mc("ID", G,
   "<p>You need to apply 50 different security policies to 12 subscriptions and report compliance for them as a single score.</p><p>What should you create and assign?</p>",
   "An initiative definition that contains the 50 policies, assigned at a management group that contains the subscriptions",
   "An <strong>initiative</strong> bundles policy definitions into one assignment with an aggregated compliance view. Assigning it at a management group covers all 12 subscriptions with one assignment.",
   [("50 individual policy assignments at each subscription", "this means 600 assignments and no single compliance view."),
    ("A custom RBAC role that contains the 50 policies", "RBAC roles define actions, not policy rules."),
    ("A resource lock with 50 conditions", "locks have no conditions and don't evaluate compliance.")],
   [INITIATIVE, POLICY], 93),

mc("ID", G,
   "<p>A team must be prevented from deploying VM sizes outside the D-series in resource group <em>RG-Batch</em>. Other resource groups must not be affected.</p><p>What should you do?</p>",
   "Assign the built-in Allowed virtual machine size SKUs policy at RG-Batch with the permitted D-series sizes",
   "<strong>Allowed virtual machine size SKUs</strong> is a built-in Deny policy. Assigning it at the resource group scope limits only RG-Batch.",
   [("Reduce the subscription vCPU quota for non-D families", "quotas are per subscription and region, so they'd affect every resource group."),
    ("Create a custom RBAC role without Microsoft.Compute/virtualMachines/write", "this would block all VM creation, not just sizes outside the D-series."),
    ("Apply a CanNotDelete lock to RG-Batch", "locks don't constrain VM size.")],
   [POLICY, L + "azure/governance/policy/samples/built-in-policies"], 92),
]
