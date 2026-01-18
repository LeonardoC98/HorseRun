"""
Urban Course - Eine städtische Hindernisbahn.

Eigenschaften:
- Viele Ablenkungen und Hindernisse
- Nervenstärke ist entscheidend
- Unvorhersehbare Situationen
- Wendigkeit hilft bei engen Stellen
"""

from ..base_track import Track, TrackSegment


class UrbanCourseTrack(Track):
    """Der Urban Course durch die Stadt."""
    
    def __init__(self):
        super().__init__()
        self.name = "Urban Course"
        self.description = (
            "Eine herausfordernde Strecke durch die Stadt! "
            "Lärm, Menschenmassen und enge Gassen erfordern Nervenstärke. "
            "Wendigkeit hilft bei den engen Passagen."
        )
        self.length = 1100.0
        self.base_injury_chance = 0.0015
        self.background_color = (100, 100, 100)  # Stadtgrau
        self.track_color = (70, 70, 70)  # Asphalt
        
        self.segments = [
            TrackSegment(0.0, 0.12, "startplatz",
                        {'urban_faktor': 1.0, 'kurven_faktor': 1.0},
                        (90, 90, 90)),
            TrackSegment(0.12, 0.25, "hauptstrasse",
                        {'urban_faktor': 1.1, 'sprint_faktor': 1.15},
                        (80, 80, 80)),
            TrackSegment(0.25, 0.40, "marktplatz",
                        {'urban_faktor': 1.4, 'kurven_faktor': 1.2},
                        (100, 95, 85)),
            TrackSegment(0.40, 0.55, "enge_gassen",
                        {'urban_faktor': 1.3, 'kurven_faktor': 1.35},
                        (65, 65, 65)),
            TrackSegment(0.55, 0.70, "parkbereich",
                        {'urban_faktor': 0.9, 'sprint_faktor': 1.1},
                        (75, 110, 75)),
            TrackSegment(0.70, 0.85, "bruecke",
                        {'urban_faktor': 1.2, 'kurven_faktor': 1.0},
                        (85, 85, 90)),
            TrackSegment(0.85, 1.0, "zielbereich",
                        {'urban_faktor': 1.0, 'sprint_faktor': 1.25},
                        (95, 95, 95))
        ]
    
    def get_modifiers_at_position(self, position: float) -> dict:
        """Gibt die Modifikatoren an der Position zurück."""
        segment = self.get_segment_at_position(position)
        if segment:
            return segment.modifiers.copy()
        return {'urban_faktor': 1.2}
    
    def get_injury_chance_at_position(self, position: float) -> float:
        """Verletzungschance variiert je nach Stadtbereich."""
        segment = self.get_segment_at_position(position)
        if segment:
            if segment.segment_type == "enge_gassen":
                return self.base_injury_chance * 2.5
            elif segment.segment_type == "marktplatz":
                return self.base_injury_chance * 2.0
            elif segment.segment_type == "bruecke":
                return self.base_injury_chance * 1.5
        return self.base_injury_chance
