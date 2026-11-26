/* Tizen native capability probe. No recording, network, or settings writes.
 * Call report_capabilities(stdout) from a supported native application.
 */
#include <stdbool.h>
#include <stdio.h>
#include <system_info.h>
#include <sound_manager.h>

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

/* Metadata only. Deliberately omit device names/IDs; never open a stream,
 * change routing, volume, permissions, or mixer controls. */
int report_input_devices(FILE *out)
{
    sound_device_list_h list;
    sound_device_h device;
    sound_device_mask_e mask = (sound_device_mask_e)(
        SOUND_DEVICE_IO_DIRECTION_IN_MASK | SOUND_DEVICE_IO_DIRECTION_BOTH_MASK);
    int rc = sound_manager_get_device_list(mask, &list);
    if (rc != SOUND_MANAGER_ERROR_NONE) {
        fprintf(out, "input_devices=unknown (error=%d)\n", rc);
        return 1;
    }
    unsigned int count = 0, unknown = 0;
    while ((rc = sound_manager_get_next_device(list, &device)) == SOUND_MANAGER_ERROR_NONE) {
        sound_device_type_e type;
        sound_device_io_direction_e dir;
        int tr = sound_manager_get_device_type(device, &type);
        int dr = sound_manager_get_device_io_direction(device, &dir);
        if (tr != SOUND_MANAGER_ERROR_NONE || dr != SOUND_MANAGER_ERROR_NONE) {
            unknown++;
            continue;
        }
        if (dir != SOUND_DEVICE_IO_DIRECTION_IN && dir != SOUND_DEVICE_IO_DIRECTION_BOTH)
            continue;
        count++;
        fprintf(out, "input_device type=%d direction=%s\n", (int)type,
                dir == SOUND_DEVICE_IO_DIRECTION_IN ? "input" : "both");
    }
    int cleanup = sound_manager_free_device_list(list);
    fprintf(out, "input_devices=%u unknown_devices=%u\n", count, unknown);
    if (rc != SOUND_MANAGER_ERROR_NO_DATA || cleanup != SOUND_MANAGER_ERROR_NONE || unknown) {
        fprintf(out, "inventory=incomplete (iteration=%d cleanup=%d)\n", rc, cleanup);
        return 1;
    }
    return 0;
}
