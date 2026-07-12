"""
Wandhalter fuer WIESEMANN 1893 Rohrsteckschluesselsatz 10tlg (Art. 81420).

Das Rohr ist KEIN glatter Zylinder: zu beiden Enden hin ist es angestaucht, damit
der Sechskant hineinpasst und man einen Maulschluessel ansetzen kann. Nur die
Mitte ist rund. Die Huelse ist deshalb dreigeteilt:

    oben    weit  - laesst den Sechskant durch
    Mitte   eng   - hier sitzt der Clip, hier ist das Rohr garantiert rund
    unten   weit  - hier steht das Rohr auf dem Boden auf

Die Uebergaenge sind 45-Grad-Konen (per loft), damit sie in der Drucklage
selbsttragend bleiben. Der Clip sitzt auf halber Rohrlaenge - dadurch muss ich
gar nicht wissen, wie weit die Stauchung reicht.

Der Boden traegt das Gewicht, der Clip sichert nur gegen Herausfallen und darf
deshalb leichtgaengig sein. Entnahme: nach vorn ziehen.

Alles hier ist Antwort auf DIESE Aufgabe. Unveraenderlich sind nur Klemmkanal und
Drucker - die stehen in wandhalter.py. Fallen: siehe CLAUDE.md.
"""

from math import asin, cos, degrees, radians, sin, sqrt

from build123d import *

from pathlib import Path

from kern.preview import render
from kern.wandhalter import KLEMMKANAL, PLATTE_D, STEG_D, haken_profil, schreibe

TITEL = "WIESEMANN 1893 Rohrsteckschluesselsatz 10tlg (81420)"
AUSGABE = Path(__file__).parent / "druck"

# --- Der Satz: (Name, Ø Mitte, Ø Ende, Laenge) ---
# Ø MITTE und Ø ENDE sind GEMESSEN. Daran klemmt bzw. passt es - nichts hergeleitet.
# Das 6x7 ist das einzige ohne Verdickung: Ende = Mitte.
# Die LAENGEN sind weiterhin interpoliert (nur 108 und 165 gemessen). Unkritisch:
# der Clip sitzt auf halber Laenge, ein paar mm Fehler verschieben ihn nur minimal.
ROHRE = [
    ("6x7", 11.00, 11.00, 108.0),
    ("8x9", 11.00, 12.20, 116.0),
    ("10x11", 13.89, 15.24, 123.0),
    ("12x13", 16.20, 18.64, 131.0),
    ("14x15", 16.24, 20.00, 138.0),
    ("16x17", 19.33, 22.70, 146.0),
    ("18x19", 22.00, 25.02, 154.0),
    ("20x22", 25.28, 28.40, 165.0),
]
MODULE = 2

# Gemessen wurde meist am kleineren Ende. Falls das andere Ende dicker ist, faengt
# die Reserve es ab. Kostet nichts: dort klemmt nichts, geklemmt wird nur in der Mitte.
ENDE_RESERVE = 1.5
STUFE_MIN = 0.3  # kleiner als das -> Rohr gilt als durchgehend rund, keine Konen

# --- Huelse, Clip, Boden ---
WAND_MIN, WAND_MAX = 1.8, 2.4  # Clipwand waechst mit dem Durchmesser (Dehnung < 1 %)
HUELSE_WAND = 1.8
CLIP_SPIEL = 0.35
CLIP_OEFFNUNG = 0.88  # Maul enger als das Rohr -> schnappt ein
CLIP_H = 14.0
CLIP_BUND = 0.3  # Clip steht ueber die Huelse hinaus - sonst deckungsgleiche Flaechen
HUELSE_SPIEL = 0.80
HUELSE_OEFFNUNG = 1.03
EINBETT = 1.5
LIPPE = 0.5

BODEN_D = 3.0
BODEN_LIPPE = 1.0

MITTE_BAND = 40.0  # enge Zone um den Clip. Muss kuerzer sein als der runde Schaft:
# beim kuerzesten Rohr (108 mm) bleiben so 34 mm Stauchung je Ende zulaessig.
Z_ROHR_OBEN = -2.0
ROHR_ABSTAND = 6.0
RAND = 8.0
H = 60.0  # Plattenhoehe

