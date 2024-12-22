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
  switch (scheme) {
  case BITSTREAM_PARITY_EVEN:
    // If the number of ones is odd, the parity bit should be 1
    expected_parity = (ones & 1U) != 0U;
    break;
  case BITSTREAM_PARITY_ODD:
    // If the number of ones is even, the parity bit should be 0
    expected_parity = (ones & 1U) == 0U;
    break;
  default:
    // No other parity schemes are supported
    break;
  }

  return expected_parity == parity_bit;
}