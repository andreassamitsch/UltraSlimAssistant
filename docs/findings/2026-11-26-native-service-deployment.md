# Work cycle 4 — native service deployment evidence (2026-11-26)

## Direct source review

The private reference snapshot is available to the assistant and contains both model indexes. The expanded source import succeeded in run 45741293855. Analysis in this cycle used direct authenticated file reads, not another archive download.

### Vendor application packaging

Q800D/Q990D share avsdk-lib-releaser.zip (component SHA256 b7c58a4c1be4a3eaeb94d6bcff0bec963526b3d9795d108efd220181aa7cd3fd).

- avsdk-lib-releaser/avsdk-lib-releaser/tizen-manifest.xml, blob b530b163abf3ab26a0d8be0da38ba4cd9acabf3a: native hidden service, tv-samsung profile, API 6.0, on-boot=false. It does not declare recorder privilege.
- avsdk-lib-releaser/avsdk-lib-releaser/src/main.cpp, blob 02f61309cdc4db3da28573992e6a45a611cb86ee: the executable merely logs the SDK release role and exits. It is not a voice-service implementation.
- avsdk-lib-releaser/packaging/com.samsung.tv.avsdk-lib-releaser.spec, blob 67331dde5349be6ea122517e90a69c14e1d89267: explicit Tizen 8.0 handling for ARM and AArch64 at lines 111–120, reusing the 6.0 SDK materials. This explains why the manifest API version is not a reliable indicator of runtime version. The build references internal rootstraps, app signing, platform re-signing and preloaded package locations (lines 17–24, 182–183, 213–224). The published spec demonstrates Samsung's firmware packaging pipeline, not permission for owners to deploy arbitrary native TPKs. No signing material or vendor credentials used.

### Vendor firmware audio services

Q800D MT8532 media component SHA256 4941bfbd57224d69bb56d9ef76e7071d3f230fe0f048276bad74c99159044dfc:

- mdp_alsa/service/swdsp_audio_in.service (blob 8ec04887eeef718550483fb3b9ccb1966e923f9a), swdsp_mas_thread.service (42f09643232315327f0db5e05b4c5afe99eac54c), swdsp_swdsplogd.service (18ca947ec5ee7df079a14b6ef06c3bcaa25c0b66): systemd service definitions for input, media-audio processing and logging; ordered dependencies, restart policies and shared environment. These are firmware-controlled services, not extension hooks. Their process management can affect normal audio and system stability; do not modify or restart them.
- packaging/tztv-media-mt8532.spec lines 58–74 and 107–140: installs units and references path units, security policy and capabilities as part of vendor system RPM installation. This is separate from application package deployment. The source snapshot omitted some nonstandard filename extensions; no implication those files are absent in firmware.
- Published PulseAudio security code confirms a recorder privilege check for ordinary native recording streams when Tizen security is built in; meson_options.txt defaults security to enabled. Source defaults are not actual S800D runtime evidence.

## Target and public interfaces

The actual S800D previously reported Tizen 8.0 and developerMode=0; standard SDB was refused twice. No new target network or physical probing in this cycle. Samsung's public TV [device setup](https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html) documents the TV Smart Hub and Web app workflow; [application testing FAQ](https://developer.samsung.com/smarttv/develop/faq/application-testing.html) distinguishes Web apps from native TPKs. Neither establishes a supported native soundbar path. Public TV documentation is not proof of an absolute soundbar restriction.

## Decision

M1 remains blocked. The new evidence strengthens the reference platform compatibility hypothesis but closes the inference that a firmware-owned TPK or systemd unit is automatically a developer extension path. Prioritize a documented owner-accessible deployment mechanism before investing in an installable package. A harmless independent host probe is feasible; do not reuse vendor signing identities, replace firmware services or modify the device. Further reference analysis should be targeted: identify audio-service interfaces and config mapping, and compare them against legitimate device capabilities. No new firmware execution, audio capture, playback, or device configuration changes.

Source hygiene note: some imported configuration filenames contain 'key_info', and the vendor packaging recipe contains signing-related metadata. No secret values were used; do not treat the current filename filter as a comprehensive secret audit. Keep the companion repository private and review candidate sensitive files separately before any distribution.
