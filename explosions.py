import stddraw as std
import parameters as p

from point import Point
"""
Die Klasse Explosion() interagiert nicht und spawned jedes mal, wenn ein Asteroid zerstört wird.
"""
class Explosion():
    def __init__(self, entity):
        self.status = 1
        self._max_size =  entity._size*entity.edge_size #Größe ist an Asteroidgröße angepasst
        self._size = entity._size*entity.edge_size
        self._pos = entity.getPosition() #spawned an der letzten Position des zerstörten Asteroiden
    
    def update(self):
        self._size -= self._max_size*0.1 #verliert jeden Frame an Größe
    
    #ist die Größe <0 wird der Status auf -1 gesetzt, was "zu löschen" bedeutet
    def status_check(self):  
        if self._size < 1:
            self.status = -1
            
    def draw(self):
        std.setPenColor(std.ORANGE)
        std.filledCircle(self._pos.x, self._pos.y, self._size)
"""
Die Nuke() Klasse ist eine riesige zerstörerische Explosion, die beim aufsammel eines "nuke"-Perks ausgelöst wird.
"""            
class Nuke():
    def __init__(self, entity):
        self.status = 1
        self._max_size = p.WHOLE_CANVAS_HEIGHT*1.5
        self._size = entity.getSize()*entity.edge_size
        self._pos = entity.getPosition()
        self._trans_vel = Point(0,0)
        
    def update(self):
        self._size += 0.015*self._max_size #die größte wächst mit jedem Frame
        self.status_check()
    
    #überschreitet die Größe die Maximalgröße, wird der Status auf -1 gesetzt, was "zu löschen" bedeutet
    def status_check(self):  
        if self._size > self._max_size:
            self.status = -1
    def draw(self):
        std.setPenColor(std.RED)
        std.filledCircle(self._pos.x, self._pos.y, self._size)
        std.setPenColor(std.ORANGE)
        std.filledCircle(self._pos.x, self._pos.y, self._size*97)
        std.setPenColor(std.WHITE)
        std.filledCircle(self._pos.x, self._pos.y, self._size*0.92)
                  
    #auskunftsfunktionen, um nicht auf private eigenschaften von außen zugreifen zu müssen
    def getPosition(self):
        return self._pos
        
    def getTransVel(self):
        return self._trans_vel

