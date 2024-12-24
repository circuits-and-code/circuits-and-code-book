#include <stdint.h>

volatile uint32_t *CNT_LOW = (uint32_t *)0x40000000;
volatile uint32_t *CNT_HIGH = (uint32_t *)0x40000004;

/**
 * @brief Get the 64 bit time from the timer
 * @return uint64_t The 64 bit time
 */
uint64_t get_64_bit_time(void);