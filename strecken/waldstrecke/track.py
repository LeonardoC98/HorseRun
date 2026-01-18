"""
Waldstrecke - Eine anspruchsvolle Strecke durch den Wald.

Eigenschaften:
- Viele Kurven und enge Passagen
- Erhöhte Verletzungsgefahr (Wurzeln, Äste)
- Waldaffinität ist sehr wichtig
- Wendigkeit hilft bei den Kurven
"""

from ..base_track import Track, TrackSegment


class WaldstreckeTrack(Track):
    """Die Waldstrecke mit dichtem Wald und Hindernissen."""
    
    def __init__(self):
        super().__init__()
        self.name = "Waldstrecke"
        self.description = (
            "Eine anspruchsvolle Strecke durch dichten Wald. "
            "Wurzeln und Äste erhöhen die Verletzungsgefahr. "
            "Wendigkeit und Waldaffinität sind entscheidend!"
        )
        self.length = 1200.0
        self.base_injury_chance = 0.0007  # Höher wegen Hindernissen
        self.background_color = (34, 100, 34)  # Dunkles Waldgrün
        self.track_color = (101, 67, 33)  # Erdig-braun
        
        # Definiere die Streckenabschnitte
        self.segments = [
            TrackSegment(0.0, 0.15, "start_lichtung", 
                        {'wald_faktor': 0.9, 'kurven_faktor': 0.95}, 
                        (139, 119, 101)),
            TrackSegment(0.15, 0.35, "dichter_wald",
                        {'wald_faktor': 1.2, 'kurven_faktor': 0.85},
                        (85, 60, 30)),
            TrackSegment(0.35, 0.50, "serpentinen",
                        {'wald_faktor': 1.0, 'kurven_faktor': 1.3},
                        (101, 80, 50)),
            TrackSegment(0.50, 0.70, "wurzelpassage",
                        {'wald_faktor': 1.3, 'kurven_faktor': 0.9},
                        (70, 50, 25)),
            TrackSegment(0.70, 0.85, "lichtung",
                        {'wald_faktor': 0.8, 'kurven_faktor': 1.0, 'sprint_faktor': 1.1},
                        (120, 100, 70)),
            TrackSegment(0.85, 1.0, "zielgerade",
                        {'wald_faktor': 0.7, 'kurven_faktor': 1.0, 'sprint_faktor': 1.2},
                        (139, 119, 101))
        ]
    
    def get_modifiers_at_position(self, position: float) -> dict:
        """Gibt die Modifikatoren an der Position zurück."""
        segment = self.get_segment_at_position(position)
        if segment:
            return segment.modifiers.copy()
        return {'wald_faktor': 1.0}
    
    def get_injury_chance_at_position(self, position: float) -> float:
        """Verletzungschance ist im dichten Wald höher."""
        segment = self.get_segment_at_position(position)
        if segment:
            if segment.segment_type == "dichter_wald":
                return self.base_injury_chance * 2.0
            elif segment.segment_type == "wurzelpassage":
                return self.base_injury_chance * 2.5
            elif segment.segment_type == "serpentinen":
                return self.base_injury_chance * 1.5
        return self.base_injury_chance
