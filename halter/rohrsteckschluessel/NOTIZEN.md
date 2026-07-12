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

## Offen

- **Freie Höhe unter dem Brett** ist nicht gemessen. Modul 2 hängt 170 mm runter,
  der Dorn 156 mm plus 45 mm freie Spitze. Wenn das nächste Brett vorher kommt,
  stoßen sie an.
- Becherböden drucken als **Brücke** über die Hülsenbohrung. Wenn sie durchhängen:
  Hülse unten auf den letzten Millimetern zu einem vollen Ring schließen, dann ist
  die Brücke rundum angebunden. Rohr dann seitlich einschieben und absenken.
