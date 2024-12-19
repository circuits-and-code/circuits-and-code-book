#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum { PIN_NUM_CS, PIN_NUM_SCLK, PIN_NUM_MISO, PIN_NUM_MOSI } spi_pin_E;

/** Externally Provided Functions - these are assumed to be error free **/
void HAL_GPIO_write(spi_pin_E pin, bool value);
bool HAL_GPIO_read(spi_pin_E pin); // Returns the logical value of the pin
void delay_nanoseconds(uint32_t ns);

/** USER IMPLEMENTED FUNCTIONS **/
/**
 * @brief Transmits and receives data over SPI using bit-banging
 * @param clk_freq_hz The frequency of the SPI clock in Hz
 * @param tx_data Pointer to the data to be transmitted
 * @param rx_data Pointer to the buffer to store the received data
 * @param len_bytes The number of bytes to transmit and receive. The length of
 * tx_data and rx_data must be at least len
 * @return true if the transaction was successful, false otherwise
 */
bool bitbang_spi_transceive(float clk_freq_hz, uint8_t const *const tx_data,
                            uint8_t *const rx_data, size_t len_bytes);
