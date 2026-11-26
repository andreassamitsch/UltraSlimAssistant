# Work cycle 12 — HyperUART compile-time conditions (2026-11-26)

## Result

[Successful source check 45745127514](https://github.com/andreassamitsch/UltraSlimAssistant/actions/runs/45745127514), job 139659194854, on commit e3dfaa949dee506b8a3385b7a359a5c3bf0be1f2. Verified actual job logs, not inferred from the previous macro-name inventory.

The known Q800D source archive was rechecked with the SHA256 guard. 68,777 kernel files inventoried; one MT8532 release defconfig; three definition/build-setting matches and 27 references.

The preprocessor context scanner reports all three macros in include/linux/usb/usbnet.h at lines 26–28 under the ordinary header include guard only (ifndef __LINUX_USB_USBNET_H):
- SAMSUNG_HYPERUART_PREALLOC_SUPPORT
- SAMSUNG_USBNET_HYPERUART_IFNAME
- SAMSUNG_HYPERUART_SDB_PUSH_FIX

The three corresponding CONFIG_SAMSUNG_* entries are not listed in MT8532_release_defconfig. They are direct source macros, not evidence of disabled Kconfig options. Together with the previously verified MT8532 release defconfig building usbnet and ASIX drivers as modules, this substantially strengthens the conclusion that the released reference kernel build includes HyperUART-specific USB Ethernet behavior when those drivers are built normally from the released source. No actual reference kernel binary was built or examined, and no installed S800D module was examined. This is not proof of target runtime enablement, SDB availability, or application installation permission.

## Decision

The compile-time question for the published source is now substantially resolved. Repeating generic kernel scans is low-value. The remaining gaps are userspace: supported activation and lifecycle of the development interface, authorized SDB connection, independent package acceptance, application launch and recorder permissions. No such installation route on the 2024 family has been demonstrated. Keep the hardware purchase on hold under the owner's stated condition.

The next useful evidence would be a supported, model-specific description of the development interface or a target userspace/package inventory obtained through an already authorized diagnostic mechanism. No undocumented writes, signature bypass, vendor key use, device changes or adapter purchase. If no such evidence is accessible, explicitly report that source-only research cannot settle installability.
