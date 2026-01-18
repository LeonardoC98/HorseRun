"""
Pferde-Modul für die Pferderennen-Simulation.

Jedes Pferd hat:
- 3 zufällige Parameter (durch Verteilungen bestimmt):
  1. Ausdauer (Normalverteilung)
  2. Alter/Resilienz (Exponentialverteilung)
  3. Beschleunigung (Gleichverteilung)

- 10 manuelle Parameter (streckenabhängig):
  1. Grundgeschwindigkeit
  2. Wendigkeit (gut für Kurven)
  3. Waldaffinität (gut für Waldstrecke)
  4. Sandtauglichkeit (gut für Sandbahn)
  5. Sprintfähigkeit (gut für Rennbahn)
  6. Bergsteiger (gut für Hügelstrecke)
  7. Nervenstärke (gut für Urban Course)
  8. Gewicht (beeinflusst Beschleunigung negativ, Stabilität positiv)
  9. Erfahrung (reduziert Fehler)
  10. Motivation (beeinflusst Endspurt)
"""

import numpy as np
import random
from dataclasses import dataclass, field
from typing import Tuple

# Farbpalette für Pferde
HORSE_COLORS = [
    (139, 69, 19),    # Braun
    (0, 0, 0),        # Schwarz
    (255, 255, 255),  # Weiß
    (210, 180, 140),  # Hellbraun
    (128, 128, 128),  # Grau
    (101, 67, 33),    # Dunkelbraun
    (205, 133, 63),   # Peru
    (244, 164, 96),   # Sandbraun
    (160, 82, 45),    # Sienna
    (85, 85, 85),     # Dunkelgrau
]

HORSE_NAMES = [
    "Blitz", "Sturm", "Schatten", "Donner", "Flamme",
    "Stern", "Wind", "Nebel", "Frost", "Funke",
    "Apollo", "Zeus", "Athena", "Hera", "Ares",
    "Pegasus", "Spirit", "Champion", "Victory", "Legend"
]


