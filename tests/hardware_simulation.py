import time
import random

# --- Physical & Circuit Parameters ---
TEMP_CRITICAL_C = 85.0    # Pyrolysis threshold (°C)
TEMP_SAFETY_CUTOFF = 110.0 # Emergency relay cutoff threshold (°C)
PIEZO_FREQ_HZ = 105000     # Hardware PWM frequency (105 kHz)

class HardwareSimulation:
    def __init__(self):
        self.current_temp = 25.0       # Ambient room temperature (°C)
        self.pwm_active = False        # MOSFET / Piezo state
        self.relay_closed = True       # Physical safety relay status
        self.duty_cycle = 0            # PWM Duty Cycle (0 - 255)

    def read_ir_sensor(self) -> float:
        """Simulates IR sensor reading with analog ADC noise."""
        noise = random.uniform(-0.5, 0.5)
        return round(self.current_temp + noise, 2)

    def update_piezo_pwm(self, active: bool, duty: int = 128):
        """Simulates ESP32 PWM timer output to MOSFET Gate."""
        if self.relay_closed and active:
            self.pwm_active = True
            self.duty_cycle = duty
            print(f"  [PWM GENERATOR] Output Active: {PIEZO_FREQ_HZ} Hz @ Duty Cycle {duty}/255")
        else:
            self.pwm_active = False
            self.duty_cycle = 0
            print("  [PWM GENERATOR] Output Inactive (0 Hz)")

    def trigger_safety_relay(self):
        """Simulates physical relay disconnect."""
        self.relay_closed = False
        self.update_piezo_pwm(False)
        print("  [SAFETY RELAY] 🔴 CRITICAL OVERHEAT DETECTED! Relay Tripped. Power Disconnected.")

    def step_thermal_model(self, thermal_input_power: float):
        """Simulates heat rise and cooling effects of ultrasonic misting."""
        if not self.relay_closed:
            # Emergency shutoff: natural cooling back to ambient
            self.current_temp -= 1.5
            return

        # Heating effect
        self.current_temp += thermal_input_power

        # Cooling effect from piezo misting
        if self.pwm_active:
            misting_cooling_rate = 2.8  # Heat dissipation via ultrasonic atomization
            self.current_temp -= misting_cooling_rate

def run_simulation():
    print("==================================================")
    print("      RPCE Hardware Circuit Simulation v1.0       ")
    print("==================================================")
    
    sim = HardwareSimulation()
    simulated_steps = 20

    for step in range(1, simulated_steps + 1):
        # Simulate varying microwave thermal power input
        thermal_input = round(random.uniform(1.2, 3.5), 2)
        sim.step_thermal_model(thermal_input)
        
        sensor_temp = sim.read_ir_sensor()
        print(f"\n[Step {step:02d}] IR Sensor Reading: {sensor_temp} °C | Relay: {'CLOSED' if sim.relay_closed else 'OPEN'}")

        # --- Control Loop Logic (Simulating ESP32 Firmware) ---
        if sensor_temp > TEMP_SAFETY_CUTOFF and sim.relay_closed:
            sim.trigger_safety_relay()
        elif sensor_temp >= TEMP_CRITICAL_C and sim.relay_closed:
            print("  [ESP32 LOGIC] High enthalpy detected. Enabling 105 kHz PWM drive...")
            sim.update_piezo_pwm(True, duty=180)
        elif sensor_temp < (TEMP_CRITICAL_C - 10.0) and sim.pwm_active:
            print("  [ESP32 LOGIC] Temperature stabilized. Disabling PWM drive...")
            sim.update_piezo_pwm(False)

        time.sleep(0.2)

    print("\n==================================================")
    print("            Simulation Cycle Complete             ")
    print("==================================================")

if __name__ == "__main__":
    run_simulation()
