/* Tizen native capability probe. No recording, network, or settings writes.
 * Call report_capabilities(stdout) from a supported native application.
 */
#include <stdbool.h>
#include <stdio.h>
#include <system_info.h>

static void report_bool(FILE *out, const char *name, const char *key)
{
    bool value = false;
    int result = system_info_get_platform_bool(key, &value);
    if (result == 0)
        fprintf(out, "%s=%s\n", name, value ? "true" : "false");
    else
        fprintf(out, "%s=unknown (error=%d)\n", name, result);
}

void report_capabilities(FILE *out)
{
    report_bool(out, "microphone", "http://tizen.org/feature/microphone");
    report_bool(out, "audio_recording", "http://tizen.org/feature/media.audio_recording");
}