SCHRIFT_H = 5.0
SCHRIFT_TIEFE = 0.6
SCHRIFT_Y = 13.0


def d_weit(d_ende):
    """Bohrungsmass der weiten Zone: gemessener Endwert plus Reserve."""
    return d_ende + ENDE_RESERVE


def wand(od):
    return min(WAND_MAX, max(WAND_MIN, 0.10 * od))


def ro_huelse(d):
    return d / 2 + HUELSE_SPIEL + HUELSE_WAND


def ro_clip(od):
    return od / 2 + CLIP_SPIEL + wand(od) + CLIP_BUND


def achse_y(d_max):
    """Rohrachse: so weit vorn, dass die dickste Huelsenzone in die Platte waechst."""
    return -PLATTE_D - ro_huelse(d_max) + EINBETT


def profil(d, spiel, oeffnung, ro):
    """C-Profil als Skizze: Ringsegment mit Maul nach vorn (-Y)."""
    ri = d / 2 + spiel
    alpha = degrees(asin(min(0.99, (oeffnung * d / 2) / ri)))

    with BuildSketch() as sk:
        Circle(ro)
        Circle(ri, mode=Mode.SUBTRACT)
        keil = [(0.0, 0.0)]
        for a in (-90 - alpha, -90 + alpha):
            keil.append((3 * ro * cos(radians(a)), 3 * ro * sin(radians(a))))
        Polygon(*keil, align=None, mode=Mode.SUBTRACT)

        # Lippenecken ueber ihre Sollposition greifen, NICHT ueber sort_by(Axis.Y):
        # der Boolean hinterlaesst Splitter-Vertices, die den Fillet abstuerzen lassen.
        ecken = ShapeList()
        for a in (-90 - alpha, -90 + alpha):
            for r in (ri, ro):
                soll = (r * cos(radians(a)), r * sin(radians(a)))
                ecken.append(
                    min(sk.vertices(), key=lambda v: (v.X - soll[0]) ** 2 + (v.Y - soll[1]) ** 2)
                )
        fillet(ecken, radius=LIPPE)
    return sk.sketch


def prisma(prof, z, hoehe):
    with BuildPart() as p:
        add(prof.faces()[0].moved(Location((0, 0, z))))
        extrude(amount=hoehe)
    return p.part


def konus(prof_unten, z_unten, prof_oben, z_oben):
    """45-Grad-Uebergang zwischen zwei C-Profilen.

    loft() MUSS die Faces explizit bekommen. Der Weg ueber zwei BuildSketch-Ebenen
    liefert einen verdrehten Koerper mit negativem Volumen - add() versetzt die
    Skizze nicht auf die Ebene.
    """
    with BuildPart() as p:
        loft(
            [
                prof_unten.faces()[0].moved(Location((0, 0, z_unten))),
                prof_oben.faces()[0].moved(Location((0, 0, z_oben))),
            ]
        )
    return p.part


def konus_hoehe(dw, od):
    """45 Grad: die Konushoehe muss die groesste radiale Aenderung abdecken."""
    d_ro = ro_huelse(dw) - ro_huelse(od)
    d_ri = (dw - od) / 2
    d_maul = HUELSE_OEFFNUNG * (dw - od) / 2
    return max(d_ro, d_ri, d_maul) + 1.0


