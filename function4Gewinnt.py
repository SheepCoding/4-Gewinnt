"""
4-Gewinnt gegen einen Computerspieler
    - alle Funktionen
    - spielbar auf Console (Spieler "O", Computer "X")
    _ KI eingeschränkt
        --> defensive Spielweise ohne Minimax-Algorithmus
        --> nicht vorausschauend
"""

'''--- Importe ---------------------------------------------------------------------------------------------------- '''
import random

'''
 Datenstruktur für ein Spielfeld
   Liste von 7 Spalten
   jede Spalte enthält max 6 Steine, also eine Liste von 6 Zeilen

   Spalte , Zeile

   0,0    1,0    2,0    3,0    4,0    5,0    6,0
   0,1    1,1    2,1    3,1    4,1    5,1    6,1
   0,2    1,2    2,2    3,2    4,2    5,2    6,2
   0,3    1,3    2,3    3,3    4,3    5,3    6,3
   0,4    1,4    2,4    3,4    4,4    5,4    6,4
   0,5    1,5    2,5    3,5    4,5    5,5    6,5

   SpielFeld [0] - ganz linke Spalte
   SpielFeld [6] - ganz rechte Spalte

   SpielFeld [0] [0] - ganz linke Spalte, oberste Zeile
   SpielFeld [0] [5] - ganz linke Spalte, unterste Zeile

 Terminologie:
   feld: ganzes Spielfeld
   zelle: ein Platz im Spielfeld
'''


def spielfeldPrint(feld: list):
    """
     Zweck:
       Ausgabe der Daten (Read), also des Spielfeldes
     Parameter:
       Spielfeld Datenstruktur
     Rückgabe: Nichts
    """
    # gehe durch alle Zeilen
    for z in range(0, 6):
        zeile = ""
        # gehe durch alle Spalten
        for s in range(0, 7):
            zeile += feld[s][z]

        print(zeile)
    print()


def spielfeldInit() -> list:
    """
     Zweck:
       Neues Anlegen der Daten, also eines Spielfeldes (Create)
     Parameter: Nichts
     Rückgabe:
       Spielfeld Datenstruktur
    """
    # neue liste
    feld = []
    # breite = 7
    for s in range(0, 7):
        # spalte neu erzeugen
        spalte = []
        # höhe = 6
        for z in range(0, 6):
            # an liste spalte ein neues element dran hängen
            spalte.append(".")
        feld.append(spalte)
    return feld


# Anlegen eines Testspielfeldes
def testSpielfeldInit() -> list:
    # neue liste
    feld = []

    spalte1 = [".", ".", ".", ".", "X", "O"]
    feld.append(spalte1)

    spalte2 = [".", ".", ".", ".", "O", "X"]
    feld.append(spalte2)

    spalte3 = [".", ".", ".", ".", "O", "X"]
    feld.append(spalte3)

    spalte4 = [".", "X", "O", "O", "X", "X"]
    feld.append(spalte4)

    spalte5 = [".", ".", ".", ".", ".", "O"]
    feld.append(spalte5)

    spalte6 = [".", ".", ".", ".", ".", "."]
    feld.append(spalte6)

    spalte7 = [".", ".", ".", ".", ".", "."]
    feld.append(spalte7)

    '''
    spalte1 = [".", ".", ".", ".", "X", "O"]
    feld.append(spalte1)

    spalte2 = [".", ".", ".", ".", "O", "X"]
    feld.append(spalte2)

    spalte3 = [".", ".", "X", "O", "O", "X"]
    feld.append(spalte3)

    spalte4 = [".", ".", ".", "O", "X", "X"]
    feld.append(spalte4)

    spalte5 = [".", ".", ".", ".", ".", "O"]
    feld.append(spalte5)

    spalte6 = [".", ".", ".", ".", ".", "."]
    feld.append(spalte6)

    spalte7 = [".", ".", ".", ".", ".", "."]
    feld.append(spalte7)
    '''
    return feld


