# Technical Architecture & Functional Safety Specification

> **Project:** NEXUS-ISA (Neutral Engagement eXecution for Intelligent Speed Assistance)  
> **Safety Level:** ISO 26262 ASIL-C / ASIL-D System Target  
> **Domain:** Drive-by-Wire Speed Regulation & Torque Neutralization  

---

## 1. System Overview

The **NEXUS-ISA** system introduces a passive-active torque neutralization layer situated between the driver input acquisition unit and the Powertrain Control Module (PCM). Upon detecting that the vehicle has reached or exceeded the active Speed Limit ($V_{\text{limit}}$), the system transitions the engine/inverter torque request into a **Neutral State** while maintaining driver override capability ($d\theta/dt > 150\%/\text{s}$ or Kick-down $> 85\%$).


---

## 2. Hardware Architecture & Redundancy

To satisfy ISO 26262 functional safety requirements (ASIL-C), all critical sensing and processing paths feature hardware redundancy:

### 2.1 Sensor Layer
* **Dual Accelerator Pedal Position (DAPP):**
  * **Channel 1 ($V_1$):** Analog output ($0.5\text{V} - 4.5\text{V}$) via Hall-effect sensor 1.
  * **Channel 2 ($V_2$):** Complementary/Inverted analog output ($4.5\text{V} - 0.5\text{V}$) via Hall-effect sensor 2.
  * **Plausibility Window:** Voltage divergence $|V_1 - (5.0\text{V} - V_2)| \le 0.15\text{V}$.
* **Wheel Speed & Velocity Acquisition:**
  * Quadrature Wheel Speed Sensors (ABS/ESP CAN bus) combined with 6-axis Inertial Measurement Unit (IMU).

### 2.2 Microcontroller Architecture
* **Dual-Core Lockstep (DCLS) Microcontroller:** High-integrity safety MCU (e.g., AURIX™ TC3xx / SPC58) running redundant cores in lockstep execution to detect hardware fault transients.
* **External Window Watchdog:** Hardware monitor requiring periodic challenge-response pulses every $10\text{ ms}$.

---

## 3. Software Architecture & Control Logic

The core execution loop operates on an AUTOSAR-compliant architecture with strict separation between Safety-Critical (ASIL-C) and Non-Safety (ASIL-A/BSW) tasks.
### 3.1 Neutral Torque Calculation
When $V_{\text{actual}} \ge V_{\text{limit}}$ and no Override condition is present, the demanded torque ($T_{\text{demand}}$) is modulated as follows:

$$T_{\text{demand}} = T_{\text{drag}} + K_p \cdot (V_{\text{limit}} - V_{\text{actual}})$$

Where $T_{\text{drag}}$ represents the aerodynamic and rolling resistance torque required to maintain steady velocity without acceleration.

### 3.2 Emergency Override Logic
The Neutral State is immediately suspended under either of the following conditions:
1. **High Dynamic Pedal Gradient:** $\frac{d\theta}{dt} > 150\%/\text{s}$
2. **Kick-down Threshold Encroachment:** $\theta_{\text{pedal}} > 85\%$

---

## 4. Safety Concept & Fail-Safe Strategy

The safety strategy enforces a **Fail-Passive / Fail-Safe** behavior. Any detected anomaly triggers an immediate release of the torque neutralization layer, returning total control directly to the base engine management system.

| Hazard ID | Failure Mode | Diagnostic Method | Fail-Safe State Action | Fault Detection Time (FDTI) |
| :--- | :--- | :--- | :--- | :--- |
| **HAZ-01** | DAPP Signal Discrepancy | Cross-channel voltage comparison | Bypass NEXUS-ISA; revert to base PCM pedal mapping. | $< 20\text{ ms}$ |
| **HAZ-02** | Loss of ISA CAN Frame | CAN Timeout monitor ($> 200\text{ ms}$) | Gentle ramp-down ($1.2\text{ s}$) to passive state; illuminate cluster warning. | $< 50\text{ ms}$ |
| **HAZ-03** | Microcontroller Lockup | Hardware Window Watchdog reset | Open hardware safety bypass relays (Fail-Passive hardware loop). | $< 10\text{ ms}$ |
| **HAZ-04** | Invalid Wheel Speed Signal | IMU vs ABS speed variance $> 5\%$ | Disable torque neutralization; issue UDS Diagnostic Trouble Code (DTC). | $< 100\text{ ms}$ |

---

## 5. Communications & Network Interface

All system interactions use dedicated CAN FD channels with **End-to-End (E2E) Profile 2** data protection.

* **Protocol:** CAN FD (500 kbps Nominal / 2 Mbps Data Rate)
* **E2E Protection:** Data CRC-8, 4-bit Alive Counter, Sequence Counter
* **Core Messages:**
  * `0x180 NEXUS_PedalStatus`: Position, gradient, override flag.
  * `0x210 ISA_SpeedLimit`: Active limit, confidence level, provider status.
  * `0x320 NEXUS_TorqueCmd`: Neutral torque request, system health status.

---

## 6. Compliance & Industry Standards

- **ISO 26262:2018:** Road Vehicles — Functional Safety (ASIL-C System Target)
- **UN/ECE Regulation No. 159 / 160:** Event Data Recorder (EDR) & ISA Systems
- **ISO 14229 (UDS):** Unified Diagnostic Services for Fault Logging and Flash Calibration
