"""
Basis-Klasse für alle Strecken.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class TrackSegment:
    """Ein Abschnitt der Strecke."""
    start: float          # Startposition (0-1)
    end: float            # Endposition (0-1)
    segment_type: str     # Art des Segments (gerade, kurve, huegel, etc.)
    modifiers: Dict       # Modifikatoren für diesen Abschnitt
    color: Tuple[int, int, int]  # Farbe für die Visualisierung


class Track(ABC):
    """Abstrakte Basisklasse für Strecken."""
    
    def __init__(self):
        self.name: str = "Unbekannte Strecke"
        self.description: str = ""
        self.length: float = 1000.0  # Streckenlänge in Metern
        self.segments: List[TrackSegment] = []
        self.base_injury_chance: float = 0.0001  # Pro Meter
        self.background_color: Tuple[int, int, int] = (34, 139, 34)
        self.track_color: Tuple[int, int, int] = (139, 119, 101)
        
    @abstractmethod
    def get_modifiers_at_position(self, position: float) -> Dict:
        """
        Gibt die Streckenmodifikatoren an einer bestimmten Position zurück.
        Position ist ein Wert zwischen 0 und 1.
        """
        pass
    
    @abstractmethod
    def get_injury_chance_at_position(self, position: float) -> float:
        """
        Gibt die Verletzungschance an einer bestimmten Position zurück.
        """
        pass
    
    def get_segment_at_position(self, position: float) -> TrackSegment:
        """Findet das Segment an einer bestimmten Position."""
        for segment in self.segments:
            if segment.start <= position < segment.end:
                return segment
        return self.segments[-1] if self.segments else None
    
    def get_display_info(self) -> Dict:
        """Gibt Anzeigeinformationen für die UI zurück."""
        return {
            'name': self.name,
            'description': self.description,
            'length': self.length,
            'segments': len(self.segments),
            'background_color': self.background_color,
            'track_color': self.track_color
        }