def steinSpielen(feld: list, spalte: int, farbe: str) -> list:
    """
     Zweck:
       Einen Stein in eine bestimmte Spalte werfen
       - von unten beginnend gucken, ob eine Zelle frei ist
       - Stein wird in die erste freie Zelle geschrieben
     Parameter:
       feld:     das Spielfeld
       spalte:   Spalte zwischen 0 und 6, von links beginnend, in die der Stein geworfen wird
       farbe:    der gespielte Stein ("X" oder "O")
     Rückgabe:
       Spielfeld Datenstruktur mit neuem Stein an der richtigen stelle
    """
    # Suche von unten die erste freie Zelle in der Spalte und speichere dort den Stein
    z = 5
    while z >= 0:
        if feld[spalte][z] == ".":
            feld[spalte][z] = farbe
            break
        else:
            z = z - 1
    return feld


def spalteNichtVoll(feld: list, spalte: int) -> bool:
    """
     Zweck
       feststellen, ob in Spalte noch gespielt werden kann
     Parameter
       feld:   Spielfeld
       spalte: wohin gespielt werden soll
     Rückgabe
       True, wenn in Spalte gespielt werden kann
    """
    return feld[spalte][0] == "."


def kannSteinSpielen(feld: list, position: list) -> bool:
    """
     Zweck
       feststellen, ob Stein an bestimmte Position gespielt werden kann
     Parameter
       feld:   Spielfeld
       position: wohin gespielt werden soll [spalte, zeile]
     Rückgabe
       True, wenn an Position gespielt werden kann
    """
    spalte = position[0]
    zeile = position[1]
    # Prüfe, ob Zelle noch auf Feld ist
    if nochAufFeld(spalte, zeile):
        # Prüfe, ob Zelle leer ist und darunterliegende Zelle voll bzw. Zelle ganz unten ist
        if (feld[spalte][zeile] == ".") and ((zeile == 5) or (feld[spalte][zeile + 1] != ".")):
            return True
        else:
            return False
    else:
        return False


def pruefeEingabeSpieler(feld: list, eingabe: str) -> int:
    """
    Zweck:
        Überprüfung der Eingabe des Spielers (spielbare Spalte)
    Parameter:
        feld: Spielfeld
        eingabe: Eingabe des Spielers
    Rückgabe:
        spielbare Spalte
        -1 , wenn fehlerhafte Eingabe
    """
    # prüfen, ob die spalte gültig ist
    # - muss eine zahl sein
    # - muss zwischen 1 .. 7 liegen
    # - wenn nicht, rückgabe: -1
    # prüfen, ob das feld spielbar ist
    # - wenn nicht, rückgabe: -1
    # - wenn ja, rückgabe: eingabe

    # Prüfe, ob Eingabe eine Zahl ist
    try:
        spalte = int(eingabe)

        # wenn ja, prüfe, ob sie 1..7 liegt
        if 0 < spalte < 8:
            # spalten werden intern 0 .. 6 gezählt
            # 0: links
            spalte = spalte - 1
            # Prüfe, Stein spielbar ist
            spielbar = spalteNichtVoll(feld, spalte)
            if spielbar:
                return spalte
        return -1
    except:
        return -1


def eingabeSpieler(feld: list) -> int:
    """
    Zweck:
        Nach Eingabe des Spielers fragen und auswerten
    Parameter:
        feld: Spielfeld
    Rückgabe:
        -1 , wenn Spieler nicht mehr spielen will
        gewählte gültige Spalte
    """
    spalte = -1
    # Solange der Spieler spielen will, und noch keine gültige Spalte gewählt hat
    # frage nach neuer Eingabe
    while spalte == -1:
        # spieler bitten, eine spalte ein zu geben
        eingabe = input("welche Spalte möchten Sie spielen (1 .. 7): ")

        # Spieler hat keine Lust mehr
        if eingabe == "":
            return -1
        else:
            # Leerzeichen aus Eingabe löschen
            eingabe = eingabe.replace(" ", "")
            # Prüfe Eingabe
            # Rückgabe: -1 bei Fehler, sonst Spalte
            spalte = pruefeEingabeSpieler(feld, eingabe)
    # Spieler hat gültige Spalte gewählt
    return spalte


