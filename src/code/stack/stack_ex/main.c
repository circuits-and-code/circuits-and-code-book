#include <stdint.h>
#include <stdio.h>

uint8_t multiply(uint8_t c, uint8_t d) { return c * d; }

uint8_t add_and_multiply(uint8_t a, uint8_t b) {
  return a + b + multiply(a, b);
}

int main() {
  uint8_t a = 10;
  uint8_t b = 20;
  uint8_t c = add_and_multiply(a, b);
  printf("Result: %u\n", c);
  return 0;
}
