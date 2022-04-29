"""
4-Gewinnt gegen einen Computerspieler mit GUI
    - GUI mit TkInter
    - Spieler rot
    - Computer gelb
"""

'''--- Importe ---------------------------------------------------------------------------------------------------- '''

# graphisch Oberfläche
from tkinter import *
# benötigt, um ButtonClick-Events mit Parameterübergabe zu realisieren
from functools import partial
# Datei mit eigenen Funktionen
import function4Gewinnt

''' --- globale Variablen ----------------------------------------------------------------------------------------- '''

# Position des letzten belegten Feldes (Spalte, Zeile)
letztesBelegteFeld = [-1, -1]
# Datenstruktur für ein Spielfeld
# 2-dim Liste von 7 Spalten und 6 Zeilen
spielListe = function4Gewinnt.spielfeldInit()

''' --- Funktionen ------------------------------------------------------------------------------------------------ '''


def buttonsDeaktivieren():
    """
    Zweck:
        deaktiviert die Spalten-Buttons und den "Zug beendet"-Button
    Parameter: keine
    Rückgabe: keine
    """
    # Spalten-Buttons deaktivieren
    for s in range(7):
        spaltenButton[s].config(state=DISABLED)
    # Zug beendet Button deaktivieren
    zugBeendetButton.config(state=DISABLED)


'''--- Button-Funktionen ------------------------------------------------------------------------------------------ '''


def zugBeendetClick():
    """
    Zweck:
        wenn "Zug beendet"-Button betätigt wird,
            wird der Zug des Spielers ausgewertet,
            der Computerspieler macht seinen Zug
            und der Zug des Computers wird ausgewertet
    Parameter: keine
    Rückgabe: keine
    """
    global letztesBelegteFeld, spielListe
    # Testen, ob der Spieler gesetzt hat
    # wenn nicht gesetzt, dann Fehlermeldung
    if letztesBelegteFeld == [-1, -1]:
        ausgabeLabel.config(text="Du hast noch nicht gesetzt!")
    else:
        # Auswerten, was Spieler getan

        # Zug in Datenstruktur spielListe eintragen
        spielListe = function4Gewinnt.steinSpielen(spielListe, letztesBelegteFeld[0], "S")

        # Auswertung, ob Spiel beendet (Spieler gewonnen oder Spielfeld voll)
        # Prüfen, ob Spieler gewonnen hat
        if function4Gewinnt.schonGewonnen(spielListe, letztesBelegteFeld, "S"):
            # Buttons deaktivieren und Ausgabe
            buttonsDeaktivieren()
            ausgabeLabel.config(text="Du hast gewonnen!")
            return
        # Prüfen, ob Spielfeld voll ist
        if function4Gewinnt.FeldVoll(spielListe):
            # Buttons deaktivieren und Ausgabe
            buttonsDeaktivieren()
            ausgabeLabel.config(text="Unentschieden")
            return

        # Position des letzten gesetzten Stein vom Spieler löschen
        letztesBelegteFeld = [-1, -1]

        # vierGewinnt.spielfeldPrint(spielListe)

        # Computer muss Stein setzen
        # print("Der Computer ist dran.")

        ausgabeLabel.config(text="Der Computer ist dran.")
        # Computer zieht einen Stein
        spalte = function4Gewinnt.eingabeComputer(spielListe, "C", "S")
        # Zug in Datenstruktur spielListe eintragen
        spielListe = function4Gewinnt.steinSpielen(spielListe, spalte, "C")

        # gerade gespielte Position ermitteln
        position = function4Gewinnt.findeLetztenStein(spielListe, spalte, "C")

        # Zug auf Spielfeld sichtbar machen
        feldLabel[position[0]][position[1]].config(bg="yellow")

        # Auswertung, ob Spiel beendet (Computer gewonnen oder Spielfeld voll)
        # Prüfen, ob Computer gewonnen hat
        if function4Gewinnt.schonGewonnen(spielListe, position, "C"):
            # Buttons deaktivieren und Ausgabe
            buttonsDeaktivieren()
            ausgabeLabel.config(text="Du hast verloren!")
        else:
            # Prüfen, ob Spielfeld voll ist
            if function4Gewinnt.FeldVoll(spielListe):
                # Buttons deaktivieren und Ausgabe
                buttonsDeaktivieren()
                ausgabeLabel.config(text="Unentschieden")
            else:
                ausgabeLabel.config(text="Du bist dran.")
        # vierGewinnt.spielfeldPrint(spielListe)


def neuesSpielClick():
    """
    Zweck:
        wenn "neues Spiel"-Button betätigt wird,
            wird ein neues Spiel gestartet
            und alle Daten aus dem letzten Spiel gehen verloren
    Parameter: keine
    Rückgabe: keine
    """
    global letztesBelegteFeld, spielListe
    # Variablen zurück setzen
    # Position des letzten belegten Feldes (Spalte, Zeile)
    letztesBelegteFeld = [-1, -1]
    # Datenstruktur für ein Spielfeld
    # 2-dim Liste von 7 Spalten und 6 Zeilen
    spielListe = function4Gewinnt.spielfeldInit()

    # Spielfeld leeren
    for s in range(7):
        for z in range(6):
            feldLabel[s][z].config(bg="white")

    # Buttons aktivieren
    # Spalten-Buttons aktivieren
    for s in range(7):
        spaltenButton[s].config(state=NORMAL)
    # Zug beendet Button deaktivieren
    zugBeendetButton.config(state=NORMAL)

    # Ausgabe
    ausgabeLabel.config(text="Du fängst an.")


