# Public Samsung source archive analysis

The public release archives are supplied by the owner via a temporary pCloud share or as a local file. For GitHub Actions, configure repository secret `PCLOUD_SOURCE_LINK` (full European share URL or code) and manually run [Samsung open-source analysis](https://github.com/andreassamitsch/UltraSlimAssistant/actions/workflows/source-analysis.yml) on main. Do not commit the link, print the URL, or share download tokens. Pushes run a synthetic self-test only. The workflow has read-only repository access, checks the share metadata and name, downloads up to 2 GiB and calculates SHA256. No archive member is executed or written to its supplied pathname. Temporary files are cleaned on exit. Never retain proprietary archives or binaries in public artifacts.

## Focused scan (default)

The analyzer prioritizes voice-relevant top-level archive names (AV SDK, tzav/tztv, MM_DTV, PulseAudio, ALSA, voice, audio, micom, SmartThings, service-management and related names). It recursively inspects selected components and logs excluded top-level archive names, coverage limits and relevant filename metadata, including candidate binary names without executing or parsing their contents. An unknown archive excluded by this scope may contain relevant code. Explicit `--scope all` restores the broader bounded scan. A full listing is not guaranteed: the printed outer directory is capped at 300 entries and selected evidence is capped. Sensitive-looking member names are skipped; logs are not an exhaustive secret-detection filter and must be reviewed.

Evidence categories include audio capture, voice services, FFP/ALSA frontend, focus/ducking, mute/privacy, deployment interfaces and privilege declarations. Counts, paths and source excerpts guide further targeted reading; a match is not proof of deployed functionality, and absence is not proof of absence.

## Local public ZIP

```sh
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
python3 tools/source_analysis.py --work "$work" --archive /path/to/HW-S800D.zip --scope voice
```

Local ZIP must be a publicly released, authorized source archive, not a private device dump. For broad bounded reference analysis, specify `--scope all`. Run `python3 tools/source_analysis.py --self-test` to test synthetic archive handling. No source download occurs during a self-test.

The assistant's GitHub connection does not support creating repository secrets or dispatching a workflow. Owner must add the secret and initiate a manual archive run. No current source link is assumed valid. Inspect actual job logs, record coverage gaps and verify target-specific evidence before claiming any implementation path. This is a research pipeline, not a firmware installer. No device change.
