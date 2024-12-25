#include <stdint.h>
#include <stdio.h>

void check_stack_dir(uint8_t *comparison) {
  uint8_t local = 0;
  if (&local < comparison) {
    // Stack grows down
    printf("Stack grows down\n");
  } else {
    // Stack grows up
    printf("Stack grows up\n");
  }
}

int main() {
  uint8_t comparison = 0;
  check_stack_dir(&comparison);
  return 0;
}