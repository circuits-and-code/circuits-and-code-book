#include "packet_parsing_header.h"
#define NUM_BITS_IN_BYTE (8U)

bool parse_packet(const uint8_t *packet, size_t len,
                  weather_data_t *weather_data) {
  bool success = false;
  // Let the compiler do the work of calculating len
  const size_t expected_len = (1U + 2U + 4U + 1U);
  if ((len == expected_len) && (packet != NULL) && (weather_data != NULL)) {
    const bool SOF_match = (packet[0] == 0x55);

    uint16_t sum_of_bytes = 0;
    for (size_t i = 0; (i < 7) && SOF_match; i++) {
      sum_of_bytes += packet[i];
    }
    const uint8_t received_checksum = packet[7];
    // Only compare the least significant byte of the sum
    const bool checksum_match = ((sum_of_bytes & 0xFF) == received_checksum);
    success = checksum_match && SOF_match;

    if (success) {
      float temperature_degC = 0.0f;
      temperature_degC += (float)packet[1] - 32.0f; // integer part;
      temperature_degC += (float)packet[2] / 10.0f; // fractional part;
      float pressure_Pa = 0.0f;
      pressure_Pa += (float)((uint32_t)packet[3] << (NUM_BITS_IN_BYTE * 3));
      pressure_Pa += (float)((uint32_t)packet[4] << (NUM_BITS_IN_BYTE * 2));
      pressure_Pa += (float)((uint32_t)packet[5] << (NUM_BITS_IN_BYTE * 1));
      pressure_Pa += (float)(packet[6]);
      weather_data->temperature_degC = temperature_degC;
      weather_data->pressure_kPa = pressure_Pa / 1000.0f; // Convert Pa to kPa
    }
  }
  return success;
}