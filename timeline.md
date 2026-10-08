# Timeline of The Realm

Built from each repository's commit history. Dates are commit dates.

## August 2026: The Keep (MavLab)

| Date | Repository | Milestone |
| --- | --- | --- |
| 08-07 | The Keep | First commit. DC1 build and Active Directory OU structure documented |
| 08-11 | The Keep | SRV2 joins the domain as a Server Core member |
| 08-18 – 08-20 | The Keep | Hyper-V `mavlab` switch, Windows NAT, `172.16.10.0/24` network, DNS troubleshooting |
| 08-21 – 08-22 | The Keep | AD OU build, PowerShell README, repository flattened and cleaned up |
| 08-23 | The Keep | `New-LabDepartment` tuned with state checks |
| 08-24 | The Keep | Employees and managers imported from CSV and sorted into OUs with PowerShell |
| 08-24 | The Sky Hold | Azure Lab created |
| 08-31 | The Sky Hold | VNet build refactored: subnet in the initial create, idempotency, context guard |

## September 2026: The Realm takes shape

| Date | Repository | Milestone |
| --- | --- | --- |
| 09-02 | The Ward | Started as ReaperSOC: Rocky Linux ↔ DC1 SSH administration |
| 09-09 | The Sky Hold | NSG on `mars1` allowing RDP only from the Bastion subnet |
| 09-11 | All | Realm naming: MavLab → The Keep, Azure Lab → The Sky Hold, ReaperSOC → The Ward. Network content moves to The Roads, tooling to The Forge |
| 09-12 | All | Realm landing pages. Storage hardening script. The Archives created with the [first audit](audits/realm-audit-2026-09-12.md) |
| 09-14 | The Sky Hold | AZ-104 instructor agent |
| 09-16 – 09-17 | The Ward | Azure security baseline notes |
| 09-21 | The Ward | Sentinel playbook journal: managed identity, Graph permission, tenant mismatch fix |
| 09-21 | The Keep | ISO files tracked with Git LFS |
| 09-27 | The Ward | Simulated privilege escalation (T1098.003): Global Administrator assigned to a test account, detected, investigated |
| 09-30 | The Ward | Playbook audit: five bugs fixed, alert grouping, break-glass exclusion, end-to-end test. Repository renamed `The_Ward_Sentinel_Soar` |

## October 2026: The Ascent

| Date | Repository | Milestone |
| --- | --- | --- |
| 10-05 | The Ascent | Workspace, Sentinel onboarding, exclusion watchlist, analytics rule in Bicep |
| 10-06 | The Ascent | Playbook, RBAC, automation rule modules; Graph and diagnostics scripts; teardown |
| 10-07 | The Ascent | Redeploy in 1 min 9 s. Live test: account disabled 15 s after the incident opened |
| 10-07 | The Ward | Account details sanitized; linked to The Ascent |
| 10-08 | The Archives | [Second audit](audits/realm-audit-2026-10-08.md), lessons learned, notes |

## Next

From the roadmap: Defender for Cloud and Azure Policy posture remediation (The Sky Hold), then identity attack detection with sign-in logs and Conditional Access.
