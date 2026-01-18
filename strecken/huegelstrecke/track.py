"""
Hügelstrecke - Eine bergige, anspruchsvolle Strecke.

Eigenschaften:
- Steigungen und Gefälle
- Bergsteiger-Fähigkeit ist entscheidend
- Beschleunigung hilft bei Anstiegen
- Ausdauer wird stark beansprucht
"""

from ..base_track import Track, TrackSegment


class HuegelstreckeTrack(Track):
    """Die Hügelstrecke mit Bergen und Tälern."""
    
    def __init__(self):
        super().__init__()
        self.name = "Hügelstrecke"
        self.description = (
            "Eine anspruchsvolle Bergstrecke mit steilen Anstiegen. "
            "Bergsteiger-Fähigkeit und Beschleunigung sind hier Gold wert! "
            "Ausdauer wird auf die Probe gestellt."
        )
        self.length = 1400.0
        self.base_injury_chance = 0.0002
        self.background_color = (100, 140, 80)  # Bergwiesen-Grün
        self.track_color = (139, 115, 85)  # Bergpfad
        
        self.segments = [
            TrackSegment(0.0, 0.10, "flacher_start",
                        {'berg_faktor': 1.0, 'kurven_faktor': 1.0},
                        (150, 125, 90)),
            TrackSegment(0.10, 0.25, "erster_anstieg",
                        {'berg_faktor': 1.4, 'kurven_faktor': 0.95},
                        (130, 105, 75)),
            TrackSegment(0.25, 0.35, "bergkamm",
                        {'berg_faktor': 1.1, 'kurven_faktor': 1.1},
                        (160, 135, 100)),
            TrackSegment(0.35, 0.50, "abfahrt",
                        {'berg_faktor': 0.8, 'sprint_faktor': 1.2},
                        (145, 120, 85)),
            TrackSegment(0.50, 0.65, "tal",
                        {'berg_faktor': 1.0, 'sprint_faktor': 1.1},
                        (140, 115, 80)),
            TrackSegment(0.65, 0.80, "steiler_anstieg",
                        {'berg_faktor': 1.5, 'kurven_faktor': 0.9},
                        (120, 95, 65)),
            TrackSegment(0.80, 0.90, "gipfel",
                        {'berg_faktor': 1.2, 'kurven_faktor': 1.0},
                        (155, 130, 95)),
            TrackSegment(0.90, 1.0, "ziel_abfahrt",
                        {'berg_faktor': 0.7, 'sprint_faktor': 1.3},
                        (165, 140, 105))
        ]
    
    def get_modifiers_at_position(self, position: float) -> dict:
        """Gibt die Modifikatoren an der Position zurück."""
        segment = self.get_segment_at_position(position)
        if segment:
            return segment.modifiers.copy()
        return {'berg_faktor': 1.2}
    
    def get_injury_chance_at_position(self, position: float) -> float:
        """Verletzungschance ist bei Anstiegen höher."""
        segment = self.get_segment_at_position(position)
        if segment:
            if "anstieg" in segment.segment_type:
                return self.base_injury_chance * 2.0
            elif segment.segment_type == "abfahrt" or segment.segment_type == "ziel_abfahrt":
                return self.base_injury_chance * 1.5
        return self.base_injury_chance
