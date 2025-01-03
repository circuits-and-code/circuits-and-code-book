#include <stdbool.h>
#include <stdint.h>

uint32_t shared_counter = 0; // Shared variable

// Interrupt Service Routine (ISR) updates the counter
void ISR_Timer(void) {
  // called every 1ms
  shared_counter++; // Increment counter
}

// Main loop checks the counter
int main(void) {
  while (1) {
    if (shared_counter % 1000 == 0) {
      // Do something every 1 second
    }
  }
  return 0;
}