# Security Notes

Microsoft Sentinel, KQL, Entra ID, and Microsoft Graph, from The Ward and The Ascent.

## The detection pipeline

```text
Entra role assignment
  -> AuditLogs (needs a tenant diagnostic setting to the workspace)
  -> Scheduled analytics rule (every 15 min, 30 min lookback)
  -> Incident (alerts grouped by Account entity)
  -> Automation rule (scoped to this analytics rule's ID)
  -> Playbook (Logic App, system-assigned managed identity)
  -> Watchlist check, then Graph PATCH accountEnabled=false, then incident comment
```

When it doesn't fire, check each arrow in order. The most common gaps: no diagnostic setting, a new route that hasn't started sending yet (up to three days), a missing entity mapping, or Sentinel lacking permission to run the playbook.

## KQL

T1098.003, role assignment to a high-impact role. Full query: [The Ascent detection](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel/blob/main/bicep/detection/T1098.003_privilege_escalation_detection.kql)

```kusto
AuditLogs
| where OperationName in ("Add member to role", "Add eligible member to role")
| extend TargetUser = tostring(TargetResources[0].userPrincipalName)
| extend TargetResourceId = tostring(TargetResources[0].id)
| mv-expand ModifiedProps = TargetResources[0].modifiedProperties
| where tostring(ModifiedProps.displayName) == "Role.DisplayName"
| extend RoleAssigned = tostring(ModifiedProps.newValue)
| where RoleAssigned has_any ("Global Administrator", "Privileged Role Administrator", "Security Administrator")
```

Is data arriving at all?

```kusto
AuditLogs
| summarize Rows = count(), Latest = max(TimeGenerated)
```

Ingestion delay for one event:

```kusto
AuditLogs
| where CorrelationId == "<id>"
| project TimeGenerated, ingestion_time()
```

Why two incidents? Compare the alerts' query windows:

```kusto
SecurityAlert
| where AlertName == "<rule name>"
| project TimeGenerated, StartTime, EndTime, SystemAlertId
```

## Entra and Graph

Grant a managed identity a Graph application permission (no portal button for this):

```powershell
Connect-MgGraph -TenantId (Get-AzContext).Tenant.Id -Scopes "Application.Read.All","AppRoleAssignment.ReadWrite.All"
$graph = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"
$role  = $graph.AppRoles | Where-Object Value -eq "User.EnableDisableAccount.All"
New-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $miId -PrincipalId $miId -ResourceId $graph.Id -AppRoleId $role.Id
```

Check before granting, so the script is safe to re-run: `Get-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $miId`.

Find who holds a directory role:

```powershell
$ga = "62e90394-69f5-4237-9190-012177145e10"   # Global Administrator template ID, same in every tenant
Get-MgRoleManagementDirectoryRoleAssignment -Filter "roleDefinitionId eq '$ga'"
```

- Always pass `-TenantId`. Without it, a personal Microsoft account can land in its own empty tenant.
- Object ID is what RBAC checks. Application ID is for authentication. Both belong to the same identity.

## Least privilege used

| Identity | Permission | Scope |
| --- | --- | --- |
| Playbook managed identity | Graph `User.EnableDisableAccount.All`, `User.Read.All` | Tenant |
| Playbook managed identity | Microsoft Sentinel Responder | The workspace only |
| Azure Security Insights (Sentinel) | Microsoft Sentinel Automation Contributor | The playbook's resource group |

## Break-glass design

- Keep two emergency-access accounts with Global Administrator, excluded from automation, not from detection.
- The playbook looks the target up in the `AutomationExclusions` watchlist. On a match it comments and asks for human review instead of disabling.
- A role change on a break-glass account should raise severity, not lower it.

## Test hygiene

- Use a throwaway test account with no groups, apps, or licenses.
- Write the cleanup before running the test: remove the role, re-enable the account, re-enable any automation rule you turned off.
- Turn off the other system's automation rule when testing a rebuild, so you know which one responded.
- Proof is the Entra audit log entry (`Disable account`, initiated by the playbook identity), not the Logic App run status.
