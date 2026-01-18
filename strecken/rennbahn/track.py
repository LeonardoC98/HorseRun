"""
Rennbahn - Die klassische Pferderennbahn.

Eigenschaften:
- Gerade, schnelle Strecke
- Sprintfähigkeit ist entscheidend
- Perfekter Untergrund, geringe Verletzungsgefahr
- Grundgeschwindigkeit ist König
"""

from ..base_track import Track, TrackSegment


class RennbahnTrack(Track):
    """Die klassische Rennbahn - schnell und professionell."""
    
    def __init__(self):
        super().__init__()
        self.name = "Rennbahn"
        self.description = (
            "Die klassische Pferderennbahn mit perfektem Untergrund. "
            "Hier zählen Sprintfähigkeit und Grundgeschwindigkeit! "
            "Minimale Verletzungsgefahr auf der professionellen Strecke."
        )
        self.length = 1600.0  # Längste Strecke
        self.base_injury_chance = 0.00002  # Sehr niedrig
        self.background_color = (50, 150, 50)  # Sattes Grün
        self.track_color = (180, 130, 90)  # Hellbraun
        
        self.segments = [
            TrackSegment(0.0, 0.10, "startbox",
                        {'sprint_faktor': 1.0, 'kurven_faktor': 1.0},
                        (160, 120, 80)),
            TrackSegment(0.10, 0.30, "erste_gerade",
                        {'sprint_faktor': 1.2, 'kurven_faktor': 1.0},
                        (180, 135, 90)),
            TrackSegment(0.30, 0.40, "erste_kurve",
                        {'sprint_faktor': 1.0, 'kurven_faktor': 1.15},
                        (170, 125, 85)),
            TrackSegment(0.40, 0.60, "gegengerade",
                        {'sprint_faktor': 1.25, 'kurven_faktor': 1.0},
                        (185, 140, 95)),
            TrackSegment(0.60, 0.70, "zweite_kurve",
                        {'sprint_faktor': 1.0, 'kurven_faktor': 1.15},
                        (170, 125, 85)),
            TrackSegment(0.70, 0.85, "zielgerade_anfang",
                        {'sprint_faktor': 1.3, 'kurven_faktor': 1.0},
                        (190, 145, 100)),
            TrackSegment(0.85, 1.0, "zielgerade_sprint",
                        {'sprint_faktor': 1.4, 'kurven_faktor': 1.0},
                        (200, 155, 110))
        ]
    
    def get_modifiers_at_position(self, position: float) -> dict:
        """Gibt die Modifikatoren an der Position zurück."""
        segment = self.get_segment_at_position(position)
        if segment:
            return segment.modifiers.copy()
        return {'sprint_faktor': 1.2}
    
    def get_injury_chance_at_position(self, position: float) -> float:
        """Verletzungschance ist auf der Rennbahn sehr gering."""
        segment = self.get_segment_at_position(position)
        if segment and "kurve" in segment.segment_type:
            return self.base_injury_chance * 2.0  # Leicht höher in Kurven
        return self.base_injury_chance