def rohr_aufnahme(od, d_ende, laenge):
    """Huelse + Clip + Boden fuer ein Rohr, Achse bei x=0.

    Bei verdicktem Ende dreigeteilt (weit - eng - weit) mit 45-Grad-Konen.
    Bei durchgehend rundem Rohr (6x7) faellt das weg: eine glatte Huelse.
    """
    dw = d_weit(d_ende)
    gestuft = d_ende - od > STUFE_MIN
    d_max = dw if gestuft else od

    y = achse_y(d_max)
    p_eng = profil(od, HUELSE_SPIEL, HUELSE_OEFFNUNG, ro_huelse(od))
    p_clip = profil(od, CLIP_SPIEL, CLIP_OEFFNUNG, ro_clip(od))

    z_mitte = Z_ROHR_OBEN - laenge / 2
    z_boden = Z_ROHR_OBEN - laenge

    with BuildPart() as p:
        if gestuft:
            p_weit = profil(dw, HUELSE_SPIEL, HUELSE_OEFFNUNG, ro_huelse(dw))
            k = konus_hoehe(dw, od)
            z_oben = z_mitte + MITTE_BAND / 2
            z_unten = z_mitte - MITTE_BAND / 2

            add(prisma(p_weit, z_oben + k, STEG_D - (z_oben + k)))  # weit, oben
            add(konus(p_eng, z_oben, p_weit, z_oben + k))
            add(prisma(p_eng, z_unten, MITTE_BAND))  # enges Band um den Clip
            add(konus(p_eng, z_unten, p_weit, z_unten - k))
            add(prisma(p_weit, z_boden, (z_unten - k) - z_boden))  # weit, unten
        else:
            add(prisma(p_eng, z_boden, STEG_D - z_boden))  # durchgehend glatt

        add(prisma(p_clip, z_mitte - CLIP_H / 2, CLIP_H))
        with Locations(Location((0, 0, z_boden - BODEN_D))):
            Cylinder(
                ro_huelse(d_max) + BODEN_LIPPE,
                BODEN_D,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )

    return p.part.moved(Location((0, y, 0)))


def gravur(text, x):
    """Schriftkoerper fuer die Stegoberseite; der Aufrufer zieht ihn ab.

    Gibt einen KOERPER zurueck: build123d findet den Builder ueber den
    Aufrufer-Frame, eine Hilfsfunktion kann nicht in ein fremdes BuildPart schreiben.
    """
    ebene = Plane(origin=(x, SCHRIFT_Y, STEG_D - SCHRIFT_TIEFE), x_dir=(1, 0, 0), z_dir=(0, 0, 1))
    with BuildPart() as p:
        with BuildSketch(ebene):
            Text(text, font_size=SCHRIFT_H)
        extrude(amount=SCHRIFT_TIEFE)
    return p.part


def aussenradius(od, d_ende):
    d = d_weit(d_ende) if d_ende - od > STUFE_MIN else od
    return ro_huelse(d)


def positionen(rohre):
    radien = [aussenradius(od, de) for _, od, de, _ in rohre]
    xs, x = [], RAND
    for i, ro in enumerate(radien):
        if i > 0:
            x += radien[i - 1] + ROHR_ABSTAND + ro
        xs.append(x)
    return xs, xs[-1] + radien[-1] + RAND


def leiste(rohre):
    xs, breite = positionen(rohre)
    with BuildPart() as teil:
        add(haken_profil(breite, H))
        for (_, od, de, laenge), x in zip(rohre, xs):
            add(rohr_aufnahme(od, de, laenge).moved(Location((x, 0, 0))))
        for (label, _, _, _), x in zip(rohre, xs):
            add(gravur(label, x), mode=Mode.SUBTRACT)
    return teil.part


# =============================================================================
#  Der Dorn (Drehstift): 10 mm auf 150 mm, dann 8 mm auf 25, dann 6 mm auf 20.
#
#  Er STEHT nicht auf einem Boden - das waeren 200 mm Haengelaenge. Stattdessen
#  sitzt er auf seiner eigenen SCHULTER: unten schliesst ein Ring mit 8,5er
#  Bohrung, durch den die 8-mm-Stufe rutscht, waehrend sich die 10-mm-Schulter
#  darauf ablegt. Der Halter ist damit nur so lang wie das dicke Stueck, und die
#  duenne Spitze haengt frei darunter - gleichzeitig der Griff zum Rausziehen.
# =============================================================================
DORN_D = 10.0
DORN_DICK_L = 150.0
DORN_STUFE_D = 8.0
SCHULTER_D = 4.0  # Dicke des tragenden Rings
SCHULTER_SPIEL = 0.5  # Luft um die 8-mm-Stufe


