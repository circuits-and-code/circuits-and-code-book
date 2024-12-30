#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum {
  BITSTREAM_PARITY_EVEN, // Parity bit = 0 if number of ones in bitstream is
                         // even, 1 otherwise
  BITSTREAM_PARITY_ODD, // Parity bit = 0 if number of ones in bitstream is odd,
                        // 1 otherwise
} bitstream_parity_E;

/**
 * @brief Check if the parity of the bitstream is valid
 * @param bitstream The byte array to check
 * @param length The length of the byte array
 * @param parity_bit The parity bit to check against
 * @param scheme The parity to use for the check
 * @return true if the bitstream has the correct parity, false otherwise
 */
bool bitstream_parity_valid(uint8_t *bitstream, uint32_t length,
                            bool parity_bit, bitstream_parity_E scheme);