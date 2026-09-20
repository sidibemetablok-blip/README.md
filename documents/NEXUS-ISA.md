# Neutral Speed Regulator & Accelerator System (RV-AN)

> **Road Safety Innovation & Automotive Homologation (ASIL-C / ISO 26262)**

## 📌 Project Overview
The **RV-AN** project introduces a passive-active assistance mechanism designed to neutralize unnecessary or unintended engine torque requests once a vehicle reaches the maximum speed limit, while guaranteeing an immediate emergency override capability for the driver.

This repository brings together the technical documentation, regulatory homologation strategy (UN/ECE - ISA), track testing protocol, and functional safety analysis.

---

## 🎯 Strategic & Safety Objectives
- **Prevention of Unintended Over-Acceleration:** Neutralization of the accelerator pedal signal at the speed limit.
- **ISO 26262 (ASIL-C) Compliance:** Fail-Safe architecture ensuring absolute priority for vehicle safety.
- **ISA (Intelligent Speed Assistance) Alignment:** Seamless integration with European driver assistance systems (AIV).
- **Energy Efficiency:** Smoothing of acceleration curves to reduce emissions and mechanical wear.

---

## 📂 Documentation Structure

- 📄 **[Technical Architecture](docs/ARCHITECTURE_TECHNIQUE.md)**: Hardware/software specifications and sensor redundancies.
- 🧪 **[Track Testing Protocol](tests/PROTOCOLE_ESSAIS_PISTE.md)**: Emergency scenarios, override tests, and fault injections (FS-01, FS-02, FS-03).
- 📊 **[Homologation Test Report](tests/RAPPORT_HOMOLOGATION.md)**: Test report template compliant with ISO/IEC 17025.

---

## 🚀 Project Status & Next Steps
- [x] Specification of the Override mechanism (dθ/dt > 150%/s and Kick-down > 85%)
- [ ] Proof of Concept (PoC) implementation on a demonstrator vehicle
- [ ] Presentation of the Policy Brief to road safety authorities

---

## 📜 License
This project is distributed under the [MIT / Apache 2.0] License. See the `LICENSE` file for more details.
