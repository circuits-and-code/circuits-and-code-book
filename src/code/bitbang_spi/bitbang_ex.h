#include <stdint.h>

#define HIGH 1
#define LOW 0

void HAL_GPIO_WritePin(uint8_t pin, uint8_t state);
void delayMicroseconds(uint8_t us);