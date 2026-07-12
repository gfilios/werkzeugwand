# Rohrsteckschlüsselsatz — Notizen

WIESEMANN 1893, 10-teilig, 6–22 mm, Art. 81420.
8 doppelseitige Rohre (6×7 … 20×22) + Drehstift (Dorn) + Rolltasche.

## Messwerte

Alle Durchmesser **über die Ecken des Sechskants** gemessen (= größte Stelle).

| Rohr | Ø Mitte | Ø Ende | Länge |
|---|---|---|---|
| 6×7 | 11,00 | 11,00 | 108 (gemessen) |
| 8×9 | 11,00 | 12,20 | 116 |
| 10×11 | 13,89 | 15,24 | 123 |
| 12×13 | 16,20 | 18,64 | 131 |
| 14×15 | 16,24 | 20,00 | 138 |
| 16×17 | 19,33 | 22,70 | 146 |
| 18×19 | 22,00 | 25,02 | 154 |
| 20×22 | 25,28 | 28,40 | 165 (gemessen) |

**Ø Mitte und Ø Ende sind gemessen. Die Längen dazwischen sind interpoliert** (nur
108 und 165 mm gemessen). Unkritisch, weil der Clip auf halber Länge sitzt — ein
paar Millimeter Fehler verschieben ihn nur minimal. Folge: Die Rohroberkanten
stehen nicht exakt bündig.

Ø Ende wurde meist am **kleineren** Ende gemessen. Das andere Ende könnte dicker
sein; dafür ist `ENDE_RESERVE = 1.5` da.

**Dorn:** Ø10 auf 150 mm, dann Ø8 auf 25 mm, dann Ø6 auf 20 mm (195 mm gesamt).

## Was gebaut wurde

`halter_modul1` (6×7 … 12×13), `halter_modul2` (14×15 … 20×22), `halter_dorn`.
Dazu `testclip_6-7` und `testclip_20-22` — verkürzte Einzelaufnahmen mit
identischer Klemm- und Hakengeometrie zum Vorabtesten.

Jedes Rohr steckt in einer durchgehenden C-Hülse: **weit – eng – weit**, mit
45°-Konen dazwischen. Weit an den Enden, weil das Rohr dort angestaucht ist; eng
in der Mitte, wo der Clip auf dem runden Schaft klemmt. Das Gewicht trägt ein
Boden ganz unten, der Clip sichert nur gegen Herausfallen.

Der Dorn steht nicht auf einem Boden (das wären 200 mm Hängelänge), sondern sitzt
auf seiner **eigenen Schulter**: unten ein Ring mit 8,5er Bohrung, die 8-mm-Stufe
rutscht durch, die 10-mm-Schulter legt sich auf. Die dünne Spitze hängt frei und
ist gleich der Griff.

## Testdrucke — was gelernt wurde

1. **Erster Entwurf: freistehender Clip + Becher an einer Rippe.** Nicht druckbar —
   die Ringe hängen in der Drucklage in der Luft. → durchgehende Hülse.
2. **Feste Wandstärke für alle Größen.** Der kleine 6×7-Clip hätte ~4 % Dehnung
   gebraucht und wäre gerissen. → Wand wächst mit dem Durchmesser.
3. **Ein Durchmesser reicht nicht.** Das Rohr ist zu den Enden hin angestaucht
   (damit ein Maulschlüssel greift). Der erste Testdruck ließ das dicke Ende nicht
   auf den Boden durch. → dreigeteilte Hülse.
4. **Verdickung nicht herleiten, messen.** Eine Formel aus der Schlüsselweite traf
   das 20×22 gut (28,87 gerechnet vs. 28,40 gemessen), erfand beim 6×7 aber eine
   Verdickung, die es gar nicht gibt (12,55 statt 11,00) → „zu groß".
