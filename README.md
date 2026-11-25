# UltraSlimAssistant

Experimental, independent research into using Samsung Ultra Slim soundbars as Home Assistant Assist voice satellites while preserving the original audio, HDMI/eARC and playback functions.

**Status:** Research only. No installable firmware, microphone capture, or custom on-device service has been demonstrated.

## Target
- Samsung HW-S800D
- Firmware family: SAT-MT8532D24WWC
- Reference version: 1072.1 (device-reported); public USB package may differ.

## Principles
- Read-only offline analysis first. No flashing or device changes during initial research.
- Keep Samsung firmware and extracted binaries out of Git, Git LFS, releases, Actions caches and artifacts.
- Download from official Samsung sources on demand. Record checksums and concise metadata, not proprietary payloads.
- Never execute extracted firmware programs on the analysis host.
- No local network identifiers, credentials, device IDs or private diagnostics in the repository.
- Do not redistribute proprietary firmware or claim official Samsung affiliation.

## Start
See [research plan](docs/research.md) and [firmware inventory tool](tools/inventory.py). Run the inventory locally with Python 3; it reads ZIP metadata and hashes the archive without extraction or execution.

Official source: https://www.samsung.com/at/support/model/HW-S800D/EN/

## Milestones
1. Establish reproducible firmware acquisition and inventory.
2. Identify file formats and documented platform/audio components.
3. Assess supported interfaces and feasibility of a voice satellite.
4. Only after a verified safe execution and recovery path, consider a prototype.

No changes to a production soundbar are part of the current milestone.
