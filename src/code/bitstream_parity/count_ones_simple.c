#include "bitstream_parity.h"

uint8_t count_ones_simple(uint8_t byte) {
  uint8_t count = 0;
  for (size_t i = 0; i < 8; i++) {
    const uint8_t mask = 1 << i;
    if (byte & mask) {
      count++;
    }
  }
  return count;
}