@dataclass
class Horse:
    """Repräsentiert ein Pferd im Rennen."""
    
    name: str
    color: Tuple[int, int, int]
    
    # Zufällige Parameter (durch Verteilungen)
    ausdauer: float = 0.0           # Normalverteilung (0-100)
    resilienz: float = 0.0          # Exponentialverteilung (0-100)
    beschleunigung: float = 0.0     # Gleichverteilung (0-100)
    
    # Manuelle Parameter (0-100)
    grundgeschwindigkeit: float = 50.0
    wendigkeit: float = 50.0
    wald_affinitaet: float = 50.0
    sand_tauglichkeit: float = 50.0
    sprint_faehigkeit: float = 50.0
    bergsteiger: float = 50.0
    nervenstaerke: float = 50.0
    gewicht: float = 50.0           # Niedriger = leichter = schneller
    erfahrung: float = 50.0
    motivation: float = 50.0
    
    # Simulationszustand
    position: float = field(default=0.0, repr=False)
    current_speed: float = field(default=0.0, repr=False)
    is_injured: bool = field(default=False, repr=False)
    injury_slowdown: float = field(default=0.0, repr=False)
    res_faktor_slowdown: float = field(default=1.0, repr=False)
    finished: bool = field(default=False, repr=False)
    finish_time: float = field(default=0.0, repr=False)
    
    # Neue Spannungs-Variablen
    fatigue: float = field(default=0.0, repr=False)  # Ermüdung (0-100)
    momentum: float = field(default=0.0, repr=False)  # Schwung/Flow
    
    def reset(self):
        """Setzt den Simulationszustand zurück."""
        self.position = 0.0
        self.current_speed = 0.0
        self.is_injured = False
        self.injury_slowdown = 0.0
        self.res_faktor_slowdown = 1.0
        self.finished = False
        self.finish_time = 0.0
        self.fatigue = 0.0
        self.momentum = 0.0
    
    def get_effective_speed(self, track_modifiers: dict, distance_covered: float, 
                            total_distance: float, race_context: dict = None) -> float:
        """
        Berechnet die effektive Geschwindigkeit basierend auf 
        Streckeneigenschaften und Pferdeparametern.
        
        race_context enthält:
        - 'leader_position': Position des führenden Pferdes
        - 'average_position': Durchschnittsposition aller Pferde
        - 'my_rank': Aktuelle Platzierung (1 = Erster)
        """
        # Basisgeschwindigkeit
        base_speed = self.grundgeschwindigkeit / 10  # Skalierung auf 0-10
        
        # === NEUE MECHANIK: Diminishing Returns ===
        # Je höher die Grundgeschwindigkeit, desto schwerer ist es, sie zu halten
        speed_penalty = (self.grundgeschwindigkeit / 100) ** 1.5 * 0.15
        base_speed *= (1.0 - speed_penalty)
        
        # === NEUE MECHANIK: Ermüdung ===
        # Schnellere Pferde ermüden schneller
        fatigue_factor = 1.0 - (self.fatigue / 100) * 0.4
        base_speed *= fatigue_factor
        
        # Ermüdung erhöhen (schnellere Pferde ermüden mehr)
        fatigue_rate = (self.grundgeschwindigkeit / 100) * 0.3 - (self.ausdauer / 100) * 0.2
        self.fatigue = min(100, self.fatigue + max(0.01, fatigue_rate) * 0.5)
        
        # === NEUE MECHANIK: Windschatten / Catch-up ===
        if race_context:
            my_rank = race_context.get('my_rank', 5)
            leader_pos = race_context.get('leader_position', self.position)
            
            # Pferde die hinten sind bekommen Windschatten-Bonus
            if my_rank > 1 and leader_pos > self.position:
                distance_behind = leader_pos - self.position
                # Maximaler Bonus von 15% wenn direkt hinter dem Führenden
                slipstream_bonus = min(0.15, distance_behind / total_distance * 0.5)
                base_speed *= (1.0 + slipstream_bonus)
                
                # Weniger Ermüdung im Windschatten
                self.fatigue = max(0, self.fatigue - 0.1)
            
            # Führendes Pferd hat mehr Druck und ermüdet schneller
            if my_rank == 1:
                self.fatigue = min(100, self.fatigue + 0.15)
                # Aber bekommt Momentum wenn es lange führt
                self.momentum = min(20, self.momentum + 0.1)
        
        # === NEUE MECHANIK: Momentum ===
        # Pferde die im Flow sind werden besser
        base_speed *= (1.0 + self.momentum / 100)
        
        # === NEUE MECHANIK: Zufällige Leistungsschwankungen ===
        # Größere Schwankungen für spannendere Rennen
        random_factor = random.gauss(1.0, 0.08)  # 8% Standardabweichung
        base_speed *= max(0.8, min(1.2, random_factor))
        
        # Beschleunigungsphase (erste 10% der Strecke)
        if distance_covered < total_distance * 0.1:
            acceleration_factor = (self.beschleunigung / 100) * (1 - self.gewicht / 150)
            base_speed *= (0.5 + 0.5 * (distance_covered / (total_distance * 0.1)))
            base_speed *= (0.8 + 0.4 * acceleration_factor)
        
        # Ausdauer-Effekt (nimmt über die Strecke ab)
        endurance_factor = 1.0 - (1.0 - self.ausdauer / 100) * (distance_covered / total_distance) * 0.3
        base_speed *= endurance_factor
        
        # Motivation für Endspurt (letzte 20%)
        if distance_covered > total_distance * 0.8:
            sprint_boost = (self.motivation / 100) * 0.2
            base_speed *= (1.0 + sprint_boost)
            # Ermüdung kann im Endspurt überwunden werden durch Motivation
            motivation_recovery = (self.motivation / 100) * 0.1
            self.fatigue = max(0, self.fatigue - motivation_recovery)
        
        # Streckenspezifische Modifikatoren anwenden
        if 'kurven_faktor' in track_modifiers:
            base_speed *= (0.7 + 0.3 * (self.wendigkeit / 100)) * track_modifiers['kurven_faktor']
        
        if 'wald_faktor' in track_modifiers:
            base_speed *= (0.6 + 0.4 * (self.wald_affinitaet / 100)) * track_modifiers['wald_faktor']
        
        if 'sand_faktor' in track_modifiers:
            base_speed *= (0.6 + 0.4 * (self.sand_tauglichkeit / 100)) * track_modifiers['sand_faktor']
        
        if 'sprint_faktor' in track_modifiers:
            base_speed *= (0.7 + 0.3 * (self.sprint_faehigkeit / 100)) * track_modifiers['sprint_faktor']
        
        if 'berg_faktor' in track_modifiers:
            # Beschleunigung hilft bei Bergen
            berg_bonus = (self.bergsteiger / 100) * 0.5 + (self.beschleunigung / 100) * 0.3
            base_speed *= (0.5 + 0.5 * berg_bonus) * track_modifiers['berg_faktor']
        
        if 'urban_faktor' in track_modifiers:
            base_speed *= (0.6 + 0.4 * (self.nervenstaerke / 100)) * track_modifiers['urban_faktor']
        
        # Erfahrung reduziert Variabilität
        variability = (1.0 - self.erfahrung / 100) * 0.1
        base_speed *= (1.0 + random.uniform(-variability, variability))
        
        # Verletzungseffekt
        if self.is_injured:
            base_speed *= (1.0 - self.injury_slowdown * self.res_faktor_slowdown)
        
        return max(0.1, base_speed)
    
    def check_injury(self, injury_chance: float):
        """Prüft ob das Pferd eine Verletzung erleidet."""
        if self.is_injured:
            return
        
        # Resilienz reduziert Verletzungschance
        actual_chance = injury_chance * (1.0 - self.resilienz / 150)
        
        if random.random() < actual_chance:
            self.is_injured = True
            # Verlangsamung basierend auf Resilienz
            self.injury_slowdown = 0.1 + (1.0 - self.resilienz / 100) * 0.2
            # Resilienzfaktor: 1 bei hoher Resilienz, 3 bei niedriger, mit Zufall
            self.res_faktor_slowdown = 1 + (1.0 - self.resilienz / 100) * 2 + random.uniform(-0.2, 0.2)
    
    def to_dict(self) -> dict:
        """Konvertiert das Pferd zu einem Dictionary."""
        return {
            'name': self.name,
            'color': self.color,
            'ausdauer': self.ausdauer,
            'resilienz': self.resilienz,
            'beschleunigung': self.beschleunigung,
            'grundgeschwindigkeit': self.grundgeschwindigkeit,
            'wendigkeit': self.wendigkeit,
            'wald_affinitaet': self.wald_affinitaet,
            'sand_tauglichkeit': self.sand_tauglichkeit,
            'sprint_faehigkeit': self.sprint_faehigkeit,
            'bergsteiger': self.bergsteiger,
            'nervenstaerke': self.nervenstaerke,
            'gewicht': self.gewicht,
            'erfahrung': self.erfahrung,
            'motivation': self.motivation
        }


