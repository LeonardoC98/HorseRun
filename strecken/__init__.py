# Strecken-Modul
from .base_track import Track
from .waldstrecke.track import WaldstreckeTrack
from .sandbahn.track import SandbahnTrack
from .rennbahn.track import RennbahnTrack
from .huegelstrecke.track import HuegelstreckeTrack
from .urban_course.track import UrbanCourseTrack

AVAILABLE_TRACKS = {
    'waldstrecke': WaldstreckeTrack,
    'sandbahn': SandbahnTrack,
    'rennbahn': RennbahnTrack,
    'huegelstrecke': HuegelstreckeTrack,
    'urban_course': UrbanCourseTrack
}

def get_track(track_name: str) -> Track:
    """Gibt eine Strecken-Instanz zurück."""
    if track_name.lower() in AVAILABLE_TRACKS:
        return AVAILABLE_TRACKS[track_name.lower()]()
    raise ValueError(f"Unbekannte Strecke: {track_name}")

def get_all_tracks() -> list:
    """Gibt alle verfügbaren Strecken zurück."""
    return [cls() for cls in AVAILABLE_TRACKS.values()]
