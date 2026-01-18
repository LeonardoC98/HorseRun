"""
Pygame-basierte Benutzeroberfläche für die Pferderennen-Simulation.

Enthält:
- Hauptmenü
- Streckenauswahl
- Pferdekonfiguration
- Rennanimation
- Ergebnisanzeige
- Detaillierte Analyse mit Graphen
"""

import pygame
import pygame.freetype
import sys
import math
import io
import matplotlib
matplotlib.use('Agg')  # Verwende Agg backend für pygame integration
import matplotlib.pyplot as plt
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass

# Farbdefinitionen
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'light_gray': (192, 192, 192),
    'red': (220, 60, 60),
    'green': (60, 180, 60),
    'blue': (60, 120, 200),
    'gold': (255, 215, 0),
    'silver': (192, 192, 192),
    'bronze': (205, 127, 50),
    'brown': (139, 69, 19),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
}


@dataclass
class Button:
    """Ein klickbarer Button."""
    rect: pygame.Rect
    text: str
    color: Tuple[int, int, int] = (70, 130, 180)
    hover_color: Tuple[int, int, int] = (100, 160, 210)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    is_hovered: bool = False
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Zeichnet den Button."""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['white'], self.rect, 2, border_radius=8)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos: Tuple[int, int]) -> bool:
        """Prüft ob die Maus über dem Button ist."""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos: Tuple[int, int], clicked: bool) -> bool:
        """Prüft ob der Button geklickt wurde."""
        return clicked and self.rect.collidepoint(pos)


@dataclass
class Slider:
    """Ein Slider für Werteeingabe."""
    rect: pygame.Rect
    label: str
    min_val: float = 0
    max_val: float = 100
    value: float = 50
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Zeichnet den Slider."""
        # Label
        label_surface = font.render(f"{self.label}: {self.value:.0f}", True, COLORS['white'])
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # Slider-Hintergrund
        pygame.draw.rect(screen, COLORS['dark_gray'], self.rect, border_radius=5)
        
        # Slider-Füllstand
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, COLORS['blue'], fill_rect, border_radius=5)
        
        # Slider-Knopf
        knob_x = self.rect.x + fill_width
        pygame.draw.circle(screen, COLORS['white'], (knob_x, self.rect.centery), 10)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Verarbeitet Maus-Events."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self._update_value(event.pos[0])
            return True
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(event.pos):
                self._update_value(event.pos[0])
                return True
        return False
    
    def _update_value(self, mouse_x: int):
        """Aktualisiert den Wert basierend auf Mausposition."""
        relative_x = max(0, min(self.rect.width, mouse_x - self.rect.x))
        self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)


