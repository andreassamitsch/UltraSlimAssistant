# Reference firmware inventory — 2026-11-25

[Successful run 1](https://github.com/andreassamitsch/UltraSlimAssistant/actions/runs/45676203518)

- Source: official Samsung HW-S800D USB archive.
- Archive size: 1,289,225,604 bytes.
- SHA-256: `2fcb3c246031a7f5687fb4a1f4a98f8063a63b2ce74e06a900ac5022a8d0a29d`.
- Eight ZIP entries; no ZIP-level encryption reported.
- SAT-MT8532D24WWC: info.txt (512 bytes), upgrade.msd (650,526,867 bytes).
- SAT-iMX8M24WWC: info.txt (497 bytes), upgrade.msd (638,303,497 bytes).
- Reference target: MediaTek family; exact package version still to be verified against device-reported 1072.1.
- The near-zero ZIP compression gain is consistent with already compressed or encrypted data, but proves neither.
- Runner had 88 GB free before download; download took about 167 seconds.
- Cleanup succeeded. No proprietary files were retained in Git, caches or artifacts.

## Next step
Read selected metadata and measure the MediaTek container's entropy and recognizable header/keyword evidence, without executing or extracting firmware binaries. OS, audio stack and microphone access remain unverified.
