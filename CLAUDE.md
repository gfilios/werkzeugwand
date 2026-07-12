# Werkstattwand — 3D-gedruckte Werkzeughalter

Halter für die Werkzeugwand in der Garage. Modelliert als Python-Code mit
**build123d** (OpenCascade-Kernel), Export als STL, 3MF und STEP.

```bash
./.venv/bin/python bauen.py --liste                       # welche Halter gibt es
./.venv/bin/python bauen.py                               # alle bauen
./.venv/bin/python bauen.py rohrsteckschluessel           # nur einen
./.venv/bin/python bauen.py rohrsteckschluessel --test    # nur dessen Testclips
```

## Aufbau

```
kern/wandhalter.py    Klemmmechanismus + Drucker + Export.  UNVERÄNDERLICH.
kern/preview.py       rendert eine STL als PNG zur Sichtkontrolle
bauen.py              findet alle Halter und baut sie
halter/<name>/
    modell.py         das Teil. Messwerte stehen oben im Kopf.
    NOTIZEN.md        Messwerte, Testergebnisse, was schiefging, was offen ist
    druck/            erzeugte STL/3MF/STEP/PNG (nicht im Repo, baut sich neu)
CLAUDE.md             dieses Dokument
```

**Ein Repo für die ganze Wand**, nicht eines pro Halter: Klemmmechanismus, Drucker
und die Erfahrungen unten gelten für jedes Teil. Getrennte Repos würden `kern/` und
diese Datei duplizieren, und ab dann driften sie auseinander.

## Neuen Halter anlegen

1. `halter/<name>/modell.py` — muss `TITEL`, `AUSGABE` und `bauen()` bereitstellen,
   optional `tests_bauen()` und `masse()`. `bauen.py` findet ihn dann von selbst.
