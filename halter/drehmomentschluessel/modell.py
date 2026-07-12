"""
Wandhalter fuer Hairich Drehmomentschluessel-Satz 1/4", 1-25 Nm, 13-teilig.

Der Koffer entfaellt, alles haengt offen an der Wand. Drei Werkzeugarten, drei
grundverschiedene Aufgaben - deshalb NICHT eine Geometrie fuer alles:

    11 Bit-Nuesse   alle identisch (Ø 11,86 x 38 mm). Sie werden auf einen
                    1/4"-VIERKANTZAPFEN aufgesteckt, wie auf den Ratschenkopf -
                    aufstecken und abziehen, kein Einfaedeln.

    Verlaengerung   102 mm, aber NICHT durchgehend rund: Schaft 8,90 mm, das
                    Aufnahme-Ende 12,67 mm. Also dreigeteilte Huelse (weit-eng-
                    weit) mit 45-Grad-Konen, Clip auf halber Laenge im runden
                    Schaft. Genau die Falle vom Rohrsteckschluessel.

    Schluessel      TODO - es fehlt die Kopflaenge entlang der Achse. Haengt dann
                    an seiner EIGENEN SCHULTER: der Ratschenkopf (27,55 x 13,51)
                    liegt auf einem C-Ring auf, dessen Bohrung das 16,09er Rohr
                    durchlaesst. Wie der Dorn beim Rohrsteckschluesselsatz.

DER VIERKANT UND DIE DRUCKLAGE
------------------------------
Ein waagerecht nach vorn ragender Zapfen ist in der Drucklage (kopfueber, Steg auf
dem Bett) ein Auskrager - eigentlich genau das, was die eiserne Regel verbietet.
Er geht trotzdem, wenn man ihn um 45 Grad AUF DIE ECKE dreht: dann stehen seine
beiden unteren Flaechen exakt 45 Grad schraeg, und das druckt der MK4S stuetzfrei.
Die Nuss sitzt dadurch als Raute auf dem Zapfen - am runden Nussgehaeuse sieht das
niemand.

Ein Zapfen NACH UNTEN waere zwar ein sauberes senkrechtes Prisma, aber dann haenge
die Nuss allein an der Reibung gegen ihr eigenes Gewicht. Waagerecht wirkt das
Gewicht quer zur Abziehrichtung - die Reibung muss gar nichts tragen.

DIE PASSUNG IST NICHT BERECHENBAR
---------------------------------
Der 1/4"-Antrieb ist mit 6,3 mm genormt, aber ob ein gedruckter Zapfen die Nuss
leicht UND haltend traegt, entscheiden Zehntelmillimeter - und die Reibung ist das
Einzige, was die Nuss haelt. Deshalb: Testclip mit drei gestaffelten Zapfen
(6,10 / 6,25 / 6,40) drucken, aufstecken, den passenden waehlen und in VIERKANT
eintragen. Erst dann die grosse Leiste.

Unveraenderlich sind nur Klemmkanal und Drucker (wandhalter.py). Fallen: CLAUDE.md.
"""

from math import asin, cos, degrees, radians, sin
from pathlib import Path

from build123d import *

from kern.preview import HALTER, HOLZ, STAHL, render
from kern.wandhalter import KLEMMKANAL, PLATTE_D, STEG_D, brett, haken_profil, schreibe

TITEL = "Hairich Drehmomentschluessel-Satz 1/4\" 1-25 Nm (13-tlg)"
AUSGABE = Path(__file__).parent / "druck"

# --- Messwerte (Messschieber, siehe NOTIZEN.md) ---
NUSS_D = 11.86  # geraendelter Nusskoerper - fuer alle elf gleich
NUSS_L = 38.0  # Gesamtlaenge - fuer alle elf gleich
BITS = ["H2", "H2.5", "H3", "H4", "H5", "H6", "H8", "H10", "T10", "T25", "T30"]

VERL_D = 8.90  # Schaft "an der normalen Stelle"
VERL_ENDE = 12.67  # Aufnahme-Ende, die dickste Stelle
VERL_L = 102.0

