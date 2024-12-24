#include <stdint.h>
/**
 * @brief Initialize the ADC
 */
void adc_init(void);

/**
 * @brief Read the ADC value
 * @param channel The channel to read from
 * @return The input voltage at the specified channel
 */
float adc_read_channel_V(uint8_t channel);