# Code-Referenz: Pferderennen-Simulation

## Projektstruktur

```
SIMPROJEKT/
├── main.py                    # Hauptanwendung und Einstiegspunkt
├── simulation.py              # Simulations-Engine
├── requirements.txt           # Python-Abhängigkeiten
├── pferde/                    # Pferde-Modul
│   ├── __init__.py
│   └── horse.py               # Horse-Klasse und Hilfsfunktionen
├── strecken/                  # Strecken-Module
│   ├── __init__.py
│   ├── base_track.py          # Abstrakte Basisklasse
│   ├── waldstrecke/           # Waldstrecke-Implementation
│   ├── sandbahn/              # Sandbahn-Implementation
│   ├── rennbahn/              # Rennbahn-Implementation
│   ├── huegelstrecke/         # Hügelstrecke-Implementation
│   └── urban_course/          # Urban Course-Implementation
├── ui/                        # Benutzeroberfläche
│   ├── __init__.py
│   ├── menus.py               # Menü-Bildschirme
│   └── race_ui.py             # Rennvisualisierung und Ergebnisse
└── dist/                      # Kompilierte .exe Datei
    └── Pferderennen.exe
```

---

## Datei-Dokumentation

### 1. main.py - Hauptanwendung

**Zweck:** Einstiegspunkt der Anwendung, verwaltet den Anwendungszustand und die Hauptschleife.

#### Klasse: `HorseRaceApp`

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `SCREEN_WIDTH` | int | Fensterbreite (1200 Pixel) |
| `SCREEN_HEIGHT` | int | Fensterhöhe (700 Pixel) |
| `FPS` | int | Bildwiederholrate (60 FPS) |
| `state` | str | Aktueller Zustand ('menu', 'track_select', 'horse_creator', 'racing', 'results') |
| `tracks` | List[Track] | Liste aller verfügbaren Strecken |
| `horses` | List[Horse] | Aktive Pferde im Rennen |
| `simulation` | RaceSimulation | Aktive Renn-Simulation |

#### Methoden:

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `__init__()` | - | - | Initialisiert Pygame, lädt Ressourcen, erstellt UI-Komponenten |
| `run()` | - | - | Startet die Hauptschleife der Anwendung |
| `_handle_events()` | - | - | Verarbeitet Pygame-Events basierend auf aktuellem Zustand |
| `_update(delta_time)` | float | - | Aktualisiert und zeichnet den aktuellen Bildschirm |
| `_start_race()` | - | - | Erstellt 10 Pferde und startet ein neues Rennen |

---

### 2. simulation.py - Simulations-Engine

**Zweck:** Kernlogik der Renn-Simulation, verwaltet Geschwindigkeit, Positionen und Ergebnisse.

#### Dataclass: `RaceResult`

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `horse` | Horse | Das Pferd |
| `position` | int | Endplatzierung (1-10) |
| `finish_time` | float | Zielzeit in Sekunden |
| `was_injured` | bool | War das Pferd verletzt? |
| `max_speed` | float | Maximale Geschwindigkeit während des Rennens |
| `avg_speed` | float | Durchschnittliche Geschwindigkeit |

#### Dataclass: `SimulationState`

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `is_running` | bool | Läuft die Simulation? |
| `is_paused` | bool | Ist pausiert? |
| `is_finished` | bool | Ist beendet? |
| `elapsed_time` | float | Vergangene Zeit in Sekunden |
| `speed_multiplier` | float | Geschwindigkeitsmultiplikator (0.1 - 5.0) |
| `tick_count` | int | Anzahl der Simulations-Ticks |

#### Klasse: `RaceSimulation`

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `__init__(horses, track)` | List[Horse], Track | - | Initialisiert die Simulation |
| `set_speed_multiplier(multiplier)` | float | - | Setzt die Simulationsgeschwindigkeit |
| `increase_speed()` | - | - | Erhöht die Geschwindigkeit um 0.25 |
| `decrease_speed()` | - | - | Verringert die Geschwindigkeit um 0.25 |
| `pause()` | - | - | Pausiert die Simulation |
| `resume()` | - | - | Setzt die Simulation fort |
| `toggle_pause()` | - | - | Wechselt zwischen Pause/Fortsetzen |
| `start()` | - | - | Startet die Simulation |
| `tick(delta_time)` | float | bool | Führt einen Simulations-Tick aus |
| `_finalize_race()` | - | - | Erstellt Endergebnisse |
| `get_current_standings()` | - | List[Tuple] | Gibt aktuelle Rangliste zurück |
| `get_progress()` | - | Dict[str, float] | Gibt Fortschritt aller Pferde zurück |

