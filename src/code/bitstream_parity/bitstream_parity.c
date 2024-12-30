#include "bitstream_parity.h"
#include "count_ones_bk.h"

bool bitstream_parity_valid(uint8_t *bitstream, uint32_t length,
                            bool parity_bit, bitstream_parity_E scheme) {

  uint32_t ones = 0U;
  // Count the number of ones in the bitstream
  for (uint32_t i = 0U; i < length; i++) {
    ones += count_ones_bk(bitstream[i]);
  }
  bool expected_parity = false;
  const bool number_of_ones_is_odd = (ones & 1U); // & 1U is equivalent to % 2
  switch (scheme) {
  case BITSTREAM_PARITY_EVEN:
    expected_parity = (number_of_ones_is_odd) == true;
    break;
  case BITSTREAM_PARITY_ODD:
    expected_parity = (number_of_ones_is_odd) == false;
    break;
  default:
    // No other parity schemes are supported
    break;
  }

  return expected_parity == parity_bit;
}