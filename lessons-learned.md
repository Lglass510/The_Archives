# Lessons Learned

Lessons from across The Realm, grouped by topic. Each one links to the write-up where it happened, which has the commands, errors, and evidence.

## Verification

- **A green run isn't proof the action happened.** The Ward's first playbook reported *Succeeded* on every run and never disabled an account. The proof is the `Disable account` entry in the Entra audit log. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))
- **The portal and the saved config can disagree.** The Logic App designer showed the disable action inside the "not protected" branch; the saved definition had it outside. An entity-mapping identifier that looked saved in the portal wasn't. Read the definition back through the API after every save. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))
- **Running without an error isn't the same as correct.** `Add-AzVirtualNetworkSubnetConfig` worked only because it happened to modify the variable in place. The documented behavior is the return value. ([The Roads](https://github.com/Lglass510/The_Roads/blob/main/networkbuild.md))
- **Write predictions down before testing.** Graph was expected to refuse disabling a new Security Administrator. It didn't. Writing the prediction first is what made the gap visible. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))
- **Check two IDs before calling something broken.** Every Entra identity has an Object ID and an Application ID. The IAM blade showed one, the identity blade the other, and the assignment was fine. ([The Ward journal](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/lab-journal/2026-09-21-azure-security-progress.md))

## Detection engineering

- **A detection is only as current as its data.** Turning on Sentinel doesn't bring in Entra logs. In The Ward, the portal's data connector had quietly created the diagnostic setting; the Bicep rebuild had nothing until a script added it. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#what-went-wrong))
- **New log routes can take days.** A new Entra-to-Log Analytics route missed a test event 13 hours after it was created, and the event was never backfilled. Microsoft documents up to three days. Check the pipeline before running the attack. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#what-went-wrong))
- **A lookback longer than the schedule creates duplicates.** A rule running every 15 minutes with a 30-minute lookback puts every event in two windows, which meant two incidents per event. The lookback was there to catch late logs, so the fix was alert grouping on the Account entity rather than a shorter window. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))
- **Match on UPNs and object IDs, not display names.** Entra often leaves `displayName` null in `InitiatedBy` and `TargetResources`. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/T1098.003_investigation_writeup.md))
- **Build broad first, then tune.** The first rule fired on any role change. Seeing the noise made the role filter an informed decision. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/T1098.003_investigation_writeup.md))
- **Exclusions belong next to the action, not in the detection.** Filtering the break-glass account out of the query would hide the account that matters most. The playbook checks a watchlist and comments instead of disabling. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))

## Identity and permissions

- **Anyone who can edit an automation inherits its identity's permissions.** Ask that before granting a managed identity more power. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))
- **Least privilege is specific.** Disabling a user needs `User.EnableDisableAccount.All` + `User.Read.All`, not `User.ReadWrite.All`. The playbook needs Sentinel Responder on one workspace, not Contributor on the subscription.
- **Delete connections you don't use.** An unused API connection held a saved, delegated sign-in token that anyone able to edit a Logic App could use. ([The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar/blob/main/privilege-escalation-case-study/playbook-audit-and-remediation.md))
- **Sign in to the right tenant on purpose.** `Connect-MgGraph` without `-TenantId` landed in a personal account's empty home tenant. A portal 401 named two different tenant IDs. Both were fixed by reading the error and pinning the tenant. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#what-went-wrong))
- **Declare `principalType` on new managed identities.** It skips the directory lookup that fails while a new identity is still replicating. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#design-decisions))

## Infrastructure as code

