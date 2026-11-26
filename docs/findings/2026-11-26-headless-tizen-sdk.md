# Work cycle 7 — headless Tizen native service SDK test (2026-11-26)

## Official platform evidence
- [IoT native service tutorial](https://docs.stg.tizen.org/application/native/get-started/iot/first-app/) describes service applications without a graphical interface and supported Raspberry Pi development deployment.
- [Native API overview](https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/api/overview.md) explicitly states that Tizen 8.0 unifies the previously separate IoT API sets. This does not imply that every API, application profile or installation method is enabled on every device.
- [Service application guide](https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/guides/applications/service-app.md) documents lifecycle callbacks and background application policy. A long-running voice assistant still needs permitted lifecycle/background behavior and explicit privacy authorization.
- [Samsung TV testing FAQ](https://developer.samsung.com/smarttv/develop/faq/application-testing.html) Q25 distinguishes public Web application testing from native C TPK support. Samsung also has separate .NET/Flutter product-specific SDK pathways; none is evidence that a soundbar accepts owner-built native services.
- [Tizen SDK archive index](https://download.tizen.org/archive/sdk/tizenstudio/official/binary/) contains generic Tizen 8.0 emulator/device rootstraps. The selected x86-64 emulator package is 154,386,242 bytes. It is not a Samsung soundbar SDK.

## Implementation and test
Added prototype/tizen/service_smoke.c: independent lifecycle logging through documented service_app_main callbacks; exits when it receives the application control event. No recording, playback, network, boot start, device identifiers, vendor identities or permissions requested. Added tools/check_tizen_sdk.py and .github/workflows/tizen-sdk-check.yml for an actual official SDK header syntax check without executing a vendor binary or connecting to a target.

First run 45743055387, job 139652473846: downloaded official rootstrap successfully, SHA256 d7118b4043ff530923c8bfc4155486cf9c44bc979103bd4dc45db8efd6bc816c; 6,046 ZIP entries. Confirmed actual service_app.h, sound_manager.h, system_info.h and dlog.h. Header syntax check initially failed due to overbroad include paths shadowing libc/compiler headers. Commit bcae711 narrows API include paths; [Rerun 45743111190](https://github.com/andreassamitsch/UltraSlimAssistant/actions/runs/45743111190), job 139652649356, completed successfully. Actual logs verify the identical SDK digest and PASS_REAL_SDK_HEADER_CHECK for both service_smoke.c and capability_probe.c using clang --target=x86_64-linux-gnu -fsyntax-only. No stubs used for these checks. Do not equate header validation with linking, TPK packaging, emulator execution or target deployment.

## Next gate
The independent code passed actual header checks. Next build and link against the documented SDK and test lifecycle on a supported test platform. Keep M1 for S800D deployment separate; neither the official generic rootstrap nor a successful emulator run establishes a soundbar installation route. No actual target changes or vendor contact.
