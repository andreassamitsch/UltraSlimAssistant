# Shared 2024 platform verification

Official Samsung product support pages for HW-S800D, HW-Q800D, HW-Q990D and HW-LS60D (Music Frame) reference the same firmware file ID 9528983 and September 2026 distribution path FM/202609/20260903095352782/Firmware_USB.zip:
- https://www.samsung.com/at/support/model/HW-S800D/EN/
- https://www.samsung.com/ie/support/model/HW-Q800D/XU/
- https://www.samsung.com/at/support/model/HW-Q990D/EN/
- https://www.samsung.com/ie/support/model/HW-LS60D/EN/

This establishes a common distribution artifact, not identical hardware, enabled functions, security policy or installed payload on each model. Do not download redundant copies. A Q990D owner also reports SAT-MT8532D24WWC-1072.1: https://www.reddit.com/r/Soundbars/comments/1w6ht37/google_cast_stopped_working_on_my_q990d_since_a/ (community report, not independent verification).

Re-read the original 2026-10-30 Q800A research: https://codon.org.uk/~mjg59/blog/p/getting-google-cast-on-my-soundbar/ . The author explicitly does not know how to enable SDB on newer soundbars. Their work relied on an older device and extracted firmware, and is not a verified installation path for our production soundbar. No supported HyperUART activation/recovery procedure was found in the broader search.

The S800D user guide directs readers to the Samsung open-source portal: https://device.report/manuals/samsung-soundbar-user-guide-hw-s800d-s81d-s81gd-s70d-s71d . The portal https://opensource.samsung.com/ timed out in this research environment. A matching downloadable source archive has not been located. Public portal retrieval or user-provided already-available corresponding source is the useful next research input, without contacting Samsung. Study source for architecture and documented interfaces, not assume a kernel feature implies a usable deployment mechanism.

Samsung Sound mobile app support is limited to 2026 products and LS60D according to https://www.samsung.com/us/support/troubleshoot/TSG10010601/ . Shared firmware does not imply the S800D supports this app. No documented microphone capture capability identified.

Conclusion: broaden research scope to common distribution; no direct microphone access, verified supported developer access, firmware modification, or new device test. Existing device, firmware, app settings remain untouched. No manufacturer outreach or Alexa.
