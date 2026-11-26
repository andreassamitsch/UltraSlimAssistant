# Reference source repository migration — 2026-11-26

Owner created [UltraSlimAssistant-Sources](https://github.com/andreassamitsch/UltraSlimAssistant-Sources) and authorized importing the previously released reference sources. Owner confirmed temporary public visibility is acceptable and will change it. Development remains in this repository; source snapshots are separate. Do not retain original firmware/archive files, executable binaries, private identifiers, keys or proprietary payloads.

## Verified source review
[One-time review run 45740245800](https://github.com/andreassamitsch/UltraSlimAssistant-Sources/actions/runs/45740245800) succeeded for both Q800D and Q990D. Actual logs show original archive lengths 849566852 and 815105236 bytes, respectively; SHA-256 matches prior analysis. Prior temporary shares remained valid at review time. No raw share URL was committed to the companion repository. No vendor material was published during review.

| Component | Q800D candidate text bytes | Q990D candidate text bytes | Decision |
|---|---:|---:|---|
| linux_kernel.tgz | 804584225 | 804584225 | Same hash; restrict to audio, relevant configurations, USB networking and license texts |
| pulseaudio.zip | 8474348 | 8474348 | Same hash; LGPL/GPL and supplied notices, initial approved scope |
| MM_DTV.zip | 233656624 | 233656624 | Same hash; first import selected GStreamer core/base/good, not whole mixed bundle |
| avsdk-lib-releaser.zip | 1961546 | 1961546 | Same hash; announcements do not establish redistribution terms for all SDK files |
| tzav-media-mt8532.zip | 2748718 | — | No standalone license notice detected; targeted per-file review required |
| tztv-media-sec.tgz | — | 54045797 | Different media stack; no general approval; Mali driver notice is not blanket permission |
| system_drv.tgz | 26430 | 675984 | Distinct; no notice detected |
| tzav-micom.tgz | 211990 | — | No notice detected |

Candidate counts are screening results, not full license review, complete source coverage or size on disk. A complete kernel candidate tree alone exceeds the 500 MB budget. The import tool preserves approved paths and license files, rejects unapproved source, excludes nontext/binary/unsafe paths, checks archive identity, deduplicates common component hashes and generates model manifests. Actual synthetic end-to-end import/dedup tests passed in run 45740206252.

Initial approved public redistribution scope: PulseAudio, selected Linux audio/configuration/USB sources, GStreamer core/base/good. See companion approval manifest for license evidence and required notices. Proprietary firmware and unreviewed content remain excluded even if the repository becomes private. [Initial import run 45740533521](https://github.com/andreassamitsch/UltraSlimAssistant-Sources/actions/runs/45740533521) completed successfully, job 139644140471. Actual logs show both downloads verified, Q800D imported 2,443 kernel files (39,363,200 bytes), 3,285 GStreamer files (48,958,312 bytes), 757 PulseAudio files (8,518,864 bytes), total 6,485 distinct source files and 96,840,376 bytes. Q990D deduplicated every one of these files and added zero source bytes. Push succeeded (c3624a0), both model indexes and direct reads of actual PulseAudio and kernel source files were verified. No source on soundbar, no changes to target. Native execution gate M1 remains open.

Next: focus on explicit license declarations and relevant configuration in MT8532 media and SDK components. Initial targeted screening run 45740660006 identified restricted-header markers in multiple SmartThings SDK headers and Apache markers in the release wrapper, then failed on in-memory TAR handling. Corrected the TAR input and triggered a fresh screening run; do not infer component-wide permission from header markers. Reuse direct repository reads instead of downloading identical source repeatedly once snapshots are present.
