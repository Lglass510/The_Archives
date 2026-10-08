# The Realm Audit - 2026-09-12

> A cross-repository record of what exists, what has been learned, and what should happen next.

## Audit Scope

This audit covers the six independent Git repositories under `C:\Projects`:

| Repository | Realm role | Current focus |
| --- | --- | --- |
| The Archives | Record hall | Evidence, history, and sanitized reference material |
| The Forge | Workshop | PowerShell automation and reusable administration tools |
| The Keep | Stronghold | Hyper-V, Windows, Linux, Active Directory, and DNS |
| The Roads | Roads and bridges | On-premises and Azure networking |
| The Sky Hold | Cloud keep | Azure identity, networking, compute, storage, and monitoring |
| The Ward | Watchtower | Security operations, detection, investigation, and response |

The audit used the current README files, tracked documentation, scripts, screenshots, and repository state. It records documented or directly observed facts; planned work is labeled as planned.

## Architecture At A Glance

The Realm is a learning and operations environment with two infrastructure planes and a defensive layer:

```text
The Forge  --->  The Keep  --->  The Ward
automation      on-prem systems  security operations
     |                |                 ^
     v                v                 |
The Sky Hold <--- The Roads ------------+
cloud systems     network paths

The Archives preserves sanitized evidence from every domain.
```

The most important current relationships are:

- The Roads provides the connectivity foundation used by The Keep and is also developing Azure network paths for The Sky Hold.
- The Keep provides the Windows and Linux systems, Active Directory, DNS, and Hyper-V environment used by The Forge and The Ward.
- The Forge contains `MavLabTools`, a PowerShell module intended for administration and deployment to `DC1`.
- The Sky Hold carries the on-premises administration lessons into Azure, especially identity, networking, security, and repeatable deployment.
- The Ward is intended to consume security-relevant activity from the infrastructure and feed safer operational practices back into the other repositories.
- The Archives preserves evidence and lessons without becoming the owner of live configuration.

## Repository Findings

### The Forge

**Verified purpose:** reusable PowerShell administration tooling.

**Documented capabilities:**

- `MavLabTools` exposes `Get-LabUsers` and `New-LabDepartment`.
- `Get-LabUsers` queries Active Directory users and selects name, account name, and enabled state.
- `New-LabDepartment` validates its parent OU choice and checks whether the department OU already exists before creating it.
- PowerShell remoting was used to connect to `DC1`, copy the module, import it, and verify exported commands.

**Lessons learned:**

- A reusable module is easier to deploy and verify than a collection of one-off commands.
- State checks make administrative automation safer to re-run.
- Deployment documentation should identify the target host, module path, session method, and verification commands.

**Follow-up:** add repeatable tests, formalize module exports, replace environment-specific paths with parameters or configuration, and document failure behavior.

### The Keep

**Verified purpose:** the MavLab on-premises systems record.

**Documented environment:**

- Hyper-V lab network: `172.16.10.0/24`.
- `DC1`: Windows Server 2025 domain controller and DNS server at `172.16.10.10`.
- `SRV2`: Windows Server 2025 Server Core domain member at `172.16.10.20` in the MavLab addressing plan.
- `Linux1`: Ubuntu server at `172.16.10.30`.
- Active Directory domain: `glasslab.local`.
- The lab uses Active Directory, DNS, organizational units, groups, PowerShell, and mixed Windows/Linux administration.

**Documented lessons:**

- A matching subnet does not guarantee communication. Virtual switching, ARP, routing, firewall policy, and the tested service all matter.
- A failed `ping` only proves that ICMP failed; TCP, DNS, and domain-controller discovery must be tested separately.
- Server Core administration benefits from explicit service, port, DNS, and domain-discovery checks.
- Active Directory onboarding is easier to reason about when source data, OU placement, manager mapping, and group membership are separate steps.

**Follow-up:** reconcile the documented `172.16.10.0/24` lab with the older `172.31.250.10` and Hyper-V Default Switch values in the SRV2 notes. Mark which values are historical and which are current. The local working tree also contains deleted PowerShell copies and other unrelated changes; resolve that migration intentionally before committing further Keep work.

### The Roads

**Verified purpose:** network construction, addressing, routing, and security boundaries.

**Documented capabilities:**

- Hyper-V switch `mavlab` and Windows NAT `MavLabNAT` provide the on-premises lab path.
- The host gateway is documented as `172.16.10.1`.
- Azure VNet `mavnetwork` uses address space `10.0.0.0/16` and subnet `mars1` at `10.0.1.0/24`.
- `10.0.0.0/24` was reserved for future use, then `10.0.0.0/26` was used for `AzureBastionSubnet`.
- `mars1` is documented with an NSG allowing RDP from the Bastion subnet rather than from the public internet.

**Lessons learned:**