def dorn_aufnahme():
    y = achse_y(DORN_D)
    p_huelse = profil(DORN_D, HUELSE_SPIEL, HUELSE_OEFFNUNG, ro_huelse(DORN_D))
    p_clip = profil(DORN_D, CLIP_SPIEL, CLIP_OEFFNUNG, ro_clip(DORN_D))
    # Schulterring: Bohrung fuer die 8er-Stufe, Maul (8,4) enger als die 10er-Schulter
    p_schulter = profil(
        DORN_STUFE_D, SCHULTER_SPIEL, HUELSE_OEFFNUNG, ro_huelse(DORN_D) + BODEN_LIPPE
    )

    z_schulter = Z_ROHR_OBEN - DORN_DICK_L  # hier liegt die 10-mm-Schulter auf
    z_mitte = Z_ROHR_OBEN - DORN_DICK_L / 2
    k = 2.0

    with BuildPart() as p:
        add(prisma(p_huelse, z_schulter + k, STEG_D - (z_schulter + k)))
        add(konus(p_schulter, z_schulter, p_huelse, z_schulter + k))
        add(prisma(p_schulter, z_schulter - SCHULTER_D, SCHULTER_D))
        add(prisma(p_clip, z_mitte - CLIP_H / 2, CLIP_H))
    return p.part.moved(Location((0, y, 0)))


def dorn_halter():
    breite = 2 * ro_huelse(DORN_D) + 2 * BODEN_LIPPE + 2 * RAND
    with BuildPart() as teil:
        add(haken_profil(breite, H))
        add(dorn_aufnahme().moved(Location((breite / 2, 0, 0))))
        add(gravur("Dorn", breite / 2), mode=Mode.SUBTRACT)
    return teil.part


# --- Testclip: verkuerzte Einzelaufnahme, identische Klemmgeometrie ---
TEST_LAENGE = 90.0


def testclip(label, od, d_ende):
    breite = 2 * aussenradius(od, d_ende) + 2 * RAND
    with BuildPart() as teil:
        add(haken_profil(breite, H))
        add(rohr_aufnahme(od, d_ende, TEST_LAENGE).moved(Location((breite / 2, 0, 0))))
        add(gravur(label, breite / 2), mode=Mode.SUBTRACT)
    return teil.part


def masse():
    print(f"{'Rohr':8}{'Mitte':>7}{'Ende':>7}{'Huelse':>8}{'Konus':>7}{'Clipwand':>10}")
    for name, od, de, _ in ROHRE:
        gestuft = de - od > STUFE_MIN
        dw = d_weit(de) if gestuft else od
        k = konus_hoehe(dw, od) if gestuft else 0.0
        print(f"{name:8}{od:7.2f}{de:7.2f}{dw:8.2f}{k:7.1f}{wand(od):10.2f}")
    print()


def tests_bauen():
    print(f"Testclips - Klemmkanal {KLEMMKANAL:.0f} mm, Rohr {TEST_LAENGE:.0f} mm\n")
    for label, od, de, _ in (ROHRE[0], ROHRE[-1]):
        name = f"testclip_{label.replace('x', '-')}"
        ziel = schreibe(testclip(label, od, de), name, AUSGABE)
        render(f"{ziel}.stl", f"{ziel}.png", titel=name)
        print()


def bauen():
    pro_modul = len(ROHRE) // MODULE
    gruppen = [ROHRE[i : i + pro_modul] for i in range(0, len(ROHRE), pro_modul)]
    for i, gruppe in enumerate(gruppen, 1):
        name = f"halter_modul{i}"
        ziel = schreibe(leiste(gruppe), name, AUSGABE)
        tief = min(Z_ROHR_OBEN - l - BODEN_D for _, _, _, l in gruppe)
        print(f"  haengt    {abs(tief):.0f} mm unter die Brettoberkante")
        render(f"{ziel}.stl", f"{ziel}.png", titel=f"{name} — {', '.join(g[0] for g in gruppe)}")
        print()

    ziel = schreibe(dorn_halter(), "halter_dorn", AUSGABE)
    print(f"  haengt    {abs(Z_ROHR_OBEN - DORN_DICK_L - SCHULTER_D):.0f} mm"
          f" (+ 45 mm freie Spitze)")
    render(f"{ziel}.stl", f"{ziel}.png", titel="halter_dorn")
    print()


if __name__ == "__main__":
    import sys

    masse()
    tests_bauen() if "test" in sys.argv else bauen()