class HorseSprite:
    """Animiertes Pferde-Sprite."""
    
    def __init__(self, horse, lane: int, track_rect: pygame.Rect):
        self.horse = horse
        self.lane = lane
        self.track_rect = track_rect
        self.animation_frame = 0
        self.animation_speed = 0.2
        
        # Position auf dem Bildschirm
        lane_height = track_rect.height // 12
        self.y = track_rect.y + 20 + lane * lane_height
        self.x = track_rect.x + 50
    
    def update(self, progress: float, delta_time: float):
        """Aktualisiert die Sprite-Position und Animation."""
        # X-Position basierend auf Fortschritt
        track_width = self.track_rect.width - 100
        self.x = self.track_rect.x + 50 + int(progress / 100 * track_width)
        
        # Animation
        if not self.horse.finished:
            speed_factor = self.horse.current_speed / 5 if self.horse.current_speed > 0 else 0.5
            self.animation_frame += self.animation_speed * speed_factor
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Zeichnet das Pferd."""
        # Pferdekörper (stilisiert)
        color = self.horse.color
        
        # Körper (Ellipse)
        body_rect = pygame.Rect(self.x - 20, self.y - 8, 40, 16)
        pygame.draw.ellipse(screen, color, body_rect)
        
        # Kopf
        head_x = self.x + 25
        head_y = self.y - 5
        pygame.draw.circle(screen, color, (head_x, head_y), 8)
        
        # Beine (animiert)
        leg_offset = math.sin(self.animation_frame) * 5 if not self.horse.finished else 0
        leg_positions = [
            (self.x - 12, self.y + 8),
            (self.x - 5, self.y + 8),
            (self.x + 5, self.y + 8),
            (self.x + 12, self.y + 8),
        ]
        for i, (lx, ly) in enumerate(leg_positions):
            offset = leg_offset if i % 2 == 0 else -leg_offset
            pygame.draw.line(screen, color, (lx, ly), (lx + offset, ly + 10), 3)
        
        # Schweif
        tail_offset = math.sin(self.animation_frame * 0.5) * 3
        pygame.draw.line(screen, color, (self.x - 20, self.y), 
                        (self.x - 30, self.y + tail_offset), 3)
        
        # Verletzungsindikator
        if self.horse.is_injured:
            pygame.draw.circle(screen, COLORS['red'], (self.x, self.y - 20), 5)
            pygame.draw.line(screen, COLORS['red'], 
                           (self.x - 3, self.y - 23), (self.x + 3, self.y - 17), 2)
            pygame.draw.line(screen, COLORS['red'], 
                           (self.x + 3, self.y - 23), (self.x - 3, self.y - 17), 2)
        
        # Name
        name_surface = font.render(self.horse.name[:10], True, COLORS['white'])
        screen.blit(name_surface, (self.x - 40, self.y - 30))


class RaceUI:
    """Hauptklasse für die Rennanzeige."""
    
    def __init__(self, screen: pygame.Surface, simulation, track):
        self.screen = screen
        self.simulation = simulation
        self.track = track
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
        
        # Track-Bereich (schmaler, um Platz für Rangliste zu lassen)
        self.track_rect = pygame.Rect(50, 150, self.width - 300, self.height - 300)
        
        # Pferde-Sprites erstellen
        self.horse_sprites = [
            HorseSprite(horse, i, self.track_rect)
            for i, horse in enumerate(simulation.horses)
        ]
        
        # Buttons
        button_y = self.height - 100
        self.pause_button = Button(
            pygame.Rect(50, button_y, 120, 40),
            "Pause"
        )
        self.speed_up_button = Button(
            pygame.Rect(180, button_y, 40, 40),
            "+"
        )
        self.speed_down_button = Button(
            pygame.Rect(230, button_y, 40, 40),
            "-"
        )
        # Neue Buttons (mit mehr Platz)
        self.skip_button = Button(
            pygame.Rect(300, button_y, 130, 40),
            "Beenden",
            color=(255, 140, 0)  # Orange
        )
        self.abort_button = Button(
            pygame.Rect(450, button_y, 130, 40),
            "Abbrechen",
            color=(178, 34, 34)  # Rot
        )
        
        # Flag für Sofort-Beenden
        self.skip_to_end = False
    
    def draw_track(self):
        """Zeichnet die Strecke."""
        # Hintergrund
        self.screen.fill(self.track.background_color)
        
        # Strecken-Header
        title = self.font_large.render(self.track.name, True, COLORS['white'])
        self.screen.blit(title, (50, 20))
        
        # Streckensegmente zeichnen
        segment_width = self.track_rect.width / len(self.track.segments)
        for i, segment in enumerate(self.track.segments):
            seg_rect = pygame.Rect(
                self.track_rect.x + i * segment_width,
                self.track_rect.y,
                segment_width + 1,
                self.track_rect.height
            )
            pygame.draw.rect(self.screen, segment.color, seg_rect)
        
        # Streckenrand
        pygame.draw.rect(self.screen, COLORS['white'], self.track_rect, 3)
        
        # Start- und Ziellinie
        pygame.draw.line(self.screen, COLORS['white'],
                        (self.track_rect.x + 50, self.track_rect.y),
                        (self.track_rect.x + 50, self.track_rect.bottom), 3)
        pygame.draw.line(self.screen, COLORS['gold'],
                        (self.track_rect.right - 50, self.track_rect.y),
                        (self.track_rect.right - 50, self.track_rect.bottom), 5)
        
        # Labels
        start_label = self.font_small.render("START", True, COLORS['white'])
        self.screen.blit(start_label, (self.track_rect.x + 30, self.track_rect.y - 25))
        
        finish_label = self.font_small.render("ZIEL", True, COLORS['gold'])
        self.screen.blit(finish_label, (self.track_rect.right - 70, self.track_rect.y - 25))
        
        # Bahnen-Linien
        lane_height = self.track_rect.height // 12
        for i in range(1, 11):
            y = self.track_rect.y + 20 + i * lane_height
            pygame.draw.line(self.screen, (*self.track.track_color, 100),
                           (self.track_rect.x, y),
                           (self.track_rect.right, y), 1)
    
    def draw_horses(self, delta_time: float):
        """Zeichnet alle Pferde."""
        progress = self.simulation.get_progress()
        
        for sprite in self.horse_sprites:
            horse_progress = progress.get(sprite.horse.name, 0)
            sprite.update(horse_progress, delta_time)
            sprite.draw(self.screen, self.font_small)
    
    def draw_ui(self):
        """Zeichnet UI-Elemente."""
        # Info-Panel
        info_y = 70
        time_text = f"Zeit: {self.simulation.state.elapsed_time:.1f}s"
        speed_text = f"Geschwindigkeit: {self.simulation.state.speed_multiplier:.1f}x"
        
        time_surface = self.font_medium.render(time_text, True, COLORS['white'])
        speed_surface = self.font_medium.render(speed_text, True, COLORS['white'])
        
        self.screen.blit(time_surface, (50, info_y))
        self.screen.blit(speed_surface, (250, info_y))
        
        # Pause-Status
        if self.simulation.state.is_paused:
            pause_text = self.font_large.render("PAUSIERT", True, COLORS['orange'])
            text_rect = pause_text.get_rect(center=(self.width // 2, info_y + 10))
            self.screen.blit(pause_text, text_rect)
        
        # Buttons
        self.pause_button.text = "Fortsetzen" if self.simulation.state.is_paused else "Pause"
        self.pause_button.draw(self.screen, self.font_medium)
        self.speed_up_button.draw(self.screen, self.font_medium)
        self.speed_down_button.draw(self.screen, self.font_medium)
        self.skip_button.draw(self.screen, self.font_medium)
        self.abort_button.draw(self.screen, self.font_medium)
        
        # Rangliste
        self.draw_standings()
        
        # Steuerungshinweise
        controls = ""
        controls_surface = self.font_small.render(controls, True, COLORS['light_gray'])
        self.screen.blit(controls_surface, (50, self.height - 40))
    
    def draw_standings(self):
        """Zeichnet die aktuelle Rangliste."""
        standings = self.simulation.get_current_standings()
        
        # Rangliste rechts neben der Strecke
        panel_x = self.track_rect.right + 20
        panel_y = self.track_rect.y
        panel_width = 200
        panel_height = 30 * len(standings) + 40
        
        # Panel-Hintergrund
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, COLORS['dark_gray'], panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['white'], panel_rect, 2, border_radius=10)
        
        # Titel
        title = self.font_medium.render("Rangliste", True, COLORS['white'])
        self.screen.blit(title, (panel_x + 50, panel_y + 5))
        
        # Platzierungen
        for i, (pos, horse) in enumerate(standings[:10]):
            y = panel_y + 35 + i * 28
            
            # Medaillenfarbe für Top 3
            if pos == 1:
                pos_color = COLORS['gold']
            elif pos == 2:
                pos_color = COLORS['silver']
            elif pos == 3:
                pos_color = COLORS['bronze']
            else:
                pos_color = COLORS['white']
            
            # Position
            pos_text = f"{pos}."
            pos_surface = self.font_small.render(pos_text, True, pos_color)
            self.screen.blit(pos_surface, (panel_x + 10, y))
            
            # Farbindikator
            pygame.draw.circle(self.screen, horse.color, (panel_x + 45, y + 8), 6)
            
            # Name
            name_text = horse.name[:12]
            name_surface = self.font_small.render(name_text, True, COLORS['white'])
            self.screen.blit(name_surface, (panel_x + 60, y))
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Verarbeitet Events.
        
        Returns:
            'continue', 'finished', oder 'quit'
        """
        if event.type == pygame.QUIT:
            return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'abort'  # Zurück zum Hauptmenü
            elif event.key == pygame.K_SPACE:
                self.simulation.toggle_pause()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                self.simulation.increase_speed()
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                self.simulation.decrease_speed()
            elif event.key == pygame.K_s:  # S für Skip/Sofort beenden
                self.skip_to_end = True
        
        if event.type == pygame.MOUSEMOTION:
            self.pause_button.check_hover(event.pos)
            self.speed_up_button.check_hover(event.pos)
            self.speed_down_button.check_hover(event.pos)
            self.skip_button.check_hover(event.pos)
            self.abort_button.check_hover(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button.is_clicked(event.pos, True):
                self.simulation.toggle_pause()
            elif self.speed_up_button.is_clicked(event.pos, True):
                self.simulation.increase_speed()
            elif self.speed_down_button.is_clicked(event.pos, True):
                self.simulation.decrease_speed()
            elif self.skip_button.is_clicked(event.pos, True):
                self.skip_to_end = True
            elif self.abort_button.is_clicked(event.pos, True):
                return 'abort'  # Zurück zum Hauptmenü
        
        return 'continue'
    
    def update(self, delta_time: float):
        """Aktualisiert die Anzeige."""
        self.draw_track()
        self.draw_horses(delta_time)
        self.draw_ui()


class ResultsScreen:
    """Ergebnisbildschirm nach dem Rennen."""
    
    def __init__(self, screen: pygame.Surface, results, track):
        self.screen = screen
        self.results = results
        self.track = track
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 56)
        self.font_xlarge = pygame.font.Font(None, 72)
        
        # Scroll-Offset für die Tabelle
        self.scroll_offset = 0
        self.max_visible_rows = 4  # Weniger Zeilen sichtbar
        self.row_height = 32
        
        # Buttons (weiter unten)
        self.analysis_button = Button(
            pygame.Rect(self.width // 2 - 350, self.height - 55, 160, 45),
            "Detailanalyse",
            color=COLORS['purple']
        )
        self.restart_button = Button(
            pygame.Rect(self.width // 2 - 180, self.height - 55, 150, 45),
            "Nochmal",
            color=COLORS['green']
        )
        self.menu_button = Button(
            pygame.Rect(self.width // 2 + 30, self.height - 55, 150, 45),
            "Hauptmenü",
            color=COLORS['blue']
        )
        
        # Animation
        self.animation_time = 0
    
    def draw(self, delta_time: float):
        """Zeichnet den Ergebnisbildschirm."""
        self.animation_time += delta_time
        
        # Hintergrund
        self.screen.fill((20, 30, 50))
        
        # Titel mit Animation
        title = self.font_xlarge.render("*** RENNERGEBNISSE ***", True, COLORS['gold'])
        title_rect = title.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Streckenname (mehr Abstand nach unten)
        track_text = f"Strecke: {self.track.name} ({self.track.length:.0f}m)"
        track_surface = self.font_medium.render(track_text, True, COLORS['light_gray'])
        track_rect = track_surface.get_rect(center=(self.width // 2, 95))
        self.screen.blit(track_surface, track_rect)
        
        # Podium für Top 3 (mehr Abstand zum Streckenname)
        self.draw_podium()
        
        # Vollständige Ergebnisliste (scrollbar)
        self.draw_results_table()
        
        # Buttons
        self.analysis_button.draw(self.screen, self.font_medium)
        self.restart_button.draw(self.screen, self.font_medium)
        self.menu_button.draw(self.screen, self.font_medium)
    
    def draw_podium(self):
        """Zeichnet das Siegerpodium."""
        podium_y = 220  # Noch mehr Abstand zum Titel
        podium_heights = [100, 130, 80]  # Silber, Gold, Bronze
        podium_colors = [COLORS['silver'], COLORS['gold'], COLORS['bronze']]
        positions = [2, 1, 3]  # Reihenfolge auf dem Podium
        x_offsets = [self.width // 2 - 150, self.width // 2, self.width // 2 + 150]
        
        for i, (pos, height, color, x) in enumerate(zip(positions, podium_heights, podium_colors, x_offsets)):
            if pos <= len(self.results):
                result = self.results[pos - 1]
                
                # Podium-Block
                podium_rect = pygame.Rect(x - 50, podium_y + 130 - height, 100, height)
                pygame.draw.rect(self.screen, color, podium_rect, border_radius=5)
                pygame.draw.rect(self.screen, COLORS['white'], podium_rect, 2, border_radius=5)
                
                # Position
                pos_text = self.font_xlarge.render(str(pos), True, COLORS['dark_gray'])
                pos_rect = pos_text.get_rect(center=(x, podium_y + 130 - height // 2))
                self.screen.blit(pos_text, pos_rect)
                
                # Pferd-Farbe
                pygame.draw.circle(self.screen, result.horse.color, (x, podium_y + 130 - height - 40), 20)
                pygame.draw.circle(self.screen, COLORS['white'], (x, podium_y + 130 - height - 40), 20, 2)
                
                # Name
                name = result.horse.name[:12]
                name_surface = self.font_medium.render(name, True, COLORS['white'])
                name_rect = name_surface.get_rect(center=(x, podium_y + 130 - height - 70))
                self.screen.blit(name_surface, name_rect)
                
                # Zeit
                time_text = f"{result.finish_time:.2f}s"
                time_surface = self.font_small.render(time_text, True, COLORS['light_gray'])
                time_rect = time_surface.get_rect(center=(x, podium_y + 145))
                self.screen.blit(time_surface, time_rect)
    
    def draw_results_table(self):
        """Zeichnet die scrollbare Ergebnistabelle."""
        table_y = 420  # Weiter nach unten
        table_x = 100
        table_width = self.width - 200
        visible_height = self.max_visible_rows * self.row_height + 40
        
        # Tabellen-Container mit Rahmen
        container_rect = pygame.Rect(table_x - 10, table_y - 10, table_width + 20, visible_height + 20)
        pygame.draw.rect(self.screen, (30, 40, 60), container_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['gold'], container_rect, 2, border_radius=10)
        
        # Header
        headers = ["Platz", "Pferd", "Zeit", "Ø Tempo", "Max Tempo", "Verletzt"]
        header_widths = [70, 180, 120, 120, 120, 100]
        
        x = table_x
        for header, width in zip(headers, header_widths):
            header_surface = self.font_small.render(header, True, COLORS['gold'])
            self.screen.blit(header_surface, (x, table_y))
            x += width
        
        # Trennlinie
        pygame.draw.line(self.screen, COLORS['gold'], 
                        (table_x, table_y + 25), 
                        (table_x + sum(header_widths), table_y + 25), 2)
        
        # Sichtbare Ergebniszeilen (mit Scroll)
        visible_results = self.results[self.scroll_offset:self.scroll_offset + self.max_visible_rows]
        
        for i, result in enumerate(visible_results):
            actual_index = i + self.scroll_offset
            y = table_y + 35 + i * self.row_height
            x = table_x
            
            # Hintergrund für ungerade Zeilen
            if actual_index % 2 == 0:
                row_rect = pygame.Rect(table_x - 5, y - 5, sum(header_widths) + 10, self.row_height)
                pygame.draw.rect(self.screen, (40, 50, 70), row_rect, border_radius=3)
            
            # Platzfarbe
            if result.position <= 3:
                pos_colors = {1: COLORS['gold'], 2: COLORS['silver'], 3: COLORS['bronze']}
                pos_color = pos_colors[result.position]
            else:
                pos_color = COLORS['white']
            
            # Daten
            data = [
                f"{result.position}.",
                result.horse.name[:18],
                f"{result.finish_time:.2f}s",
                f"{result.avg_speed:.2f}",
                f"{result.max_speed:.2f}",
                "Ja" if result.was_injured else "Nein"
            ]
            
            colors = [pos_color, COLORS['white'], COLORS['white'], 
                     COLORS['white'], COLORS['white'], 
                     COLORS['red'] if result.was_injured else COLORS['green']]
            
            for (text, width, color) in zip(data, header_widths, colors):
                text_surface = self.font_small.render(text, True, color)
                self.screen.blit(text_surface, (x, y))
                x += width
        
        # Scroll-Indikatoren
        if len(self.results) > self.max_visible_rows:
            scroll_x = table_x + sum(header_widths) + 20
            scroll_y = table_y + 35
            scroll_height = self.max_visible_rows * self.row_height
            
            # Scrollbar-Hintergrund
            scrollbar_bg = pygame.Rect(scroll_x, scroll_y, 15, scroll_height)
            pygame.draw.rect(self.screen, COLORS['dark_gray'], scrollbar_bg, border_radius=5)
            
            # Scrollbar-Position
            scroll_ratio = self.scroll_offset / max(1, len(self.results) - self.max_visible_rows)
            scrollbar_height = max(30, scroll_height * self.max_visible_rows // len(self.results))
            scrollbar_y = scroll_y + int(scroll_ratio * (scroll_height - scrollbar_height))
            
            scrollbar = pygame.Rect(scroll_x, scrollbar_y, 15, scrollbar_height)
            pygame.draw.rect(self.screen, COLORS['gold'], scrollbar, border_radius=5)
            
            # Scroll-Hinweis (unter dem Container)
            hint = "Pfeiltasten oder Mausrad zum Scrollen"
            hint_surface = self.font_small.render(hint, True, COLORS['gray'])
            hint_rect = hint_surface.get_rect(center=(table_x + sum(header_widths) // 2, table_y + visible_height + 25))
            self.screen.blit(hint_surface, hint_rect)
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Verarbeitet Events.
        
        Returns:
            'continue', 'restart', 'menu', oder 'quit'
        """
        if event.type == pygame.QUIT:
            return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'menu'
            elif event.key == pygame.K_RETURN:
                return 'restart'
            # Scrollen mit Pfeiltasten
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.key == pygame.K_DOWN:
                max_scroll = max(0, len(self.results) - self.max_visible_rows)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
        
        # Scrollen mit Mausrad
        if event.type == pygame.MOUSEWHEEL:
            max_scroll = max(0, len(self.results) - self.max_visible_rows)
            self.scroll_offset = max(0, min(max_scroll, self.scroll_offset - event.y))
        
        if event.type == pygame.MOUSEMOTION:
            self.analysis_button.check_hover(event.pos)
            self.restart_button.check_hover(event.pos)
            self.menu_button.check_hover(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.analysis_button.is_clicked(event.pos, True):
                return 'analysis'
            elif self.restart_button.is_clicked(event.pos, True):
                return 'restart'
            elif self.menu_button.is_clicked(event.pos, True):
                return 'menu'
        
        return 'continue'

class DetailedAnalysisScreen:
    """Detaillierte Analyse-Ansicht mit Graphen für Renndaten."""
    
    def __init__(self, screen: pygame.Surface, results, track):
        self.screen = screen
        self.results = results
        self.track = track
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
        
        # Berechne Durchschnittsgeschwindigkeit aller Pferde pro Segment
        self.segment_averages = self._calculate_segment_averages()
        
        # Ausgewähltes Pferd (standardmäßig der Gewinner)
        self.selected_horse_index = 0
        self.selected_result = self.results[0]
        
        # Graph-Oberflächen
        self.speed_graph_surface = None
        self.position_graph_surface = None
        self.segment_graph_surface = None
        self.graphs_need_update = True
        
        # Scroll-Funktionalität
        self.scroll_offset = 0
        self.max_scroll = 0  # Wird nach Graph-Erstellung berechnet
        
        # Buttons
        button_y = self.height - 60
        self.back_button = Button(
            pygame.Rect(self.width // 2 - 75, button_y, 150, 45),
            "Zurück",
            color=COLORS['blue']
        )
        
        # Pferdeauswahl-Buttons
        self.prev_horse_button = Button(
            pygame.Rect(50, 120, 40, 40),
            "<",
            color=COLORS['gray']
        )
        self.next_horse_button = Button(
            pygame.Rect(self.width - 90, 120, 40, 40),
            ">",
            color=COLORS['gray']
        )
        
        # Erstelle Graphen
        self._update_graphs()
    
    def _calculate_segment_averages(self):
        """Berechnet die durchschnittliche Geschwindigkeit aller Pferde pro Segment."""
        segment_averages = {}
        
        # Sammle alle Geschwindigkeiten pro Segment
        for result in self.results:
            for segment_type, perf in result.segment_performance.items():
                if segment_type not in segment_averages:
                    segment_averages[segment_type] = []
                segment_averages[segment_type].append(perf['avg_speed'])
        
        # Berechne Durchschnitt
        for segment_type in segment_averages:
            speeds = segment_averages[segment_type]
            segment_averages[segment_type] = sum(speeds) / len(speeds) if speeds else 0
        
        return segment_averages
    
    def _update_graphs(self):
        """Erstellt die Graphen für das ausgewählte Pferd mit matplotlib."""
        result = self.selected_result
        
        # Konfiguriere matplotlib Style
        plt.style.use('dark_background')
        
        # === GESCHWINDIGKEITS-GRAPH ===
        fig_speed, ax_speed = plt.subplots(figsize=(9, 2.5), facecolor='#1a1a2e')
        ax_speed.set_facecolor('#16213e')
        
        if result.speed_over_time:
            times = [t for t, s in result.speed_over_time]
            speeds = [s for t, s in result.speed_over_time]
            
            ax_speed.plot(times, speeds, color='#00d4ff', linewidth=2, label='Geschwindigkeit')
            ax_speed.fill_between(times, speeds, alpha=0.3, color='#00d4ff')
            
            # Markiere Verletzungszeitpunkte
            for injury_time in result.injury_times:
                ax_speed.axvline(x=injury_time, color='red', linestyle='--', linewidth=2, alpha=0.7)
                ax_speed.text(injury_time, max(speeds) * 0.95, 'Verletzung!', 
                            color='red', fontsize=10, ha='center', va='top')
            
            # Durchschnittsgeschwindigkeit als horizontale Linie
            ax_speed.axhline(y=result.avg_speed, color='yellow', linestyle=':', 
                           linewidth=1.5, alpha=0.7, label=f'Ø {result.avg_speed:.1f}')
            
            ax_speed.set_xlabel('Zeit (s)', fontsize=11, color='white')
            ax_speed.set_ylabel('Geschwindigkeit', fontsize=11, color='white')
            ax_speed.set_title(f'Geschwindigkeitsverlauf - {result.horse.name}', 
                             fontsize=13, color='#00d4ff', fontweight='bold', pad=10)
            ax_speed.grid(True, alpha=0.2, linestyle='--')
            ax_speed.legend(loc='upper right', fontsize=9)
            ax_speed.tick_params(colors='white', labelsize=9)
        
        fig_speed.tight_layout()
        
        # Konvertiere zu Pygame Surface
        buf = io.BytesIO()
        fig_speed.savefig(buf, format='png', dpi=90, facecolor='#1a1a2e')
        buf.seek(0)
        self.speed_graph_surface = pygame.image.load(buf, 'speed_graph.png')
        plt.close(fig_speed)
        buf.close()
        
        # === POSITIONS-GRAPH ===
        fig_pos, ax_pos = plt.subplots(figsize=(9, 2.5), facecolor='#1a1a2e')
        ax_pos.set_facecolor('#16213e')
        
        if result.position_over_time:
            times = [t for t, p in result.position_over_time]
            positions = [p for t, p in result.position_over_time]
            
            ax_pos.plot(times, positions, color='#00ff88', linewidth=2, label='Position')
            ax_pos.fill_between(times, positions, alpha=0.3, color='#00ff88')
            
            # Markiere Ziellinie
            ax_pos.axhline(y=self.track.length, color='gold', linestyle='-', 
                         linewidth=2, alpha=0.8, label='Ziellinie')
            
            # Markiere Verletzungszeitpunkte
            for injury_time in result.injury_times:
                # Finde Position bei Verletzung
                injury_pos = None
                for t, p in result.position_over_time:
                    if t >= injury_time:
                        injury_pos = p
                        break
                if injury_pos:
                    ax_pos.plot(injury_time, injury_pos, 'ro', markersize=10, 
                              markeredgewidth=2, markeredgecolor='white')
            
            ax_pos.set_xlabel('Zeit (s)', fontsize=11, color='white')
            ax_pos.set_ylabel('Position (m)', fontsize=11, color='white')
            ax_pos.set_title(f'Streckenverlauf - {result.horse.name}', 
                           fontsize=13, color='#00ff88', fontweight='bold', pad=10)
            ax_pos.grid(True, alpha=0.2, linestyle='--')
            ax_pos.legend(loc='upper left', fontsize=9)
            ax_pos.tick_params(colors='white', labelsize=9)
        
        fig_pos.tight_layout()
        
        # Konvertiere zu Pygame Surface
        buf = io.BytesIO()
        fig_pos.savefig(buf, format='png', dpi=90, facecolor='#1a1a2e')
        buf.seek(0)
        self.position_graph_surface = pygame.image.load(buf, 'position_graph.png')
        plt.close(fig_pos)
        buf.close()
        
        # === SEGMENT-PERFORMANCE GRAPH ===
        fig_seg, ax_seg = plt.subplots(figsize=(9, 2.5), facecolor='#1a1a2e')
        ax_seg.set_facecolor('#16213e')
        
        if result.segment_performance:
            # Bereite Daten vor
            segment_names = []
            avg_speeds = []
            colors = []
            
            # Sortiere nach Reihenfolge in der Strecke
            for segment in self.track.segments:
                seg_type = segment.segment_type
                if seg_type in result.segment_performance:
                    perf = result.segment_performance[seg_type]
                    # Formatiere Namen (ersetze _ mit Leerzeichen und kapitalisiere)
                    display_name = seg_type.replace('_', ' ').title()
                    segment_names.append(display_name)
                    avg_speeds.append(perf['avg_speed'])
                    
                    # Farbe basierend auf Performance im Vergleich zum Durchschnitt ALLER Pferde in diesem Segment
                    segment_avg = self.segment_averages.get(seg_type, perf['avg_speed'])
                    if perf['avg_speed'] >= segment_avg * 1.1:
                        colors.append('#00ff88')  # Grün - überdurchschnittlich (>110% vom Feld)
                    elif perf['avg_speed'] >= segment_avg * 0.9:
                        colors.append('#ffdd00')  # Gelb - durchschnittlich (90-110% vom Feld)
                    else:
                        colors.append('#ff6666')  # Rot - unterdurchschnittlich (<90% vom Feld)
            
            # Umkehren damit erster Abschnitt oben ist
            segment_names.reverse()
            avg_speeds.reverse()
            colors.reverse()
            
            if segment_names and avg_speeds:
                bars = ax_seg.barh(segment_names, avg_speeds, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
                
                # Durchschnittsgeschwindigkeit als vertikale Linie
                ax_seg.axvline(x=result.avg_speed, color='white', linestyle='--', 
                             linewidth=2, alpha=0.7, label=f'Gesamt-Ø {result.avg_speed:.1f}')
                
                # Werte auf den Balken anzeigen
                for i, (bar, speed) in enumerate(zip(bars, avg_speeds)):
                    ax_seg.text(speed + 0.05, i, f'{speed:.1f}', 
                              va='center', ha='left', fontsize=9, color='white', fontweight='bold')
                
                ax_seg.set_xlabel('Durchschnittsgeschwindigkeit', fontsize=11, color='white')
                ax_seg.set_ylabel('Streckenabschnitt', fontsize=11, color='white')
                ax_seg.set_title(f'Performance pro Streckenabschnitt - {result.horse.name}', 
                               fontsize=13, color='#ffdd00', fontweight='bold', pad=10)
                ax_seg.grid(True, alpha=0.2, linestyle='--', axis='x')
                ax_seg.legend(loc='lower right', fontsize=9)
                ax_seg.tick_params(colors='white', labelsize=9)
        
        fig_seg.tight_layout()
        
        # Konvertiere zu Pygame Surface
        buf = io.BytesIO()
        fig_seg.savefig(buf, format='png', dpi=90, facecolor='#1a1a2e')
        buf.seek(0)
        self.segment_graph_surface = pygame.image.load(buf, 'segment_graph.png')
        plt.close(fig_seg)
        buf.close()
        
        # Berechne maximales Scroll basierend auf Content-Höhe
        content_height = 200 + 250 + 250 + 250 + 70  # Header + Graph1 + Graph2 + Graph3 + Buttons
        self.max_scroll = max(0, content_height - self.height)
        
        self.graphs_need_update = False
    
    def select_horse(self, index: int):
        """Wählt ein Pferd zur Anzeige aus."""
        if 0 <= index < len(self.results):
            self.selected_horse_index = index
            self.selected_result = self.results[index]
            self.graphs_need_update = True
            self._update_graphs()
    
    def draw(self, delta_time: float):
        """Zeichnet die Analyse-Ansicht."""
        # Hintergrund
        self.screen.fill((20, 30, 50))
        
        # Titel (fixiert oben)
        title = self.font_large.render("Detaillierte Rennanalyse", True, COLORS['gold'])
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Pferdauswahl-Sektion (fixiert oben)
        self._draw_horse_selector()
        
        # Statistik-Panel (fixiert oben)
        self._draw_stats_panel()
        
        # Definiere Clipping-Bereich für scrollbaren Content
        # Beginnt unter der Pferdauswahl und Statistiken (bei y=210) und endet vor den Buttons
        clip_rect = pygame.Rect(0, 210, self.width, self.height - 210 - 70)
        self.screen.set_clip(clip_rect)
        
        # Graphen (mit Scroll-Offset)
        graph_y = 200 - self.scroll_offset
        if self.speed_graph_surface:
            # Skaliere und zentriere
            graph_rect = self.speed_graph_surface.get_rect()
            graph_rect.centerx = self.width // 2
            graph_rect.y = graph_y
            self.screen.blit(self.speed_graph_surface, graph_rect)
        
        if self.position_graph_surface:
            graph_rect = self.position_graph_surface.get_rect()
            graph_rect.centerx = self.width // 2
            graph_rect.y = graph_y + 240
            self.screen.blit(self.position_graph_surface, graph_rect)
        
        if self.segment_graph_surface:
            graph_rect = self.segment_graph_surface.get_rect()
            graph_rect.centerx = self.width // 2
            graph_rect.y = graph_y + 480
            self.screen.blit(self.segment_graph_surface, graph_rect)
        
        # Clipping zurücksetzen
        self.screen.set_clip(None)
        
        # Scroll-Indikator (wenn scrollbar benötigt)
        if self.max_scroll > 0:
            self._draw_scroll_indicator()
        
        # Buttons (fixiert unten)
        self.back_button.draw(self.screen, self.font_medium)
        self.prev_horse_button.draw(self.screen, self.font_medium)
        self.next_horse_button.draw(self.screen, self.font_medium)
    
    def _draw_horse_selector(self):
        """Zeichnet die Pferdauswahl."""
        result = self.selected_result
        
        # Hintergrund-Panel
        panel_rect = pygame.Rect(100, 100, self.width - 200, 80)
        pygame.draw.rect(self.screen, (30, 40, 60), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['gold'], panel_rect, 2, border_radius=10)
        
        # Platzierung
        pos_text = f"#{result.position}"
        pos_surface = self.font_large.render(pos_text, True, COLORS['gold'])
        self.screen.blit(pos_surface, (120, 115))
        
        # Pferd-Farbe
        pygame.draw.circle(self.screen, result.horse.color, (220, 140), 25)
        pygame.draw.circle(self.screen, COLORS['white'], (220, 140), 25, 2)
        
        # Pferdename
        name_surface = self.font_large.render(result.horse.name, True, COLORS['white'])
        self.screen.blit(name_surface, (270, 115))
        
        # Pferdeauswahl-Hinweis
        hint = f"Pferd {self.selected_horse_index + 1} von {len(self.results)}"
        hint_surface = self.font_small.render(hint, True, COLORS['light_gray'])
        hint_rect = hint_surface.get_rect(center=(self.width // 2, 165))
        self.screen.blit(hint_surface, hint_rect)
    
    def _draw_scroll_indicator(self):
        """Zeichnet einen Scroll-Indikator am rechten Rand."""
        scrollbar_x = self.width - 20
        scrollbar_y = 90
        scrollbar_height = self.height - 180
        
        # Scrollbar-Hintergrund
        pygame.draw.rect(self.screen, COLORS['dark_gray'], 
                        (scrollbar_x, scrollbar_y, 12, scrollbar_height), 
                        border_radius=6)
        
        # Scrollbar-Position
        scroll_ratio = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
        thumb_height = max(30, scrollbar_height * 0.3)
        thumb_y = scrollbar_y + int(scroll_ratio * (scrollbar_height - thumb_height))
        
        pygame.draw.rect(self.screen, COLORS['gold'], 
                        (scrollbar_x, thumb_y, 12, thumb_height), 
                        border_radius=6)
        
        # Scroll-Hinweis
        if self.scroll_offset == 0:
            hint = "↓ Scrollen mit Mausrad"
            hint_surface = self.font_small.render(hint, True, COLORS['gray'])
            self.screen.blit(hint_surface, (self.width - 200, self.height - 100))
    
    def _draw_stats_panel(self):
        """Zeichnet das Statistik-Panel."""
        result = self.selected_result
        
        # Kompakte Statistiken rechts neben Pferdeauswahl
        stats_x = self.width - 350
        stats_y = 105
        
        stats = [
            f"Zeit: {result.finish_time:.2f}s",
            f"Ø Tempo: {result.avg_speed:.2f}",
            f"Max Tempo: {result.max_speed:.2f}",
            f"Verletzungen: {len(result.injury_times)}"
        ]
        
        for i, stat in enumerate(stats):
            color = COLORS['red'] if 'Verletzungen' in stat and len(result.injury_times) > 0 else COLORS['white']
            stat_surface = self.font_small.render(stat, True, color)
            self.screen.blit(stat_surface, (stats_x, stats_y + i * 25))
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Verarbeitet Events.
        
        Returns:
            'continue', 'back', oder 'quit'
        """
        if event.type == pygame.QUIT:
            return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
            elif event.key == pygame.K_LEFT:
                self.select_horse(max(0, self.selected_horse_index - 1))
            elif event.key == pygame.K_RIGHT:
                self.select_horse(min(len(self.results) - 1, self.selected_horse_index + 1))
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 30)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
        
        # Scrollen mit Mausrad
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 30))
        
        if event.type == pygame.MOUSEMOTION:
            self.back_button.check_hover(event.pos)
            self.prev_horse_button.check_hover(event.pos)
            self.next_horse_button.check_hover(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event.pos, True):
                return 'back'
            elif self.prev_horse_button.is_clicked(event.pos, True):
                self.select_horse(max(0, self.selected_horse_index - 1))
            elif self.next_horse_button.is_clicked(event.pos, True):
                self.select_horse(min(len(self.results) - 1, self.selected_horse_index + 1))
        
        return 'continue'