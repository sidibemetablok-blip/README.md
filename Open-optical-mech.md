# Open-Optical-Mesh (OOM)

## 1. Vision & Problématique
Les infrastructures de géolocalisation et de transmission actuelles (GPS, radiofréquences) reposent sur des signaux hertzierns ouverts, particulièrement vulnérables à l'entropie, au brouillage (*jamming*) et à la falsification (*spoofing*). 

Le projet **Open-Optical-Mesh** propose de contourner ces failles structurelles en inversant la topologie classique des télécommunications spatiales :
- **L'émetteur/récepteur radio centralisé** est remplacé par une **liaison optique directe en ligne de vue**.
- La sécurité ne repose plus sur une couche logicielle ou une autorité centrale, mais sur la **géométrie et la physique pure du signal**.

---

## 2. Architecture du Système

### A. Le Satellite-Écran (Passive/Reflective Unit)
Au lieu d'émettre des fréquences radio omnibus :
- Le satellite agit comme une **surface passive ou un réflecteur directionnel**.
- Il projette ou renvoie des états lumineux / impulsions optiques déterministes.

### B. La Diode Structurelle (Ground Sensor)
Au sol, le capteur agit comme une **rétine optique physique** :
- Réception directe de l'impulsion (laser / infrarouge / optique quantique).
- Immunité totale aux perturbations hertziennes et aux attaques par injection de bruit.

---

## 3. Propriétés de Sécurité & Modèle de Vérité

| Menace Classique | Réponse de l'Architecture OOM |
| :--- | :--- |
| **Brouillage Radio (Jamming)** | Inopérant (Le capteur lit la lumière, pas la fréquence radio). |
| **Falsification (Spoofing GPS)** | Impossible sans interposition physique directe dans le faisceau. |
| **Interception Man-In-The-Middle** | Détection immédiate par rupture ou altération de la ligne de vue (*Line-of-Sight*). |
| **Dépendance Cloud / Serveurs** | Modèle déterministe « tir direct » sans intermédiaire centralisé. |

---

## 4. Cas d'Usage
- **Sécurité Publique & Secours :** Maintien d'un canal de synchronisation lors d'un effondrement des réseaux cellulaires ou GPS.
- **Infrastructures Critiques :** Horodatage et transmission de données pour grilles électriques ou transports autonomes.
- **Zones à Haut Bruit Entropique :** Télécommunications résilientes en environnement hostile ou saturé.

---

## 5. Feuille de Route (*Roadmap*)
- [x] Spécification du modèle conceptuel (Inversion Satellite/Diode)
- [ ] Simulation de la propagation optique à travers les couches atmosphériques
- [ ] Prototypage de la diode réceptrice au sol
- [ ] Rédaction des équations de ciblage optique point-à-point

---

## License
Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
