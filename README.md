[← Back to The Realm](https://github.com/Lglass510)

# The Archives

![The Archives](archives.jpg)

> **The record hall of The Realm.**

The Archives holds the notes, lessons, audits, and history of the work across The Realm. The repositories that did the work keep their own configuration, scripts, and evidence. This one keeps the record that ties them together.

## Start here

| Record | What's in it |
| --- | --- |
| [Lessons learned](lessons-learned.md) | Every lesson from every project, grouped by topic, each linked to the write-up where it happened |
| [Timeline](timeline.md) | How The Realm grew, from the first domain controller in August to the Bicep rebuild in October |
| [Realm audit - 2026-10-08](audits/realm-audit-2026-10-08.md) | Current state of each repository, security and hygiene findings, prioritized fixes |
| [Realm audit - 2026-09-12](audits/realm-audit-2026-09-12.md) | First audit and the baseline the second one measures against |

## Notes

Reference sheets built from commands that were actually run in the labs, with links back to the source.

| Note | Covers |
| --- | --- |
| [Azure](notes/azure.md) | Az PowerShell context guards, VNets, NSGs, storage baseline, `Invoke-AzRestMethod`, Bicep patterns, teardown |
| [Security](notes/security.md) | Sentinel detection pipeline, KQL, Graph app roles for managed identities, least privilege, break-glass, test hygiene |
| [PowerShell](notes/powershell.md) | Script skeleton, idempotency, secrets, modules, remoting, CSV-driven AD, syntax traps |
| [Networking](notes/networking.md) | Lab addressing, layer-by-layer troubleshooting, Hyper-V NAT, Windows DNS, Azure network rules |
| [Linux](notes/linux.md) | `ip` commands, Netplan, SSH between Linux and a Windows DC |

## Exam prep

| Item | What's in it |
| --- | --- |
| [AZ-104 practice exam](exam-prep/viewer/az104-exam-viewer.html) | 200 original questions in 4 timed 50-question tests, mapped to the April 17, 2026 skills outline, with explanations, Microsoft Learn references, and confidence scores. Download and open in a browser. |

The bank source and build script are in `exam-prep/temp/`. Rebuild with `python temp/build_az104.py --check-links` from `exam-prep/`. Don't edit the generated HTML.

## The Realm

| Repository | Role | Highlight |
| --- | --- | --- |
| [The Ascent](https://github.com/Lglass510/The_Ascent_Bicep_Sentinel) | Infrastructure as code | The Ward rebuilt in Bicep: 1 deployment + 2 scripts, account disabled 15 s after the incident |
| [The Ward](https://github.com/Lglass510/The_Ward_Sentinel_Soar) | Security operations | Sentinel detection for T1098.003 and a playbook that went from "Succeeded, did nothing" to working |
| [The Sky Hold](https://github.com/Lglass510/The_Sky_Hold) | Azure administration | VNet, NSG, and storage hardening scripts, AZ-104 study |
| [The Keep](https://github.com/Lglass510/The_Keep) | On-prem systems | Windows Server 2025 domain, Server Core, Linux, CSV-driven AD onboarding |
| [The Roads](https://github.com/Lglass510/The_Roads) | Networking | Hyper-V NAT network built and debugged layer by layer |
| [The Forge](https://github.com/Lglass510/The_Forge) | PowerShell tooling | `MavLabTools` module deployed to DC1 over remoting |

## Archive conventions

Anything added here follows these rules:

- **Sanitize first.** No passwords, keys, tokens, tenant IDs, UPNs, or object IDs. Use placeholders like `<tenant>.onmicrosoft.com` or `<object-id>`.
- **Link, don't copy.** Point to the file in the repository that owns it. Copies drift.
- **Date it.** Audits and dated records use `YYYY-MM-DD` in the file name.
- **Say where it came from.** Evidence carries its source repository, the exercise, the date, and whether it has been sanitized.

| Folder | Holds |
| --- | --- |
| `audits/` | Dated cross-repository audits |
| `notes/` | Reference sheets by topic |
| `exam-prep/` | Certification practice exams: generated viewer in `viewer/`, question bank and build script in `temp/` |
| root | Lessons learned, timeline, this index |