---

### 3. pferde/horse.py - Pferde-Modul

**Zweck:** Definiert die Pferde-Datenstruktur mit allen 13 Parametern und Berechnungslogik.

#### Konstanten:

- `HORSE_COLORS`: Liste von 10 RGB-Farbtuples für Pferde
- `HORSE_NAMES`: Liste von 20 möglichen Pferdenamen

#### Dataclass: `Horse`

**Zufällige Parameter (durch Verteilungen bestimmt):**

| Attribut | Verteilung | Beschreibung |
|----------|------------|--------------|
| `ausdauer` | Normalverteilung (μ=50, σ=15) | Beeinflusst Geschwindigkeit über längere Strecken |
| `resilienz` | Exponentialverteilung (λ=30) | Reduziert Verletzungschance und -auswirkung |
| `beschleunigung` | Gleichverteilung (0-100) | Beeinflusst Startphase und Bergpassagen |

**Manuelle Parameter (0-100):**

| Attribut | Beschreibung |
|----------|--------------|
| `grundgeschwindigkeit` | Basisgeschwindigkeit des Pferdes |
| `wendigkeit` | Verbesserung in Kurven |
| `wald_affinitaet` | Bonus auf Waldstrecken |
| `sand_tauglichkeit` | Bonus auf Sandbahnen |
| `sprint_faehigkeit` | Bonus auf Rennbahnen |
| `bergsteiger` | Bonus auf Hügelstrecken |
| `nervenstaerke` | Bonus auf Urban Course |
| `gewicht` | Beeinflusst Beschleunigung (niedriger = besser) |
| `erfahrung` | Reduziert Leistungsschwankungen |
| `motivation` | Bonus im Endspurt |

**Simulationszustand:**

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `position` | float | Aktuelle Position auf der Strecke |
| `current_speed` | float | Aktuelle Geschwindigkeit |
| `is_injured` | bool | Verletzungsstatus |
| `injury_slowdown` | float | Verlangsamung durch Verletzung |
| `finished` | bool | Hat das Ziel erreicht |
| `finish_time` | float | Zielzeit |
| `fatigue` | float | Ermüdungswert (0-100) |
| `momentum` | float | Schwung/Flow-Wert |

#### Methoden der Klasse `Horse`:

| Methode | Beschreibung |
|---------|--------------|
| `reset()` | Setzt alle Simulationswerte zurück |
| `get_effective_speed(track_modifiers, distance_covered, total_distance, race_context)` | Berechnet die effektive Geschwindigkeit mit allen Faktoren |
| `check_injury(injury_chance)` | Prüft auf Verletzung basierend auf Resilienz |
| `to_dict()` | Konvertiert das Pferd zu einem Dictionary |

#### Hilfsfunktionen:

| Funktion | Beschreibung |
|----------|--------------|
| `generate_random_stats()` | Generiert die 3 Verteilungsparameter |
| `create_random_horse(name, color)` | Erstellt ein komplett zufälliges Pferd |
| `create_custom_horse(...)` | Erstellt ein benutzerdefiniertes Pferd |

---

### 4. strecken/base_track.py - Strecken-Basisklasse

**Zweck:** Abstrakte Basisklasse für alle Streckentypen.

#### Dataclass: `TrackSegment`

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `start` | float | Startposition (0-1) |
| `end` | float | Endposition (0-1) |
| `segment_type` | str | Art des Segments |
| `modifiers` | Dict | Modifikatoren |
| `color` | Tuple[int,int,int] | Visualisierungsfarbe |

#### Abstrakte Klasse: `Track`

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `name` | str | Streckenname |
| `description` | str | Beschreibung |
| `length` | float | Länge in Metern |
| `segments` | List[TrackSegment] | Liste der Segmente |
| `base_injury_chance` | float | Basis-Verletzungschance |
| `background_color` | Tuple | Hintergrundfarbe |
| `track_color` | Tuple | Streckenfarbe |

