# HyperUART comparative review

## Direct evidence
HW-S800D InfoLink exposes hyperUARTSetting with OFF and several named modes. Actual mode semantics and recovery behavior are unknown. The manufacturer documents the micro-USB SERVICE connector as a USB storage firmware-update host interface: https://www.samsung.com/at/support/model/HW-S800D/EN/ and https://manualsfile.com/product/k47yn687sus.html . This does not establish USB Ethernet or SDB support.

## Comparative research
Matthew Garrett's 2026-10-30 article https://codon.org.uk/~mjg59/blog/p/getting-google-cast-on-my-soundbar/ demonstrates that HyperUART on HW-Q800A is a USB network-backed debugging mechanism rather than necessarily a physical serial link. He explicitly says newer soundbars lack the legacy listener used on his model and that he does not know how to enable SDB on them. The 2024 HW-S800D implementation remains unverified. No supported activation or rollback procedure was found.

LocalThings upstream registers InfoLink as an informational capability rather than a documented control entity: https://github.com/mbillow/localthings/blob/main/custom_components/localthings/registry/capabilities/soundbar.py .

## Broader platform scope
Public documentation and community reports identify SAT-MT8532D24WWC on S800D, Q800D, Q930D, Q995D and LS60D. Model-specific capabilities may differ, even on a shared firmware family. Relevant references: https://github.com/home-assistant/core/issues/131362 , https://eu.community.samsung.com/t5/audio-video/hw-q800d-xu-wifi-disconnected-no-bluetooth-nor-q-symphony/td-p/13658838 and https://www.samsung.com/at/support/model/HW-S800D/EN/ .

## Decision
Research the shared 2024 platform rather than only S800D. No setting change, root access, firmware modification or adapter purchase undertaken. Do not assume the previous Q800A method transfers to newer hardware. The owner has excluded Alexa and manufacturer outreach. Current native deployment gate is unresolved. A physical accessory test on an isolated bench would require suitable hardware and a known safe configuration/recovery procedure; a negative result with HyperUART disabled would not disprove support. No microphone access demonstrated.
