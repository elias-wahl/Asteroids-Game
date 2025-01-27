from point import Point
import stddraw as std

from random import choice as rand_choice
from random import randint
"""
Die Klasse Perk() implementiert die sogenannten Perks (Power-Ups), die zuflällig als Kreise spawnen.
Fliegt der Spieler mit dem Schiff durch die Kreise, verschwindet dieser und der Spieler nimmt das Perk auf.
Es gibt 4 verschiedene Perks:
    "shield" - hellblauer Kreis:       beim nächsten Kontakt des Schiffes mit einem Asteroiden wird, der Asteroid und nicht das Schiff zerstört.
    "laser" - roter Kreis:             der Spieler bekommt für eine bestimme Zeit anstelle seines normalen Schusses einen mächtigen Laser
    "rainbow" - bunt-blinkender Kreis: der Spieler wird für eine bestimmte Zeit unzerstörbar und zerstört Asteroiden bei physischem Kontakt
    "nuke" - weißer Kreis:             gibt dem Spieler kurzeitig ein Schild und zündet eine nuke, die alle Asteroiden zerstört
"""
class Perk():
    def __init__(self):
        self.status = 0
        self.edge_size = 50
        self.type = str(rand_choice(list(["shield", "laser", "nuke", "rainbow"]))) #zufälliges perk
        self._pos = Point().random() #zufälliger spawn-ort
        self._color = {"shield":std.BOOK_LIGHT_BLUE, "laser":std.RED, "nuke":std.WHITE, "rainbow":self.get_random_color()}[self.type]
        self._size = 0.1
        self._counter = 0
    
    def update(self):
        self.status_check() 
    
    def status_check(self):
        #Initierungsphase in der das Objekt wächst und noch nicht interagiert.
        if self.status == 0:
            self._size +=0.01
            #Mit dem erreichen der size==1 ist die Initierungsphase beendet und status wird auf 1 gesetzt.
            if self._size >= 1:
                self.status = 1
        #jede 10 frames wird die Farbe des Schiffes gewechselt
        if self.type == "rainbow":
            self._counter += 1
            if self._counter == 10:
                self._color = self.get_random_color()
                self._counter = 1
        
    #malt das Perk
    def draw(self):
        std.setPenColor(self._color)
        std.filledCircle(self._pos.x, self._pos.y, self._size*self.edge_size)
        std.setPenColor(std.BLACK)
        std.filledCircle(self._pos.x, self._pos.y, self._size*self.edge_size*0.9)
        
    #generiert eine zufällige (nicht zu dunkle) Farbe
    def get_random_color(self):
        return std.color.Color(randint(100, 255), randint(100,255), randint(100,255))

    #auskunftsfunktionen, um nicht auf private eigenschaften von außen zugreifen zu müssen
    def getPosition(self):
        return self._pos
   
    def getSize(self):
        return self._size   