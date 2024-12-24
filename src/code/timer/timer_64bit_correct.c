#include "timer_registers.h"

uint64_t get_64_bit_time(void) {
  uint64_t high = *CNT_HIGH;
  uint64_t low = *CNT_LOW;
  // check if the high word has changed since reading low
  if (high != *CNT_HIGH) {
    // roll-over occurred between reading low and high, read low again
    low = *CNT_LOW;
    high = *CNT_HIGH;
  }
  const uint64_t time = ((uint64_t)high << 32) | low;
  return time;
}