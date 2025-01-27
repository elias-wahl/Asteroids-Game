from math import pi, atan
from random import randint, uniform
from moving_object import MovingObj
from point import Point

import stddraw as std
"""
Asteroid ist die Klasse die, die einzelenen Asteroiden implementiert. Die werden am Anfang mit zufälligen Werten initialisiert.

"""
class Asteroid(MovingObj):
    def __init__(self, edge_size, position, transitional_velocity, size):
        self.edge_size = edge_size
        self.number_of_corners = randint(5,13)
        self.shape = list([Point(0,0)])
        self.random_asteroid_shape()
  
        rotation = randint(1,360)
        rotational_velocity = uniform(-1,1)
        status = 0
        color = std.WHITE
        super().__init__(self.shape, position, rotation, size, rotational_velocity, transitional_velocity, status, color)
    
    #übergibt ein zufällige Form an self.shape
    def random_asteroid_shape(self):
        for i in range(1,self.number_of_corners-1):
            self.next_point_for_shape(i)
        #übergibt für den letzten Punkt der shape genauere Angaben, damit die Form des Asteroiden möglicht keine komischen Spitzen hat.    
        forced_length = ((self.shape[-1].x**2+self.shape[-1].y**2)**(1/2))/2
        forced_angle = atan(self.shape[-1].y/self.shape[-1].x)
        self.next_point_for_shape(i, forced_length, forced_angle)
    
    #übergibt vom letzten Punkt aus und des Platzes im Kreis, den nächsten Punkt der Asteroid.shape
    #Der Prozess wird zur Vereinfachung in Polarkoordinaten gerechnet unter danach in kartesische umgerechnet
    def next_point_for_shape(self, i, forced_length = 0, forced_angle = 0):
        if forced_length != 0:
            length = forced_length
            alpha = uniform(1,1.2)*forced_angle
        else:    
            length = uniform(0.4,1.4)*self.edge_size
            alpha = uniform(0.5,1.5)*(2*pi/self.number_of_corners)+(2*pi/self.number_of_corners)*i
        
        polar_point = Point(length, alpha)
        polar_point.polar_to_euklid()
        new_point = Point(polar_point.x + self.shape[-1].x, polar_point.y + self.shape[-1].y)
        self.shape.append(new_point)
        
    #auskunftsfunktion, um nicht auf private eigenschaften von außen zugreifen zu müssen        
    def getTransVel(self):
        return self._trans_vel
"""
Asteroids ist eine Klasse, um Methoden zur Asteroideninitialisierung zusammenzufassen und die Anzahl der aktiven zu zählen
"""            
class Asteroids():
    def __init__(self):
        self.quantity = 0
    
    #erstellt einen brandneuen Asteroiden  
    def new_asteroid(self):
        self.quantity += 1
        edge_size = randint(60,70)
        position = Point()
        position.random()
        transitional_velocity = Point(randint(-3,3),randint(-3,3))
        size = 0.1
        return Asteroid(edge_size, position, transitional_velocity, size)
    
    #erstellt, die Bruchstücke eines großen zerstörten Asterodien der zerfällt
    #es gehen, die Größe des zerstörten Asteroiden ein, sowie die Richtung und Geschwindigkeit
    #der Sache, die den Asteroiden zerstört hat
    def asteroid_pieces(self, entity, other):
        numberOfNewParts = randint(2,5)
        new_asteroid_pieces = list([])
        for i in range(numberOfNewParts):
            self.quantity += 1
            edge_size = entity.edge_size * uniform(0.4, 0.6)
            alpha = 2*pi/numberOfNewParts*i+uniform(-0.3,0.3)
            length = edge_size
            point = Point(length, alpha)
            point.polar_to_euklid()
            position = point + entity.getPosition()
            transitional_velocity = entity.getTransVel()*0.8 + other.getTransVel()*0.1 + point*0.05
            size = 0.8
            new_asteroid_pieces.append(Asteroid(edge_size, position, transitional_velocity, size))
        return new_asteroid_pieces