def eingabeComputer(feld: list, computerFarbe: str, spielerFarbe: str) -> int:
    """
     Zweck:
        Computer spielt einen Zug
     Parameter
        feld:   Spielfeld
        computerFarbe:  Farbe der Steine vom Computer
        spielerFarbe: Farbe der Steine vom Spieler
     Rückgabe
        Spalte, in die gespielt werden soll
    """
    # finde besten Zug
    spalte = findeBestenZug(feld, computerFarbe, spielerFarbe)
    if spalte != -1:
        return spalte
    # wenn kein guten Zug gefunden, wähle zufälligen Zug
    else:
        return zufallsSpalte(feld)


def zufallsSpalte(feld: list) -> int:
    """
    Zweck:
        Finde zufällige Spalte, in der man ein Stein spielen kann
    Parameter:
        feld: Spielfeld
    Rückgabe:
        ermittelte Spalte
    """
    # wähle zufällige Spalte
    spalte = random.randint(0, 6)
    # prüfen, ob das feld spielbar ist
    # - wenn nicht, neue zufallszahl
    # - rückgabe der spalte
    while not (spalteNichtVoll(feld, spalte)):
        spalte = random.randint(0, 6)
    return spalte


def FeldVoll(feld):
    """
     Zweck
        feststellen, ob das ganze spielfeld voll ist
     Parameter
       feld:   Spielfeld
     Rückgabe
       True, wenn das feld voll ist
    """
    # wenn KannSteinSpielen () nirgends mehr erfüllt ist, dann ist das feld voll

    # erste linke Spalte bis zur letzten Spalte
    s = 0
    while s < 7:
        # Prüfen, ob Spalte voll ist
        spielbar = spalteNichtVoll(feld, s)
        if spielbar:
            # feld noch nicht voll
            return False
        # weiter zählen
        s = s + 1
    # kann nirgendwo hin spielen
    return True


def nebeneinanderReihe(reihe: list, farbe: str, anzahl: int) -> int:
    """
    Zweck:
        Prüfen, ob eine bestimmte Anzahl an Steinen nebeneinander in der Reihe sind
    Parameter:
        reihe: eine Zeile oder Spalte als Liste
        farbe: Farbe der Steine
        anzahl: gewünschte Anzahl der Steine, die nebeneinander sind
    Rückgabe:
        Spalte, in der der letzte Stein der zusammenhängenden Steine liegt
        -1 wenn nichts gefunden wurde
    """
    zaehler = 0  # Zähler der Steine nebeneinander
    i = 0
    laenge = len(reihe)
    while i < laenge and zaehler < anzahl:
        # wenn richtige Farbe gefunden, Zähler erhöhen
        if reihe[i] == farbe:
            zaehler = zaehler + 1
        # wenn falsche Farbe, Zähler zurück setzen
        else:
            zaehler = 0
        i = i + 1
    if zaehler >= anzahl:
        # Stelle, in der der letzte Stein der zusammenhängenden Steine liegt
        # i geht eine Stelle weiter, bevor die while-Schleife abbricht
        return i - 1
    else:
        return -1


def nochAufFeld(spalte: int, zeile: int) -> bool:
    """
    Zweck:
        Prüfen, ob übergebene Zelle noch auf Spielfeld ist
    Parameter:
        spalte: Spalte, der übergebenen Zelle
        zeile: Zeile, der übergebenen Zelle
    Rückgabe:
        True: wenn übergebene Zelle noch auf Spielfeld
    """
    # Prüfen, ob übergebene Zelle noch auf Spielfeld ist
    return (0 <= spalte <= 6) and (0 <= zeile <= 5)


