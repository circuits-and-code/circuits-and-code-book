#include <stdint.h>
const float V_REF = 3.3;

volatile uint8_t *const ADC_CONFIG_REG = (uint8_t *)0x4000007C;
const uint8_t BITPOS_ADC_EN = 7;
const uint8_t BITPOS_ADC_CONVERSION_BEGIN = 6;
const uint8_t BITPOS_ADC_MUX_SEL = 4;

const uint8_t MAX_ADC_CHANNEL = 3;
const uint8_t MUX_SEL_MASK = MAX_ADC_CHANNEL << BITPOS_ADC_MUX_SEL;
// 0b00110000

volatile uint8_t *const ADC_STATUS_REG = (uint8_t *)0x4000007D;
const uint8_t BITPOS_ADC_CONVERSION_INITIALIZED = 7;
const uint8_t BITPOS_ADC_BUSY = 0;

volatile uint8_t *const ADC_DATA_HIGH_REG = (uint8_t *)0x4000007E;
volatile uint8_t *const ADC_DATA_LOW_REG = (uint8_t *)0x4000007F;