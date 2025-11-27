typedef struct {
    float commanded_bus_voltage_V; // Commanded motor bus voltage in Volts
    // float proposed_sensor_UNIT; 
} motor_input_data_t;

typedef struct {
    bool is_stalled; // True if the motor is stalled, false otherwise
    // Additional variables can be added as needed
} motor_handle_t;

/**
 * @brief Function to be called every 1 ms for motor stall detection
 * @param input_data Pointer to the motor input data structure
 * @param motor Pointer to the static motor handle structure
 */
void motor_stall_detect_period_run_1ms(const motor_input_data_t* const input_data, motor_handle_t *motor);

