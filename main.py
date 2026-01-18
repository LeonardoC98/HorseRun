"""
🏇 Pferderennen-Simulation 🏇
============================

Ein visuell ansprechendes Simulationsprojekt für BS Rostock.

Starte das Programm mit:
    python main.py

Features:
- 10 Pferde mit 13 Parametern (3 zufällig, 10 manuell)
- 5 verschiedene Strecken mit einzigartigen Eigenschaften
- Echtzeit-Animation mit Geschwindigkeitssteuerung
- Ergebnisauswertung mit Statistiken
- Eigenes Pferd erstellen

Autoren: Simulationsprojekt-Team
Datum: Januar 2026
"""

import pygame
import sys
import time
from typing import Optional, List

# Lokale Module
from pferde.horse import Horse, create_random_horse, create_custom_horse
from strecken import get_all_tracks, get_track
from simulation import RaceSimulation
from ui import MainMenu, TrackSelectionMenu, HorseCreatorMenu, RaceUI, ResultsScreen, DetailedAnalysisScreen


class HorseRaceApp:
    """Hauptanwendungsklasse für die Pferderennen-Simulation."""
    
    # Bildschirmgröße
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    FPS = 60
    
    def __init__(self):
        """Initialisiert Pygame und die Anwendung."""
        pygame.init()
        pygame.display.set_caption("🏇 Pferderennen-Simulation")
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Zustand
        self.running = True
        self.state = 'menu'  # menu, track_select, horse_creator, racing, results, detailed_analysis
        
        # Daten
        self.tracks = get_all_tracks()
        self.selected_track = None
        self.custom_horse: Optional[Horse] = None
        self.horses: List[Horse] = []
        self.simulation: Optional[RaceSimulation] = None
        self.results = None
        
        # UI-Komponenten
        self.main_menu = MainMenu(self.screen)
        self.track_menu = TrackSelectionMenu(self.screen, self.tracks)
        self.horse_creator = HorseCreatorMenu(self.screen)
        self.race_ui = None
        self.results_screen = None
        self.detailed_analysis_screen = None
        
        # Zeitmessung
        self.last_time = time.time()
    
    def run(self):
        """Hauptschleife der Anwendung."""
        while self.running:
            # Delta-Zeit berechnen
            current_time = time.time()
            delta_time = current_time - self.last_time
            self.last_time = current_time
            
            # Events verarbeiten
            self._handle_events()
            
            # Zustand aktualisieren und zeichnen
            self._update(delta_time)
            
            # Display aktualisieren
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        """Verarbeitet alle Pygame-Events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if self.state == 'menu':
                result = self.main_menu.handle_event(event)
                if result == 'quit':
                    self.running = False
                elif result == 'start':
                    self.state = 'track_select'
                elif result == 'custom':
                    self.state = 'horse_creator'
            
            elif self.state == 'track_select':
                action, index = self.track_menu.handle_event(event)
                if action == 'quit':
                    self.running = False
                elif action == 'back':
                    self.state = 'menu'
                elif action == 'confirm' and index is not None:
                    self.selected_track = self.tracks[index]
                    self._start_race()
            
            elif self.state == 'horse_creator':
                action, data = self.horse_creator.handle_event(event)
                if action == 'quit':
                    self.running = False
                elif action == 'back':
                    self.state = 'menu'
                elif action == 'confirm' and data:
                    self.custom_horse = create_custom_horse(**data)
                    self.state = 'track_select'
            
            elif self.state == 'racing':
                result = self.race_ui.handle_event(event)
                if result == 'quit':
                    self.state = 'menu'
                elif result == 'abort':
                    # Abbrechen - zurück zum Hauptmenü
                    self.state = 'menu'
                    self.custom_horse = None
            
            elif self.state == 'results':
                result = self.results_screen.handle_event(event)
                if result == 'quit':
                    self.running = False
                elif result == 'menu':
                    self.state = 'menu'
                    self.custom_horse = None
                elif result == 'restart':
                    self._start_race()
                elif result == 'analysis':
                    # Wechsel zur Detailanalyse
                    self.detailed_analysis_screen = DetailedAnalysisScreen(
                        self.screen, self.results, self.selected_track
                    )
                    self.state = 'detailed_analysis'
            
            elif self.state == 'detailed_analysis':
                result = self.detailed_analysis_screen.handle_event(event)
                if result == 'quit':
                    self.running = False
                elif result == 'back':
                    self.state = 'results'
    
    def _update(self, delta_time: float):
        """Aktualisiert den aktuellen Zustand."""
        if self.state == 'menu':
            self.main_menu.draw(delta_time)
        
        elif self.state == 'track_select':
            self.track_menu.draw(delta_time)
        
        elif self.state == 'horse_creator':
            self.horse_creator.draw(delta_time)
        
        elif self.state == 'racing':
            # Prüfen ob "Sofort beenden" geklickt wurde
            if self.race_ui and self.race_ui.skip_to_end:
                # Simulation mit hoher Geschwindigkeit zu Ende bringen
                while self.simulation.tick(0.1):  # Schnelle Ticks bis fertig
                    pass
                self.race_ui.skip_to_end = False
                self.results = self.simulation.results
                self.results_screen = ResultsScreen(
                    self.screen, self.results, self.selected_track
                )
                self.state = 'results'
            else:
                # Normale Simulation
                if self.simulation:
                    still_running = self.simulation.tick(delta_time)
                    if not still_running:
                        self.results = self.simulation.results
                        self.results_screen = ResultsScreen(
                            self.screen, self.results, self.selected_track
                        )
                        self.state = 'results'
            
            # UI aktualisieren
            if self.race_ui:
                self.race_ui.update(delta_time)
        
        elif self.state == 'results':
            if self.results_screen:
                self.results_screen.draw(delta_time)
        
        elif self.state == 'detailed_analysis':
            if self.detailed_analysis_screen:
                self.detailed_analysis_screen.draw(delta_time)
    
    def _start_race(self):
        """Startet ein neues Rennen."""
        # 10 Pferde erstellen (1 custom falls vorhanden, rest zufällig)
        self.horses = []
        
        if self.custom_horse:
            self.custom_horse.reset()
            self.horses.append(self.custom_horse)
            num_random = 9
        else:
            num_random = 10
        
        # Zufällige Pferde erstellen
        used_names = {h.name for h in self.horses}
        for i in range(num_random):
            horse = create_random_horse()
            # Eindeutigen Namen sicherstellen
            while horse.name in used_names:
                horse = create_random_horse()
            used_names.add(horse.name)
            self.horses.append(horse)
        
        # Simulation erstellen
        self.simulation = RaceSimulation(self.horses, self.selected_track)
        self.simulation.start()
        
        # UI erstellen
        self.race_ui = RaceUI(self.screen, self.simulation, self.selected_track)
        
        self.state = 'racing'
    
    def _show_results(self):
        """Zeigt die Ergebnisse an."""
        self.state = 'results'


def main():
    """Einstiegspunkt der Anwendung."""
    print("=" * 50)
    print("Pferderennen-Simulation")
    print("=" * 50)
    print()
    print("Starte Anwendung...")
    print()
    print("Steuerung:")
    print("  SPACE    - Pause/Fortsetzen")
    print("  +/-      - Geschwindigkeit anpassen")
    print("  Pfeile   - Navigation in Menüs")
    print("  ENTER    - Bestätigen")
    print("  ESC      - Zurück/Beenden")
    print()
    
    app = HorseRaceApp()
    app.run()


if __name__ == "__main__":
    main()
