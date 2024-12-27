#include <stdbool.h>
#include <stdint.h>
/**
 * @brief Initialize the ADC.
 * @note Blocking function
 */
void adc_init(void);
/**
 * @brief Read the ADC value
 * @param channel The channel to read from
 * @param voltage The voltage at the specified channel
 * @return true if the read was successful, false otherwise
 */
bool adc_read_channel_V(uint8_t channel, float *voltage);