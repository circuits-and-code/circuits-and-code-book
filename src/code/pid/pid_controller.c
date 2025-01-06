#include "pid_typedef.h"
#include <stddef.h>

void pid_init(pid_t *pid) {
  if (pid != NULL) {
    pid->integral = 0.0F;
    pid->prev_error = 0.0F;
  }
}

float pid_step(pid_t *pid, float setpoint, float measured_output, float dt) {
  float ret = 0.0F;
  // Check for NULL pointer and positive time step
  if ((pid != NULL) && (dt > 0.0F)) {
    const float error = setpoint - measured_output;
    pid->integral += error * dt;

    const float p_term = pid->kp * error;
    const float i_term = pid->ki * pid->integral;
    const float d_term = pid->kd * (error - pid->prev_error) / dt;

    pid->prev_error = error;
    ret = p_term + i_term + d_term;
  }
  return ret;
}