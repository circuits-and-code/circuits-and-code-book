#include <stdint.h>
#include <stdio.h>

void some_function(void) {
  static uint32_t counter = 0; // Static local variable
  printf("%u ", counter);
  counter++;
}

int main(void) {
  for (uint32_t i = 0; i < 5; i++) {
    some_function();
  }
  // prints: 0 1 2 3 4
  return 0;
}