def generate_random_stats() -> Tuple[float, float, float]:
    """
    Generiert die 3 zufälligen Parameter mit den geforderten Verteilungen.
    
    Returns:
        Tuple (ausdauer, resilienz, beschleunigung)
    """
    # Ausdauer: Normalverteilung (Mittelwert 50, Standardabweichung 15)
    ausdauer = np.clip(np.random.normal(50, 15), 0, 100)
    
    # Resilienz/Alter: Exponentialverteilung (skaliert auf 0-100)
    # Jüngere Pferde haben höhere Resilienz
    raw_exp = np.random.exponential(scale=30)
    resilienz = np.clip(100 - raw_exp, 0, 100)
    
    # Beschleunigung: Gleichverteilung (0-100)
    beschleunigung = np.random.uniform(0, 100)
    
    return float(ausdauer), float(resilienz), float(beschleunigung)


def create_random_horse(name: str = None, color: Tuple[int, int, int] = None) -> Horse:
    """
    Erstellt ein komplett zufälliges Pferd.
    """
    if name is None:
        name = random.choice(HORSE_NAMES) + " " + str(random.randint(1, 99))
    
    if color is None:
        color = random.choice(HORSE_COLORS)
    
    ausdauer, resilienz, beschleunigung = generate_random_stats()
    
    return Horse(
        name=name,
        color=color,
        ausdauer=ausdauer,
        resilienz=resilienz,
        beschleunigung=beschleunigung,
        grundgeschwindigkeit=random.uniform(30, 80),
        wendigkeit=random.uniform(20, 90),
        wald_affinitaet=random.uniform(20, 90),
        sand_tauglichkeit=random.uniform(20, 90),
        sprint_faehigkeit=random.uniform(20, 90),
        bergsteiger=random.uniform(20, 90),
        nervenstaerke=random.uniform(20, 90),
        gewicht=random.uniform(30, 80),
        erfahrung=random.uniform(10, 90),
        motivation=random.uniform(30, 90)
    )


def create_custom_horse(name: str, color: Tuple[int, int, int],
                        grundgeschwindigkeit: float,
                        wendigkeit: float,
                        wald_affinitaet: float,
                        sand_tauglichkeit: float,
                        sprint_faehigkeit: float,
                        bergsteiger: float,
                        nervenstaerke: float,
                        gewicht: float,
                        erfahrung: float,
                        motivation: float) -> Horse:
    """
    Erstellt ein benutzerdefiniertes Pferd.
    Die 3 Verteilungsparameter werden zufällig generiert.
    """
    ausdauer, resilienz, beschleunigung = generate_random_stats()
    
    return Horse(
        name=name,
        color=color,
        ausdauer=ausdauer,
        resilienz=resilienz,
        beschleunigung=beschleunigung,
        grundgeschwindigkeit=np.clip(grundgeschwindigkeit, 0, 100),
        wendigkeit=np.clip(wendigkeit, 0, 100),
        wald_affinitaet=np.clip(wald_affinitaet, 0, 100),
        sand_tauglichkeit=np.clip(sand_tauglichkeit, 0, 100),
        sprint_faehigkeit=np.clip(sprint_faehigkeit, 0, 100),
        bergsteiger=np.clip(bergsteiger, 0, 100),
        nervenstaerke=np.clip(nervenstaerke, 0, 100),
        gewicht=np.clip(gewicht, 0, 100),
        erfahrung=np.clip(erfahrung, 0, 100),
        motivation=np.clip(motivation, 0, 100)
    )
