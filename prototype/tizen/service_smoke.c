/* Minimal independent lifecycle smoke test; no capture, playback, network,
 * service registration, auto-start, vendor identities or settings changes. */
#include <stdbool.h>
#include <service_app.h>
#include <dlog.h>

#define TAG "UltraSlimProbe"

static bool created(void *data)
{
    (void)data;
    dlog_print(DLOG_INFO, TAG, "lifecycle:create");
    return true;
}
static void terminated(void *data)
{
    (void)data;
    dlog_print(DLOG_INFO, TAG, "lifecycle:terminate");
}
static void control_received(app_control_h control, void *data)
{
    (void)control;
    (void)data;
    dlog_print(DLOG_INFO, TAG, "lifecycle:control");
    service_app_exit();
}
int main(int argc, char **argv)
{
    service_app_lifecycle_callback_s callbacks = {0};
    callbacks.create = created;
    callbacks.terminate = terminated;
    callbacks.app_control = control_received;
    return service_app_main(argc, argv, &callbacks, NULL);
}
