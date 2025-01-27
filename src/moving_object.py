import parameters as p
import stddraw as std

from polygon import Polygon
"""
Die Klasse MovingObj baut auf der Klasse Polygon auf und bildet die Grundlage für die Klassen Asteroid, Spacecraft und Projectile.
"""
class MovingObj(Polygon):
    def __init__(self, shape, position, rotation, size, rotational_velocity, transitional_velocity, status, color):
        super().__init__(shape, position, rotation, size)
        self.status = status                       #Status des Objekt
        self._color = color                        #Farbe des Objekts
        self._rot_vel = rotational_velocity        #in radians pro frame
        self._trans_vel = transitional_velocity    #in pixel pro frame

    #checked den status und erhöht Position und Rotation um deren Geschwindigkeit              
    def update(self):
        self.status_check()
        self._rot += self._rot_vel
        self._pos.add(self._trans_vel)
    def status_check(self):
        #Initierungsphase in der das Objekt wächst und noch nicht interagiert.
        if self.status == 0:
            self._size +=0.01
            #Mit dem erreichen der size==1 ist die Initierungsphase beendet und status wird auf 1 gesetzt.
            if self._size >= 1: 
                self.status = 1
        #negative Stati werden teilweise als lebensdauer benutzt. Das Objekt wird gelöcht, wenn der status == -1 erreicht.
        if self.status < -1:
            self.status +=1
        
    def draw(self):
        std.setPenColor(self._color)
        corner_points = self.transfrom_into_drawable()
        #stoppt (in Theorie) Glitches, die beim passieren der periodischen Ränder beim Zeichnen passieren.
        if (max(corner_points[0]) - min(corner_points[0])) < p.SEEN_CANVAS_WIDTH_HALF and (max(corner_points[1]) - min(corner_points[1])) < p.SEEN_CANVAS_HEIGHT_HALF:
            std.polygon(*corner_points)
 
    #transformiert die ausgabe von getPoints(), sodass sie von std.polygon eingesen werden kann.
    def transfrom_into_drawable(self):
        moved_points = self.getPoints()
        x_i =  [point.x for point in moved_points]
        y_i =  [point.y for point in moved_points]
        return x_i, y_i    


        
