#!/usr/bin/env python
"""
Zentrales Baukommando fuer alle Wandhalter.

    ./.venv/bin/python bauen.py                       alle Halter
    ./.venv/bin/python bauen.py rohrsteckschluessel   nur diesen
    ./.venv/bin/python bauen.py rohrsteckschluessel --test    nur die Testclips
    ./.venv/bin/python bauen.py --liste               was es gibt

Ein Halter ist ein Ordner  halter/<name>/  mit einer  modell.py , die
    TITEL    einen Klartextnamen
    bauen()  baut und exportiert alles
und optional
    tests_bauen()  baut die Testclips
bereitstellt. Mehr braucht es nicht - neue Halter werden automatisch gefunden.

Die Dateien landen in  halter/<name>/druck/  (STL, 3MF, STEP, PNG).
"""

import importlib
import sys
from pathlib import Path

WURZEL = Path(__file__).parent
HALTER = WURZEL / "halter"


def gefunden():
    return sorted(p.name for p in HALTER.iterdir() if (p / "modell.py").exists())


def lade(name):
    return importlib.import_module(f"halter.{name}.modell")


def main(argv):
    namen = gefunden()
    test = "--test" in argv
    args = [a for a in argv if not a.startswith("-")]

    if "--liste" in argv:
        print(f"Halter in {HALTER}:\n")
        for n in namen:
            print(f"  {n:24} {getattr(lade(n), 'TITEL', '')}")
        return 0

    ziel = args or namen
    unbekannt = [n for n in ziel if n not in namen]
    if unbekannt:
        print(f"Unbekannt: {', '.join(unbekannt)}\nVorhanden: {', '.join(namen)}")
        return 1

    for n in ziel:
        m = lade(n)
        print(f"\n=== {n} — {getattr(m, 'TITEL', '')}\n")
        if hasattr(m, "masse"):
            m.masse()
        if test:
            if not hasattr(m, "tests_bauen"):
                print("  (keine Testclips definiert)")
                continue
            m.tests_bauen()
        else:
            m.bauen()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
