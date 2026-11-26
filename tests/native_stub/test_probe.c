#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "system_info.h"
#include "sound_manager.h"
int report_input_devices(FILE *);
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
static int list_mode, pos, freed;
static int handle;
static int devices[] = {0, 1, 2};
int sound_manager_get_device_list(sound_device_mask_e mask, sound_device_list_h *out)
{
    assert(mask == (SOUND_DEVICE_IO_DIRECTION_IN_MASK | SOUND_DEVICE_IO_DIRECTION_BOTH_MASK));
    pos = 0;
    if (list_mode == 1) return -9;
    *out = &handle;
    return 0;
}
int sound_manager_get_next_device(sound_device_list_h list, sound_device_h *out)
{
    assert(list == &handle);
    if (list_mode == 2 && pos == 1) return -8;
    if (list_mode == 4 || pos == 3) return SOUND_MANAGER_ERROR_NO_DATA;
    *out = &devices[pos++];
    return 0;
}
int sound_manager_get_device_type(sound_device_h dev, sound_device_type_e *out)
{
    int i = *(int *)dev;
    if (list_mode == 3 && i == 0) return -7;
    *out = (sound_device_type_e)(i + 1);
    return 0;
}
int sound_manager_get_device_io_direction(sound_device_h dev, sound_device_io_direction_e *out)
{
    sound_device_io_direction_e dirs[] = {SOUND_DEVICE_IO_DIRECTION_IN,
        SOUND_DEVICE_IO_DIRECTION_BOTH, SOUND_DEVICE_IO_DIRECTION_OUT};
    *out = dirs[*(int *)dev];
    return 0;
}
int sound_manager_free_device_list(sound_device_list_h list)
{
    assert(list == &handle);
    freed++;
    return list_mode == 5 ? -6 : 0;
}
static void test_inventory(void)
{
    for (list_mode = 0; list_mode < 6; list_mode++) {
        char buf[512] = {0};
        FILE *out = tmpfile();
        assert(out != NULL);
        freed = 0;
        int rc = report_input_devices(out);
        rewind(out);
        assert(fread(buf, 1, sizeof(buf)-1, out) > 0);
        fclose(out);
        assert(freed == (list_mode != 1));
        assert(rc == ((list_mode == 0 || list_mode == 4) ? 0 : 1));
        if (list_mode == 0) {
            assert(strstr(buf, "input_devices=2 unknown_devices=0"));
            assert(strstr(buf, "direction=input"));
            assert(strstr(buf, "direction=both"));
            assert(!strstr(buf, "type=3"));
        }
        if (list_mode == 1) assert(strstr(buf, "input_devices=unknown"));
        if (list_mode == 2 || list_mode == 3 || list_mode == 5)
            assert(strstr(buf, "inventory=incomplete"));
        if (list_mode == 4) assert(strstr(buf, "input_devices=0 unknown_devices=0"));
    }
    puts("Sound Manager metadata inventory host stub tests passed");
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
    test_inventory();
    return 0;
}
