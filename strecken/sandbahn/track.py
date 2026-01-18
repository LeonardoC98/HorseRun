"""
Sandbahn - Eine klassische Sandstrecke.

Eigenschaften:
- Lockerer Untergrund erschwert das Laufen
- Sandtauglichkeit ist entscheidend
- Leichtere Pferde haben Vorteile
- Weniger Verletzungsgefahr
"""

from ..base_track import Track, TrackSegment


class SandbahnTrack(Track):
    """Die Sandbahn mit weichem Untergrund."""
    
    def __init__(self):
        super().__init__()
        self.name = "Sandbahn"
        self.description = (
            "Eine klassische Sandstrecke mit weichem Untergrund. "
            "Sandtauglichkeit und ein leichteres Gewicht sind von Vorteil. "
            "Geringere Verletzungsgefahr, aber hoher Kraftaufwand!"
        )
        self.length = 1000.0
        self.base_injury_chance = 0.00005  # Niedriger, Sand ist weich
        self.background_color = (210, 180, 140)  # Sandig
        self.track_color = (244, 164, 96)  # Sandfarben
        
        self.segments = [
            TrackSegment(0.0, 0.20, "fester_sand",
                        {'sand_faktor': 1.1, 'kurven_faktor': 1.0},
                        (210, 180, 140)),
            TrackSegment(0.20, 0.40, "tiefer_sand",
                        {'sand_faktor': 1.4, 'kurven_faktor': 0.95},
                        (194, 154, 110)),
            TrackSegment(0.40, 0.55, "kurvenbereich",
                        {'sand_faktor': 1.2, 'kurven_faktor': 1.2},
                        (220, 180, 130)),
            TrackSegment(0.55, 0.75, "gemischter_sand",
                        {'sand_faktor': 1.25, 'kurven_faktor': 1.0},
                        (200, 165, 120)),
            TrackSegment(0.75, 0.90, "fester_bereich",
                        {'sand_faktor': 1.0, 'sprint_faktor': 1.1},
                        (230, 195, 150)),
            TrackSegment(0.90, 1.0, "zielgerade",
                        {'sand_faktor': 0.9, 'sprint_faktor': 1.2},
                        (240, 210, 170))
        ]
    
    def get_modifiers_at_position(self, position: float) -> dict:
        """Gibt die Modifikatoren an der Position zurück."""
        segment = self.get_segment_at_position(position)
        if segment:
            return segment.modifiers.copy()
        return {'sand_faktor': 1.2}
    
    def get_injury_chance_at_position(self, position: float) -> float:
        """Verletzungschance ist auf Sand generell niedrig."""
        segment = self.get_segment_at_position(position)
        if segment and segment.segment_type == "tiefer_sand":
            return self.base_injury_chance * 1.5  # Etwas höher in tiefem Sand
        return self.base_injury_chance
