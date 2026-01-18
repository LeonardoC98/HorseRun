# Benutzerhandbuch
# Pferderennen-Simulation

---

## 1. Systemanforderungen

| Komponente | Mindestanforderung |
|------------|-------------------|
| Betriebssystem | Windows 10/11 |
| Auflösung | 1200 x 700 Pixel |
| RAM | 4 GB |
| Speicherplatz | 50 MB |

---

## 2. Installation

### Option A: Ausführbare Datei (.exe)

1. Navigieren Sie zum Ordner `dist/`
2. Doppelklicken Sie auf `Pferderennen.exe`
3. Die Anwendung startet direkt ohne weitere Installation

### Option B: Python-Ausführung

1. Stellen Sie sicher, dass Python 3.10+ installiert ist
2. Installieren Sie die Abhängigkeiten:
   ```
   pip install pygame numpy
   ```
3. Starten Sie die Anwendung:
   ```
   python main.py
   ```

---

## 3. Programmoberfläche

### 3.1 Hauptmenü

Nach dem Start erscheint das Hauptmenü mit folgenden Optionen:

| Button | Funktion |
|--------|----------|
| **Rennen starten** | Direkt zur Streckenauswahl |
| **Pferd erstellen** | Eigenes Pferd konfigurieren |
| **Beenden** | Programm schließen |

### 3.2 Streckenauswahl

Wählen Sie eine der 5 verfügbaren Strecken:

| Strecke | Länge | Besonderheit |
|---------|-------|--------------|
| **Waldstrecke** | 1200m | Waldpassagen, erhöhte Verletzungsgefahr |
| **Sandbahn** | 1000m | Sandiger Untergrund, variable Bodenbeschaffenheit |
| **Rennbahn** | 800m | Professionell, schneller Sprint |
| **Hügelstrecke** | 1500m | Steigungen/Gefälle, Ausdauertest |
| **Urban Course** | 1100m | Urbane Umgebung, Nervenstärke-Test |

**Navigation:**
- Links-/Rechtspfeile: Strecke wechseln
- "Auswählen"-Button: Rennen starten
- "Zurück"-Button: Zum Hauptmenü

### 3.3 Pferde-Editor

Im Pferde-Editor können Sie Ihr eigenes Pferd erstellen:

**Eingabefelder:**

| Parameter | Bereich | Beschreibung |
|-----------|---------|--------------|
| Name | Text | Name Ihres Pferdes |
| Grundgeschwindigkeit | 0-100 | Basisgeschwindigkeit |
| Wendigkeit | 0-100 | Kurvenfähigkeit |
| Wald-Affinität | 0-100 | Bonus auf Waldstrecken |
| Sand-Tauglichkeit | 0-100 | Bonus auf Sandbahnen |
| Sprint-Fähigkeit | 0-100 | Bonus auf Rennbahnen |
| Bergsteiger | 0-100 | Bonus auf Hügelstrecken |
| Nervenstärke | 0-100 | Bonus auf Urban Course |
| Gewicht | 0-100 | Niedriger = schnellere Beschleunigung |
| Erfahrung | 0-100 | Reduziert Leistungsschwankungen |
| Motivation | 0-100 | Bonus im Endspurt |

**Hinweis:** 3 Parameter (Ausdauer, Resilienz, Beschleunigung) werden automatisch durch statistische Verteilungen generiert.

### 3.4 Rennansicht

Während des Rennens sehen Sie:

- **Strecke:** Horizontale Darstellung mit Pferde-Sprites
- **Rangliste:** Rechts die aktuelle Platzierung
- **Zeitanzeige:** Verstrichene Zeit
- **Geschwindigkeit:** Aktueller Geschwindigkeitsmultiplikator

**Steuerelemente:**

| Taste/Button | Funktion |
|--------------|----------|
| SPACE / Pause-Button | Pause / Fortsetzen |
| + / Plus-Button | Geschwindigkeit erhöhen |
| - / Minus-Button | Geschwindigkeit verringern |
| S / Beenden-Button | Rennen sofort abschließen |
| ESC / Abbrechen-Button | Zurück zum Hauptmenü |

