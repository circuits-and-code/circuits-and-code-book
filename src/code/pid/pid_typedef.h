typedef struct {
  float kp; // Proportional gain constant
  float ki; // Integral gain constant
  float kd; // Derivative gain constant

  float integral;   // Stored integral value
  float prev_error; // Stored last input value
} pid_t;