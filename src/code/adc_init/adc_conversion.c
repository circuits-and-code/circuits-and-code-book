#include "adc_init_registers.h"
#include <stdbool.h>
#include <stddef.h>

float adc_read_channel_V(uint8_t channel, float *voltage) {
  bool ret = false;
  const bool channel_valid = (channel <= MAX_ADC_CHANNEL);
  const bool adc_ready =
      (*ADC_STATUS_REG & (1 << BITPOS_ADC_CONVERSION_INITIALIZED));
  if (channel_valid && adc_ready && (voltage != NULL)) {
    // reset the MUX_SEL bits - & with the inverse of the mask, which sets the
    // masked bits to 0
    *ADC_CONFIG_REG &= ~(MUX_SEL_MASK);
    // Set the MUX_SEL bits to the channel
    *ADC_CONFIG_REG |= (channel << BITPOS_ADC_MUX_SEL);
    // Start the conversion
    *ADC_CONFIG_REG |= (1 << BITPOS_ADC_CONVERSION_BEGIN);
    // Wait for the conversion to complete
    while ((*ADC_STATUS_REG & (1 << BITPOS_ADC_BUSY)))
      ;
    // Read the ADC value.
    const uint16_t adc_value =
        ((uint16_t)(*ADC_DATA_HIGH_REG) << 8) | *ADC_DATA_LOW_REG;

    const uint16_t ADC_MAX = 4095; // 2^12 - 1 for 12-bit ADC
    *voltage = (adc_value * V_REF) / (float)ADC_MAX;
    ret = true;
  }
  return ret;
}