def nebeneinanderDiagonale(feld: list, farbe: str, anzahl: int) -> list:
    """
    Zweck:
        Prüfen, ob eine bestimmte Anzahl an Steinen nebeneinander in einer Diagonalen sind
    Parameter:
        feld: Spielfeld
        farbe: Farbe der Steine
        anzahl: gewünschte Anzahl der Steine, die nebeneinander sind
    Rückgabe:
        Liste aus [Spalte, Zeile, Richtung] Position und Richtung, in der die Diagonalen enden
            "l" - Diagonale von links oben, "r" - Diagonale von rechts oben
        [] - wenn gesuchte Anzahl an Steinen nicht nebeneinander sind
    """
    # Prüfe alle Diagonalen, in der 4 Steine nebeneinander liegen könnten
    # es gibt 12:
    #   6 von links oben nach rechts unten --> Diagonale links
    #   6 von rechts oben nach links unten --> Diagonale rechts
    # Startpositionen von Diagonale links: [0,2], [0,1], [0,0], [1,0], [2,0], [3,0]
    # Startpositionen von Diagonale rechts: [6,2], [6,1], [6,0], [5,0], [4,0], [3,0]

    # Setze Startpositionen von Diagonale links
    startPosDiagLinks = [[0, 2], [0, 1], [0, 0], [1, 0], [2, 0], [3, 0]]

    # Setze Startpositionen von Diagonale rechts
    startPosDiagRechts = [[6, 2], [6, 1], [6, 0], [5, 0], [4, 0], [3, 0]]

    # Lege leere Rückgabeliste an
    rueckListe = []

    # Gehe durch alle Diagonalen links
    for i in range(6):
        # Setze spalte und zeile auf die Startposition der i. Diagonale
        spalte = startPosDiagLinks[i][0]
        zeile = startPosDiagLinks[i][1]
        # setze Zähle zurück
        zaehler = 0

        # gehe, solange das Feldende noch nicht erreicht
        # und die gewünschte Anzahl nebeneinander noch nicht gefunden wurde, durch die Diagonale
        while nochAufFeld(spalte, zeile) and (zaehler < anzahl):
            # Wenn Feld richtige Farbe hat, setze Zähler hoch
            if feld[spalte][zeile] == farbe:
                zaehler = zaehler + 1
            # sonst setze Zähler zurück auf 0
            else:
                zaehler = 0

            # gehe auf nächstes Feld der Diagonalen
            spalte = spalte + 1
            zeile = zeile + 1

        # Wenn Diagonale mit gewünschter Anzahl gefunden wurde, füge Endposition und Art an Rückgabeliste an
        if zaehler == anzahl:
            rueckListe.append([spalte - 1, zeile - 1, "l"])

    # Gehe durch alle Diagonalen rechts
    for i in range(6):
        # Setze spalte und zeile auf die Startposition der i. Diagonale
        spalte = startPosDiagRechts[i][0]
        zeile = startPosDiagRechts[i][1]
        # setze Zähle zurück
        zaehler = 0

        # gehe, solange das Feldende noch nicht erreicht
        # und die gewünschte Anzahl nebeneinander noch nicht gefunden wurde, durch die Diagonale
        while nochAufFeld(spalte, zeile) and (zaehler < anzahl):
            # Wenn Feld richtige Farbe hat, setze Zähler hoch
            if feld[spalte][zeile] == farbe:
                zaehler = zaehler + 1
            # sonst setze Zähler zurück auf 0
            else:
                zaehler = 0

            # gehe auf nächstes Feld der Diagonalen
            spalte = spalte - 1
            zeile = zeile + 1

        # Wenn Diagonale mit gewünschter Anzahl gefunden wurde, füge Endposition und Art an Rückgabeliste an
        if zaehler == anzahl:
            rueckListe.append([spalte + 1, zeile - 1, "r"])

    # Rückgabe der Liste aller gefundenen Diagonalen
    return rueckListe


def schonGewonnen(feld: list, position: list, farbe: str) -> bool:
    """
    Zweck:
        Prüfen, ob schon übergebene Farbe gewonnen hat (4 in einer Reihe)
    Parameter:
        feld: Spielfeld
        position: [Spalte, Zeile] des letzten gesetzten Steins
        farbe: Farbe des letzten Steins
    Rückgabe:
        True: wenn gewonnen
    """
    spalte = feld[position[0]]
    # wenn in der Spalte 4 nebeneinander sind
    if nebeneinanderReihe(spalte, farbe, 4) > -1:
        return True
    else:
        # eine Zeile aus dem Feld in Liste Zeile speichern
        zeile = []
        for s in range(7):
            zeile.append(feld[s][position[1]])
        # wenn in der Zeile 4 nebeneinander sind
        if nebeneinanderReihe(zeile, farbe, 4) > -1:
            return True
        else:
            # Wenn in einer Diagonalen 4 nebeneinander sind
            if nebeneinanderDiagonale(feld, farbe, 4):
                return True
            else:
                return False