# --- Der Schluessel ---
# Der Ratschenkopf ist eine RUNDE Scheibe: Ø 39,0, Dicke 13,51.
# Die 27,55 aus dem ersten Foto waren NICHT die breiteste Stelle - der Messschieber
# sass unterhalb, naeher am Hals. Fuer die Huelse zaehlt nur das groesste Mass,
# sonst passt der Kopf nicht hinein. Wieder die alte Lehre: nach der DICKSTEN
# Stelle fragen, nicht nach "dem" Durchmesser.
# Weil die Scheibe rund ist, ist ihre Ausdehnung LAENGS der Achse ebenfalls 39.
KOPF_D_MAX = 39.0  # Durchmesser der Ratschenscheibe
KOPF_DICK = 13.51  # Scheibendicke (flache Richtung)
KOPF_L = 39.0  # = Durchmesser: so weit baut der Kopf entlang der Achse
SCHAFT_D = 16.09  # Rohr direkt unter dem Kopf - HIER haengt er auf
ROT_D = 29.5  # roter Verstellring, die dickste Stelle des Schluessels
GRIFF_D = 24.4
SCHLUESSEL_L = 194.0
KOPF_BIS_GRIFF = 66.22  # Kopf-Unterkante -> Anfang des schwarzen Griffs
GRIFF_L = SCHLUESSEL_L - KOPF_L - KOPF_BIS_GRIFF  # 88,78 - nicht gemessen, gerechnet

KOPF_SPIEL = 1.0  # Luft um den Kopf in der weiten Huelse
SCHULTER_SPIEL = 0.5  # Luft um den Schaft im Ring
SCHULTER_D = 4.0  # Hoehe des fuehrenden Rings unter dem Konus
SCHULTER_RO = 12.0  # Aussenradius des Rings - KLEINER als die Huelse, siehe unten

# --- Der Vierkant ---
# ERMITTELT, nicht gerechnet - in zwei Runden Testclip:
#   Runde 1 (6,10 / 6,25 / 6,40): selbst der dickste haelt nur "gerade so".
#   Runde 2 (6,50 / 6,60 / 6,70): der KLEINSTE passt am besten.
# Erst beide Runden zusammen taugen etwas: Runde 1 begrenzt von unten (6,40 zu
# locker), Runde 2 von oben (6,60 schon schlechter). 6,50 liegt damit wirklich im
# Optimum und nicht bloss am Rand einer Staffel - genau der Fehler, den Runde 1
# allein gemacht haette.
VIERKANT = 6.50
PASSUNGEN = [6.50, 6.60, 6.70]  # Staffel der letzten Testrunde
ZAPFEN_FREI = 15.0  # frei stehende Laenge vor der Platte
ZAPFEN_FASE = 1.0  # Anfasung der Spitze: die Nuss findet von selbst drauf
Z_ZAPFEN = -22.0  # Hoehe der Zapfenachse unter der Brettoberkante
NUSS_ABSTAND = 19.0  # Raster: 11,86 Nuss + 7 mm Luft, damit die Finger drankommen

# --- Huelse, Clip, Boden (nur noch fuer die Verlaengerung) ---
HUELSE_WAND = 1.8
HUELSE_SPIEL = 0.5  # laeuft frei: die Huelse haelt nicht, sie fuehrt nur
HUELSE_OEFFNUNG = 1.03  # Maul weiter als das Werkzeug -> rutscht durch
CLIP_SPIEL = 0.3
CLIP_OEFFNUNG = 0.88  # Maul enger als das Werkzeug -> schnappt ein
CLIP_WAND = 1.8
CLIP_BUND = 0.3  # Clip steht ueber die Huelse hinaus - sonst deckungsgleiche Flaechen
CLIP_H = 10.0
LIPPE = 0.5
EINBETT = 1.5  # so tief waechst die Huelse in die Frontplatte

# Der Boden ist ein 45-Grad-Kegel, keine flache Scheibe: eine Scheibe liegt in der
# Drucklage OBEN und ist eine Decke ueber der ganzen Bohrung. Beim
# Rohrsteckschluessel wurde daraus ein Fadengewirr (gedruckt und gesehen, 2026).
# BODEN_D ist zugleich die Hoehe des Kegels UND sein radialer Einzug - das ist die
# 45-Grad-Bedingung. Je groesser, desto kleiner das Restloch und desto breiter die
# Auflage; 4 mm lassen 6,7 mm offen, da faellt auch der Vierkant nicht durch.
BODEN_D = 4.0

ENDE_RESERVE = 1.0  # Zuschlag auf das gemessene dicke Ende
Z_OBEN = -2.0  # Oberkante Werkzeug, knapp unter der Brettoberkante