- **Deterministic names make redeploys safe.** `guid(law.id, 'T1098.003')` gives the same rule name every time, so a redeploy updates instead of duplicating. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#design-decisions))
- **`dependsOn` only where no reference exists.** Bicep orders resources by their references. Write the dependency out only when nothing else forces the order.
- **Platform state can outlive the resource.** Sentinel kept rules filed under a force-deleted workspace's ID, so reusing the name failed. Remove Sentinel before deleting the workspace, or use a new name. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#what-went-wrong))
- **Exported definitions carry hardcoded IDs.** The Logic App exported from The Ward still pointed at The Ward's workspace. Unchanged, the rebuilt playbook would have checked the old exclusion list, then failed silently once The Ward was gone. Parameterize everything an export brings with it.
- **Know what What-If noise means.** `Modify` on a watchlist, `Unsupported` on an assignment named from a runtime ID, `NoEffect` on write-only properties: none are real changes. ([The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel#reading-what-if))
- **Some things live outside the resource group.** Graph app roles and tenant diagnostic settings can't be deployed at resource group scope, so they're idempotent post-deploy scripts.

## Scripting

- **Make scripts safe to re-run.** Check state before changing it (`New-LabDepartment`, `Add-Subnet.ps1`, `Grant-GraphPermissions.ps1`) or use an idempotent verb (PUT in `Set-EntraDiagnostics.ps1`). POST needs an existence check first. ([The Forge](https://github.com/Lglass510/The_Forge), [The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel/tree/main/bicep/scripts))
- **Stop at the first error.** `$ErrorActionPreference = 'Stop'` turns a confusing null-reference three lines later into the real error.
- **Guard the context.** Check `Get-AzContext` before deploying anything.
- **A backtick must be the last character on the line.** A trailing comment ended the statement early and ran it half-built. ([The Roads](https://github.com/Lglass510/The_Roads/blob/main/networkbuild.md))
- **`*Config` cmdlets only build local objects.** They validate nothing against Azure, so a missing `$` passed a literal string that would only fail at `Set-AzVirtualNetwork`.
- **`-Force` on a management-port rule is a decision.** The prompt exists because open RDP and SSH are common entry points. Use `-Force` only when the source is already narrow.
- **Command not found? Check the version first.** `New-NetNat` didn't exist in Windows PowerShell 5.1 on that host; it did in PowerShell 7. ([The Roads](https://github.com/Lglass510/The_Roads))
- **A module needs the right folder layout.** Copying a `.psm1` isn't deploying it. It must sit in `Modules\<Name>\<Name>.psm1` on a path in `$env:PSModulePath`. ([The Forge](https://github.com/Lglass510/The_Forge))
- **`Enter-PSSession` is interactive; `Invoke-Command` isn't.** Use the second for anything repeatable.

## Networking

- **Test one layer at a time.** Local link, gateway, internet by IP, DNS service, external DNS. Change one thing per test. ([The Roads](https://github.com/Lglass510/The_Roads))
- **A failed ping only proves ICMP failed.** SRV2 couldn't ping DC1, but `Test-NetConnection -Port 53` succeeded. Test the service you need. ([The Keep](https://github.com/Lglass510/The_Keep/blob/main/ServerCore/srv2-deployment.md))
- **Same subnet doesn't mean connected.** Virtual switch, ARP, routing, firewall, and the service all have to line up.
- **An unreachable DNS forwarder breaks external resolution quietly.** DC1 still forwarded to the old Default Switch gateway. Replacing it fixed every client that used DC1 for DNS.
- **Region is a hard boundary for networking.** A NIC must be in the VNet's region. A resource group's location is only metadata. ([The Roads](https://github.com/Lglass510/The_Roads/blob/main/networkbuild.md))
- **YAML indentation is syntax.** `netplan try` catches errors and rolls back if you lose the connection.

## Operations and documentation

- **Cleanup is part of the test plan.** Three test accounts kept Global Administrator for three days after a simulation. Later tests had their cleanup written before they started.
- **Sanitize before the first commit.** Ignore real data files (`*.local.csv`) before they exist and commit a `.sample` file instead. Deleting a file later leaves it in public history, and getting it out takes a history rewrite.
- **Copies drift.** The same storage script lives in two repositories and already differs. Keep one owner and link to it.
- **Document the failure, not just the fix.** The most useful write-ups here (The Ward remediation, The Ascent's "What went wrong", The Roads' VNet attempts) are built around something that broke.
