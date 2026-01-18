"""
Menü-Bildschirme für die Pferderennen-Simulation.
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from ui.race_ui import Button, Slider, COLORS


class MainMenu:
    """Hauptmenü der Anwendung."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font_small = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_large = pygame.font.Font(None, 72)
        self.font_title = pygame.font.Font(None, 96)
        
        # Buttons
        button_width = 300
        button_height = 60
        center_x = self.width // 2 - button_width // 2
        
        self.start_button = Button(
            pygame.Rect(center_x, 280, button_width, button_height),
            "> Rennen starten",
            color=(46, 139, 87)
        )
        self.custom_button = Button(
            pygame.Rect(center_x, 360, button_width, button_height),
            "> Pferd erstellen",
            color=(70, 130, 180)
        )
        self.quit_button = Button(
            pygame.Rect(center_x, 440, button_width, button_height),
            "X Beenden",
            color=(178, 34, 34)
        )
        
        # Animation
        self.animation_time = 0
        self.horse_particles = []
        self._init_particles()
    
    def _init_particles(self):
        """Initialisiert Partikel für Hintergrundanimation."""
        for _ in range(20):
            self.horse_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(1, 3),
                'size': random.randint(3, 8),
                'color': random.choice([
                    (139, 69, 19), (101, 67, 33), (160, 82, 45),
                    (210, 180, 140), (85, 85, 85)
                ])
            })
    
    def draw(self, delta_time: float):
        """Zeichnet das Hauptmenü."""
        self.animation_time += delta_time
        
        # Gradient-Hintergrund
        for y in range(self.height):
            ratio = y / self.height
            r = int(20 + 30 * ratio)
            g = int(60 + 40 * ratio)
            b = int(30 + 50 * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
        
        # Partikel (laufende Punkte)
        self._draw_particles()
        
        # Titel mit Schattierung
        title_text = "PFERDERENNEN"
        title_y = 80 + 5 * math.sin(self.animation_time * 2)
        
        # Schatten
        shadow = self.font_title.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self.width // 2 + 3, title_y + 3))
        self.screen.blit(shadow, shadow_rect)
        
        # Haupttitel
        title = self.font_title.render(title_text, True, COLORS['gold'])
        title_rect = title.get_rect(center=(self.width // 2, title_y))
        self.screen.blit(title, title_rect)
        
        # Untertitel
        subtitle = self.font_medium.render("Simulations-Projekt", True, COLORS['light_gray'])
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Buttons
        self.start_button.draw(self.screen, self.font_medium)
        self.custom_button.draw(self.screen, self.font_medium)
        self.quit_button.draw(self.screen, self.font_medium)
        
        # Footer
        footer_text = "BS Rostock - Simulationsprojekt 2026"
        footer = self.font_small.render(footer_text, True, COLORS['gray'])
        footer_rect = footer.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(footer, footer_rect)
    
    def _draw_particles(self):
        """Zeichnet animierte Partikel."""
        for p in self.horse_particles:
            p['x'] += p['speed']
            if p['x'] > self.width:
                p['x'] = -10
                p['y'] = random.randint(0, self.height)
            
            pygame.draw.circle(self.screen, p['color'], 
                             (int(p['x']), int(p['y'])), p['size'])
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Verarbeitet Events.
        
        Returns:
            'start', 'custom', 'quit', oder 'continue'
        """
        if event.type == pygame.QUIT:
            return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'quit'
            elif event.key == pygame.K_RETURN:
                return 'start'
        
        if event.type == pygame.MOUSEMOTION:
            self.start_button.check_hover(event.pos)
            self.custom_button.check_hover(event.pos)
            self.quit_button.check_hover(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos, True):
                return 'start'
            elif self.custom_button.is_clicked(event.pos, True):
                return 'custom'
            elif self.quit_button.is_clicked(event.pos, True):
                return 'quit'
        
        return 'continue'


class TrackSelectionMenu:
    """Streckenauswahl-Menü."""
    
    def __init__(self, screen: pygame.Surface, tracks):
        self.screen = screen
        self.tracks = tracks
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.selected_index = 0
        
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
        
        # Buttons
        self.confirm_button = Button(
            pygame.Rect(self.width // 2 - 150, self.height - 80, 140, 50),
            "Bestätigen",
            color=COLORS['green']
        )
        self.back_button = Button(
            pygame.Rect(self.width // 2 + 10, self.height - 80, 140, 50),
            "Zurück",
            color=COLORS['gray']
        )
        
        self.animation_time = 0
    
    def draw(self, delta_time: float):
        """Zeichnet das Streckenauswahl-Menü."""
        self.animation_time += delta_time
        
        # Hintergrund
        self.screen.fill((30, 40, 50))
        
        # Titel
        title = self.font_large.render("Strecke auswaehlen", True, COLORS['white'])
        title_rect = title.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Strecken-Karten
        card_width = 200
        card_height = 280
        start_x = (self.width - len(self.tracks) * (card_width + 20) + 20) // 2
        
        for i, track in enumerate(self.tracks):
            x = start_x + i * (card_width + 20)
            y = 120
            
            is_selected = i == self.selected_index
            
            # Karten-Rahmen
            card_rect = pygame.Rect(x, y, card_width, card_height)
            
            if is_selected:
                # Ausgewählte Karte hervorheben
                glow_rect = card_rect.inflate(8, 8)
                pygame.draw.rect(self.screen, COLORS['gold'], glow_rect, border_radius=15)
            
            # Kartenfarbe basierend auf Strecke
            pygame.draw.rect(self.screen, track.background_color, card_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS['white'] if is_selected else COLORS['gray'], 
                           card_rect, 3, border_radius=10)
            
            # Streckenname
            name = self.font_medium.render(track.name, True, COLORS['white'])
            name_rect = name.get_rect(center=(x + card_width // 2, y + 30))
            self.screen.blit(name, name_rect)
            
            # Streckensymbol (als farbiger Kreis mit Buchstabe)
            symbol_colors = {
                'Waldstrecke': (34, 139, 34),
                'Sandbahn': (210, 180, 140),
                'Rennbahn': (70, 130, 180),
                'Hügelstrecke': (139, 119, 101),
                'Urban Course': (100, 100, 100)
            }
            symbol_letters = {
                'Waldstrecke': 'W',
                'Sandbahn': 'S',
                'Rennbahn': 'R',
                'Hügelstrecke': 'H',
                'Urban Course': 'U'
            }
            sym_color = symbol_colors.get(track.name, (128, 128, 128))
            pygame.draw.circle(self.screen, sym_color, (x + card_width // 2, y + 80), 30)
            pygame.draw.circle(self.screen, COLORS['white'], (x + card_width // 2, y + 80), 30, 3)
            letter = symbol_letters.get(track.name, '?')
            letter_surface = self.font_large.render(letter, True, COLORS['white'])
            letter_rect = letter_surface.get_rect(center=(x + card_width // 2, y + 80))
            self.screen.blit(letter_surface, letter_rect)
            
            # Länge
            length_text = f"{track.length:.0f}m"
            length_surface = self.font_small.render(length_text, True, COLORS['light_gray'])
            self.screen.blit(length_surface, (x + 10, y + 120))
            
            # Mini-Streckenvorschau
            preview_rect = pygame.Rect(x + 10, y + 145, card_width - 20, 40)
            pygame.draw.rect(self.screen, track.track_color, preview_rect, border_radius=5)
            
            # Segmente anzeigen
            seg_width = (card_width - 20) / len(track.segments)
            for j, seg in enumerate(track.segments):
                seg_rect = pygame.Rect(x + 10 + j * seg_width, y + 145, seg_width + 1, 40)
                pygame.draw.rect(self.screen, seg.color, seg_rect)
        
        # Beschreibung der ausgewählten Strecke
        selected_track = self.tracks[self.selected_index]
        desc_y = 430
        
        # Beschreibungsbox
        desc_rect = pygame.Rect(50, desc_y, self.width - 100, 100)
        pygame.draw.rect(self.screen, (40, 50, 60), desc_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['gold'], desc_rect, 2, border_radius=10)
        
        # Beschreibungstext
        desc_lines = self._wrap_text(selected_track.description, self.font_small, desc_rect.width - 20)
        for i, line in enumerate(desc_lines[:3]):
            line_surface = self.font_small.render(line, True, COLORS['white'])
            self.screen.blit(line_surface, (desc_rect.x + 10, desc_rect.y + 10 + i * 25))
        
        # Buttons
        self.confirm_button.draw(self.screen, self.font_medium)
        self.back_button.draw(self.screen, self.font_medium)
        
        # Steuerungshinweise
        controls = ""
        controls_surface = self.font_small.render(controls, True, COLORS['gray'])
        controls_rect = controls_surface.get_rect(center=(self.width // 2, self.height - 20))
        self.screen.blit(controls_surface, controls_rect)
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Bricht Text in Zeilen um."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def handle_event(self, event: pygame.event.Event) -> Tuple[str, Optional[int]]:
        """
        Verarbeitet Events.
        
        Returns:
            (action, selected_index) wobei action 'confirm', 'back', 'quit' oder 'continue' ist
        """
        if event.type == pygame.QUIT:
            return ('quit', None)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ('back', None)
            elif event.key == pygame.K_RETURN:
                return ('confirm', self.selected_index)
            elif event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.tracks)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.tracks)
        
        if event.type == pygame.MOUSEMOTION:
            self.confirm_button.check_hover(event.pos)
            self.back_button.check_hover(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.confirm_button.is_clicked(event.pos, True):
                return ('confirm', self.selected_index)
            elif self.back_button.is_clicked(event.pos, True):
                return ('back', None)
            
            # Karten-Klick
            card_width = 200
            start_x = (self.width - len(self.tracks) * (card_width + 20) + 20) // 2
            for i in range(len(self.tracks)):
                x = start_x + i * (card_width + 20)
                card_rect = pygame.Rect(x, 120, card_width, 280)
                if card_rect.collidepoint(event.pos):
                    self.selected_index = i
        
        return ('continue', None)


class HorseCreatorMenu:
    """Menü zum Erstellen eines eigenen Pferdes."""
    
    # Verfügbare Farben
    AVAILABLE_COLORS = [
        ((139, 69, 19), "Braun"),
        ((0, 0, 0), "Schwarz"),
        ((255, 255, 255), "Weiß"),
        ((210, 180, 140), "Hellbraun"),
        ((128, 128, 128), "Grau"),
        ((101, 67, 33), "Dunkelbraun"),
        ((205, 133, 63), "Goldbraun"),
        ((160, 82, 45), "Kastanie"),
    ]
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font_small = pygame.font.Font(None, 22)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 42)
        
        self.horse_name = "MeinPferd"
        self.selected_color_index = 0
        self.name_input_active = False
        
        # Sliders für alle 10 manuellen Parameter
        self.sliders = self._create_sliders()
        
        # Buttons
        self.confirm_button = Button(
            pygame.Rect(self.width // 2 - 150, self.height - 70, 140, 45),
            "Erstellen",
            color=COLORS['green']
        )
        self.random_button = Button(
            pygame.Rect(self.width // 2 + 10, self.height - 70, 140, 45),
            "Zufällig",
            color=COLORS['orange']
        )
        self.back_button = Button(
            pygame.Rect(50, self.height - 70, 100, 45),
            "Zurück",
            color=COLORS['gray']
        )
    
    def _create_sliders(self) -> List[Slider]:
        """Erstellt die Slider für alle Parameter."""
        params = [
            "Grundgeschwindigkeit",
            "Wendigkeit",
            "Waldaffinität",
            "Sandtauglichkeit",
            "Sprintfähigkeit",
            "Bergsteiger",
            "Nervenstärke",
            "Gewicht",
            "Erfahrung",
            "Motivation"
        ]
        
        sliders = []
        start_x = 80
        start_y = 200
        slider_width = 180
        slider_height = 15
        
        for i, param in enumerate(params):
            col = i // 5
            row = i % 5
            
            x = start_x + col * (slider_width + 120)
            y = start_y + row * 70
            
            slider = Slider(
                pygame.Rect(x, y, slider_width, slider_height),
                param,
                min_val=0,
                max_val=100,
                value=50
            )
            sliders.append(slider)
        
        return sliders
    
    def draw(self, delta_time: float):
        """Zeichnet das Pferd-Erstellungsmenü."""
        # Hintergrund
        self.screen.fill((35, 45, 55))
        
        # Titel
        title = self.font_large.render("Pferd erstellen", True, COLORS['white'])
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Namenfeld
        name_label = self.font_medium.render("Name:", True, COLORS['white'])
        self.screen.blit(name_label, (80, 90))
        
        name_rect = pygame.Rect(160, 85, 200, 35)
        border_color = COLORS['gold'] if self.name_input_active else COLORS['gray']
        pygame.draw.rect(self.screen, (50, 60, 70), name_rect, border_radius=5)
        pygame.draw.rect(self.screen, border_color, name_rect, 2, border_radius=5)
        
        name_surface = self.font_medium.render(self.horse_name, True, COLORS['white'])
        self.screen.blit(name_surface, (name_rect.x + 10, name_rect.y + 5))
        
        # Farbauswahl
        color_label = self.font_medium.render("Farbe:", True, COLORS['white'])
        self.screen.blit(color_label, (400, 90))
        
        for i, (color, name) in enumerate(self.AVAILABLE_COLORS):
            x = 480 + i * 45
            y = 85
            
            # Farbkreis
            pygame.draw.circle(self.screen, color, (x + 15, y + 17), 15)
            
            # Auswahlrahmen
            if i == self.selected_color_index:
                pygame.draw.circle(self.screen, COLORS['gold'], (x + 15, y + 17), 18, 3)
        
        # Pferdevorschau
        self._draw_horse_preview()
        
        # Info über zufällige Parameter
        info_text = "* Die folgenden Werte werden zufaellig bestimmt:"
        info_surface = self.font_small.render(info_text, True, COLORS['orange'])
        self.screen.blit(info_surface, (self.width - 350, 200))
        
        random_params = [
            "- Ausdauer (Normalverteilung)",
            "- Resilienz/Alter (Exponentialverteilung)",
            "- Beschleunigung (Gleichverteilung)"
        ]
        for i, param in enumerate(random_params):
            param_surface = self.font_small.render(param, True, COLORS['light_gray'])
            self.screen.blit(param_surface, (self.width - 340, 225 + i * 22))
        
        # Sliders
        for slider in self.sliders:
            slider.draw(self.screen, self.font_small)
        
        # Buttons
        self.confirm_button.draw(self.screen, self.font_medium)
        self.random_button.draw(self.screen, self.font_medium)
        self.back_button.draw(self.screen, self.font_medium)
        
        # Hinweis
        hint = "Klicke auf die Slider, um Werte anzupassen | Klicke auf den Namen zum Bearbeiten"
        hint_surface = self.font_small.render(hint, True, COLORS['gray'])
        hint_rect = hint_surface.get_rect(center=(self.width // 2, self.height - 20))
        self.screen.blit(hint_surface, hint_rect)
    
    def _draw_horse_preview(self):
        """Zeichnet eine Vorschau des Pferdes."""
        preview_x = self.width - 150
        preview_y = 120
        
        color = self.AVAILABLE_COLORS[self.selected_color_index][0]
        
        # Körper
        body_rect = pygame.Rect(preview_x - 30, preview_y - 10, 60, 25)
        pygame.draw.ellipse(self.screen, color, body_rect)
        
        # Kopf
        pygame.draw.circle(self.screen, color, (preview_x + 35, preview_y - 8), 12)
        
        # Beine
        leg_positions = [(preview_x - 18, preview_y + 15), (preview_x - 8, preview_y + 15),
                        (preview_x + 8, preview_y + 15), (preview_x + 18, preview_y + 15)]
        for lx, ly in leg_positions:
            pygame.draw.line(self.screen, color, (lx, ly), (lx, ly + 20), 4)
        
        # Schweif
        pygame.draw.line(self.screen, color, (preview_x - 30, preview_y), 
                        (preview_x - 45, preview_y + 5), 4)
    
    def randomize_sliders(self):
        """Setzt alle Slider auf zufällige Werte."""
        import random
        for slider in self.sliders:
            slider.value = random.uniform(20, 90)
    
    def get_horse_data(self) -> dict:
        """Gibt die eingegebenen Pferdedaten zurück."""
        return {
            'name': self.horse_name,
            'color': self.AVAILABLE_COLORS[self.selected_color_index][0],
            'grundgeschwindigkeit': self.sliders[0].value,
            'wendigkeit': self.sliders[1].value,
            'wald_affinitaet': self.sliders[2].value,
            'sand_tauglichkeit': self.sliders[3].value,
            'sprint_faehigkeit': self.sliders[4].value,
            'bergsteiger': self.sliders[5].value,
            'nervenstaerke': self.sliders[6].value,
            'gewicht': self.sliders[7].value,
            'erfahrung': self.sliders[8].value,
            'motivation': self.sliders[9].value
        }
    
    def handle_event(self, event: pygame.event.Event) -> Tuple[str, Optional[dict]]:
        """
        Verarbeitet Events.
        
        Returns:
            (action, horse_data) wobei action 'confirm', 'back', 'quit' oder 'continue' ist
        """
        if event.type == pygame.QUIT:
            return ('quit', None)
        
        # Slider-Events
        for slider in self.sliders:
            slider.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.name_input_active:
                    self.name_input_active = False
                else:
                    return ('back', None)
            elif self.name_input_active:
                if event.key == pygame.K_RETURN:
                    self.name_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.horse_name = self.horse_name[:-1]
                elif len(self.horse_name) < 15 and event.unicode.isprintable():
                    self.horse_name += event.unicode
        
        if event.type == pygame.MOUSEMOTION:
            self.confirm_button.check_hover(event.pos)
            self.random_button.check_hover(event.pos)
            self.back_button.check_hover(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Namenfeld
            name_rect = pygame.Rect(160, 85, 200, 35)
            self.name_input_active = name_rect.collidepoint(event.pos)
            
            # Farbauswahl
            for i in range(len(self.AVAILABLE_COLORS)):
                x = 480 + i * 45
                y = 85
                color_rect = pygame.Rect(x, y, 30, 34)
                if color_rect.collidepoint(event.pos):
                    self.selected_color_index = i
            
            # Buttons
            if self.confirm_button.is_clicked(event.pos, True):
                return ('confirm', self.get_horse_data())
            elif self.random_button.is_clicked(event.pos, True):
                self.randomize_sliders()
            elif self.back_button.is_clicked(event.pos, True):
                return ('back', None)
        
        return ('continue', None)