RAND = 8.0
H_NUESSE = 45.0  # Plattenhoehe der Nussleiste
H_VERL = 50.0  # Plattenhoehe des Verlaengerungshalters
H_SCHLUESSEL = 80.0  # Plattenhoehe des Schluesselhalters

SCHRIFT_H = 4.0
SCHRIFT_TIEFE = 0.6
SCHRIFT_Y = 13.0


# --- Der Vierkantzapfen -----------------------------------------------------


def zapfen(a=None):
    """1/4"-Vierkant, waagerecht nach vorn (-Y), um 45 Grad auf die Ecke gedreht.

    Die 45-Grad-Drehung ist keine Kosmetik, sondern der Grund, warum das Teil ohne
    Stuetzen druckt: auf der Ecke stehend sind die beiden unteren Flaechen des
    Zapfens 45-Grad-Schraegen statt einer waagerechten Decke ins Nichts.

    Faengt bei y=0 an (also PLATTE_D tief in der Frontplatte drin) und ragt
    ZAPFEN_FREI davor hinaus - die Platte selbst ist der Anschlag fuer die Nuss.
    """
    a = VIERKANT if a is None else a
    laenge = PLATTE_D + ZAPFEN_FREI

    with BuildPart() as p:
        with BuildSketch(Plane.XZ):
            Rectangle(a, a, rotation=45)
        extrude(amount=laenge)
        # Spitze anfasen, damit die Nuss von selbst drauffindet.
        spitze = p.faces().sort_by(Axis.Y)[0]
        chamfer(spitze.edges(), length=ZAPFEN_FASE)
    return p.part


# --- Die Verlaengerung: dreigeteilte Huelse ---------------------------------


def ro_huelse(d):
    return d / 2 + HUELSE_SPIEL + HUELSE_WAND


def ro_clip(d):
    return d / 2 + CLIP_SPIEL + CLIP_WAND + CLIP_BUND


def achse_y(d_max):
    """Werkzeugachse: so weit vorn, dass die dickste Huelsenzone in die Platte waechst."""
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

    loft() MUSS die Faces explizit bekommen - der Weg ueber zwei BuildSketch-Ebenen
    liefert einen verdrehten Koerper mit negativem Volumen.
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


def boden_kegel(d_max, z_boden):
    """Der Boden als 45-Grad-Kegel - NICHT als flache Scheibe. Siehe BODEN_D.

    Zieht sich mit 45 Grad nach innen zusammen, also liegt jede Schicht auf der
    vorigen auf - keine einzige Bruecke. Das Restloch ist kleiner als die
    Verlaengerung, es traegt also weiterhin. Aussen verjuengt sich der Kegel mit:
    dadurch entsteht keine deckungsgleiche Zylinderflaeche mit der Huelse, die
    sonst den 3MF-Export killt.
    """
    oben = profil(d_max, HUELSE_SPIEL, HUELSE_OEFFNUNG, ro_huelse(d_max))
    unten = profil(
        d_max - 2 * BODEN_D,
        HUELSE_SPIEL,
        HUELSE_OEFFNUNG,
        ro_huelse(d_max) - BODEN_D,
    )
    return konus(unten, z_boden - BODEN_D, oben, z_boden)


def verlaengerung_aufnahme():
    """Weit - eng - weit, wie beim Rohrsteckschluessel. Achse bei x=0.

    Der Schaft ist 8,90, das Aufnahme-Ende 12,67. Eine Huelse auf 8,90 liesse das
    Ende nicht durch; eine auf 12,67 wuerde nirgends fuehren. Also enges Band nur
    um den Clip, auf halber Laenge - dort ist der Schaft garantiert rund.
    """
    dw = VERL_ENDE + ENDE_RESERVE
    y = achse_y(dw)

    p_eng = profil(VERL_D, HUELSE_SPIEL, HUELSE_OEFFNUNG, ro_huelse(VERL_D))
    p_weit = profil(dw, HUELSE_SPIEL, HUELSE_OEFFNUNG, ro_huelse(dw))
    p_clip = profil(VERL_D, CLIP_SPIEL, CLIP_OEFFNUNG, ro_clip(VERL_D))

    k = konus_hoehe(dw, VERL_D)
    z_boden = Z_OBEN - VERL_L
    z_mitte = Z_OBEN - VERL_L / 2
    band = CLIP_H + 2 * k + 8.0  # enges Band, grosszuegig um den Clip herum
    z_oben, z_unten = z_mitte + band / 2, z_mitte - band / 2

    with BuildPart() as p:
        add(prisma(p_weit, z_oben + k, STEG_D - (z_oben + k)))  # weit, oben
        add(konus(p_eng, z_oben, p_weit, z_oben + k))
        add(prisma(p_eng, z_unten, band))  # enges Band um den Clip
        add(konus(p_eng, z_unten, p_weit, z_unten - k))
        add(prisma(p_weit, z_boden, (z_unten - k) - z_boden))  # weit, unten
        add(prisma(p_clip, z_mitte - CLIP_H / 2, CLIP_H))
        add(boden_kegel(dw, z_boden))
    return p.part.moved(Location((0, y, 0)))


