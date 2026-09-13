#include <Arduino.h>

// --- Hardware Pinouts & Configuration ---
const uint8_t PIEZO_PWM_PIN = 18;      // PWM output to MOSFET / Piezo Driver
const uint8_t IR_SENSOR_PIN = 34;      // Analog input from IR Sensor Matrix
const uint8_t SAFETY_RELAY_PIN = 23;   // Hardware emergency cutoff relay

// --- Physical Parameters & Frequencies ---
const uint32_t PIEZO_FREQ_HZ = 105000; // Ultrasonic resonance frequency (105 kHz)
const uint8_t PWM_RESOLUTION = 8;      // 8-bit resolution (0 - 255)
const uint8_t PWM_CHANNEL = 0;

// --- Thermodynamic Safety Thresholds ---
const float TEMP_CRITICAL_C = 85.0;    // Critical temperature for pyrolysis initiation
const float VOLTAGE_REF = 3.3;

// Local telemetry state structure
struct SystemState {
    float currentTemp;
    bool mistActive;
    bool emergencyCutoff;
};

SystemState state = {20.0, false, false};

// Read and convert IR thermal telemetry
float readIRTemperature() {
    int rawAnalog = analogRead(IR_SENSOR_PIN);
    float voltage = (rawAnalog / 4095.0) * VOLTAGE_REF;
    // Simplified linear conversion: 10mV/°C with offset
    float temperature = voltage * 30.0; 
    return temperature;
}

// Trigger piezoelectric micro-injection (Quantum H2O micro-mist)
void setPiezoState(bool enable, uint8_t dutyCycle = 128) {
    if (enable && !state.emergencyCutoff) {
        ledcWrite(PWM_CHANNEL, dutyCycle); // 50% duty cycle at 105 kHz
        state.mistActive = true;
        Serial.println(F("[HARDWARE] Piezo Injector: ACTIVE (105 kHz)"));
    } else {
        ledcWrite(PWM_CHANNEL, 0);
        state.mistActive = false;
        Serial.println(F("[HARDWARE] Piezo Injector: INACTIVE"));
    }
}

// Hardware Fail-Safe Protocol (Electromechanical Disconnect)
void triggerSafetyCutoff() {
    state.emergencyCutoff = true;
    setPiezoState(false);
    digitalWrite(SAFETY_RELAY_PIN, LOW); // Open physical power relay
    Serial.println(F("[FAIL-SAFE] CRITICAL ALERT: Enthalpy threshold exceeded. Hardware cutoff engaged."));
}

void setup() {
    Serial.begin(115200);
    
    pinMode(SAFETY_RELAY_PIN, OUTPUT);
    digitalWrite(SAFETY_RELAY_PIN, HIGH); // Maintain power circuit closed
    
    // Configure hardware PWM timer for ultrasonic piezo frequency
    ledcSetup(PWM_CHANNEL, PIEZO_FREQ_HZ, PWM_RESOLUTION);
    ledcAttachPin(PIEZO_PWM_PIN, PWM_CHANNEL);
    
    Serial.println(F("--- Initializing RPCE Firmware v1.0.2 ---"));
    Serial.println(F("Piezoelectric injection system ready."));
}

void loop() {
    // 1. Telemetry acquisition
    state.currentTemp = readIRTemperature();
    
    Serial.print(F("[TELEM] IR Temperature: "));
    Serial.print(state.currentTemp);
    Serial.println(F(" °C"));
    
    // 2. Entropic regulation evaluation
    if (state.currentTemp >= TEMP_CRITICAL_C && !state.mistActive) {
        Serial.println(F("[REGULATION] Pyrolysis risk detected. Deploying micro-mist."));
        setPiezoState(true, 180); // Targeted injection
    } else if (state.currentTemp < (TEMP_CRITICAL_C - 10.0) && state.mistActive) {
        Serial.println(F("[REGULATION] Enthalpy stabilized. Stopping injection."));
        setPiezoState(false);
    }
    
    // 3. Absolute overtemperature fail-safe check
    if (state.currentTemp > 110.0) {
        triggerSafetyCutoff();
    }
    
    delay(100); // 10 Hz control loop
}
