"""
Simulations-Engine für das Pferderennen.

Verwaltet die Simulation, Geschwindigkeitssteuerung und Ergebnisberechnung.
"""

import time
from typing import List, Dict, Callable, Optional, Tuple
from dataclasses import dataclass, field
from pferde.horse import Horse
from strecken.base_track import Track


@dataclass
class RaceResult:
    """Ergebnis eines Rennens für ein Pferd."""
    horse: Horse
    position: int
    finish_time: float
    was_injured: bool
    max_speed: float
    avg_speed: float
    injury_at_position: Optional[float] = None
    speed_over_time: List[Tuple[float, float]] = field(default_factory=list)  # (time, speed)
    position_over_time: List[Tuple[float, float]] = field(default_factory=list)  # (time, position)
    injury_times: List[float] = field(default_factory=list)  # Zeitpunkte von Verletzungen
    segment_performance: Dict[str, Dict] = field(default_factory=dict)  # Performance pro Segment


@dataclass
class SimulationState:
    """Aktueller Zustand der Simulation."""
    is_running: bool = False
    is_paused: bool = False
    is_finished: bool = False
    elapsed_time: float = 0.0
    speed_multiplier: float = 1.0
    tick_count: int = 0


class RaceSimulation:
    """Hauptklasse für die Renn-Simulation."""
    
    def __init__(self, horses: List[Horse], track: Track):
        self.horses = horses
        self.track = track
        self.state = SimulationState()
        self.results: List[RaceResult] = []
        self.finish_order: List[Horse] = []
        
        # Statistiken während des Rennens
        self.speed_history: Dict[str, List[Tuple[float, float]]] = {h.name: [] for h in horses}  # (time, speed)
        self.position_history: Dict[str, List[Tuple[float, float]]] = {h.name: [] for h in horses}  # (time, position)
        self.injury_history: Dict[str, List[float]] = {h.name: [] for h in horses}  # Zeitpunkte der Verletzungen
        self.segment_stats: Dict[str, Dict[str, List[float]]] = {h.name: {} for h in horses}  # Performance pro Segment
        
        # Callbacks für UI-Updates
        self.on_update: Optional[Callable] = None
        self.on_finish: Optional[Callable] = None
        
        # Reset all horses
        for horse in self.horses:
            horse.reset()
    
    def set_speed_multiplier(self, multiplier: float):
        """Setzt den Geschwindigkeitsmultiplikator (0.1 - 5.0)."""
        self.state.speed_multiplier = max(0.1, min(5.0, multiplier))
    
    def increase_speed(self):
        """Erhöht die Simulationsgeschwindigkeit."""
        self.set_speed_multiplier(self.state.speed_multiplier + 0.25)
    
    def decrease_speed(self):
        """Verringert die Simulationsgeschwindigkeit."""
        self.set_speed_multiplier(self.state.speed_multiplier - 0.25)
    
    def pause(self):
        """Pausiert die Simulation."""
        self.state.is_paused = True
    
    def resume(self):
        """Setzt die Simulation fort."""
        self.state.is_paused = False
    
    def toggle_pause(self):
        """Wechselt zwischen Pause und Fortsetzen."""
        self.state.is_paused = not self.state.is_paused
    
    def start(self):
        """Startet die Simulation."""
        self.state.is_running = True
        self.state.is_paused = False
        self.state.is_finished = False
        self.state.elapsed_time = 0.0
        self.state.tick_count = 0
        self.results = []
        self.finish_order = []
        
        for horse in self.horses:
            horse.reset()
            self.speed_history[horse.name] = []
            self.position_history[horse.name] = []
            self.injury_history[horse.name] = []
            # Initialisiere Segment-Performance-Tracking
            self.segment_stats[horse.name] = {}
            for segment in self.track.segments:
                self.segment_stats[horse.name][segment.segment_type] = []
    
    def tick(self, delta_time: float) -> bool:
        """
        Führt einen Simulations-Tick aus.
        
        Args:
            delta_time: Zeit seit dem letzten Tick in Sekunden
            
        Returns:
            True wenn die Simulation noch läuft, False wenn beendet
        """
        if not self.state.is_running or self.state.is_paused:
            return not self.state.is_finished
        
        # Angepasste Zeit basierend auf Geschwindigkeitsmultiplikator
        adjusted_delta = delta_time * self.state.speed_multiplier
        self.state.elapsed_time += adjusted_delta
        self.state.tick_count += 1
        
        # Race Context berechnen für Spannungs-Mechanik
        active_horses = [h for h in self.horses if not h.finished]
        if active_horses:
            positions = [h.position for h in active_horses]
            leader_position = max(positions)
            average_position = sum(positions) / len(positions)
            
            # Platzierungen berechnen
            sorted_horses = sorted(active_horses, key=lambda h: h.position, reverse=True)
            horse_ranks = {h.name: i + 1 for i, h in enumerate(sorted_horses)}
        else:
            leader_position = 0
            average_position = 0
            horse_ranks = {}
        
        all_finished = True
        
        for horse in self.horses:
            if horse.finished:
                continue
            
            all_finished = False
            
            # Aktuelle Position als Bruchteil der Strecke
            relative_position = horse.position / self.track.length
            
            # Streckenmodifikatoren holen
            modifiers = self.track.get_modifiers_at_position(relative_position)
            
            # Aktuelles Segment ermitteln
            current_segment = self.track.get_segment_at_position(relative_position)
            
            # Race Context für dieses Pferd
            race_context = {
                'leader_position': leader_position,
                'average_position': average_position,
                'my_rank': horse_ranks.get(horse.name, 5)
            }
            
            # Verletzungsprüfung
            injury_chance = self.track.get_injury_chance_at_position(relative_position)
            was_injured_before = horse.is_injured
            horse.check_injury(injury_chance * adjusted_delta * 10)
            
            # Verletzung tracken
            if not was_injured_before and horse.is_injured:
                self.injury_history[horse.name].append(self.state.elapsed_time)
            
            # Geschwindigkeit berechnen (mit race_context für Spannungs-Mechanik)
            speed = horse.get_effective_speed(
                modifiers, 
                horse.position, 
                self.track.length,
                race_context
            )
            
            # Segment-Performance tracken
            if current_segment and current_segment.segment_type in self.segment_stats[horse.name]:
                self.segment_stats[horse.name][current_segment.segment_type].append(speed)
            
            # Position aktualisieren
            distance_moved = speed * adjusted_delta * 10  # Skalierung für sichtbare Bewegung
            horse.position += distance_moved
            horse.current_speed = speed
            
            # Statistiken speichern
            if self.state.tick_count % 5 == 0:  # Alle 5 Ticks
                self.speed_history[horse.name].append((self.state.elapsed_time, speed))
                self.position_history[horse.name].append((self.state.elapsed_time, horse.position))
            
            # Ziellinie überprüfen
            if horse.position >= self.track.length:
                horse.position = self.track.length
                horse.finished = True
                horse.finish_time = self.state.elapsed_time
                self.finish_order.append(horse)
        
        # Callback für UI-Update
        if self.on_update:
            self.on_update(self)
        
        # Prüfen ob alle fertig sind
        if all_finished:
            self._finalize_race()
            return False
        
        return True
    
    def _finalize_race(self):
        """Finalisiert das Rennen und erstellt die Ergebnisliste."""
        self.state.is_running = False
        self.state.is_finished = True
        
        # Ergebnisse erstellen
        for i, horse in enumerate(self.finish_order):
            speeds = self.speed_history[horse.name]
            
            # Extrahiere nur die Geschwindigkeitswerte für avg/max
            speed_values = [s[1] for s in speeds] if speeds else [0]
            avg_speed = sum(speed_values) / len(speed_values) if speed_values else 0
            max_speed = max(speed_values) if speed_values else 0
            
            # Segment-Performance berechnen
            segment_performance = {}
            for segment_type, speed_list in self.segment_stats[horse.name].items():
                if speed_list:
                    segment_performance[segment_type] = {
                        'avg_speed': sum(speed_list) / len(speed_list),
                        'max_speed': max(speed_list),
                        'min_speed': min(speed_list),
                        'samples': len(speed_list)
                    }
            
            result = RaceResult(
                horse=horse,
                position=i + 1,
                finish_time=horse.finish_time,
                was_injured=horse.is_injured,
                max_speed=max_speed,
                avg_speed=avg_speed,
                speed_over_time=self.speed_history[horse.name].copy(),
                position_over_time=self.position_history[horse.name].copy(),
                injury_times=self.injury_history[horse.name].copy(),
                segment_performance=segment_performance
            )
            self.results.append(result)
        
        # Callback für Rennende
        if self.on_finish:
            self.on_finish(self.results)
    
    def get_current_standings(self) -> List[tuple]:
        """
        Gibt die aktuelle Reihenfolge der Pferde zurück.
        
        Pferde die bereits im Ziel sind behalten ihre finale Platzierung.
        Noch laufende Pferde werden nach Position sortiert.
        
        Returns:
            Liste von (Position, Horse) Tupeln
        """
        standings = []
        
        # Zuerst: Pferde die bereits angekommen sind (in Zielreihenfolge)
        for i, horse in enumerate(self.finish_order):
            standings.append((i + 1, horse))
        
        # Dann: Noch laufende Pferde nach Position sortiert
        running_horses = [h for h in self.horses if not h.finished]
        running_horses_sorted = sorted(running_horses, key=lambda h: h.position, reverse=True)
        
        # Platzierungen für laufende Pferde beginnen nach den Angekommenen
        start_pos = len(self.finish_order) + 1
        for i, horse in enumerate(running_horses_sorted):
            standings.append((start_pos + i, horse))
        
        return standings
    
    def get_progress(self) -> Dict[str, float]:
        """
        Gibt den Fortschritt aller Pferde als Prozent zurück.
        """
        return {
            horse.name: min(100, (horse.position / self.track.length) * 100)
            for horse in self.horses
        }
