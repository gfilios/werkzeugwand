"""
Die zwei unveraenderlichen Groessen der Werkstattwand: der Klemmmechanismus und
der Drucker. Sonst nichts.

Alles Weitere - wie ein Werkzeug gehalten wird, welche Wandstaerke ein Clip
braucht, wo die Beschriftung sitzt - ist Sache des jeweiligen Teils und gehoert
in dessen eigenes Skript. Was fuer Rohrsteckschluessel richtig ist, kann fuer
Ratschen falsch sein.

Koordinaten
-----------
    y = Tiefe   0 = Brettvorderseite, + = zur Wand hin
    z = Hoehe   0 = Brettoberkante,   - = nach unten
    x = Breite  entlang des Bretts
"""

from pathlib import Path

from build123d import *

# --- Der Klemmmechanismus (gemessen am funktionierenden Probehaken) ---
KLEMMKANAL = 25.0  # lichte Weite Platte <-> hinterer Schenkel. Bretter sind knapp duenner.
PLATTE_D = 3.5  # Frontplatte, liegt am Brett an
STEG_D = 5.0  # Steg ueber der Brettkante
HAKEN_D = 3.5  # hinterer Schenkel, greift in den Luftspalt
HAKEN_L = 30.0  # Eingriffstiefe

Y_HINTEN = KLEMMKANAL  # Innenflaeche des hinteren Schenkels

# --- Der Drucker ---
BETT = (250.0, 210.0, 220.0)  # Prusa MK4S


def haken_profil(breite, hoehe):
    """Haken + Frontplatte als Querschnitt, entlang X extrudiert.

    Der Kanal oeffnet sich nach unten (-z), das Teil wird also KOPFUEBER gedruckt,
    mit der Stegoberseite auf dem Bett. Nur so bleibt der Kanal stuetzfrei.
    """
    y_aussen = Y_HINTEN + HAKEN_D
    pts = [
        (-PLATTE_D, -hoehe),
        (-PLATTE_D, STEG_D),
        (y_aussen, STEG_D),
        (y_aussen, -HAKEN_L),
        (Y_HINTEN, -HAKEN_L),
        (Y_HINTEN, 0.0),
        (0.0, 0.0),
        (0.0, -hoehe),
    ]
    with BuildPart() as p:
        with BuildSketch(Plane.YZ):
            Polygon(*pts, align=None)
        extrude(amount=breite)
        chamfer(p.faces().sort_by(Axis.Z)[-1].edges(), length=0.5)
    return p.part


def druckfertig(teil):
    """Kopfueber drehen und aufs Bett setzen: Steg unten, Kanal und Huelsen nach oben.

    Wird beim Export der Slicer-Dateien angewandt, damit die Drucklage gar nicht
    erst verwechselt werden kann. Falsch herum gedruckt braucht dasselbe Teil
    Stuetzen unter jedem Boden und im ganzen Hakenkanal.
    """
    gedreht = teil.rotate(Axis.X, 180)
    bb = gedreht.bounding_box()
    return gedreht.moved(Location((0, 0, -bb.min.Z)))


BRETT_DICKE = 23.0  # nur fuer Bilder: knapp duenner als der Klemmkanal
BRETT_HOEHE = 110.0


def brett(breite, ueberstand=30.0):
    """Ein Stueck Brett - NUR fuer Renderings, wird nie exportiert.

    Zeigt, wie der Halter ueber die Oberkante greift. Sitzt mittig im Klemmkanal.
    """
    luft = (KLEMMKANAL - BRETT_DICKE) / 2
    with BuildPart() as p:
        with BuildSketch(Plane.XY):
            Rectangle(breite + 2 * ueberstand, BRETT_DICKE, align=(Align.MIN, Align.MIN))
        extrude(amount=-BRETT_HOEHE)
    return p.part.moved(Location((-ueberstand, luft, 0)))


def schreibe(teil, name, ordner):
    """STEP in Wandkoordinaten (fuer CAD), STL/3MF fertig gedreht (fuer den Slicer)."""
    ordner = Path(ordner)
    ordner.mkdir(parents=True, exist_ok=True)
    ziel = ordner / name

    # STEP fuer Fusion 360 & Co: echter Volumenkoerper mit Flaechen und Kanten,
    # kein Dreiecksnetz. Eine native .f3d gibt es nicht - das Format ist proprietaer.
    # Bleibt im Wandkoordinatensystem (z=0 = Brettoberkante), damit man dort misst.
    export_step(teil, f"{ziel}.step", unit=Unit.MM)

    druck = druckfertig(teil)
    export_stl(druck, f"{ziel}.stl")
    m = Mesher(unit=Unit.MM)
    # Feine Standardtoleranz. Mit linear_deflection=0.01 kollabieren duenne Waende
    # und kleine Verrundungen zu entarteten Dreiecken -> "3mf mesh is invalid".
    m.add_shape(druck)
    m.write(f"{ziel}.3mf")

    bb = teil.bounding_box()
    passt = all(s <= b for s, b in zip((bb.size.X, bb.size.Y, bb.size.Z), BETT))
    print(f"{name}")
    print(f"  Bauraum   {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm"
          f"  -> MK4S: {'passt' if passt else 'PASST NICHT'}")
    print(f"  Ausladung {abs(bb.min.Y):.0f} mm vor dem Brett")
    print(f"  Volumen   {teil.volume / 1000:.0f} cm3 (massiv gerechnet)")
    print(f"  Gueltig   {teil.is_valid}")
    return ziel