5. **Klemmmechanismus und Clip funktionieren.** Bestätigt am gedruckten Testclip.
6. **Die Becherböden sind durchgehängt — und zwar heftig.** Das Risiko stand hier
   als „wenn sie durchhängen" unter Offen; es ist eingetreten. Am gedruckten Satz
   sind die Böden ein Fadengewirr, am leeren Becher am deutlichsten sichtbar.
   Ursache ist die Form, nicht der Drucker: in der Drucklage liegt der Boden oben
   und ist eine Decke über der **ganzen** Bohrung — beim 20×22 gut 30 mm, und über
   einen **runden** Umriss, bei dem die ersten Brückenlinien an den Rändern im
   Nichts anfangen. Das kann kein Drucker.
   → **Behoben:** Boden ist jetzt ein **45°-Kegel** (`boden_kegel()`), der sich nach
   innen zusammenzieht. Keine Brücke mehr, jede Schicht liegt auf der vorigen auf.
   In der Mitte bleibt ein Loch, das um 2 × `BODEN_D` = 6 mm kleiner ist als das
   Rohr — es trägt weiterhin, das Rohr sitzt sogar leicht zentriert im Kegel, und
   Dreck fällt unten heraus. Weil sich der Kegel außen mitverjüngt, entfällt auch
   die frühere `BODEN_LIPPE` (sie war nur da, um deckungsgleiche Flächen zu
   vermeiden).
   Die alten Module sind damit **veraltet** — neu drucken, wenn die Böden stören.

7. **Der Kegelboden funktioniert.** Gedruckt und an der Wand: die Böden kommen als
   saubere, geschlossene Ringe mit Schichtlinien statt als Fadengewirr. Die
   Rohre stehen darauf.
8. **Die freie Höhe unter dem Brett ist kein Problem** — das war eine falsche
   Sorge. Die Werkzeuge hängen durch die Ausladung des Halters **vor** den unteren
   Brettern, nicht in einer Nische zwischen ihnen. Das nächste Brett ist also gar
   kein Hindernis; lange Halter dürfen ruhig weit herunterhängen.

9. **Die interpolierten Längen waren falsch — und das fiel erst auf, als der Boden
   trug.** Solange der Clip das Rohr hielt, war die Länge fast egal: Der Clip sitzt
   auf halber Höhe, ein paar Millimeter verschieben ihn kaum. Seit der Boden das
   Gewicht trägt, bestimmt sie direkt, **wie tief das Rohr sitzt** — 6 mm zu lang
   angenommen heißt 6 mm zu tief versunken. Eine harmlose Ungenauigkeit wurde durch
   eine Konstruktionsänderung zum sichtbaren Fehler.

   | Rohr | interpoliert | gemessen | Fehler |
   |---|---|---|---|
   | 6×7 | 108 | 108 | — (war gemessen) |
   | 8×9 | 116 | **110** | 6 mm zu lang |
   | 10×11 | 123 | **120** | 3 mm zu lang |
   | 12×13 | 131 | **136** | 5 mm zu **kurz** |
   | 14×15 … 20×22 | 138/146/154/165 | am Druck bestätigt | — |

   Die Rohre wachsen **nicht linear**: von 6×7 auf 8×9 sind es 2 mm, nicht 8. Unten
   lag die Interpolation deshalb daneben, oben (nahe dem gemessenen Ankerpunkt 165)
   traf sie zufällig. Merke: eine Größe, die heute unkritisch ist, kann es morgen
   nicht mehr sein — bei jeder Konstruktionsänderung prüfen, welche Annahmen
   dadurch **tragend** werden.

10. **Die Einsinktiefe im Kegel muss herausgerechnet werden.** Auf der 45°-Schräge
    sitzt das Rohr dort auf, wo der Kegel so weit ist wie das Rohrende — und das
    ist 0,8 bis 1,6 mm tiefer als die Kegeloberkante. Beim Umbau übersehen; jetzt
    zieht `einsinktiefe()` den Boden entsprechend höher. Die Messungen an der Wand
    bestätigen die Rechnung auf den Zehntel (8×9: erwartet 14,6 mm Luft, gemessen
    15; 10×11: erwartet 11,6, gemessen 12).

## Offen

- **Modul 1 ist veraltet** und muss neu gedruckt werden — mit den echten Längen
  sitzen alle vier Rohre bündig 2 mm unter der Brettkante.
- Sitzt das Rohr auf dem Kegel sauber auf, oder sinkt es mit der Zeit tiefer ein
  (Kriechen unter Dauerlast)? Erst nach Wochen zu beurteilen.
