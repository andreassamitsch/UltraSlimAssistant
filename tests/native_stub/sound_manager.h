/* Synthetic host-only interface; not a vendor SDK or ABI declaration. */
#ifndef TEST_SOUND_MANAGER_H
#define TEST_SOUND_MANAGER_H
typedef void *sound_device_list_h;
typedef void *sound_device_h;
typedef enum { SOUND_DEVICE_IO_DIRECTION_IN_MASK=1,
               SOUND_DEVICE_IO_DIRECTION_BOTH_MASK=2 } sound_device_mask_e;
typedef enum { SOUND_DEVICE_IO_DIRECTION_IN=1, SOUND_DEVICE_IO_DIRECTION_OUT=2,
               SOUND_DEVICE_IO_DIRECTION_BOTH=3 } sound_device_io_direction_e;
typedef enum { TEST_MIC=1, TEST_HEADSET=2, TEST_SPEAKER=3 } sound_device_type_e;
enum { SOUND_MANAGER_ERROR_NONE=0, SOUND_MANAGER_ERROR_NO_DATA=-1 };
int sound_manager_get_device_list(sound_device_mask_e, sound_device_list_h *);
int sound_manager_get_next_device(sound_device_list_h, sound_device_h *);
int sound_manager_get_device_type(sound_device_h, sound_device_type_e *);
int sound_manager_get_device_io_direction(sound_device_h, sound_device_io_direction_e *);
int sound_manager_free_device_list(sound_device_list_h);
#endif
