# The Realm Audit - 2026-10-08

> Second cross-repository audit. The first one is [2026-09-12](realm-audit-2026-09-12.md).

## Scope

Seven Git repositories under `C:\Projects`, their public GitHub pages, and the local folders that hold Realm work but aren't in any repository.

| Repository | Realm role | Last push | State |
| --- | --- | --- | --- |
| [The Archives](https://github.com/Lglass510/The_Archives) | Record hall | 2026-10-08 | Updated by this audit |
| [The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel) | Infrastructure as code | 2026-10-07 | Complete. Rebuild and end-to-end test passed |
| [The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar) | Security operations | 2026-10-07 | Complete case study, short open-items list |
| [The Sky Hold](https://github.com/Lglass510/The_Sky_Hold) | Azure administration | 2026-09-21 | Networking and Storage documented; Identity, Compute, Monitoring still planned |
| [The Keep](https://github.com/Lglass510/The_Keep) | On-prem systems | 2026-09-21 | Documented, with broken links and a large untracked ISO |
| [The Forge](https://github.com/Lglass510/The_Forge) | PowerShell tooling | 2026-09-12 | No changes since the first audit |
| [The Roads](https://github.com/Lglass510/The_Roads) | Networking | 2026-09-12 | No changes since the first audit |

Method: `git log`, `git ls-files`, and `git status` per repository; a search of tracked files and history for passwords, keys, tokens, GUIDs, and UPNs; a link check of every relative link and image in tracked Markdown; file hashes to find duplicated content; the GitHub API for descriptions and topics. Screenshots were not reviewed image by image (see [Audit boundary](#audit-boundary)).

## What changed since 2026-09-12

The first audit's main recommendation for The Ward was "create one safe detection, record an investigation, then build a reversible playbook." That happened, and then some:

- **The Ward** went from SSH notes to a working Sentinel detection for MITRE ATT&CK T1098.003, an investigation write-up, and a playbook that disables the targeted account. The first build of that playbook reported success and disabled no one. The remediation write-up documents five configuration bugs and their fixes, plus alert grouping and a break-glass exclusion.
- **The Ascent** rebuilt The Ward from an empty resource group with one Bicep deployment and two PowerShell scripts (1 min 9 s). The rebuilt system disabled a test account 15 seconds after the incident opened.
- **The Sky Hold** gained the storage hardening script and an AZ-104 study agent.
- **The Keep** started tracking ISO files with Git LFS.

## Status of the 2026-09-12 actions

| # | Action | Status |
| --- | --- | --- |
| 1 | Remove the plaintext password example and review history | **Open.** Still at `The Forge/Scripts/Active Directory Script.md` line 33, and in history |
| 2 | Mark historical vs current network values | **Open.** `The Keep/ServerCore/srv2-deployment.md` still documents the `172.31.x` Default Switch addressing without saying it was replaced by `172.16.10.0/24` |
| 3 | One canonical home for duplicated network docs | **Open, and wider.** See [H3](#h3-duplicated-content) |
| 4 | Complete The Realm architecture files | **Partial.** `The Realm Architect` exists locally (CLAUDE.md, 6 agents, 9 skills) but isn't version-controlled |
| 5 | Evidence metadata in The Archives | **Started.** Conventions are now in the [README](../README.md#archive-conventions) |
| 6 | First Ward detection and reversible response | **Done.** T1098.003 detection, playbook, remediation, and Bicep rebuild |

## Findings

Severity is about the public GitHub pages, since they're the portfolio.

### Security

#### S1. Real account identifiers in Git history (High)

A history review found one repository where an early commit contains real account identifiers from the lab tenant. The current files are clean. Removing the data from public history needs a history rewrite and a force push. The details stay out of this public record until that's done.

#### S2. Tenant details still in The Ward's case-study files (Medium)

The 2026-10-07 sanitization pass replaced account details in the README and parts of the journal. These files still contain the tenant domain, the tenant ID, test-account UPNs, and managed identity object IDs:

- `privilege-escalation-case-study/T1098.003_investigation_writeup.md`
- `privilege-escalation-case-study/playbook-audit-and-remediation.md` (Step 8 lists three UPNs)
- `lab-journal/2026-09-21-azure-security-progress.md`

None of these are credentials, and tenant IDs can be looked up publicly. The tenant domain is built from a personal email address, though, and the stated goal was to remove tenant data. Replace them with placeholders such as `<tenant>.onmicrosoft.com` and `<object-id>`, or the truncated `xxxxxxxx-…` form the Ascent README uses.

#### S3. Lab password in The Forge (Medium, carried over)

Same as action 1 above. Replace the literal with `Read-Host -AsSecureString` and note that it was a lab-only value. If that password was ever used outside the lab, rotate it.

#### S4. Sentinel service principal ID in `main.bicepparam` (Low, accepted)

The Ascent's parameter file holds the tenant's Azure Security Insights object ID. It's tenant-specific and not secret, and the file explains how to look up your own. No change needed.

### Repository hygiene

#### H1. Ubuntu ISO in The Keep's working tree

`Ubuntu-Server/ubuntu-26.04.1-desktop-amd64.iso` (6.5 GB) is untracked, and `.gitattributes` routes `*.iso` to Git LFS. A `git add .` would try to upload it, and GitHub LFS rejects files over 2 GB on the Free plan. The Rocky Linux ISO (1.8 GB) is already in LFS and uses LFS storage and bandwidth quota for something anyone can download from the vendor.

Fix: add `*.iso` to `.gitignore`, remove the Rocky ISO from the repo, and document the download URL and SHA-256 checksum instead.

#### H2. Stray and misnamed files

| File | Issue |
| --- | --- |
| `The Roads/Lglass510`, `The Sky Hold/Networking/Lglass510` | Empty files |
| `The Keep/Lglass510/Lglass510` | Old copy of the GitHub profile README, still branded MAVLAB |
| `The Sky Hold/assets` | A 2-byte file where a folder was probably intended |
| `The Sky Hold/TestDocs/test.txt.txt` | Test file |
| `The Forge/Scripts/storage_account_scripts` | A PowerShell script with no `.ps1` extension, so GitHub doesn't highlight it and it can't be run as-is |
| `The Forge/Scripts/Active Directory Script.md` and `.txt` | Two versions of the same script; neither is a `.ps1` |
| `The Roads/network-build.md` and `networkbuild.md` | Two different documents with nearly the same name |

#### H3. Duplicated content

Byte-identical copies, found by hash:

| Content | Copies |
| --- | --- |
| `VNET.ps1`, `VNET.original.ps1`, `Add-Subnet.ps1`, `NSG-mars1.ps1`, `networkbuild.md` | The Roads (root) and The Sky Hold/Networking |
| `network-build.md` | The Roads and The Keep/Networking |
| Hyper-V NAT Gateway README | The Roads and The Keep/Networking |

The storage hardening script exists in The Forge and The Sky Hold. The two copies already differ (tabs vs spaces), which is how copies drift apart. Pick one owner per file and leave a link in the other repository. A reasonable split: The Roads owns network docs, The Sky Hold owns Azure scripts, The Forge owns reusable tooling.

#### H4. Broken links

| File | Link | Fix |
| --- | --- | --- |
| `The Keep/ActiveDirectory/README.md` | `images/manager_creation.png`, `images/managermap_setup.png`, `images/employee_onboarding_script.png` | Files are in the same folder; drop `images/` |
| `The Keep/README.md` | `./Linux/linux-networking.md` | Folder is `Ubuntu-Server/` |
| `The Keep/Networking/network-build.md`, `The Roads/network-build.md` | `../Linux/screenshots/LinuxIPRouteOutput.png` | Image is not in either repository |
| `The Sky Hold/Storage/README.md` | `../../The%20Forge/...` | A relative path to another repository only works on this PC. Use the GitHub URL |

#### H5. Stale status sections

- The Roads "Still To Configure" and "Next Steps" lists (SVR2 gateway, persistent DC1 gateway, Netplan permissions) haven't changed since August. Mark each item done, dropped, or still open.
- The Sky Hold README describes Identity & Governance, Compute, and Monitoring sections. The folders exist locally but are empty and untracked. Label those sections "Planned" until they have content.
- The Forge's "Future improvements" are still all open: no module manifest (`.psd1`), no Pester tests, no `Export-ModuleMember` list.

### GitHub presentation

#### G1. Profile README is behind the work

- The Ascent section still reads "Future Focus" and "Preparing to build repeatable infrastructure through code." The Ascent is finished and has evidence. Lead with its result.
- "Current Quests" lists ARM + Bicep as preparation.
- The Ward links to `github.com/Lglass510/The_Ward`. GitHub redirects the old name for now, but the redirect breaks if a repository named `The_Ward` is ever created. Link to `The_Ward_Sentinel_Soar`.
- Image alt text still says MAVLAB in two places.
- The Archives section promises Azure, PowerShell, Security, Linux, and Networking notes, cheat sheets, and lessons learned. Those now exist in [notes/](../notes/) and [lessons-learned.md](../lessons-learned.md).

#### G2. Repository metadata

- No repository has topics. Topics drive GitHub search and make the profile easier to scan. Suggested: `azure`, `bicep`, `microsoft-sentinel`, `kql`, `soar`, `logic-apps`, `entra-id`, `powershell`, `homelab`, `active-directory`, `hyper-v`, `networking`.
- The Ascent and The Sky Hold have no description. The Ward's description ("exploring Security+ concepts...") describes the SSH-era lab, not the Sentinel/SOAR project it became.
- `Mav-ToolKit` and `PersonalProjects` (2025) sit next to the Realm repositories with no README context. Archive them on GitHub or give each a one-line description.

### Work that isn't in any repository

| Local folder | Contents | Suggestion |
| --- | --- | --- |
| `Cyber_OnPrem` | 9 screenshots (by file name): nmap discovery, port and OS scans, NSE `vulners` against DC1, a missing OS update | An undocumented vulnerability-assessment exercise. Write it up in The Ward or The Keep |
| `Defender Lab` | 2 screenshots: Defender plans enabled, sample alerts | Fits the planned Defender for Cloud + Policy project |
| `SSH Lab Notes/sshconfig.md` | Full Rocky Linux ↔ DC1 SSH write-up | The Keep's copy (`ReaperSOC/SSH/sshconfig.md`) is a short stub. Replace it with this version |
| `The Realm Architect` | Claude Code instructions, agents, and skills for the lab | Put it in a private repository so changes are versioned |
| `emergency access` | A Word document on emergency access (not opened during this audit) | If it describes break-glass accounts, keep it out of public repositories |

## Prioritized actions

1. Rewrite the history flagged in S1 and force-push.
2. Replace tenant details in The Ward's case-study files (S2) and the password literal in The Forge (S3).
3. Ignore ISOs in The Keep and remove the Rocky ISO from LFS (H1).
4. Update the GitHub profile README and add descriptions and topics (G1, G2).
5. Fix the seven broken links (H4) and delete the stray files (H2).
6. Pick one owner for each duplicated file and replace the other copies with links (H3).
7. Write up the `Cyber_OnPrem` scan as a short exercise.
8. Mark stale status sections done, dropped, or open (H5).

## Audit boundary

This audit describes repository contents and public GitHub metadata. It doesn't confirm that any Azure resource is still deployed. The 48 screenshots in The Ward and The Ascent weren't checked image by image for tenant names, UPNs, or IDs; given S2, they should be checked before the projects are featured.
