import math as m
import parameters as p

from random import randint
from math import pi, sin, cos
"""
Die Klasse Polar vereinfacht das Rechnen mit Polarkoordinaten
"""
class Polar():
    def __init__(self, length, alpha):
        self.length = length
        self.alpha = alpha
    
    def drehen(self, d):
        self.alpha = (self.alpha + d)%360
        return self
    
    def skalieren(self, f):
        self.length = f*self.length
        return self
    
    def euklid(self):
        radial_alpha = self.alpha/180*pi
        x = self.length*cos(radial_alpha)
        y = self.length*sin(radial_alpha)
        return (x,y)
"""
Die Klasse Point besteht aus einem Paar floats und Rechenoperationen.
Sie wird vor allem als Koordinate im Ortsraum verwendet, aber auch für die translatorische Geschwindigkeit von Objekten.
"""    
class Point():
    def __init__(self, x = 0, y = 0):
        self.x=x
        self.y=y
###Zum Rechnen um Ortsraum -> periodische Randbedingungen
    def random(self):
        self.x = randint(0, p.WHOLE_CANVAS_WIDTH)
        self.y = randint(0, p.WHOLE_CANVAS_HEIGHT)
        return self
        
    def add(self, other_point):
        self.x = (self.x + other_point.x)%p.WHOLE_CANVAS_WIDTH
        self.y = (self.y + other_point.y)%p.WHOLE_CANVAS_HEIGHT
        
    def sub(self, other_point):
        self.x = (self.x - other_point.x)%p.WHOLE_CANVAS_WIDTH
        self.y = (self.y - other_point.y)%p.WHOLE_CANVAS_HEIGHT
    #transformiert Point-Koordinaten von Polar zu Kartesischen
    def polar_to_euklid(self):
        alpha = self.y
        length = self.x
        x = length*m.cos(alpha)
        y = length*m.sin(alpha)
        self.x = x
        self.y = y
    
###Zum Rechnen mit Geschwindigkeiten -> KEINE periodische Randbedingungen
###Mit den "Zauberfunktionen" umrundet mit doppelten Unterstrichen werden hier
###die Rechenymbole zwischen der Klasse Point und einem Skalar bzw. zwischen
###zwei Objekten der Klasse Point umdefiniert 
    def __mul__(self, other):
        x = self.x*other
        y = self.y*other
        return(Point(x,y))
        
    def __add__(self, other_point):
        x = (self.x + other_point.x)
        y = (self.y + other_point.y)
        return Point(x,y)
        
    def __sub__(self, other_point):
        x = (self.x - other_point.x)
        y = (self.y - other_point.y)
        return Point(x,y)

