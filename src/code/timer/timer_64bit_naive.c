#include "timer_registers.h"

uint64_t get_64_bit_time(void) {
  uint64_t time = 0;
  time |= *CNT_LOW;
  time |= ((uint64_t)*CNT_HIGH) << 32;
  return time;
}