def findeLetztenStein(feld: list, spalte: int, farbe: str) -> list:
    """
    Zweck:
        Finde die genaue Position des letzten gespielten Steins
    Parameter:
        feld: Spielfeld
        spalte: letzte gespielte Spalte
        farbe:  Farbe des Steins
    Rückgabe:
        [Spalte, Zeile] Position des letzten gespielten Steins
    """
    zeile = 0
    # gehe von oben durch die Spalte und suche Stein in der Farbe
    while feld[spalte][zeile] != farbe:
        zeile = zeile + 1
    return [spalte, zeile]


def diagonaleVerlaengern(feld: list, diagonalEnde: list, laenge: int) -> int:
    """
    Zweck:
        Prüfen, ob die Diagonale verlängerbar ist
    Parameter:
        feld: Spielfeld
        diagonalEnde: Position in der die Diagonale endet
        laenge: Länge der Diagonale
    Rückgabe:
        Spalte, mit der die Diagonale verlängert werden kann
        -1 wenn Diagonale nicht verlängerbar
    """
    position = [-1, -1]
    # wenn Diagonale von links oben nach rechts unten geht
    if diagonalEnde[2] == "l":
        # Gehe zum unteren Ende der Diagonalen
        position[0] = diagonalEnde[0] + 1
        position[1] = diagonalEnde[1] + 1
        # Prüfe, ob Stein spielbar ist
        if kannSteinSpielen(feld, position):
            # Rückgabe Spalte
            return position[0]
        else:
            # Gehe zum oberen Ende der Diagonalen
            position[0] = diagonalEnde[0] - laenge
            position[1] = diagonalEnde[1] - laenge
            # Prüfe, ob Stein spielbar ist
            if kannSteinSpielen(feld, position):
                # Rückgabe Spalte
                return position[0]

    # wenn Diagonale von rechts oben nach links unten geht
    elif diagonalEnde[2] == "r":
        # Gehe zum unteren Ende der Diagonalen
        position[0] = diagonalEnde[0] - 1
        position[1] = diagonalEnde[1] + 1
        # Prüfe, ob Stein spielbar ist
        if kannSteinSpielen(feld, position):
            # Rückgabe Spalte
            return position[0]
        else:
            # Gehe zum anderen Ende der Diagonalen
            position[0] = diagonalEnde[0] + laenge
            position[1] = diagonalEnde[1] - laenge
            # Prüfe, ob Stein spielbar ist
            if kannSteinSpielen(feld, position):
                # Rückgabe Spalte
                return position[0]

    # Diagonale ist nicht verlängerbar

    return -1


def findeSpalte(feld: list, farbe: str, anzahl: int) -> int:
    """
    Zweck:
        Finde Spalte, in der die übergebene Anzahl an Steine in der Farbe nebeneinander sind
    Parameter:
        feld: Spielfeld
        farbe: Farbe der Steine
        anzahl: Anzahl der nebeneinander liegenden Steine
    Rückgabe:
        ermittelte Spalte
        -1 - keine Spalte gefunden
    """
    # gehe durch alle Spalten
    for s in range(7):
        spalte = feld[s]
        # letzte Zeile, wo 3 nebeneinander liegen
        posZeile = nebeneinanderReihe(spalte, farbe, anzahl)
        if posZeile > -1:
            # Prüfe, ob man Stein darüber setzen kann
            if kannSteinSpielen(feld, [s, posZeile - anzahl]):
                return s
    return -1


