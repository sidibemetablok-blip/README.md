# 🔌 RPCE — Hardware & Circuit Schematic Specifications

This document outlines the hardware requirements, Component Bill of Materials (BOM), and circuit connection layout for the **Entropic Control Pasta Reactor (RPCE)**.

---

## 🛠️ Bill of Materials (BOM)

| Component | Specification / Model | Function |
| :--- | :--- | :--- |
| **Microcontroller** | ESP32-WROOM-32 (33-pin) | System logic, PWM timing, and telemetry processing |
| **Power MOSFET** | IRLZ44N (N-Channel, Logic Level) | High-frequency switching driver for the piezo atomizer |
| **Piezoelectric Injector** | Zirconia Ceramic Disk (105 kHz, 3–12V) | Ultrasonic micro-mist generation |
| **Thermal Sensor** | MLX90614 or Analog IR Module | Non-contact surface temperature telemetry |
| **Safety Relay** | 5V SRD-05VDC-SL-C Electromechanical Relay | Physical power disconnect on critical failure |
| **Pull-down Resistor** | 10 kΩ | Gate stabilization for MOSFET |
| **Flyback Diode** | 1N4007 | Inductive kickback protection across relay coil |
| **Power Supply** | 5V / 2A DC Adapter | System primary power |

---

## 📐 Circuit Pinout & Wiring Connections

| Component Pin | ESP32 / Circuit Connection | Signal / Purpose |
| :--- | :--- | :--- |
| **MOSFET Gate (G)** | GPIO 18 (via 10kΩ Pull-down to GND) | 105 kHz Ultrasonic PWM signal |
| **MOSFET Drain (D)** | Piezo Injector Negative (-) Pin | Atomizer drive loop |
| **MOSFET Source (S)** | Common Ground (GND) | Reference ground |
| **Piezo Positive (+)** | 5V DC (Relay Switched) | Power supply line |
| **IR Sensor Output** | GPIO 34 (ADC Input) | Real-time infrared thermal reading |
| **IR Sensor Power** | 3.3V / GND | Sensor logic power |
| **Relay Signal Input** | GPIO 23 | Electromechanical safety toggle |
| **Relay Power Circuit** | Series inline with 5V Main Rail | Complete power cutoff during critical overtemperature |

---

> **⚠️ Hardware Design Note:** Ensure a 10 kΩ pull-down resistor is connected between the MOSFET Gate and GND to prevent unintentional activation during micro-controller bootup sequence.