2. Aus `kern.wandhalter` kommen `haken_profil()` und `schreibe()`. **Sonst nichts
   von woanders kopieren** — was für den Rohrsteckschlüssel richtig war, kann für
   das nächste Werkzeug falsch sein (siehe „Erfahrungen").
3. `NOTIZEN.md` anlegen und die **Messwerte** dort festhalten. Die sind aus nichts
   herleitbar und der teuerste Teil der Arbeit.
4. Erst einen **Testclip** drucken, dann das große Teil.

---

## Unveränderlich

Nur zwei Dinge. Sie stehen in `wandhalter.py`, sonst nichts.

**1. Der Klemmmechanismus.** Die Wand besteht aus waagerechten Brettern auf
senkrechten Latten, hinter jedem Brett ist ein Luftspalt. Ein Halter greift über
die **Oberkante** eines Bretts: hinterer Schenkel in den Spalt, Steg über die
Kante, Frontplatte davor. Nicht geschraubt, frei verschiebbar.

- **Klemmkanal 25 mm** (lichte Weite Platte ↔ hinterer Schenkel). Gemessen am
  funktionierenden Probehaken; die Bretter sind knapp dünner.
- Wo eine **senkrechte Latte** hinter dem Brett sitzt, gibt es **keinen Spalt**.
  Halter dazwischen setzen.
- **Nach unten ist Platz.** Ein Halter darf ruhig weit unter die Brettkante reichen:
  durch seine Ausladung hängt das Werkzeug **vor** den Brettern darunter, nicht in
  einer Nische zwischen ihnen. Das nächste Brett ist kein Hindernis (an der Wand
  bestätigt). Lange Werkzeuge brauchen also keinen Sonderaufbau.

**2. Der Drucker.** Prusa MK4S, 250 × 210 × 220 mm.

Daraus folgt die **Drucklage: kopfüber, Steg auf dem Bett.** Nur so öffnet sich
der Hakenkanal nach oben und braucht keine Stützen. Andersherum drehen hilft
nicht — der Haken zeigt nach hinten, die Aufnahmen nach vorn; eines von beidem
zeigt immer ins Bett.

**Und daraus die eiserne Regel für jedes neue Teil:** Jedes Merkmal muss als
senkrechtes Prisma vom Steg aus durchlaufen. Ein Ring oder eine Öse, die frei vor
der Platte schwebt, hängt in der Drucklage in der Luft und lässt sich nicht
drucken — auch nicht mit Stützen, die säßen mitten in der Aufnahme.

**Die Slicer-Dateien (`.3mf`/`.stl`) werden bereits gedreht exportiert** (`druckfertig()`
in `wandhalter.py`) — im Slicer nichts mehr drehen, sonst steht es wieder falsch.
Die `.step` bleibt im Wandkoordinatensystem (z = 0 ist die Brettoberkante), damit man
in Fusion an der Wand messen kann.

Slicer: **Brim an**, **Supports AUS**. Supports sind hier nicht nur unnötig, sondern
schädlich — sie landen in den Hülsenbohrungen und im Hakenkanal. Ohne Stützen
druckbar zu sein ist damit keine Kür, sondern Bedingung: **jede waagerechte Decke
über einem Hohlraum muss durch 45°-Geometrie ersetzt werden** (siehe „Kein flacher
Boden über einer Bohrung" unten).

---

## Erfahrungen — nicht ungeprüft übernehmen

Das Folgende war die **Antwort auf Rohrsteckschlüssel** (gleichmäßige Rohre, hohl,
108–165 mm). Für ein anderes Werkzeug kann es falsch sein. Eine Ratsche etwa hat
einen dicken Kopf und einen dünnen Griff — eine Hülse über die volle Länge passt
da nicht. Also: als Denkanstoß lesen, nicht als Vorlage kopieren.

- **Ein Werkzeug hat nicht *einen* Durchmesser.** Der Rohrsteckschlüssel ist zu
  beiden Enden hin angestaucht (damit der Sechskant reinpasst und ein Maulschlüssel
  greift) — nur die Mitte ist rund. Ein Modell auf einen einzigen gemessenen
  Durchmesser zu bauen, ging schief. Immer nach der **dicksten Stelle** fragen, nicht
  nach „dem" Durchmesser. Konsequenz hier: Hülse dreigeteilt (weit–eng–weit), Clip
  auf halber Länge, wo das Rohr garantiert rund ist — dann muss man die Länge der
  Verdickung gar nicht kennen.
- **Eine Konstruktionsänderung kann eine harmlose Annahme tragend machen.** Die
  Rohrlängen waren teils interpoliert — egal, solange der *Clip* das Rohr hielt: der
  sitzt auf halber Höhe, ein paar Millimeter verschieben ihn kaum. Als der *Boden*
  das Gewicht übernahm, bestimmte dieselbe Zahl plötzlich, **wie tief das Rohr
  sitzt**, und 6 mm Schätzfehler wurden zu 6 mm Versinken. Also: bei jeder Änderung
  fragen, **welche bisher unkritische Größe jetzt trägt** — und die dann messen.
  (Und Werkzeuge wachsen nicht linear: von 6×7 auf 8×9 sind es 2 mm, nicht 8.)
- **Last und Sicherung trennen.** Ein C-Clip hält nur radial; senkrecht rutscht
  das Werkzeug durch. Das Gewicht trug am Ende ein **Boden**, auf dem das Rohr
  steht; der Clip sichert nur gegen Herausfallen und darf leichtgängig sein.
- **Nicht über die ganze Länge klemmen.** Eine Hülse mit Klemmung über 165 mm
  bekäme man nie wieder auf. Die Hülse läuft frei (Maul > Durchmesser), nur auf
  ~14 mm Höhe zieht sie sich zum Clip zusammen (Maul ≈ 0,88 × Durchmesser).
- **Clip-Wandstärke mit dem Durchmesser mitwachsen lassen.** Bei fester Wand sind
  die Arme eines kleinen Clips kurz und dick, müssten sich um mehrere Prozent
  dehnen und reißen — während ein großer Clip mit derselben Wand butterweich wäre.
  Ziel: Randfaserdehnung unter 1 % über alle Größen.
- **Kein flacher Boden über einer Bohrung.** Hier stand mal, die Becherböden seien
  „Brücken über die Bohrung: die druckt der MK4S problemlos". **Das ist falsch, und
  zwar gedruckt und angeschaut.** In der Drucklage liegt so ein Boden *oben* und ist
  eine Decke über der ganzen Bohrung — beim 20×22 gut 30 mm Spannweite, und das über
  einen **runden** Umriss, bei dem die ersten Brückenlinien an den Rändern im Nichts
  anfangen und nichts zum Ankern haben. Ergebnis: ein Fadengewirr. Kein Drucker kann
  das, es ist keine Frage der Maschine. Der Boden muss ein **45°-Kegel** sein, der
  sich nach innen zusammenzieht: jede Schicht liegt auf der vorigen auf, keine
  einzige Brücke. Das Restloch in der Mitte ist kleiner als das Werkzeug — es trägt
  weiterhin, und Dreck fällt heraus statt sich zu sammeln. Verjüngt sich der Kegel
  außen mit, entfällt zugleich die deckungsgleiche Fläche zur Hülse.
- **Ein waagerechter Zapfen geht doch — auf der Ecke.** Ein 1/4″-Vierkant zum
  Aufstecken (Nüsse) ragt waagerecht nach vorn und ist damit erst mal genau der
  verbotene Auskrager. Um **45° auf die Ecke gedreht** stehen seine unteren Flächen
  exakt 45° schräg und er druckt stützfrei. Die eiserne Regel ist also nicht „nur
  senkrechte Prismen", sondern „**nirgends flacher als 45°**".
- **Beschriftung nur graviert, in die Stegoberseite.** Das ist die Bettfläche —
  erhabene Schrift ginge dort nicht.
- Material **PETG**, nicht PLA: die Garage wird im Sommer warm, PLA kriecht unter
  Dauerlast.

**Vorgehen, das sich bewährt hat:** vor dem großen Druck erst einen **Testclip** —
eine verkürzte Einzelaufnahme mit identischer Klemm- und Hakengeometrie, ~30 min
Druckzeit. Immer die **Extreme** testen (kleinstes und größtes Werkzeug), nicht die
Mitte. Und vor dem Slicen mit `preview.py` rendern, statt dem Code zu vertrauen.

**Passungen ertesten, gestaffelt — und den Randwert nicht glauben.** Ob ein
gedruckter Zapfen eine Nuss leicht *und* haltend trägt, entscheiden Zehntel; das
rechnet man nicht aus, das druckt man (mehrere Maße nebeneinander auf einem Clip).
Wichtig: **Gewinnt der äußerste Wert der Staffel, ist nichts gefunden** — dann war
die Staffel falsch gewählt und das Optimum liegt dahinter. Erst wenn der beste Wert
von beiden Seiten eingeklammert ist, stimmt er. (Beim 1/4″-Vierkant brauchte es
dafür zwei Runden: 6,10–6,40 gewann am oberen Rand, erst 6,50–6,70 klammerte den
echten Wert 6,50 ein.)

---

## build123d-Fallen (hier alle schon reingetreten)

- **Der Builder-Kontext wird über den Aufrufer-Frame gefunden.** Eine Hilfsfunktion
  kann *nicht* in ein `BuildPart` hineinarbeiten, das eine Ebene darüber offen ist —
  `extrude()` findet dort keine Skizze. Helfer machen ihr **eigenes** `BuildPart`
  auf und **geben einen Körper zurück**; der Aufrufer macht `add(...)` bzw.
  `add(..., mode=Mode.SUBTRACT)`.
- **`loft()` braucht die Faces explizit**: `loft([f1.moved(...), f2.moved(...)])`.
  Der Weg über zwei `BuildSketch`-Ebenen (`with BuildSketch(Plane.XY.offset(h)): add(...)`)
  liefert einen verdrehten Körper mit **negativem Volumen** — `add()` versetzt die
  Skizze nicht auf die Ebene. `is_valid` meldet trotzdem `True`. Also nach jedem Loft
  das Volumen prüfen: negativ oder viel zu klein heißt kaputt.
- **`Box()`/`Cylinder()` im aktiven `BuildPart` fügen sich selbst am Ursprung ein.**
  Wer zusätzlich `add(Box(...).moved(...))` schreibt, hat das Teil doppelt drin.
  Über `with Locations(...)` platzieren.
- **Deckungsgleiche Flächen killen den 3MF-Export** („3mf mesh is invalid"). Zwei
  Zylinder mit identischem Radius, die verschmolzen werden, erzeugen entartete
  Dreiecke. Immer einen kleinen Versatz geben (Bund, Lippe). Die Geometrie ist
  dabei laut `is_valid` in Ordnung — der Fehler kommt erst beim Vernetzen.
- **`Mesher.add_shape()` nur mit der feinen Standardtoleranz.** Mit
  `linear_deflection=0.01` kollabieren dünne Wände und kleine Verrundungen.
- **Kanten/Ecken nicht über `sort_by()` greifen.** Booleans hinterlassen
  Splitter-Vertices, die dann mitausgewählt werden und `fillet()` abstürzen lassen.
  Sollposition ausrechnen und den nächstgelegenen Vertex nehmen.
- `is_valid` ist eine **Property**, keine Methode. 3MF schreibt man über die Klasse
  `Mesher`, nicht über ein `export_3mf()`.
