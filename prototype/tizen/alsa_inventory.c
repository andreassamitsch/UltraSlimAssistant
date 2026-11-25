/* SPDX-License-Identifier: Apache-2.0
 * Host-testable ALSA metadata probe. Never opens a PCM or mixer.
 */
#include <alsa/asoundlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int candidate(const char *s) {
    return s && (!strcmp(s,"ffp_in") || !strcmp(s,"Capture_Mic_normal") ||
                 !strcmp(s,"Capture_Mic_ais_only"));
}
static void safe_print(const char *s) {
    if (!s) { fputs("-",stdout); return; }
    for (size_t i=0;s[i] && i<300;i++) {
        unsigned char c=(unsigned char)s[i];
        putchar(c>=32 && c<127 ? c : ' ');
    }
}
int main(int argc,char **argv) {
    if (argc != 2 || strcmp(argv[1],"--list")) {
        fputs("Usage: alsa_inventory --list (metadata only; no recording)\n",stderr);
        return 2;
    }
    void **hints=NULL;
    int rc=snd_device_name_hint(-1,"pcm",&hints);
    if (rc<0) {
        fprintf(stderr,"ALSA enumeration failed: %s\n",snd_strerror(rc));
        return 1;
    }
    unsigned count=0, candidates=0;
    for (void **h=hints;h && *h;h++) {
        char *name=snd_device_name_get_hint(*h,"NAME");
        char *direction=snd_device_name_get_hint(*h,"IOID");
        if (name && (!direction || strcmp(direction,"Output"))) {
            int found=candidate(name);
            printf("PCM ");safe_print(name);
            printf(" direction=");safe_print(direction?direction:"unspecified");
            printf(" source_candidate=%s\n",found?"yes":"no");
            count++;candidates+=(unsigned)found;
        }
        free(name);free(direction);
    }
    snd_device_name_free_hint(hints);
    printf("Capture-capable hints or unknown direction: %u; named candidates: %u\n",count,candidates);
    puts("A hint does not prove availability, permissions, microphone routing or physical mute behavior.");
    return 0;
}
