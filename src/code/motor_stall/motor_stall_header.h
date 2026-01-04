typedef struct {
    float measured_current_A;  // Measured current in Amperes
    float commanded_bus_voltage_V; // Commanded bus voltage in Volts
    float motor_speed_rad_per_s; // Motor speed in radians per second from encoder
} motor_input_data_t;

typedef struct {
    motor_input_data_t input_data;
    bool is_stalled; // True if the motor is stalled, false otherwise
    // Additional variables can be added as needed
} motor_handle_t;

/**
 * @brief Function to be called every 1 ms for motor stall detection
 * @param motor Pointer to the motor handle structure
 */
void motor_stall_detect_period_run_1ms(motor_handle_t *motor);

