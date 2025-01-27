import parameters as p
import stddraw as std
import math as m

from moving_object import MovingObj
from point import Point
"""
Die Klasse Projectile(MovingObj) nimmt seine meisten Eigenschaften von der Klasse MovinObj und bietet
die Basis für die beiden Geschossklassen.
"""
class Projectile(MovingObj):
    def __init__(self,shape,rotation,rotational_velocity, transitional_velocity, status, color, size, spacecraft):      
        self._spacecraft = spacecraft
        #die Position ist der Anfangspunkt des Geschosses und liegt vorne mitte unter dem Schiff
        position = Point(spacecraft.getPosition().x +spacecraft.getSize()*(1+1.8*m.cos(m.radians(spacecraft.getRotation()))), spacecraft.getPosition().y+spacecraft.getSize()*(1+1.8*m.sin(m.radians(spacecraft.getRotation()))))
        super().__init__(shape, position, rotation, size, rotational_velocity, transitional_velocity, status, color)
    
    #auskunftsfunktion, um nicht auf private eigenschaften von außen zugreifen zu müssen
    def getTransVel(self):
        return self._trans_vel
"""
Die Klasse SimpleShot implementiert den normelen Schuss, den das Schiff ohne Perks schießt.
Die Geschwindigkeit der Kugeln ist auch von der Geschwindigkeit des Schiffes abhängig.
Beim Kontakt mit einem Asteroiden, wird das Geschoss und der Asteroid zerstört.
"""
class SimpleShot(Projectile):
    def __init__(self, spacecraft):
        rotation = spacecraft.getRotation()
        rotational_velocity = 0
        shape = list([Point(0.2*spacecraft.getSize(),0), Point(0,0)])
        spacecraft_speed = (spacecraft.getTransVel().x**2 + spacecraft.getTransVel().y**2)**(1/2)
        transitional_velocity = Point(spacecraft.getTransVel().x+(spacecraft_speed+5)*m.cos(m.radians(spacecraft.getRotation())),spacecraft.getTransVel().y+(spacecraft_speed+5)*m.sin(m.radians(spacecraft.getRotation())))
        status = -100 #dient als timer bis zum Verschwinden des Geschosses
        color = std.ORANGE
        size = 1
        super().__init__(shape, rotation,rotational_velocity, transitional_velocity, status, color, size, spacecraft)  
        
    def draw(self):
        std.setPenColor(self._color)
        std.filledCircle(self._pos.x, self._pos.y, self._shape[0].x)
"""
Die Klasse Laser implementiert das Geschoss Laser, was der Spieler durch das Einsammeln des Perks "laser"
für eine bestimmte Zeit aktivieren kann. Der Laser zerstört instantan alle Asteroiden in der Schusslinie
"""
class Laser(Projectile):
    def __init__(self, spacecraft):
        self._trans_vel = spacecraft.getTransVel()
        self._rot = spacecraft.getRotation()
        rotational_velocity = 0
        shape = list([Point(p.WHOLE_CANVAS_WIDTH, 0), Point(0,0)]) #nicht die wirkliche From des Lasers
        status = -5 #dient als timer bis zum Verschwinden des Geschosses
        size = 1
        color = std.RED
        super().__init__(shape, self._rot, rotational_velocity, self._trans_vel, status, color, size, spacecraft) 
        
        #berechnet Endpunkt des Laser
        self._beam_end_x = self._pos.x + m.cos(m.radians(self._rot))*p.WHOLE_CANVAS_WIDTH
        self._beam_end_y = self._pos.y +m.sin(m.radians(self._rot))*p.WHOLE_CANVAS_HEIGHT
    
    #updated die Daten des Lasers, sodass er weiter direkt aus dem Schiff feuert auch wenn es sich wegbewegt
    def update(self):
        self.status_check()
        self._rot = self._spacecraft.getRotation()
        self._pos = Point(self._spacecraft.getPosition().x +self._spacecraft.getSize()*(1+1.8*m.cos(m.radians(self._spacecraft.getRotation()))), self._spacecraft.getPosition().y+self._spacecraft.getSize()*(1+1.8*m.sin(m.radians(self._spacecraft.getRotation()))))
    
    #malt den Laser
    def draw(self):
        std.setPenColor(self._color)
        std.setPenRadius(abs(2*self.status))
        std.line(self._pos.x, self._pos.y, self._beam_end_x, self._beam_end_y)
        std.setPenRadius(0.005)   

    #performance optimierte methode um festzustellen, ob ein asteroid vom laser getroffen wird
    def in_beam(self, asteroid):
        ancathete = m.cos(m.radians(self._rot))
        if ancathete == 0: ancathete = 0.0001 #catch the zero
        slope = m.sin(m.radians(self._rot))/ancathete #slope of the laser
        #wir beschreiben nun den Laser als lineare Funktion und setzen je nachdem was von der Steigung her besser ist
        #den x- oder y-Wert der Position des Asteroiden ein und vergleichen das Ergebnis mit der jeweils anderen Koordinate.
        #Unterschreitet die Differenz einen geschätzten Wert, werden 10 Punkte nahe des berechneten Punktes auf der Laser-Funktion
        #gewählt und geprüft, ob sich einer dieser innerhalb des Asteroiden befindet.
        if (slope >= 1) or (slope <= -1): #große Steigung: y-Änderung dominiert
            x = (asteroid.getPosition().y-self._pos.y)/slope + self._pos.x
            if abs(x-asteroid.getPosition().x) <= 4*asteroid.edge_size and self.right_direction(x):
            #Closer check
                for i in range(10):
                    point_to_test_y = asteroid.getPosition().y + 2*(i/10 - 0.5)*(asteroid.edge_size)
                    point_to_test_x = (point_to_test_y-self._pos.y)/slope + self._pos.x
                    point_to_test = Point(point_to_test_x,point_to_test_y)
                    if asteroid.contains(point_to_test):
                        return True
        else: #eher kleine Steigung: x-Änderung überwiegt
            y = (asteroid.getPosition().x-self._pos.x)*slope + self._pos.y
            if abs(y-asteroid.getPosition().y) <= 4*asteroid.edge_size and self.right_direction(asteroid.getPosition().x):
                #Closer check
                for i in range(10):
                    point_to_test_x = asteroid.getPosition().x + 2*(i/10 - 0.5)*(asteroid.edge_size)
                    point_to_test_y = (point_to_test_x-self._pos.x)*slope + self._pos.y
                    point_to_test = Point(point_to_test_x,point_to_test_y)
                    if asteroid.contains(point_to_test):
                        return True
        return False
    
    #checked, dass der Punkt x wirklich im Strahl liegt und nicht in gedachten, verlängerten Linie des Lasers hinter der Schiff      
    def right_direction(self, x):
        if (self._rot <= 90 or self._rot >= 270) and self._pos.x < x:
            return True
        if 90 < self._rot < 270 and self._pos.x > x:
            return True
        else: return False
                

       