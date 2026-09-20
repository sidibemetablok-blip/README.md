#!/usr/bin/env python3
"""
PediaFlow — Engine de Simulation de Routage Dynamique 4D
Description: Simulation de régulation de flux piétons anonymisée basée sur
             la pression piézoélectrique et le balisage lumineux dynamique.
License: MIT
"""

import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Footstep:
    """Représente l'empreinte cinétique d'un pas (Niveau 2 - Piézoélectrique)."""

    sensor_id: str
    x: float  # Coordonnée X en mètres
    y: float  # Coordonnée Y en mètres
    pressure_kpa: float  # Pression exercée (kPa)
    cadence_hz: float  # Cadence de marche (Hz)
    timestamp: float


@dataclass
class Zone:
    """Représente une section du sol instrumenté."""

    zone_id: str
    x_min: float
    x_max: float
    capacity_limit: int
    current_density: int = 0
    light_vector_speed: float = 1.2  # Vitesse de l'onde lumineuse (m/s)
    light_color_hex: str = "#00FFCC"  # Couleur du balisage dynamique (Niveau 3)


class PediaFlowEngine:
    def __init__(self):
        # Définition des zones du sol (Couloir principal et bifurcations A / B)
        self.zones = {
            "main_corridor": Zone("Main_Corridor", 0.0, 10.0, capacity_limit=15),
            "exit_a": Zone("Exit_A", 10.0, 20.0, capacity_limit=8),
            "exit_b": Zone("Exit_B", 10.0, 20.0, capacity_limit=8),
        }
        self.active_steps: List[Footstep] = []

    def register_footstep(self, step: Footstep):
        """Enregistre un pas détecté par la matrice de sol sans collecter d'identifiant personnel."""
        self.active_steps.append(step)

    def process_frame(self):
        """Analyse la densité actuelle et ajuste la rétroaction lumineuse 4D."""
        # Réinitialisation du comptage de densité
        for zone in self.zones.values():
            zone.current_density = 0

        # Mapping anonyme des pas dans les zones
        for step in self.active_steps:
            if step.x < 10.0:
                self.zones["main_corridor"].current_density += 1
            elif step.y >= 0:
                self.zones["exit_a"].current_density += 1
            else:
                self.zones["exit_b"].current_density += 1

        # Vider le buffer des pas traités (données volatiles, zéro stockage PII)
        self.active_steps.clear()

        # Logique de régulation du Dr. Solution / Dr. Virus
        self._balance_flows()

    def _balance_flows(self):
        """Ajuste le balisage dynamique en fonction de la saturation des voies."""
        exit_a = self.zones["exit_a"]
        exit_b = self.zones["exit_b"]

        print(
            f"--- [PediaCore Status] Densités -> Couloir: {self.zones['main_corridor'].current_density} | Exit A: {exit_a.current_density}/{exit_a.capacity_limit} | Exit B: {exit_b.current_density}/{exit_b.capacity_limit}"
        )

        # Détection de saturation sur l'accès A
        if exit_a.current_density >= exit_a.capacity_limit:
            print(
                "⚠️  [Alerte Saturation] Voie A saturée ! Activation de la bifurcation dynamique vers la Voie B."
            )
            exit_a.light_color_hex = "#FF3333"  # Rouge / Ralentissement
            exit_a.light_vector_speed = 0.5  # Signal d'amortissement

            exit_b.light_color_hex = "#00FF00"  # Vert / Fluide
            exit_b.light_vector_speed = 1.8  # Vecteur d'accélération
        else:
            # Mode nominal
            exit_a.light_color_hex = "#00FFCC"
            exit_a.light_vector_speed = 1.2
            exit_b.light_color_hex = "#00FFCC"
            exit_b.light_vector_speed = 1.2


# --- Simulation de flux piéton ---
if __name__ == "__main__":
    engine = PediaFlowEngine()
    print("🚀 Démarrage du moteur de simulation PediaFlow (NuaRts Framework)...")
    print("Suivi vectoriel anonyme actif. Zéro donnée biométrique collectée.\n")

    # Simulation sur 5 cycles de marche
    for cycle in range(1, 6):
        print(f"\n=== Cycle de simulation #{cycle} ===")

        # Génération d'une foule simulée avec surcharge progressive sur l'Exit A
        num_pedestrians = random.randint(10, 25)
        for p in range(num_pedestrians):
            # Ciblage volontairement saturé vers l'exit A pour déclencher le régulateur
            dest_y = 2.0 if cycle > 2 else random.choice([-2.0, 2.0])

            step = Footstep(
                sensor_id=f"SENSE_{random.randint(100,999)}",
                x=random.uniform(0.0, 15.0),
                y=dest_y,
                pressure_kpa=random.uniform(60.0, 95.0),
                cadence_hz=random.uniform(1.1, 1.6),
                timestamp=time.time(),
            )
            engine.register_footstep(step)

        engine.process_frame()
        time.sleep(1)
