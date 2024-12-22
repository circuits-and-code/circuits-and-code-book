#include "pid_typedef.h"
#include <stddef.h>

float pid_step(pid_t *pid, float setpoint, float measured_output, float dt) {
  float ret = 0.0F;
  if (pid != NULL) {
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