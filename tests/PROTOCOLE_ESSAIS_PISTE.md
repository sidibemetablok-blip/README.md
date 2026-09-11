# Track Testing Protocol & Homologation Validation Plan

> **Project:** NEXUS-ISA (Neutral Engagement eXecution for Intelligent Speed Assistance)  
> **Safety Standard:** ISO 26262 (ASIL-C Target) / UN ECE Regulation No. 159 & 160 Alignment  
> **Facility Requirement:** Closed Proving Ground / Track Validation Facility (ISO 17025 Certified)  

---

## 1. Test Objectives & Scope

This testing protocol defines the operational, safety, and validation procedures required to verify the functional integrity, failure modes, and driver override capabilities of the **NEXUS-ISA** Drive-by-Wire torque neutralization system on a closed track.

* **Primary Objective:** Ensure accurate torque suppression upon reaching set speed limits ($V_{\text{limit}}$).
* **Secondary Objective:** Validate driver safety override mechanisms ($\frac{d\theta}{dt} > 150\%/\text{s}$ and Kick-down $> 85\%$).
* **Fault Injection Objective:** Verify Fail-Passive behavior under sensor, CAN bus, or hardware fault conditions within Fault Detection Time Intervals (FDTI).

---

## 2. Test Track Setup & Environmental Conditions

Tests must be conducted under controlled track conditions to ensure reproducibility:

* **Surface:** Dry asphalt, zero gradient ($\le 0.5\%$), friction coefficient $\mu \ge 0.8$.
* **Ambient Conditions:** Temperature $10^\circ\text{C}$ to $35^\circ\text{C}$, wind speed $< 5\text{ m/s}$, zero precipitation.
* **Telemetry Setup:** High-precision Differential GPS (DGPS) + IMU logging at $100\text{ Hz}$ synced via CAN bus acquisition (e.g., Vector CANalyzer / Dewesoft).

---

## 3. Test Scenarios & Procedure Specifications

| Test ID | Category | Scenario Description | Initial Speed ($V_{\text{init}}$) | Speed Limit ($V_{\text{limit}}$) | Target Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS-01** | Torque Regulation | Steady acceleration into speed limit zone | $30\text{ km/h}$ | $50\text{ km/h}$ | Smooth torque neutralization at $50\text{ km/h} \pm 1\text{ km/h}$; no torque overshoot. |
| **TS-02** | Rapid Override | Kick-down engagement during active limit | $50\text{ km/h}$ (Limited) | $50\text{ km/h}$ | Pedal $> 85\%$ triggers full torque release in $< 50\text{ ms}$. |
| **TS-03** | Dynamic Override | Fast pedal gradient kick during active limit | $50\text{ km/h}$ (Limited) | $50\text{ km/h}$ | $\frac{d\theta}{dt} > 150\%/\text{s}$ releases neutralization in $< 30\text{ ms}$. |
| **TS-04** | ISA Transition | Dynamic speed limit step reduction | $80\text{ km/h}$ | $80 \rightarrow 50\text{ km/h}$ | Deceleration curve matches $T_{\text{drag}}$ profile smoothly without lockup. |

---

## 4. Fault Injection & Functional Safety (ASIL-C)

To validate safety compliance (ISO 26262), fault injection hardware will trigger simulated hardware/software failures during motion:


* **FS-01 (Sensor Discrepancy):** Inject a $1.0\text{V}$ offset into DAPP Channel 1.
  * *Expected Behavior:* System must disconnect within $< 20\text{ ms}$, illuminate the dashboard hazard indicator, and return full control to the baseline engine map.
* **FS-02 (CAN Timeout):** Disconnect ISA CAN communication line during torque regulation.
  * *Expected Behavior:* System transitions to passive mode within $< 50\text{ ms}$ via smooth $1.2\text{ s}$ ramp-down.
* **FS-03 (Watchdog Reset):** Force microcontroller watchdog timeout.
  * *Expected Behavior:* Safety relays open immediately ($< 10\text{ ms}$ hardware isolation).

---

## 5. Test Log & Execution Summary Template
