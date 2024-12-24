#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct {
  float temperature_degC;
  float pressure_kPa;
} weather_data_t;

/**
 * @brief Parse a packet of data and extract the weather data
 * @param packet The packet of data to parse
 * @param len The length of the received packet
 * @param weather_data The weather data to populate
 * @return true if the packet was parsed successfully, false otherwise
 */
bool parse_packet(const uint8_t *packet, size_t len,
                  weather_data_t *weather_data);