/* Minimal read-only driver for the pinned rcheevos PlayStation hash API.
 *
 * This program does not implement the hash algorithm. It invokes the selected
 * rcheevos source revision so an evidence record can identify the exact
 * implementation used. The input path is intentionally not echoed.
 */
#include <stdio.h>

#include "rc_consoles.h"
#include "rc_hash.h"

static void on_error(const char* message, const rc_hash_iterator_t* iterator)
{
  (void)iterator;
  fprintf(stderr, "rcheevos: %s\n", message);
}

int main(int argc, char** argv)
{
  char hash[33];
  int result;
  rc_hash_iterator_t iterator;

  if (argc != 2)
  {
    fprintf(stderr, "usage: hash_psx <private-disc-or-cue-path>\n");
    return 2;
  }

  rc_hash_initialize_iterator(&iterator, argv[1], NULL, 0);
  iterator.callbacks.error_message = on_error;
  result = rc_hash_generate(hash, RC_CONSOLE_PLAYSTATION, &iterator);
  rc_hash_destroy_iterator(&iterator);

  if (!result)
    return 1;

  puts(hash);
  return 0;
}