def findeZeile(feld: list, farbe: str, anzahl: int) -> int:
    """
    Zweck:
        Finde Zeile, in der die übergebene Anzahl an Steine in der Farbe nebeneinander sind
    Parameter:
        feld: Spielfeld
        farbe: Farbe der Steine
        anzahl: Anzahl der nebeneinander liegenden Steine
    Rückgabe:
        Spalte, in der man die Zeile verlängern kann
        -1 - keine Spalte gefunden
    """
    # gehe durch alle Zeilen
    for z in range(6):
        # eine Zeile aus dem Feld in Liste Zeile speichern
        zeile = []
        for s in range(6):
            zeile.append(feld[s][z])
        # posSpalte = Spalte, wo 3. Stein nebeneinander liegt
        posSpalte = nebeneinanderReihe(zeile, farbe, anzahl)
        if posSpalte > -1:
            # Prüfe, ob man Stein dahinter setzen kann
            if kannSteinSpielen(feld, [posSpalte + 1, z]):
                return posSpalte + 1
            else:
                # Prüfe, ob man Stein davor setzen kann
                if kannSteinSpielen(feld, [posSpalte - anzahl, z]):
                    print()
                    return posSpalte - anzahl
    return -1


def findeDiagonale(feld: list, farbe: str, anzahl: int) -> int:
    """
    Zweck:
        Finde Diagonale, in der die übergebene Anzahl an Steine in der Farbe nebeneinander sind
        und verlängerbar ist
    Parameter:
        feld: Spielfeld
        farbe: Farbe der Steine
        anzahl: Anzahl der nebeneinander liegenden Steine
    Rückgabe:
        Spalte, in der man die Diagonale verlängern kann
        -1 - keine Spalte gefunden
    """
    # Suche alle Diagonalen-Enden, die die entsprechende Farbe und Länge besitzen
    diagonalEndeListe = nebeneinanderDiagonale(feld, farbe, anzahl)
    # gehe durch alle gefundenen Diagonalen
    for i in range(len(diagonalEndeListe)):
        # Prüfe, wo man Diagonale verlängern kann
        spalte = diagonaleVerlaengern(feld, diagonalEndeListe[i], anzahl)
        if spalte != -1:
            return spalte
    return -1


def findeBestenZug(feld: list, eigeneFarbe: str, gegnerFarbe: str) -> int:
    """
    Zweck:
        Finde beste Spalte, um einen Stein zu setzen
    Parameter:
        feld: Spielfeld
        eigeneFarbe: Farbe der eigenen Steine
        gegnerFarbe: Farbe der gegnerischen Steine
    Rückgabe:
        ermittelte Spalte
        -1 - wenn es keine gute Spalte gab
    """

    ''' Prüfe, ob es 3 Steine der eigenen Farbe nebeneinander gibt (Spalte, Zeile, Diagonale)
         --> setzen und gewinnen
    '''
    # Prüfe, ob es eine Spalte mit 3 Steinen der eigenen Farbe zum Verlängern gibt
    spalte = findeSpalte(feld, eigeneFarbe, 3)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Zeile mit 3 Steinen der eigenen Farbe zum Verlängern gibt
    spalte = findeZeile(feld, eigeneFarbe, 3)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Diagonale mit 3 Steinen der eigenen Farbe zum Verlängern gibt
    spalte = findeDiagonale(feld, eigeneFarbe, 3)
    if spalte != -1:
        return spalte

    ''' Prüfe, ob es 3 Steine der gegnerischen Farbe nebeneinander gibt (Spalte, Zeile, Diagonale)
        --> setzen und gewinnen des Gegners verhindern
    '''
    # Prüfe, ob es eine Spalte mit 3 Steinen der gegnerischen Farbe zum Verhindern gibt
    spalte = findeSpalte(feld, gegnerFarbe, 3)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Zeile mit 3 Steinen der gegnerischen Farbe zum Verhindern gibt
    spalte = findeZeile(feld, gegnerFarbe, 3)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Diagonale mit 3 Steinen der gegnerischen Farbe zum Verhindern gibt
    spalte = findeDiagonale(feld, gegnerFarbe, 3)
    if spalte != -1:
        return spalte

    ''' Prüfe, ob es 2 Steine der gegnerischen Farbe nebeneinander gibt (Spalte, Zeile, Diagonale)
        --> setzen und verhindern, dass der Gegner 3 nebeneinander bekommt
    '''
    # Prüfe, ob es eine Spalte mit 2 Steinen der gegnerischen Farbe zum Verhindern gibt
    spalte = findeSpalte(feld, gegnerFarbe, 2)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Zeile mit 2 Steinen der gegnerischen Farbe zum Verhindern gibt
    spalte = findeZeile(feld, gegnerFarbe, 2)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Diagonale mit 2 Steinen der gegnerischen Farbe zum Verhindern gibt
    spalte = findeDiagonale(feld, gegnerFarbe, 2)
    if spalte != -1:
        return spalte

    ''' Prüfe, ob es 2 Steine der eigenen Farbe nebeneinander gibt (Diagonale, Spalte, Zeile)
     --> setzen und selber 3 nebeneinander bekommen
    '''
    # Prüfe, ob es eine Spalte mit 2 Steinen der eigenen Farbe zum Verlängern gibt
    spalte = findeSpalte(feld, eigeneFarbe, 2)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Zeile mit 2 Steinen der eigenen Farbe zum Verlängern gibt
    spalte = findeZeile(feld, eigeneFarbe, 2)
    if spalte != -1:
        return spalte

    # Prüfe, ob es eine Diagonale mit 2 Steinen der eigenen Farbe zum Verlängern gibt
    spalte = findeDiagonale(feld, eigeneFarbe, 2)
    if spalte != -1:
        return spalte

    # wenn keine Spalte gefunden
    return -1


