# Projektdokumentation
# Pferderennen-Simulation

**Simulationsprojekt BS Rostock**

**Projektdokumentation nach IHK-Standard**

---

**Projektbezeichnung:** Pferderennen-Simulation mit statistischen Verteilungen

**Projektdauer:** Januar 2026

**Dokumentationsversion:** 1.0

---

## Inhaltsverzeichnis

1. [Projektziele und Kundenwünsche](#1-projektziele-und-kundenwünsche)
2. [Vorgehensmodell](#2-vorgehensmodell)
3. [Projektphasen](#3-projektphasen)
   - 3.1 Planungsphase
   - 3.2 Analysephase
   - 3.3 Entwurfsphase
   - 3.4 Implementierungsphase
   - 3.5 Testphase
   - 3.6 Abschlussphase
4. [Ressourcen- und Ablaufplanung](#4-ressourcen--und-ablaufplanung)
5. [Kostenplanung](#5-kostenplanung)
6. [Risikoanalyse](#6-risikoanalyse)
7. [Auswahl der Verteilungsfunktionen](#7-auswahl-der-verteilungsfunktionen)
8. [Auswahl Programmiersprache und Framework](#8-auswahl-programmiersprache-und-framework)
9. [Planung der Benutzerschnittstelle](#9-planung-der-benutzerschnittstelle)
10. [Testplanung](#10-testplanung)
11. [Umsetzung des Projekts](#11-umsetzung-des-projekts)
12. [Benutzerhandbuch](#12-benutzerhandbuch)

---

## 1. Projektziele und Kundenwünsche

### 1.1 Projektauftrag

Der Auftraggeber (Berufsschule Rostock) beauftragte die Entwicklung einer Pferderennen-Simulation für den Unterricht im Fach Simulation/Modellierung. Das Projekt dient als praktisches Beispiel für die Anwendung statistischer Verteilungsfunktionen in einer visuell ansprechenden Echtzeit-Simulation.

### 1.2 Projektziele

| Nr. | Ziel | Priorität |
|-----|------|-----------|
| Z1 | Entwicklung einer funktionsfähigen Pferderennen-Simulation | Hoch |
| Z2 | Integration von 3 statistischen Verteilungen (Normal-, Exponential-, Gleichverteilung) | Hoch |
| Z3 | Implementierung von 10 manuell konfigurierbaren Parametern pro Pferd | Hoch |
| Z4 | Bereitstellung von 5 unterschiedlichen Rennstrecken | Mittel |
| Z5 | Visuell ansprechende Echtzeit-Animation | Hoch |
| Z6 | Erstellung einer ausführbaren Datei (.exe) | Mittel |
| Z7 | Benutzerdefinierte Pferdeerstellung | Niedrig |

### 1.3 Kundenwünsche (Anforderungskatalog)

**Funktionale Anforderungen:**

1. **10 Pferde** nehmen an jedem Rennen teil
2. Jedes Pferd besitzt **13 verschiedene Parameter**:
   - 3 Werte werden **zufällig durch statistische Verteilungen** bestimmt
   - 10 Werte können **manuell eingepflegt** werden
3. **5 verschiedene Strecken** mit unterschiedlichen Eigenschaften
4. **Echtzeit-Animation** der Rennen
5. **Geschwindigkeitssteuerung** während der Simulation (+/-)
6. **Ergebnisanzeige** mit Statistiken nach dem Rennen
7. Option zur **eigenen Pferdeerstellung**

**Nicht-funktionale Anforderungen:**

1. Intuitive Benutzeroberfläche
2. Stabile Ausführung ohne Abstürze
3. Bildwiederholrate von mindestens 30 FPS
4. Standalone-Ausführung ohne Python-Installation

### 1.4 Abgrenzungskriterien

Folgende Funktionen sind **nicht** Bestandteil des Projekts:
- Mehrspieler-Modus
- Netzwerkfunktionalität
- Speichern/Laden von Spielständen
- Wettsystem mit virtueller Währung

---

## 2. Vorgehensmodell

### 2.1 Ausgewähltes Modell: Wasserfallmodell mit iterativen Elementen

Für dieses Projekt wurde das **modifizierte Wasserfallmodell** gewählt. Dieses Vorgehensmodell verbindet die strukturierte, sequenzielle Vorgehensweise des klassischen Wasserfallmodells mit der Flexibilität, bei Bedarf in frühere Phasen zurückzukehren.

### 2.2 Begründung der Auswahl

| Kriterium | Begründung |
|-----------|------------|
| **Überschaubarer Projektumfang** | Das Projekt hat klar definierte Anforderungen und einen begrenzten Umfang, was ein sequenzielles Vorgehen begünstigt |
| **Feste Deadline** | Der Abgabetermin ist fix, weshalb eine planbare Struktur wichtig ist |
| **Bekannte Technologien** | Python und Pygame sind etablierte Technologien mit geringem Explorationsrisiko |
| **Dokumentationspflicht** | Das Wasserfallmodell unterstützt die systematische Dokumentation jeder Phase |
| **Einzelentwickler** | Bei kleinen Teams reduziert das Modell Koordinationsaufwand |

### 2.3 Phasenübersicht

```
┌─────────────────┐
│   Planung       │ ──────────────────────────────┐
└────────┬────────┘                               │
         │                                         │
         ▼                                         │
┌─────────────────┐                               │
│    Analyse      │ ──────────────────────────────┤
└────────┬────────┘                               │
         │                                         │
         ▼                                         │  Rückkopplung
┌─────────────────┐                               │  bei Bedarf
│    Entwurf      │ ──────────────────────────────┤
└────────┬────────┘                               │
         │                                         │
         ▼                                         │
┌─────────────────┐                               │
│ Implementierung │ ◄─────────────────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Test        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Abschluss     │
└─────────────────┘
```

### 2.4 Abgrenzung zu alternativen Modellen

| Modell | Nicht gewählt weil... |
|--------|----------------------|
| **Scrum/Agile** | Zu hoher Overhead für Einzelentwickler, kein kontinuierliches Kundenfeedback verfügbar |
| **V-Modell** | Zu dokumentationsintensiv für Schulprojekt |
| **Prototyping** | Anforderungen sind bereits klar definiert |
| **Spiralmodell** | Risikoanalyse bei jedem Zyklus unnötig für diesen Umfang |

---

## 3. Projektphasen

### 3.1 Planungsphase

**Dauer:** 2 Stunden

**Aktivitäten:**
- Projektauftrag erfassen und verstehen
- Anforderungskatalog erstellen
- Machbarkeitsanalyse durchführen
- Vorgehensmodell auswählen
- Zeitplan erstellen

**Ergebnisse:**
- Dokumentierter Projektauftrag
- Priorisierte Anforderungsliste
- Grobe Zeitplanung

### 3.2 Analysephase

**Dauer:** 2 Stunden

**Aktivitäten:**
- Detaillierte Anforderungsanalyse
- Recherche statistischer Verteilungen
- Technologieauswahl treffen
- Schnittstellen definieren

**Ergebnisse:**
- Technisches Konzept
- Dokumentierte Verteilungsfunktionen
- Technologie-Stack-Entscheidung

### 3.3 Entwurfsphase

**Dauer:** 3 Stunden

**Aktivitäten:**
- Softwarearchitektur entwerfen
- Klassendiagramm erstellen
- UI-Mockups anfertigen
- Datenbankmodell (entfällt - keine persistente Speicherung)

**Ergebnisse:**
- Modulstruktur
- Klassendiagramm
- UI-Wireframes

### 3.4 Implementierungsphase

**Dauer:** 15 Stunden

**Aktivitäten:**
- Implementierung der Kernlogik (Horse, Track, Simulation)
- UI-Entwicklung mit Pygame
- Integration der statistischen Verteilungen
- Strecken-Implementierungen
- Fehlerbehandlung

**Ergebnisse:**
- Funktionsfähige Anwendung
- Quellcode aller Module

### 3.5 Testphase

**Dauer:** 3 Stunden

**Aktivitäten:**
- Funktionstests aller Features
- Performance-Tests (FPS-Messung)
- Usability-Tests
- Fehlerbehebung

**Ergebnisse:**
- Testprotokolle
- Bereinigte Anwendung

### 3.6 Abschlussphase

**Dauer:** 3 Stunden

**Aktivitäten:**
- Erstellung der .exe-Datei
- Dokumentation finalisieren
- Benutzerhandbuch erstellen
- Projektübergabe

**Ergebnisse:**
- Ausführbare Datei (Pferderennen.exe)
- Vollständige Dokumentation

---

## 4. Ressourcen- und Ablaufplanung

### 4.1 Ressourcenplanung

**Personelle Ressourcen:**

| Rolle | Anzahl | Aufgaben |
|-------|--------|----------|
| Entwickler | 1 | Komplette Projektdurchführung |

**Technische Ressourcen:**

| Ressource | Spezifikation | Verfügbarkeit |
|-----------|---------------|---------------|
| Entwicklungsrechner | Windows 10, 16GB RAM | Vorhanden |
| Python 3.13 | Aktuelle Version | Kostenlos verfügbar |
| Pygame 2.6.1 | Aktuelle stabile Version | Kostenlos (Open Source) |
| NumPy | Aktuelle Version | Kostenlos (Open Source) |
| PyInstaller | 6.15.0 | Kostenlos (Open Source) |
| VS Code | Aktuellste Version | Kostenlos |

### 4.2 Ablaufplanung (Gantt-Darstellung)

```
Phase                    | Woche 1 | Woche 2 | Woche 3 | Woche 4 |
─────────────────────────┼─────────┼─────────┼─────────┼─────────┤
Planung                  | ████    |         |         |         |
Analyse                  | ████    |         |         |         |
Entwurf                  |   ██████|         |         |         |
Implementierung          |     ████|█████████|█████████|         |
- Kernlogik              |     ████|████     |         |         |
- UI-Entwicklung         |         |    █████|████     |         |
- Strecken               |         |         |    █████|         |
- Integration            |         |         |     ████|         |
Test                     |         |         |         |█████    |
Abschluss                |         |         |         |    █████|
```

### 4.3 Meilensteine

| Nr. | Meilenstein | Termin | Kriterium |
|-----|-------------|--------|-----------|
| M1 | Analyse abgeschlossen | Woche 1 | Technologieentscheidung dokumentiert |
| M2 | Entwurf abgeschlossen | Woche 1 | Klassendiagramm erstellt |
| M3 | Kernlogik fertig | Woche 2 | Simulation läuft (ohne UI) |
| M4 | UI-Integration | Woche 3 | Visuelle Darstellung funktioniert |
| M5 | Tests abgeschlossen | Woche 4 | Alle Testfälle bestanden |
| M6 | Projektabschluss | Woche 4 | .exe und Dokumentation fertig |

---

## 5. Kostenplanung

### 5.1 Kostenaufstellung

Da es sich um ein Schulprojekt handelt und ausschließlich Open-Source-Software verwendet wird, entstehen **keine direkten Materialkosten**.

| Kostenart | Betrag | Anmerkung |
|-----------|--------|-----------|
| **Softwarelizenzen** | 0,00 € | Alle Tools sind Open Source |
| Python | 0,00 € | PSF License |
| Pygame | 0,00 € | LGPL License |
| NumPy | 0,00 € | BSD License |
| PyInstaller | 0,00 € | GPL License |
| VS Code | 0,00 € | MIT License |
| **Hardware** | 0,00 € | Vorhandene Infrastruktur |
| **Personalkosten** | 0,00 € | Schulprojekt (unbezahlt) |
| **Gesamtkosten** | **0,00 €** | |

### 5.2 Fiktive Kostenberechnung (Industriekontext)

Für eine realistische Kostenschätzung in einem Industriekontext:

| Position | Stunden | Stundensatz | Kosten |
|----------|---------|-------------|--------|
| Planung & Analyse | 4 | 80 € | 320 € |
| Entwurf | 3 | 80 € | 240 € |
| Implementierung | 15 | 80 € | 1.200 € |
| Test | 3 | 60 € | 180 € |
| Dokumentation | 3 | 60 € | 180 € |
| **Gesamt** | **28 h** | | **2.120 €** |

---

## 6. Risikoanalyse

### 6.1 Risikoidentifikation und -bewertung

| ID | Risiko | Eintritts-wahrscheinlichkeit | Auswirkung | Risiko-wert |
|----|--------|------------------------------|------------|-------------|
| R1 | Pygame-Inkompatibilität mit Python 3.13 | Gering (10%) | Hoch | 0.3 |
| R2 | Performance-Probleme bei Animation | Mittel (30%) | Mittel | 0.6 |
| R3 | Verteilungsfunktionen liefern unrealistische Werte | Mittel (40%) | Mittel | 0.8 |
| R4 | UI wird unübersichtlich | Mittel (30%) | Niedrig | 0.3 |
| R5 | Zeitüberschreitung | Gering (20%) | Hoch | 0.4 |
| R6 | .exe-Erstellung schlägt fehl | Gering (15%) | Mittel | 0.2 |

### 6.2 Risikomatrix

```
           │ Niedrig │ Mittel  │ Hoch    │
───────────┼─────────┼─────────┼─────────┤
   Hoch    │         │         │   R1    │
           │         │         │   R5    │
───────────┼─────────┼─────────┼─────────┤
   Mittel  │         │   R2    │         │
           │         │   R3    │         │
           │         │   R6    │         │
───────────┼─────────┼─────────┼─────────┤
   Gering  │   R4    │         │         │
───────────┴─────────┴─────────┴─────────┘
            Eintrittswahrscheinlichkeit
```

### 6.3 Maßnahmen zur Risikominimierung

| Risiko | Maßnahme |
|--------|----------|
| R1 | Vorab-Test der Pygame-Kompatibilität, Fallback auf Python 3.11 |
| R2 | Optimierung der Render-Logik, Reduzierung der Partikelanzahl |
| R3 | Extensive Tests mit verschiedenen Parameterbereichen, Clipping der Werte |
| R4 | Iteratives UI-Design mit regelmäßigen Tests |
| R5 | Priorisierung der Kernfunktionen, Pufferzeiten eingeplant |
| R6 | Frühzeitiger Test von PyInstaller, alternative Tools (cx_Freeze) bereithalten |

---

## 7. Auswahl der Verteilungsfunktionen

### 7.1 Anforderung

Gemäß Projektauftrag sollen drei Pferdeparameter durch statistische Verteilungen bestimmt werden. Die Auswahl der Verteilungen muss fachlich begründet sein.

### 7.2 Ausgewählte Verteilungen

#### 7.2.1 Normalverteilung für Ausdauer

**Parameter:** μ = 50, σ = 15

**Begründung:**
Die Normalverteilung ist ideal für Eigenschaften, die durch viele unabhängige Faktoren beeinflusst werden. Die Ausdauer eines Pferdes hängt von Genetik, Training, Ernährung und vielen weiteren Faktoren ab. Nach dem Zentralen Grenzwertsatz ist die Summe vieler unabhängiger Einflüsse normalverteilt.

**Eigenschaften:**
- Symmetrisch um den Mittelwert
- 68% der Werte liegen im Bereich μ ± σ (35-65)
- 95% der Werte liegen im Bereich μ ± 2σ (20-80)
- Extreme Werte sind selten, aber möglich

```
     ▲
     │      ████
     │    ████████
     │  ████████████
     │████████████████
     └────────────────────► Ausdauer
        0   50        100
```

#### 7.2.2 Exponentialverteilung für Resilienz/Alter

**Parameter:** λ = 30 (Scale-Parameter)

**Begründung:**
Die Exponentialverteilung modelliert die "Gedächtnislosigkeit" - ältere Pferde haben eine geringere Wahrscheinlichkeit für hohe Resilienz. Die Verteilung eignet sich für:
- Alterungseffekte: Junge Pferde haben höhere Resilienz
- Verletzungsanfälligkeit: Akkumuliert sich über die Zeit

**Umsetzung:** `resilienz = 100 - exponential(30)`, geclippt auf [0, 100]

**Eigenschaften:**
- Asymmetrisch (rechtssteil)
- Viele hohe Werte (junge, resiliente Pferde)
- Wenige niedrige Werte (alte, anfällige Pferde)

```
     ▲
     │██
     │████
     │██████
     │████████
     │██████████████
     └────────────────────► Resilienz
        0              100
```

#### 7.2.3 Gleichverteilung für Beschleunigung

**Parameter:** a = 0, b = 100

**Begründung:**
Die Gleichverteilung (Uniform Distribution) wird verwendet, wenn keine Information über die Wahrscheinlichkeitsverteilung vorliegt. Die Beschleunigungsfähigkeit ist ein angeborenes Merkmal, das nicht systematisch verteilt ist - jeder Wert ist gleich wahrscheinlich.

**Eigenschaften:**
- Alle Werte im Intervall [0, 100] sind gleich wahrscheinlich
- Erwartungswert: 50
- Keine Häufung um einen Mittelwert

```
     ▲
     │████████████████████
     │████████████████████
     │████████████████████
     │████████████████████
     └────────────────────► Beschleunigung
        0              100
```

### 7.3 Mathematische Formeln

| Verteilung | Dichtefunktion | Python-Implementierung |
|------------|----------------|------------------------|
| Normal | f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²) | `np.random.normal(50, 15)` |
| Exponential | f(x) = λe^(-λx) | `np.random.exponential(30)` |
| Gleichverteilung | f(x) = 1/(b-a) | `np.random.uniform(0, 100)` |

---

## 8. Auswahl Programmiersprache und Framework

### 8.1 Ausgewählte Technologien

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Programmiersprache | Python | 3.13.5 |
| Grafik-Framework | Pygame | 2.6.1 |
| Numerik | NumPy | Latest |
| Deployment | PyInstaller | 6.15.0 |

### 8.2 Begründung: Python

| Kriterium | Bewertung |
|-----------|-----------|
| **Lernkurve** | ★★★★★ - Einfach zu erlernen, ideal für Schulprojekt |
| **Verfügbarkeit** | ★★★★★ - Kostenlos, große Community |
| **Bibliotheken** | ★★★★★ - NumPy, Pygame, etc. sofort verfügbar |
| **Dokumentation** | ★★★★★ - Ausgezeichnete Dokumentation |
| **Performance** | ★★★☆☆ - Ausreichend für 2D-Simulation |
| **Cross-Platform** | ★★★★☆ - Windows, Linux, macOS |

**Alternativen und Abgrenzung:**

| Alternative | Nicht gewählt weil... |
|-------------|----------------------|
| Java | Höherer Boilerplate-Code, komplexere GUI-Entwicklung |
| C++ | Zu hohe Lernkurve, manuelle Speicherverwaltung |
| JavaScript | Keine native Desktop-Anwendung ohne Electron |
| C# | Plattformabhängigkeit (primär Windows) |

### 8.3 Begründung: Pygame

| Kriterium | Bewertung |
|-----------|-----------|
| **2D-Grafik** | ★★★★★ - Spezialisiert auf 2D-Spiele |
| **Einfachheit** | ★★★★☆ - Schneller Einstieg |
| **Performance** | ★★★★☆ - SDL-basiert, hardwarebeschleunigt |
| **Community** | ★★★★☆ - Aktive Community, viele Tutorials |
| **Dokumentation** | ★★★★☆ - Gute offizielle Docs |

**Alternativen und Abgrenzung:**

| Alternative | Nicht gewählt weil... |
|-------------|----------------------|
| Tkinter | Nicht für Spiele/Animationen optimiert |
| PyQt5 | Zu komplex, Lizenzfragen |
| Arcade | Weniger verbreitet, weniger Ressourcen |
| Pyglet | Weniger Features als Pygame |

### 8.4 Begründung: NumPy

NumPy wird für die Implementierung der statistischen Verteilungen verwendet:

- `np.random.normal()` - Normalverteilung
- `np.random.exponential()` - Exponentialverteilung
- `np.random.uniform()` - Gleichverteilung
- `np.clip()` - Wertebegrenzung

**Vorteil:** Mathematisch korrekte Implementierungen, hohe Performance, Standardbibliothek für wissenschaftliches Rechnen in Python.

---

## 9. Planung der Benutzerschnittstelle

### 9.1 UI-Konzept

Die Benutzeroberfläche folgt dem Prinzip der **progressiven Offenlegung** - komplexere Funktionen werden erst sichtbar, wenn sie benötigt werden.

### 9.2 Bildschirmfluss

```
┌─────────────────┐
│   Hauptmenü     │
│                 │
│ ┌─────────────┐ │
│ │ Rennen      │◄┼──────────────────────────┐
│ │ starten     │ │                          │
│ └─────────────┘ │                          │
│ ┌─────────────┐ │       ┌────────────┐     │
│ │ Pferd       │─┼──────►│  Pferde-   │     │
│ │ erstellen   │ │       │  Editor    │     │
│ └─────────────┘ │       └─────┬──────┘     │
│ ┌─────────────┐ │             │            │
│ │ Beenden     │ │             ▼            │
│ └─────────────┘ │       ┌────────────┐     │
└────────┬────────┘       │  Strecken- │     │
         │                │  Auswahl   │     │
         ▼                └─────┬──────┘     │
    ┌────────────────┐          │            │
    │     EXIT       │          ▼            │
    └────────────────┘    ┌────────────┐     │
                          │   Rennen   │     │
                          └─────┬──────┘     │
                                │            │
                                ▼            │
                          ┌────────────┐     │
                          │ Ergebnisse │─────┘
                          └────────────┘
```

### 9.3 Wireframes

#### 9.3.1 Hauptmenü

```
┌──────────────────────────────────────────────────┐
│                                                  │
│           ╔═══════════════════════╗              │
│           ║   PFERDERENNEN        ║              │
│           ║   Simulations-Projekt ║              │
│           ╚═══════════════════════╝              │
│                                                  │
│            ┌──────────────────────┐              │
│            │   > Rennen starten   │              │
│            └──────────────────────┘              │
│            ┌──────────────────────┐              │
│            │   > Pferd erstellen  │              │
│            └──────────────────────┘              │
│            ┌──────────────────────┐              │
│            │     X Beenden        │              │
│            └──────────────────────┘              │
│                                                  │
│      ~ ~ ~ ~ Animierte Partikel ~ ~ ~ ~          │
└──────────────────────────────────────────────────┘
```

#### 9.3.2 Rennansicht

```
┌────────────────────────────────────┬────────────┐
│                                    │ Rangliste  │
│   ══════════════════════════════   │            │
│   ███ Blitz 5                      │ 1. Sturm   │
│   ══════════════════════════════   │ 2. Blitz   │
│   █████ Sturm 12                   │ 3. Apollo  │
│   ══════════════════════════════   │ 4. Zeus    │
│   ████ Apollo 8                    │ ...        │
│   ══════════════════════════════   │            │
│   ██ Zeus 3                        │            │
│   ══════════════════════════════   │            │
│                                    │            │
├────────────────────────────────────┴────────────┤
│  Zeit: 12.5s    Speed: 1.5x                     │
│                                                 │
│  [Pause] [+] [-] [Beenden] [Abbrechen]          │
│                                                 │
│  SPACE=Pause | +/-=Speed | S=Beenden | ESC=Zurück│
└─────────────────────────────────────────────────┘
```

#### 9.3.3 Ergebnisanzeige

```
┌─────────────────────────────────────────────────┐
│                                                 │
│              ★ ERGEBNISSE ★                     │
│                                                 │
│         [2.]        [1.]        [3.]            │
│         Silber      Gold        Bronze          │
│         Blitz       Sturm       Apollo          │
│                                                 │
├─────────────────────────────────────────────────┤
│  #  │ Name    │ Zeit   │ Max-Speed │ Status    │
│ ────┼─────────┼────────┼───────────┼────────── │
│  1  │ Sturm   │ 45.2s  │ 8.5       │ OK        │
│  2  │ Blitz   │ 46.1s  │ 8.2       │ OK        │
│  3  │ Apollo  │ 47.5s  │ 7.9       │ Verletzt  │
│ ... │                                           │
│                    [▲ Scroll ▼]                 │
├─────────────────────────────────────────────────┤
│       [Nochmal spielen]  [Hauptmenü]            │
└─────────────────────────────────────────────────┘
```

### 9.4 Farbschema

| Element | Farbe | Hex-Code | Verwendung |
|---------|-------|----------|------------|
| Primär | Grün | #2E8B57 | Start-Button, positive Aktionen |
| Sekundär | Blau | #4682B4 | Sekundäre Buttons |
| Akzent | Gold | #FFD700 | Titel, 1. Platz |
| Warnung | Orange | #FF8C00 | Pause-Status, Skip-Button |
| Gefahr | Rot | #B22222 | Beenden, Abbrechen |
| Hintergrund | Dunkelgrau | #404040 | Panels |
| Text | Weiß | #FFFFFF | Standardtext |

---

## 10. Testplanung

### 10.1 Teststrategie

Es werden folgende Testarten durchgeführt:

1. **Unit-Tests:** Testen einzelner Funktionen (Verteilungen, Geschwindigkeitsberechnung)
2. **Integrationstests:** Zusammenspiel von Modulen (Horse + Track + Simulation)
3. **Systemtests:** Vollständiger Durchlauf der Anwendung
4. **Usability-Tests:** Bedienbarkeit der Oberfläche

### 10.2 Testfälle

| ID | Kategorie | Testfall | Erwartetes Ergebnis |
|----|-----------|----------|---------------------|
| T01 | Unit | Normalverteilung erzeugt Werte im Bereich [0, 100] | Alle Werte geclippt |
| T02 | Unit | Exponentialverteilung erzeugt Werte im Bereich [0, 100] | Alle Werte geclippt |
| T03 | Unit | Gleichverteilung erzeugt gleichmäßig verteilte Werte | Statistische Prüfung |
| T04 | Unit | Pferd-Geschwindigkeit ist positiv | speed > 0 |
| T05 | Integration | Simulation startet mit 10 Pferden | Alle Pferde erstellt |
| T06 | Integration | Alle Pferde erreichen das Ziel | 10 Ergebnisse |
| T07 | Integration | Rangliste zeigt korrekte Reihenfolge | 1. = schnellstes Pferd |
| T08 | System | .exe startet ohne Python-Installation | Fenster öffnet sich |
| T09 | System | Alle 5 Strecken sind auswählbar | Rennen auf jeder Strecke möglich |
| T10 | System | Pferde-Editor speichert alle 10 Parameter | Custom-Pferd im Rennen |
| T11 | Performance | FPS ≥ 30 während Rennen | Flüssige Animation |
| T12 | Usability | Alle Buttons sind klickbar | Reaktion auf Klick |

### 10.3 Testumgebung

- **Hardware:** Windows 10/11 PC, mind. 4GB RAM
- **Software:** Windows 10 Build 19045+
- **Auflösung:** 1200x700 Pixel oder höher

### 10.4 Testprotokolle

Siehe **Anhang A: Testprotokolle** für die vollständigen Testdurchläufe.

---

## 11. Umsetzung des Projekts

### 11.1 Implementierungsübersicht

Das Projekt wurde in folgender Reihenfolge implementiert:

1. **Datenmodelle:** `Horse`-Klasse mit allen 13 Parametern
2. **Statistische Verteilungen:** NumPy-basierte Generatoren
3. **Strecken-Basisklasse:** Abstrakte `Track`-Klasse
4. **5 Strecken-Implementierungen:** Je mit eigenen Modifikatoren
5. **Simulations-Engine:** Tick-basierte Simulation
6. **Pygame-UI:** Menüs, Rennansicht, Ergebnisse
7. **Spannungs-Mechanik:** Ermüdung, Windschatten, Momentum
8. **.exe-Erstellung:** PyInstaller-Build

### 11.2 Besondere Herausforderungen

| Herausforderung | Lösung |
|-----------------|--------|
| Rennen zu vorhersehbar | Einführung von Ermüdung, Windschatten-Bonus, zufällige Schwankungen |
| Rangliste zeigte falsche Positionen | Trennung von "angekommen" und "noch laufend" Pferden |
| Button-Text überlappt | Dynamische Button-Größen angepasst |
| Emojis nicht darstellbar | Ersetzt durch ASCII-Text und geometrische Formen |

### 11.3 Codequalität

- **Modularisierung:** Klare Trennung von Logik, UI und Daten
- **Dokumentation:** Docstrings in allen Modulen
- **Typisierung:** Type Hints für bessere Wartbarkeit
- **Dataclasses:** Für saubere Datenstrukturen

---

## 12. Benutzerhandbuch

Das vollständige Benutzerhandbuch ist als separates Dokument verfügbar:

📄 **Siehe:** `DOCUMENTATIONS/02_Benutzerhandbuch/README.md`

### 12.1 Kurzanleitung

1. **Start:** `Pferderennen.exe` ausführen
2. **Rennen starten:** Button "Rennen starten" klicken
3. **Strecke wählen:** Eine der 5 Strecken auswählen
4. **Rennen verfolgen:** Animation beobachten
5. **Steuerung:**
   - `SPACE` - Pause/Fortsetzen
   - `+/-` - Geschwindigkeit anpassen
   - `S` - Rennen sofort beenden
   - `ESC` - Abbrechen

---

## Anhang

### Anhang A: Testprotokolle

Siehe separates Dokument: `DOCUMENTATIONS/03_Anhang/Testprotokolle.md`

### Anhang B: Quellenverzeichnis

1. Pygame-Dokumentation: https://www.pygame.org/docs/
2. NumPy Random-Modul: https://numpy.org/doc/stable/reference/random/
3. Python Dataclasses: https://docs.python.org/3/library/dataclasses.html
4. PyInstaller-Dokumentation: https://pyinstaller.org/en/stable/

---

**Dokumentation erstellt:** Januar 2026

**Version:** 1.0
