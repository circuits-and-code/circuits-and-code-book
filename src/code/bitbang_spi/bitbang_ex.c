#include "bitbang_ex.h"

void square_wave(uint8_t pin, uint8_t cycles, uint8_t period_us) {
  for (uint8_t i = 0; i < cycles; i++) {
    HAL_GPIO_WritePin(pin, HIGH);
    delayMicroseconds(period_us / 2);
    HAL_GPIO_WritePin(pin, LOW);
    delayMicroseconds(period_us / 2);
  }
}