def spielen(test=False):
    """
    Zweck:
        Spiel auf Python-Konsole spielen
    Parameter:
        test: optional -> True -> nur wenn ein Testspielfeld benutzt werden soll
    Rückgabe: keine
    """

    # neues spielfeld
    if test:
        spielFeld = testSpielfeldInit()
    else:
        spielFeld = spielfeldInit()
    # Spielfeld anzeigen
    spielfeldPrint(spielFeld)

    # Spielerfarben festlegen
    spielerFarbe = "O"
    computerFarbe = "X"

    # Schleife bis Spiel beendet ist
    while True:
        # Spieler zieht einen Stein (farbe)
        spalte = eingabeSpieler(spielFeld)

        # wenn Spieler keine Lust mehr hat -> beenden
        if spalte == -1:
            print("Spiel beendet.")
            # raus aus der while schleife
            break
        # Stein spielen
        else:
            spielFeld = steinSpielen(spielFeld, spalte, spielerFarbe)

        # Spielfeld anzeigen
        spielfeldPrint(spielFeld)

        # gerade gespielte Position ermitteln
        position = findeLetztenStein(spielFeld, spalte, spielerFarbe)

        # Prüfen, ob Spieler gewonnen hat --> Ausgabe: gewonnen + Spiel beenden
        if schonGewonnen(spielFeld, position, spielerFarbe):
            print("Du hast gewonnen!")
            print("Spalte: " + str(position[0] + 1))
            break

        # Prüfen, ob Spielfeld voll ist --> Ausgabe: unentschieden + Spiel beenden
        if FeldVoll(spielFeld):
            print("Unentschieden")
            break

        # Computer zieht einen Stein
        print("Der Computer ist dran.")
        # beste Spalte wählen
        spalte = eingabeComputer(spielFeld, computerFarbe, spielerFarbe)
        # Stein spielen
        spielFeld = steinSpielen(spielFeld, spalte, computerFarbe)

        # Spielfeld anzeigen
        spielfeldPrint(spielFeld)

        # gerade gespielte Position ermitteln
        position = findeLetztenStein(spielFeld, spalte, computerFarbe)
        print("Spalte: " + str(position[0] + 1))

        # Prüfen, ob Computer gewonnen hat --> Ausgabe: verloren + Spiel beenden
        if schonGewonnen(spielFeld, position, computerFarbe):
            print("Der Computer hat gewonnen und du hast verloren!")
            print("Spalte: " + str(position[0] + 1))
            break

        # Prüfen, ob Spielfeld voll ist --> Ausgabe: unentschieden + Spiel beenden
        if FeldVoll(spielFeld):
            print("Unentschieden")
            break
