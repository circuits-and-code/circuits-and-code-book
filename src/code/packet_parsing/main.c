#include "packet_parsing_header.h"
#include <math.h>
#include <stdio.h>

// Use a macro to compare floating point numbers since == is not reliable for
// floats
#define FLOAT_EQUALS(a, b) (fabsf(a - b) < 0.0001f)

bool test_invalid_args(void) {
  weather_data_t weather_data;
  uint8_t data[8U] = {0};
  bool success = parse_packet(NULL, 0, &weather_data);
  success |= parse_packet(data, 0, &weather_data);
  success |= parse_packet(data, 8, NULL);

  return !success;
}

bool test_incorrect_SOF(void) {
  uint8_t packet[] = {0x54, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x54};

  weather_data_t weather_data;
  bool success = parse_packet(packet, sizeof(packet), &weather_data);

  return !success;
}

bool test_incorrect_checksum(void) {
  uint8_t packet[] = {0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x53};

  weather_data_t weather_data;
  bool success = parse_packet(packet, sizeof(packet), &weather_data);

  return !success;
}

bool test_correct_packet(void) {
  uint8_t packet[] = {0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55};

  weather_data_t weather_data;
  bool success = parse_packet(packet, sizeof(packet), &weather_data);

  success &= (FLOAT_EQUALS(weather_data.temperature_degC, -32.0f));
  success &= (FLOAT_EQUALS(weather_data.pressure_kPa, 0.0f));

  return success;
}

int main() {
  bool success = true;
  if (test_invalid_args() == false) {
    printf("test_invalid_args failed\n");
    success = false;
  }

  if (test_incorrect_SOF() == false) {
    printf("test_incorrect_SOF failed\n");
    success = false;
  }

  if (test_incorrect_checksum() == false) {
    printf("test_incorrect_checksum failed\n");
    success = false;
  }

  if (test_correct_packet() == false) {
    printf("test_correct_packet failed\n");
    success = false;
  }

  if (success) {
    printf("All tests passed\n");
  }

  return success ? 0 : 1;
}