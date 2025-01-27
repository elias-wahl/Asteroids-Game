import math as m
import parameters as p
import stddraw as std
import pygame as py

from moving_object import MovingObj
from random import randint
from point import Point

"""
Die Klasse Spacecraft() ist das Raumschiff, dass vom Spielen mit Pfeiltasten und SPACE kontrolliert werden kann.
Seine Geschosse zerstören all Asteroide mit einem Schuss, allerdings zerschellt das Schiff ohne Perks auch beim 
ersten physischen Kontakt mit einem Asteroiden. Der Spieler in Perks fliegen, um diese aufzunehmen und an starke
Fähigkeiten zu gelangen. Jeder zerstörte Asteroid gibt einen Punkt.
"""
class Spacecraft(MovingObj):
    def __init__(self):
        self.destroyed = False #wird bei zerstörtem Schiff True
        self.max_vel = 8       #maximale Geschwindigkeit des Schiffs
        self.edge_size= 5      #ungefähre Größe des Schiffes
        self.perkz = {"laser" : 0, "shield" : 0, "rainbow" : 0} #Hier werden eingesammelte, aktive Perks vermerkt
        self._counter = 0 #wird für den Farbenwechsels bei perk "rainbow" benötigt
        shape = list([Point(4, 0), Point(-1, 2), Point(0, 0), Point(-1,-2)]) #Form des schiffes
        position = Point(p.WHOLE_CANVAS_WIDTH/2, p.WHOLE_CANVAS_HEIGHT/2) #Anfangsposition
        rotation = 0
        size = 20
        rotational_velocity = 0
        transitional_velocity = Point(0,0)
        status = 1
        color = std.BLUE
        #Die restlichen eigenschafen werden über eltern-klasse initialisiert
        super().__init__(shape, position, rotation, size, rotational_velocity, transitional_velocity, status, color)
        
    #updated die Bewegung des Schiffes und den Countdown aktiver Perks
    def update(self):
        #Das Schiff wird immer leicht gebremst, sodass es ohne inputs langsam zum stehen kommt
        self._trans_vel.x *= 0.99
        self._trans_vel.y *= 0.99
        self._rot_vel *=0.9
        
        #Prüfen auf Eingaben
        if py.key.get_pressed()[py.K_LEFT]:
            self._rot_vel += 0.6
        if py.key.get_pressed()[py.K_RIGHT]:
            self._rot_vel -= 0.6
        if py.key.get_pressed()[py.K_UP]:
            self._trans_vel.x += m.cos(m.radians(self._rot))
            self._trans_vel.y += m.sin(m.radians(self._rot))
        if py.key.get_pressed()[py.K_DOWN]:
            self._trans_vel.x -= m.cos(m.radians(self._rot))
            self._trans_vel.y -= m.sin(m.radians(self._rot))
        
        #Geschwindigkeitsbregrenzungen damit das Schiff nicht zu schnell wird
        if self._trans_vel.x > self.max_vel: self._trans_vel.x = self.max_vel
        if self._trans_vel.y > self.max_vel: self._trans_vel.y = self.max_vel
        if self._trans_vel.x < -self.max_vel: self._trans_vel.x = -self.max_vel
        if self._trans_vel.y < -self.max_vel: self._trans_vel.y = -self.max_vel
        self._pos.add(self._trans_vel)
        self._rot = (self._rot + self._rot_vel)%360
        
        #Countdown aktiver Perks, außer dem Schild, denn das läuft zeitlich nicht ab
        for perk in self.perkz:
            if perk != "shield":
                self.perkz[perk] = max(0, self.perkz[perk]-1)
    
    #malt das Schiff    
    def draw(self):
        #ist das Perk "rainbow" aktiv ändert das Schiff alle 10 frames sein Farbe.
        if self.perkz["rainbow"] > 0 :
            self._counter += 1
            if self._counter == 10:
                self._color = std.color.Color(randint(100, 255), randint(100,255), randint(100,255))
                self._counter = 0
        else: self._color = std.BLUE #normalerweise ist das Schiff dunkelblau
        #ist das Perk "shield" aktiv, wird um das Schild ein blaues Schild gezeichnet
        if self.perkz["shield"] > 0:
            std.setPenColor(std.BOOK_LIGHT_BLUE)
            std.circle(self._pos.x + self._size, self._pos.y + self._size, self._size*3.5)
        std.setPenColor(self._color)
        std.filledPolygon(*self.transfrom_into_drawable())  
    
    #auskunftsfunktionen, um nicht auf private eigenschaften von außen zugreifen zu müssen        
    def getTransVel(self):
        return self._trans_vel
    
    def getRotation(self):
        return self._rot
    
    def getSize(self):
        return self._size
        
        

     