# --- Der Schluessel: haengt in einem Konus, gesichert durch einen Clip ------


def ro_kopf():
    return KOPF_D_MAX / 2 + KOPF_SPIEL + HUELSE_WAND


def schluessel_aufnahme():
    """Der Schluessel haengt an seinem eigenen Ratschenkopf. Achse bei x=0.

    ERSTER ENTWURF, VERWORFEN: ein Schulterring, auf dem der Kopf OBEN aufliegt.
    Geht nicht - ueber dem Ring sitzt der Kopf, dort kann also keine Huelse sein,
    und ohne Huelse darueber haengt der Ring in der Drucklage frei in der Luft.
    Genau der Auskrager, den die eiserne Regel verbietet.

    STATTDESSEN: der Kopf sinkt von oben in einen 45-Grad-KONUS und liegt mit
    seinem Rand darauf auf. Darueber laeuft eine weite Huelse (Bohrung 40), die den
    Kopf umschliesst - die traegt in der Drucklage alles ab. Der Konus verengt sich
    von der Kopfbohrung auf die Schaftbohrung, und zwar mit exakt 45 Grad, also
    stuetzfrei.

    Last und Sicherung sind getrennt (wie beim Rohrsteckschluessel): der KONUS
    traegt das ganze Gewicht, der CLIP am Schaft darunter sichert nur gegen
    Herausfallen nach vorn und darf leichtgaengig sein. Beide Maeuler sind weiter
    als der Kopf bzw. enger als der Schaft - eingelegt wird von vorn.
    """
    y = achse_y_kopf()

    p_kopf = profil(KOPF_D_MAX, KOPF_SPIEL, HUELSE_OEFFNUNG, ro_kopf())
    p_ring = profil(SCHAFT_D, SCHULTER_SPIEL, HUELSE_OEFFNUNG, SCHULTER_RO)
    p_clip = profil(SCHAFT_D, CLIP_SPIEL, CLIP_OEFFNUNG, ro_clip(SCHAFT_D))

    # 45 Grad: der Konus muss die groesste radiale Aenderung abdecken.
    d_ro = ro_kopf() - SCHULTER_RO
    d_ri = (KOPF_D_MAX / 2 + KOPF_SPIEL) - (SCHAFT_D / 2 + SCHULTER_SPIEL)
    k = max(d_ro, d_ri) + 1.0

    z_schulter = Z_OBEN - KOPF_L  # Unterkante Kopf: hier faengt der Konus an
    z_ring = z_schulter - k
    z_clip = z_ring - SCHULTER_D

    with BuildPart() as p:
        add(prisma(p_kopf, z_schulter, STEG_D - z_schulter))  # weite Huelse um den Kopf
        add(konus(p_ring, z_ring, p_kopf, z_schulter))  # 45 Grad - hier haengt er
        add(prisma(p_ring, z_clip, SCHULTER_D))  # kurzer Ring, fuehrt den Schaft
        add(prisma(p_clip, z_clip - CLIP_H, CLIP_H))  # Sicherung gegen Herausfallen
    return p.part.moved(Location((0, y, 0)))


def achse_y_kopf():
    """Achse des Schluessels.

    Ergibt sich aus der Kopfhuelse - und liegt damit von selbst weit genug vorn,
    dass der rote Verstellring (29,5, die dickste Stelle des Schluessels) unter dem
    Halter frei am Brett vorbeihaengt und nicht dagegenstoesst.
    """
    return -PLATTE_D - ro_kopf() + EINBETT