- Capture the return value of Az `*Config` cmdlets instead of depending on undocumented in-place mutation.
- Check Azure context and location explicitly before deployment.
- Make scripts safe to re-run, but understand that idempotency varies by underlying API semantics.
- A backtick must be the final character on a PowerShell line; comments after it break parsing.
- Filter collections by an identifying property such as name instead of assuming positional ordering.
- `-Force` on management-port rules is a reviewed security decision, not merely an error bypass.

**Follow-up:** choose one canonical location for the duplicated Hyper-V NAT documentation and screenshots, then leave a pointer in the other location. Add explicit checks for VNet existence, subnet address overlap, region compatibility, and the expected NSG rule set.

### The Sky Hold

**Verified purpose:** Azure administration and the transition from portal-based learning to repeatable cloud infrastructure.

**Documented areas:**

- Identity and governance, including Entra ID, RBAC, policy, resource groups, locks, and managed identities.
- Storage accounts, blobs, files, redundancy, lifecycle, and data protection.
- Compute, virtual machines, disks, images, extensions, scaling, and administration.
- Networking, VNets, subnets, NSGs, DNS, routing, peering, VPN concepts, and load balancing.
- Monitoring through Azure Monitor, Log Analytics, metrics, activity logs, diagnostics, alerts, and workbooks.
- Azure CLI, Azure PowerShell, Portal workflows, and Bicep as complementary interfaces.

**Lessons learned:** the repository explicitly values understanding resource relationships, deployment location, identity boundaries, traffic paths, observability, and reproducibility rather than treating Azure as a collection of portal exercises.

**Follow-up:** distinguish planned architecture from deployed resources, add subscription/resource-group/region metadata where safe, and make Bicep or another declarative source the eventual authority for rebuildable infrastructure. The untracked `Networking/Lglass510` item should be classified before it is committed or archived.

### The Ward

**Verified purpose:** security operations learning and defensive workflow development.

**Current state:** the SSH administration path between Rocky Linux `reaper1`, `DC1`, and VS Code is documented. SIEM selection, detection creation, SOAR selection, playbook construction, and evidence capture remain planned work.

**Lessons learned and controls:**

- Test only systems and accounts that are owned or explicitly authorized.
- Keep the lab isolated and use least privilege.
- Sanitize screenshots, logs, usernames, addresses, and other evidence before sharing.
- Start response automation with reversible actions and approval gates.
- A useful exercise records objective, scenario, environment, procedure, evidence, result, lesson, and cleanup.

**Follow-up:** choose a log source and SIEM, create one safe detection, record an investigation, then build a reversible playbook with explicit safeguards and a test record.

### The Archives

**Verified purpose:** preserve the history and evidence of The Realm without replacing source-repository ownership.

**Current contents:** the landing page, this audit, and an untracked image named `archives.jpg`. The image should be reviewed and classified before it is committed.

**Follow-up:** adopt stable artifact names and metadata containing source repository, system or exercise, date, evidence type, sanitization status, and a short description.

## Evidence Register

The source repositories currently contain evidence that should remain with the work that produced it, with selected sanitized copies or references added here only when they improve cross-repository understanding.

| Evidence area | Source | Archive treatment |
| --- | --- | --- |
| Hyper-V switch, NAT, routes, DNS, and firewall screenshots | The Keep / The Roads | Keep source copies; archive only sanitized, labeled milestones |
| AD OU, group, and onboarding screenshots | The Keep | Do not copy employee data or credentials; archive sanitized structural evidence only |
| PowerShell module deployment screenshots | The Forge | Archive a deployment milestone after confirming no hostnames, usernames, or secrets are exposed |
| Azure VNet, storage, and CLI screenshots | The Sky Hold | Classify by subscription/resource exposure before copying |
| SSH administration notes | The Ward | Keep connection examples generic; never archive private keys or real connection details |

## Security Findings

The audit found material that is unsuitable for archival and should be reviewed at its source:

- `The Forge/Scripts/Active Directory Script.md` contains a plaintext lab password in example code.
- `The Keep/ActiveDirectory/` contains employee and manager sample data and mapping information.
- Several notes mention administrator accounts, local paths, domain names, and connection details.
- The repositories correctly state that passwords, tokens, private keys, and unredacted logs must not be committed, but the older plaintext example should still be removed or replaced with a placeholder.

No sensitive values from those findings are reproduced in this audit.

## Prioritized Actions

1. Remove or replace the plaintext password example and review Git history for exposed credentials.
2. Mark historical versus current network values, especially the `172.16.10.0/24` MavLab plan versus older `172.31.250.10` SRV2 notes.
3. Establish one canonical home for duplicated network documentation and screenshots.
4. Complete The Realm architecture files using this audit as the initial source material.
5. Add sanitized evidence metadata and link selected milestones into The Archives.
6. Build the first Ward detection and reversible response exercise from the Keep/Roads activity sources.

## Audit Boundary

This record describes repository contents and documented lab outcomes. It does not prove that every documented resource is still deployed or reachable. Live-state verification should be performed before operational changes, and credentials should be supplied interactively rather than written into documentation.