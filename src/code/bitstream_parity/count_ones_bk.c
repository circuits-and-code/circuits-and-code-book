#include "count_ones_bk.h"

uint8_t count_ones_bk(uint8_t byte) {
  uint8_t count = 0;
  while (byte != 0) {
    byte &= (byte - 1);
    count++;
  }
  return count;
}