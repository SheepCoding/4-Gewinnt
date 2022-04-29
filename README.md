# 4-Gewinnt
4-Gewinnt in Python ohne Minimax-Algorithmus


Es wird gegen einen Computerspieler gespielt.
Für die Oberfläche wurde TkInter benutzt. 
Es ist möglich das Spiel auf der Konsole zu spielen, wenn man nur die function4Gewinnt-Datei benutzt und dort die mainloop hinzufügt.

Der Computer spielt defensive und nicht vorausschauend, da es ohne Minimax-Algorithmus oder vergleichbaren umgesetzt wurde. Der Computer schaut sich nur das aktuelle Spielfeld an und entscheidet dann, was er tut.
  1. Priorität: im nächsten Zug selbst gewinnen --> 3er Reihe vervollständigen
  2. Priorität: verhindern, dass Spieler im nächsten Zug gewinnt --> 3er Reihe des Spielers mit eigenen Stein vervollständigen
  3. Priorität: verhindern, dass Spieler im nächsten Zug 3er Reihe bekommen kann
  4. Priorität: eigene 2er Reihe verlängern
  5. sonst: zufälligen Zug ausführen
