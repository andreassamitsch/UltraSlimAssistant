#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "system_info.h"
void report_capabilities(FILE *);
static int mode;
int system_info_get_platform_bool(const char *key, bool *value)
{
    assert(!strcmp(key, "http://tizen.org/feature/microphone") ||
           !strcmp(key, "http://tizen.org/feature/media.audio_recording"));
    if (mode == 2) { *value = true; return -1; }
    *value = mode == 0;
    return 0;
}
int main(void)
{
    const char *expected[] = {
        "microphone=true\naudio_recording=true\n",
        "microphone=false\naudio_recording=false\n",
        "microphone=unknown (error=-1)\naudio_recording=unknown (error=-1)\n"
    };
    for (mode = 0; mode < 3; ++mode) {
        char buf[256] = {0};
        FILE *out = tmpfile();
        assert(out != NULL);
        report_capabilities(out);
        rewind(out);
        assert(fread(buf, 1, sizeof(buf)-1, out) == strlen(expected[mode]));
        assert(strcmp(buf, expected[mode]) == 0);
        fclose(out);
    }
    puts("Native feature-query host stub tests passed");
    return 0;
}
