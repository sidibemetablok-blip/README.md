#!/usr/bin/env python3
"""
PediaFlow Routing Engine - Earbud Telemetry & Dynamic Spatial Adaptation
Author: Moussa Sidibé / NuaRt Integration
Description: Ingests telemetry from sensory edge nodes (earbuds) to modulate 
             floor lighting corridors and thermal compensation zones.
"""

import json
import logging
import time
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] PediaFlow: %(message)s")

class PediaFlowEarbudBridge:
    def __init__(self, zone_id: str = "zone_alpha_coastal"):
        self.zone_id = zone_id
        self.node_state: Dict[str, Any] = {
            "device_id": None,
            "in_ear": True,
            "temperature_c": 25.0,
            "volume_gain": 1.0,
            "last_update": 0.0
        }
        self.routing_mode = "IMMERSIVE_BUBBLE"

    def process_telemetry(self, payload_json: str) -> Dict[str, Any]:
        """
        Traite le paquet JSON envoyé par l'ESP32 de l'écouteur.
        Exemple de payload :
        {
          "device_id": "earbud_esp32_01",
          "in_ear": false,
          "temperature_c": 29.4,
          "volume_gain": 1.0,
          "timestamp": 1731970200
        }
        """
        try:
            data = json.loads(payload_json)
            self.node_state.update({
                "device_id": data.get("device_id", "unknown"),
                "in_ear": data.get("in_ear", True),
                "temperature_c": data.get("temperature_c", 25.0),
                "volume_gain": data.get("volume_gain", 0.5),
                "last_update": time.time()
            })
            
            # Évaluation des déclencheurs spatiaux PediaFlow
            self._evaluate_spatial_transition()
            
            return {
                "status": "success",
                "zone": self.zone_id,
                "current_mode": self.routing_mode,
                "thermal_offset": self.node_state["temperature_c"] - 25.0
            }
            
        except json.JSONDecodeError as e:
            logging.error(f"Erreur de décodage du flux télémétrique: {e}")
            return {"status": "error", "message": str(e)}

    def _evaluate_spatial_transition(self) -> None:
        """Bascule le comportement de la matrice selon l'état de l'écouteur."""
        in_ear = self.node_state["in_ear"]
        temp = self.node_state["temperature_c"]
        
        if not in_ear:
            # L'écouteur est posé / hors de l'oreille -> Alerte / Mode Ouvert
            self.routing_mode = "VIGILANT_CORRIDOR"
            logging.warning(
                f"[{self.zone_id}] Écouteur hors de l'oreille détecté! "
                f"Volume arrière-plan à 100%. Activation du couloir lumineux de guidage au sol."
            )
        else:
            self.routing_mode = "IMMERSIVE_BUBBLE"
            logging.info(
                f"[{self.zone_id}] Utilisateur en mode immersif. "
                f"Température ambiante captée : {temp}°C."
            )

# Simulation d'exécution locale pour test du firmware
if __name__ == "__main__":
    engine = PediaFlowEarbudBridge(zone_id="San-Pedro-Lagoon-Hub")
    
    # Simulation d'un événement où l'usager retire l'écouteur
    simulated_packet = json.dumps({
        "device_id": "esp32_earbud_node_77",
        "in_ear": False,
        "temperature_c": 28.5,
        "volume_gain": 1.0,
        "timestamp": time.time()
    })
    
    result = engine.process_telemetry(simulated_packet)
    print("Résultat du routage PediaFlow:", json.dumps(result, indent=2))