def schluessel_halter():
    breite = 2 * ro_kopf() + 2 * RAND
    with BuildPart() as teil:
        add(haken_profil(breite, H_SCHLUESSEL))
        add(schluessel_aufnahme().moved(Location((breite / 2, 0, 0))))
        add(gravur("1-25 Nm", breite / 2), mode=Mode.SUBTRACT)
    return teil.part


# --- Attrappen: NUR fuer Renderings, werden nie exportiert ------------------


def schluessel_attrappe():
    """Kopf (runde Scheibe), Schaft, roter Ring, Griff - nur fuers Bild."""
    z_kopf = Z_OBEN - KOPF_L / 2
    z_absatz = Z_OBEN - KOPF_L
    z_griff = z_absatz - KOPF_BIS_GRIFF
    z_rot = z_griff + 12.0  # Lage des roten Rings geschaetzt, nur fuers Bild

    with BuildPart() as p:
        with BuildSketch(Plane.XZ.offset(KOPF_DICK / 2)):
            with Locations((0, z_kopf)):
                Circle(KOPF_D_MAX / 2)
        extrude(amount=KOPF_DICK)
        with Locations(Location((0, 0, z_griff))):
            Cylinder(SCHAFT_D / 2, z_absatz - z_griff,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(Location((0, 0, z_rot - 12.0))):
            Cylinder(ROT_D / 2, 12.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(Location((0, 0, z_griff - GRIFF_L))):
            Cylinder(GRIFF_D / 2, GRIFF_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return p.part


def nuss_attrappe():
    """Nuss auf dem Zapfen: Koerper + Bitspitze, waagerecht nach vorn."""
    koerper = 20.0  # Laenge des geraendelten Teils - geschaetzt, nur fuers Bild
    with BuildPart() as p:
        with BuildSketch(Plane.XZ):
            Circle(NUSS_D / 2)
        extrude(amount=PLATTE_D + koerper)
        with BuildSketch(Plane.XZ.offset(-(PLATTE_D + koerper))):
            Circle(3.2)
        extrude(amount=NUSS_L - koerper)
    return p.part.moved(Location((0, 0, Z_ZAPFEN)))


def verlaengerung_attrappe():
    zb = Z_OBEN - VERL_L
    ende = 20.0  # geschaetzt, nur fuers Bild
    with BuildPart() as p:
        with Locations(Location((0, 0, zb))):
            Cylinder(VERL_D / 2, VERL_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(Location((0, 0, zb))):
            Cylinder(VERL_ENDE / 2, ende, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return p.part


# --- Gravur -----------------------------------------------------------------


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


# --- Die Teile --------------------------------------------------------------


def nuss_positionen(n):
    xs = [RAND + NUSS_D / 2 + i * NUSS_ABSTAND for i in range(n)]
    return xs, xs[-1] + NUSS_D / 2 + RAND


def nuss_leiste():
    """Alle elf Nuesse auf einer Leiste: Vierkantzapfen, waagerecht nach vorn."""
    xs, breite = nuss_positionen(len(BITS))
    with BuildPart() as teil:
        add(haken_profil(breite, H_NUESSE))
        for x in xs:
            add(zapfen().moved(Location((x, 0, Z_ZAPFEN))))
        for label, x in zip(BITS, xs):
            add(gravur(label, x), mode=Mode.SUBTRACT)
    return teil.part


def verlaengerung_halter():
    dw = VERL_ENDE + ENDE_RESERVE
    breite = 2 * ro_huelse(dw) + 2 * RAND
    with BuildPart() as teil:
        add(haken_profil(breite, H_VERL))
        add(verlaengerung_aufnahme().moved(Location((breite / 2, 0, 0))))
        add(gravur("Verl", breite / 2), mode=Mode.SUBTRACT)
    return teil.part


def testclip_zapfen():
    """Drei Zapfen mit gestaffeltem Vierkant. Nuss aufstecken, den passenden waehlen.

    Die Passung ist der einzige unbekannte Wert am ganzen Teil - und der einzige,
    den ein Bild nicht zeigt und ein Messschieber schlecht trifft. Also drucken.
    """
    xs, breite = nuss_positionen(len(PASSUNGEN))
    with BuildPart() as teil:
        add(haken_profil(breite, H_NUESSE))
        for a, x in zip(PASSUNGEN, xs):
            add(zapfen(a).moved(Location((x, 0, Z_ZAPFEN))))
        for a, x in zip(PASSUNGEN, xs):
            add(gravur(f"{a:.2f}", x), mode=Mode.SUBTRACT)
    return teil.part


def testclip_verlaengerung():
    return verlaengerung_halter()


def masse():
    print(f"Vierkant   {VIERKANT:.2f} mm (am Testclip ermittelt, 2 Runden)")
    print(f"Zapfen     {ZAPFEN_FREI:.0f} mm frei, Achse {abs(Z_ZAPFEN):.0f} mm unter der Kante")
    print(f"Nuss       Ø {NUSS_D:.2f} x {NUSS_L:.0f} mm, 11x identisch, Raster {NUSS_ABSTAND:.0f} mm")
    dw = VERL_ENDE + ENDE_RESERVE
    print(f"Verl       Ø {VERL_D:.2f}, Ende {VERL_ENDE:.2f} -> weit {dw:.2f},"
          f" Konus {konus_hoehe(dw, VERL_D):.1f}, Huelse {2 * ro_huelse(dw):.1f}")
    print()


def tests_bauen():
    print(f"Testclips - Klemmkanal {KLEMMKANAL:.0f} mm\n")

    teil = testclip_zapfen()
    # Name traegt die Passungen: sonst verwechselt man die Runden im Slicer.
    stempel = "_".join(f"{a:.2f}".replace(".", "") for a in PASSUNGEN)
    ziel = schreibe(teil, f"testclip_zapfen_{stempel}", AUSGABE)
    xs, breite = nuss_positionen(len(PASSUNGEN))
    print(f"  Zapfen    {', '.join(f'{a:.2f}' for a in PASSUNGEN)} mm"
          f" -> welcher haelt die Nuss?")
    render(
        [(teil, HALTER)]
        + [(nuss_attrappe().moved(Location((xs[0], 0, 0))), STAHL)]
        + [(brett(breite, 15), HOLZ)],
        f"{ziel}.png",
        titel="testclip_zapfen — 6,10 / 6,25 / 6,40",
    )
    print()

    teil = testclip_verlaengerung()
    ziel = schreibe(teil, "testclip_verl", AUSGABE)
    dw = VERL_ENDE + ENDE_RESERVE
    breite = 2 * ro_huelse(dw) + 2 * RAND
    render(
        [
            (teil, HALTER),
            (verlaengerung_attrappe().moved(Location((breite / 2, achse_y(dw), 0))), STAHL),
            (brett(breite, 15), HOLZ),
        ],
        f"{ziel}.png",
        titel="testclip_verl",
    )
    print()


def bauen():
    teil = nuss_leiste()
    ziel = schreibe(teil, "halter_nuesse", AUSGABE)
    xs, breite = nuss_positionen(len(BITS))
    nuesse = [nuss_attrappe().moved(Location((x, 0, 0))) for x in xs]
    render(
        [(teil, HALTER)] + [(n, STAHL) for n in nuesse] + [(brett(breite), HOLZ)],
        f"{ziel}.png",
        titel=f"halter_nuesse — {', '.join(BITS)}",
    )
    print()

    teil = verlaengerung_halter()
    ziel = schreibe(teil, "halter_verlaengerung", AUSGABE)
    dw = VERL_ENDE + ENDE_RESERVE
    breite = 2 * ro_huelse(dw) + 2 * RAND
    print(f"  haengt    {abs(Z_OBEN - VERL_L - BODEN_D):.0f} mm unter die Brettoberkante")
    render(
        [
            (teil, HALTER),
            (verlaengerung_attrappe().moved(Location((breite / 2, achse_y(dw), 0))), STAHL),
            (brett(breite, 15), HOLZ),
        ],
        f"{ziel}.png",
        titel="halter_verlaengerung",
    )
    print()

    teil = schluessel_halter()
    ziel = schreibe(teil, "halter_schluessel", AUSGABE)
    breite = 2 * ro_kopf() + 2 * RAND
    haengt = abs(Z_OBEN - KOPF_L) + (SCHLUESSEL_L - KOPF_L)
    print(f"  haengt    {haengt:.0f} mm unter die Brettoberkante (Schluessel frei)")
    render(
        [
            (teil, HALTER),
            (schluessel_attrappe().moved(Location((breite / 2, achse_y_kopf(), 0))), STAHL),
            (brett(breite, 15), HOLZ),
        ],
        f"{ziel}.png",
        titel="halter_schluessel",
    )
    print()


if __name__ == "__main__":
    import sys

    masse()
    tests_bauen() if "test" in sys.argv else bauen()
