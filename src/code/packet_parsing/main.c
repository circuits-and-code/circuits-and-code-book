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
  uint8_t packet[] = {0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

  uint8_t fake_temperature_degC = 12U;
  packet[1] = fake_temperature_degC + 32U;

  uint8_t fake_temperature_fraction_degC = 5U;
  packet[2] = fake_temperature_fraction_degC;

  uint32_t fake_pressure_pA = 101325U;
  packet[3] = (fake_pressure_pA >> 24) & 0xFF;
  packet[4] = (fake_pressure_pA >> 16) & 0xFF;
  packet[5] = (fake_pressure_pA >> 8) & 0xFF;
  packet[6] = fake_pressure_pA & 0xFF;

  uint32_t checksum = 0U;
  for (size_t i = 0; i < 7; i++) {
    checksum += packet[i];
  }

  packet[7] = checksum & 0xFF;

  weather_data_t weather_data;
  bool success = parse_packet(packet, sizeof(packet), &weather_data);

  success &= (FLOAT_EQUALS(weather_data.temperature_degC, 12.5f));
  success &= (FLOAT_EQUALS(weather_data.pressure_kPa,
                           (float)fake_pressure_pA / 1000.0f));

  printf("Temperature: %.2f degC\n", weather_data.temperature_degC);
  printf("Pressure: %.2f kPa\n", weather_data.pressure_kPa);

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