| Methode | Beschreibung |
|---------|--------------|
| `get_modifiers_at_position(position)` | **Abstrakt:** Gibt Modifikatoren an Position zurück |
| `get_injury_chance_at_position(position)` | **Abstrakt:** Gibt Verletzungschance zurück |
| `get_segment_at_position(position)` | Findet Segment an Position |
| `get_display_info()` | Gibt UI-Anzeigedaten zurück |

---

### 5. Strecken-Implementierungen

#### 5.1 strecken/waldstrecke/track.py
- **Modifikator:** `wald_faktor`
- **Eigenschaften:** Waldpassagen, erhöhte Verletzungsgefahr, Kurven
- **Länge:** 1200m

#### 5.2 strecken/sandbahn/track.py
- **Modifikator:** `sand_faktor`
- **Eigenschaften:** Sandiger Untergrund, variable Bodenbeschaffenheit
- **Länge:** 1000m

#### 5.3 strecken/rennbahn/track.py
- **Modifikator:** `sprint_faktor`
- **Eigenschaften:** Professionelle Rennbahn, schneller Untergrund
- **Länge:** 800m

#### 5.4 strecken/huegelstrecke/track.py
- **Modifikator:** `berg_faktor`
- **Eigenschaften:** Steigungen und Gefälle, Ausdauertest
- **Länge:** 1500m

#### 5.5 strecken/urban_course/track.py
- **Modifikator:** `urban_faktor`
- **Eigenschaften:** Urbane Umgebung, Ablenkungen, Nervenstärke-Test
- **Länge:** 1100m

---

### 6. ui/menus.py - Menü-Bildschirme

**Zweck:** Implementiert alle Menü-Oberflächen der Anwendung.

#### Klasse: `MainMenu`
- Startbildschirm mit animiertem Titel
- Buttons: "Rennen starten", "Pferd erstellen", "Beenden"
- Partikel-Animation im Hintergrund

#### Klasse: `TrackSelectionMenu`
- Streckenauswahl mit Vorschau
- Zeigt Streckenbeschreibung und Länge
- Navigation zwischen Strecken

#### Klasse: `HorseCreatorMenu`
- Eingabe der 10 manuellen Parameter
- Slider für jeden Wert (0-100)
- Farbauswahl für das Pferd
- Namensvergabe

---

### 7. ui/race_ui.py - Rennvisualisierung

**Zweck:** Echtzeit-Visualisierung des Rennens und Ergebnisanzeige.

#### Klasse: `Button`
- Klickbarer UI-Button mit Hover-Effekt

#### Klasse: `Slider`
- Werte-Eingabe per Schieberegler

#### Klasse: `HorseSprite`
- Animiertes Pferde-Sprite auf der Strecke
- Bewegt sich basierend auf Fortschritt

#### Klasse: `RaceUI`
- Zeichnet die Strecke und alle Pferde
- Zeigt Rangliste, Zeitanzeige, Geschwindigkeit
- Steuerungs-Buttons: Pause, +/-, Beenden, Abbrechen

| Methode | Beschreibung |
|---------|--------------|
| `draw_track()` | Zeichnet die Strecke mit Segmenten |
| `draw_horses(delta_time)` | Zeichnet und animiert alle Pferde |
| `draw_ui()` | Zeichnet UI-Elemente (Buttons, Infos) |
| `draw_standings()` | Zeichnet die Live-Rangliste |
| `handle_event(event)` | Verarbeitet Benutzereingaben |
| `update(delta_time)` | Aktualisiert die gesamte Anzeige |

#### Klasse: `ResultsScreen`
- Zeigt Endergebnisse als scrollbare Tabelle
- Podiumsanzeige (Gold, Silber, Bronze)
- Statistiken pro Pferd
- Buttons: "Nochmal", "Hauptmenü"

---

## Verwendete Technologien

| Technologie | Version | Verwendung |
|-------------|---------|------------|
| Python | 3.13.5 | Programmiersprache |
| Pygame | 2.6.1 | Grafik und Animation |
| NumPy | Latest | Statistische Verteilungen |
| PyInstaller | 6.15.0 | .exe-Erstellung |
| Dataclasses | Built-in | Datenstrukturen |
