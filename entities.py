import pygame as py
import math as m
import parameters as p

from random import randint, uniform, random
from point import Point
from asteroids import Asteroid, Asteroids
from spacecraft import Spacecraft
from score import Score
from projectiles import SimpleShot, Laser
from explosions import Explosion, Nuke
from perkz import Perk

"""
Die Klasse Entities ist eine zusammenfassende Überklasse, die als Liste alle Entitäten des Spiels hält 
und einfachen Zugriff auf alle ermöglicht. Über die Liste werden jeden Frame alle Entities abgearbeitet,
sodass ihre Bewegung angepassst wird, ihre anderen Eigenschaften geupdatet werden und Interaktionen
verarbeitet werden.
"""
class Entities(list):
    def __init__(self):
        self.score = Score()            #Der Punktestand
        self.spacecraft = Spacecraft()  #Das Raumschiff
        self.asteroids = Asteroids()    #Die Asteroiden
        self._projectile_cooldown = 0   #Speichert wie viele Frames auf die Benutztung des Geschosses gewartet werden muss
        #Raumschiff und Asteroiden werden der liste hinzugefügt 
        self.append(self.spacecraft)
        for n in range(p.ASTEROID_START_NUMBER):
            self.append(self.asteroids.new_asteroid())
    
    #updated die Entitäten    
    def update(self):
        self.check_projectile_spawn() #spawned bei playerinput und cooldown == 0 ein Geschoss
        for entity in self:
            #Entitäten mit status -1 werden zersört
            if entity.status == -1:
                self.remove(entity)
            entity.update()
            self.collisions(entity) #check auf Kollisionen
    #malt alle Entitäten             
    def draw(self):
        for entity in reversed(self):
            entity.draw()
        self.score.draw() 
   
    #zerstört eine Entität inkl. Explosion und löscht von der Liste    
    def destroy(self, entity):
        self.append(Explosion(entity))
        self.remove(entity)
                
    #spawned bei playerinput und cooldown == 0 ein Geschoss.
    #Das Geschoss ist ein Laser, wenn das entsprechende Perk davor aufgesammelt wurde.
    def check_projectile_spawn(self):
        if self.spacecraft.perkz["laser"] > 0: 
            if py.key.get_pressed()[py.K_SPACE] and self._projectile_cooldown == 0: 
                self.append(Laser(self.spacecraft))
                self._projectile_cooldown = 30
            self._projectile_cooldown = max(0, self._projectile_cooldown -1) 
        else:
            if py.key.get_pressed()[py.K_SPACE] and self._projectile_cooldown == 0: 
                self.append(SimpleShot(self.spacecraft))
                self._projectile_cooldown = 30
            self._projectile_cooldown = max(0, self._projectile_cooldown -1) 
    
    #spawned mit einer wahrscheinlichkeit ein zufälliges perk am zufälligen Ort
    def random_perk_spawn(self):
        r = random()
        if r <= p.PERK_SPAWN_PROB_PER_FRAME:
            self.append(Perk())
    #spawned mit einer wahrscheinlichkeit einen zufälligen Asteroiden am zufälligen Ort
    def random_asteroid_spawn(self, spawn_rate):
        r = random()
        if r <= spawn_rate:
            self.append(self.asteroids.new_asteroid())
    
    #check auf Kollisionen, wenn entity ein Asteroid oder ein Perk ist und 
    #deren size schon ==1 ist, das Objekt also schon komplett initialisiert ist.
    def collisions(self, entity):
        if str(type(entity)) == "<class 'asteroids.Asteroid'>" and entity._size>=1:
            for other in self:
                if self.is_interacting(entity,other) == True:
                   self.score.score += 1 #jeder zerstörte Asteroid bringt einen Punkt
                   self.asteroids.quantity -= 1 #die Anzahl der Asteroiden nimmt um 1 ab
                   #Wenn der zerstörte Asteroid groß genug war, zersplittert er in neue Asteroiden
                   if not (entity._findArea() < 15000 or len(entity._shape)<4):
                       self.extend(self.asteroids.asteroid_pieces(entity, other))   
                   try: self.destroy(entity)
                   except: pass
        elif str(type(entity)) == "<class 'perkz.Perk'>" and entity._size>=1:
            for other in self:
                if self.is_interacting(entity,other) == True:
                    try: self.destroy(entity)
                    except: pass 
                
    #Diese Methode checked die genauen Hitboxen und führt die Interaktionen teilweise aus
    def is_interacting(self, entity, other):
        distance_approx = entity.edge_size*entity._size*4 #grobe Abschätzung zur Optimierung
        if str(type(entity)) == "<class 'asteroids.Asteroid'>": 
            match str(type(other)):
                case "<class 'projectiles.SimpleShot'>":
                    if other.getPosition().x - entity.getPosition().x < distance_approx and other.getPosition().y - entity.getPosition().y < distance_approx:
                        if entity.contains(other.getPosition()):
                            self.remove(other)
                            return True
                case "<class 'projectiles.Laser'>":
                    return other.in_beam(entity) #komplexere Berechnung in externer Funktion
           
                case "<class 'spacecraft.Spacecraft'>":
                     if other.getPosition().x - entity.getPosition().x < distance_approx and other.getPosition().y - entity.getPosition().y < distance_approx:
                         #Doppelter check für möglichst gute Hitboxen
                         for point in other.getPoints():
                             if entity.contains(point):
                                 #Wenn das Perk "rainbow" oder "shield" aktiv ist, zerstört das Schiff den Asteroiden bei Kollision
                                 if other.perkz["rainbow"] > 0:
                                     return True
                                 elif other.perkz["shield"] > 0:
                                     other.perkz["shield"] = 0
                                     return True
                                 else: self.spacecraft.destroyed = True
                         for point in entity.getPoints():
                             if other.contains(point):
                                 if other.perkz["rainbow"] > 0:
                                     return True
                                 elif other.perkz["shield"] > 0:
                                     other.perkz["shield"] = 0
                                     return True
                                 else: self.spacecraft.destroyed = True
                case "<class 'explosions.Nuke'>":
                    for point in entity.getPoints():
                        if (point.x - other.getPosition().x)**2 + (point.y - other.getPosition().y)**2 < (other._size)**2:
                            return True
        
        elif str(type(entity)) == "<class 'perkz.Perk'>":
            if str(type(other)) == "<class 'spacecraft.Spacecraft'>":
                if other.getPosition().x - entity.getPosition().x < distance_approx and other.getPosition().y - entity.getPosition().y < distance_approx:
                    for point in other.getPoints():
                        if (point.x - entity.getPosition().x)**2 + (point.y - entity.getPosition().y)**2 < (entity.edge_size*entity._size)**2:
                            if entity.type == "nuke":
                                other.perkz["shield"] = 50 #bei der Zündung einer nuke gibt es zum Schutz kurzzeitig ein schild
                                self.append(Nuke(entity))
                            else:
                                other.perkz[entity.type] = 400 #das perk wird für 400 frames gewährt.
                            entity.status = -1
        return False
                         
   
                    
           
        

 