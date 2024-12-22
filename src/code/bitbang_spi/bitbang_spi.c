#include "bitbang_spi_header.h"

#define NUM_BITS_IN_BYTE 8
#define NS_PER_SECOND 1000000000

bool bitbang_spi_transceive(float clk_freq_hz, uint8_t const *const tx_data,
                            uint8_t *const rx_data, size_t len_bytes) {
  const bool ret = (tx_data != NULL) && (rx_data != NULL) && (len_bytes > 0);

  if (ret) {
    // clock calcs - integer division is used, but error is acceptable
    const uint32_t period_ns = NS_PER_SECOND / clk_freq_hz;
    const uint32_t half_period_ns = period_ns / 2;

    HAL_GPIO_write(PIN_NUM_SCLK, true);
    HAL_GPIO_write(PIN_NUM_CS, false);
    delay_nanoseconds(period_ns); // CS setup time, arbitrary value

    for (uint32_t byte = 0; byte < len_bytes; byte++) {
      const uint8_t tx_byte = tx_data[byte];
      for (uint32_t bit = 0; bit < NUM_BITS_IN_BYTE; bit++) {
        // falling edge - write MOSI output here
        HAL_GPIO_write(PIN_NUM_SCLK, false);
        const uint8_t tx_bit = (tx_byte >> (7 - bit)) & 0x01;
        HAL_GPIO_write(PIN_NUM_MOSI, (bool)tx_bit);
        delay_nanoseconds(half_period_ns);
        // rising edge - read MISO input here
        HAL_GPIO_write(PIN_NUM_SCLK, true);
        delay_nanoseconds(half_period_ns);
        rx_data[byte] |= HAL_GPIO_read(PIN_NUM_MISO) << (7 - bit);
      }
    }

    HAL_GPIO_write(PIN_NUM_CS, true);
  }

  return ret;
}