def spaltenButtonClick(spalte):
    """
    Zweck:
        wenn Spalten-Button betätigt wird,
            wird das unterste freie Feld der Spalte in der Spielerfarbe gefärbt
            und eine eventuelle Auswahl im gleichen Spielzug rückgängig gemacht
    Parameter:
        spalte: Nummer der Spalte, die angeklickt wurde
    Rückgabe: keine
    """
    # unterstes freies Feld in der Spalte färben

    # globale Variable belegtesFeld
    global letztesBelegteFeld

    # AusgabeLabel leeren
    ausgabeLabel.config(text="")

    # Wenn schon mal ein Feld in diesem Zug belegt wurde, dieses Feld weiß färben
    if letztesBelegteFeld != [-1, -1]:
        # Position von belegten Feld ermitteln
        s = letztesBelegteFeld[0]
        z = letztesBelegteFeld[1]
        # belegtes Feld auf weiß setzen
        feldLabel[s][z].config(bg="white")
        # Position des letzten belegten Feldes löschen
        letztesBelegteFeld = [-1, -1]

    zeile = 5
    # Wenn Spalte voll, dann Fehlermeldung
    if feldLabel[spalte][0].cget("bg") != "white":
        ausgabeLabel.config(text="Die Spalte ist schon voll.")
    # sonst (Spalte noch nicht voll),
    else:
        # Ausgabetext löschen
        ausgabeLabel.config(text="")

        # Von unten durch Spalte gehen,
        # um unterstes freie Feld zu finden und dann zu färben
        while zeile >= 0:
            # Wenn Feld leer, Feld rot färben
            if feldLabel[spalte][zeile].cget("bg") == "white":
                # neues Feld färben
                feldLabel[spalte][zeile].config(bg="red")
                letztesBelegteFeld = [spalte, zeile]

                # Wenn ein Feld gefärbt wurde, While-Schleife abbrechen
                # zeile = -1
                break
            # sonst (Feld voll), ein Feld nach oben gehen
            else:
                # gehe ein Feld nach oben
                zeile = zeile - 1


''' --- Oberfläche ------------------------------------------------------------------------------------------------ '''
# Fenster
VierGewinntFenster = Tk()
VierGewinntFenster.title("4-Gewinnt")
VierGewinntFenster.geometry("450x520")

# Einteilung des Fensters in 3 Bereiche:
# Ausgabe - oben
# Spielfeld - mitte
# Aktionsbereich - unten

ausgabeBereich = Frame(master=VierGewinntFenster, bg="aquamarine2")
ausgabeBereich.pack(side="top", fill="x")

aktionsBereich = Frame(master=VierGewinntFenster, bg="aquamarine4")
aktionsBereich.pack(side="bottom", fill="x")

spielBereich = Frame(master=VierGewinntFenster, bg="aquamarine3")
spielBereich.pack(fill="both", expand=True)

# Ausgabefeld
ausgabeLabel = Label(master=ausgabeBereich, bg="aquamarine", text="Du bist dran.", font=('Arial', 18), bd=10)
ausgabeLabel.pack(side="top")

# -Beginn Spielfeld
# Hintergrund
hintergrundLabel = LabelFrame(master=spielBereich, bg="light blue", width=375, height=380)
hintergrundLabel.pack(padx=10, pady=10)

# Spaltenknöpfe
spaltenButton = []
for s in range(7):  # Spalten
    # command=partial(spaltenButtonClick, s)
    # -> ermöglicht beim Drücken des Button die Funktion spaltenButtonClick mit Parameter s aufzurufen
    spaltenButton.append(Button(master=hintergrundLabel, bg="navy", text=str(s + 1), fg="white", font=('Arial', 18),
                                command=partial(spaltenButtonClick, s)))
    spaltenButton[s].place(x=10 + s * 50, y=10, width=50, height=50)

# Felder
feldLabel = []
for s in range(7):  # Spalten
    # Erzeugen einer Spalten
    spalte = []
    for z in range(6):  # Zeilen
        # hängt ein Element an die aktuelle Spalte an
        spalte.append(
            Label(master=hintergrundLabel, bg="white", borderwidth=3, relief="sunken", text=str(s) + "," + str(z),
                  fg="gray"))
        spalte[z].place(x=10 + s * 50, y=65 + z * 50, width=50, height=50)
    # hängt an das Feld eine Spalte an
    feldLabel.append(spalte)
# -Ende Spielfeld

# Knöpfe
neuesSpielButton = Button(master=aktionsBereich, bg="dark cyan", text="Neues Spiel", font=('Arial', 14),
                          command=neuesSpielClick)
neuesSpielButton.pack(side="left", padx=10, pady=10)

zugBeendetButton = Button(master=aktionsBereich, bg="dark cyan", text="Zug beendet", font=('Arial', 14),
                          command=zugBeendetClick)
zugBeendetButton.pack(side="right", padx=10, pady=10)

''' --- mainloop -------------------------------------------------------------------------------------------------- '''

VierGewinntFenster.mainloop()
