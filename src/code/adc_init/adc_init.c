#include "adc_init_registers.h"
#include <stdbool.h>

void adc_init(void) {
  // Set the prescaler to 3
  const uint8_t PRESCALER_1MHZ_ADC_CLK = 7;
  *ADC_CONFIG_REG = PRESCALER_1MHZ_ADC_CLK;

  // Enable the ADC
  *ADC_CONFIG_REG |= (1 << BITPOS_ADC_EN);

  // Wait for the ADC to be ready
  while ((*ADC_STATUS_REG & (1 << BITPOS_ADC_CONVERSION_RDY)) == false)
    ;
}