**Geschwindigkeitsstufen:** 0.25x bis 5.0x

### 3.5 Ergebnisanzeige

Nach dem Rennen erscheint die Ergebnisanzeige:

- **Podium:** Top 3 Plätze mit Gold, Silber, Bronze
- **Tabelle:** Alle 10 Pferde mit Details
  - Platzierung
  - Name
  - Zielzeit
  - Max-Geschwindigkeit
  - Status (OK / Verletzt)

**Tabellen-Navigation:**
- Mausrad: Scrollen
- Pfeil hoch/runter: Scrollen

**Buttons:**
- "Nochmal": Gleiche Strecke, neue Pferde
- "Hauptmenü": Zurück zum Start

---

## 4. Spielprinzip

### 4.1 Wie funktioniert die Simulation?

1. **10 Pferde** treten gegeneinander an
2. Jedes Pferd hat **13 Parameter**, die seine Leistung beeinflussen
3. Die Strecke hat verschiedene **Segmente** mit unterschiedlichen Anforderungen
4. **Zufallsfaktoren** sorgen für Spannung

### 4.2 Parameter-Einfluss

| Strecke | Wichtigste Parameter |
|---------|---------------------|
| Waldstrecke | Wald-Affinität, Wendigkeit |
| Sandbahn | Sand-Tauglichkeit, Ausdauer |
| Rennbahn | Sprint-Fähigkeit, Grundgeschwindigkeit |
| Hügelstrecke | Bergsteiger, Beschleunigung, Ausdauer |
| Urban Course | Nervenstärke, Erfahrung |

### 4.3 Spannungs-Mechaniken

- **Ermüdung:** Schnelle Pferde ermüden schneller
- **Windschatten:** Pferde hinten bekommen einen Bonus
- **Momentum:** Führende Pferde bauen Schwung auf
- **Zufällige Schwankungen:** Leistung variiert leicht

### 4.4 Verletzungen

- Verletzungen können auf schwierigen Streckenabschnitten auftreten
- Hohe Resilienz reduziert das Verletzungsrisiko
- Verletzte Pferde werden langsamer (10-30%)

---

## 5. Tipps für die Pferdeerstellung

### 5.1 Allrounder

Für alle Strecken geeignet:
- Mittlere Werte (40-60) bei allen Parametern
- Hohe Ausdauer und Erfahrung

### 5.2 Sprinter

Für kurze Strecken (Rennbahn):
- Hohe Grundgeschwindigkeit (80+)
- Hohe Sprint-Fähigkeit (80+)
- Niedriges Gewicht (20-40)

### 5.3 Ausdauer-Typ

Für lange Strecken (Hügelstrecke):
- Mittlere Grundgeschwindigkeit (50-60)
- Hoher Bergsteiger-Wert (80+)
- Hohe Motivation für den Endspurt

### 5.4 Spezialist

Für spezifische Strecken:
- Maximieren Sie den streckenspezifischen Parameter
- Ausgleich durch hohe Erfahrung

---

## 6. Tastaturkürzel

| Taste | Funktion | Verfügbar in |
|-------|----------|--------------|
| SPACE | Pause/Fortsetzen | Rennen |
| + | Geschwindigkeit + | Rennen |
| - | Geschwindigkeit - | Rennen |
| S | Sofort beenden | Rennen |
| ESC | Zurück/Abbrechen | Überall |
| ENTER | Bestätigen | Menüs |
| ↑/↓ | Navigieren/Scrollen | Menüs, Ergebnisse |
| ←/→ | Strecke wechseln | Streckenauswahl |

---

## 7. Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| Schwarzer Bildschirm | Grafiktreiber aktualisieren |
| Kein Sound | Sound ist nicht implementiert (kein Fehler) |
| Fenster zu klein | Mindestauflösung 1200x700 erforderlich |
| Langsame Animation | Andere Programme schließen |
| .exe startet nicht | Windows Defender-Ausnahme hinzufügen |

---

## 8. Kontakt & Support

Bei Fragen wenden Sie sich an das Projektteam.

---

**Benutzerhandbuch Version:** 1.0

**Stand:** Januar 2026
