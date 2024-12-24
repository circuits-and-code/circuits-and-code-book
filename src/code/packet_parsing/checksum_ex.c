#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool verify_checksum(const uint8_t *buf, size_t len, uint16_t expected) {
  uint16_t checksum = 0; // note: overflow possibility if len > 255
  for (size_t i = 0; i < len; i++) {
    checksum += buf[i];
  }

  return checksum == expected;
}