import stddraw as std
import pygame as py
import time as t
import parameters as p

from entities import Entities
"""
Die Klasse Game bildet den Rahmen für das gesamte Spiel.
"""
class Game():
    def __init__(self):
        self._start_time = t.time() #Anfangszeit des Spiels
        self._entities = Entities() #Alle Entitäten des Spiels können hierrüber aufgerufen werden
    
    #Erstellung eines neuen Canvas
    def new_canvas(self):
        std.setCanvasSize(p.SEEN_CANVAS_WIDTH, p.SEEN_CANVAS_HEIGHT)
        std.setXscale(p.SEEN_CANVAS_X_MIN, p.SEEN_CANVAS_X_MAX)
        std.setYscale(p.SEEN_CANVAS_Y_MIN, p.SEEN_CANVAS_Y_MAX)
        std.setFontSize(50)
    
    #Der Loop der jeden Frame durchgegangen werden muss wird nur dann gebrochen, 
    #wenn das Raumschiff zerstört wird und das Spiel damit verloren ist
    def run(self):
       while self._entities.spacecraft.destroyed == False:
            self.random_spawn()             #spanwed zufällig neue Asteroiden und Perks    
            self._entities.update()         #checked und updated alle Entitäten 
            self._entities.draw()           #malt alle Entitäten 
            std.show(1000/p.FPS)            #zeigt den neuen Frame auf dem Canvas
            if py.key.get_pressed()[py.K_p]:
                t.sleep(100000)
            std.clear(std.BLACK)            #löscht den alten Frame auf dem Canvas
    
    #Diese Methode steuert, die Spawnrate von neuen Asteroiden und gibt jeden Frame den Auftrag diese und Perks
    #mit eine gewissen Wahrscheinlichkeit zu spawnen.
    def random_spawn(self):
         timer = self._start_time - t.time() #Sekunden seit Start des Spiels
         #Geringere Spawnrate, wenn schon sehr viele Asteroiden da sind
         if self._entities.asteroids.quantity > 20:
             spawn_rate = 0.1/p.FPS
         #Hohe Spawnrate, wenn nur wenige Asteroiden da sind    
         elif self._entities.asteroids.quantity < 5:
             spawn_rate = 2/p.FPS
        #Ansonsten steigt die Spawnwahrscheinlichkeit mit der Länge des Spiels bis es einen Höhepunkt erreicht. 
         else:
             spawn_rate = min(0.8/p.FPS, p.INITIAL_ASTEROID_SPAWN_PROB_PER_FRAME * (1+timer/60*p.INCREASE_PER_MINUTE_OF_ASTEROID_SPAWN_PROB_PER_FRAME))
         self._entities.random_perk_spawn()
         self._entities.random_asteroid_spawn(spawn_rate) 
         
    #Wird aufgerufen, wenn das Spiel verloren ist. Der erreichte Score ist auf dem Game-Over-Screen zu sehen 
    #und es besteht die Möglichkeit zu beenden oder weiterzuspielen
    def end(self):
        #Erstellen des Game-Over-Screens     
        std.clear(std.BLACK)
        std.setPenColor(std.color.RED)
        std.setFontSize(150) 
        std.text(p.SEEN_CANVAS_WIDTH * 0.6, p.SEEN_CANVAS_HEIGHT*0.65, "GAME OVER")
        std.setPenColor(std.color.WHITE)
        
        #Falls der erreichte Score ein Highscore ist, wird das gespeichert und angemerkt
        if self._entities.score.score > self._entities.score.highscore:
            with open("highscore.txt", "w") as file:
                file.writelines(str(self._entities.score.score))
            std.setFontSize(70)
            std.text(p.SEEN_CANVAS_WIDTH * 0.6, p.SEEN_CANVAS_HEIGHT*0.56, "NEW HIGHSCORE! : " + str(self._entities.score.score)) 
        else:
            std.setFontSize(50)
            std.text(p.SEEN_CANVAS_WIDTH * 0.6, p.SEEN_CANVAS_HEIGHT*0.55, "SCORE: " + str(self._entities.score.score))        
        
        std.setFontSize(50)
        std.text(p.SEEN_CANVAS_WIDTH * 0.6, p.SEEN_CANVAS_HEIGHT*0.5, "PRESS ENTER TO TRY AGAIN AND ESC TO END")
        
        #Input entscheidet, ob weitergespielt und beendet wird
        while True:
            std.show(50)
            if py.key.get_pressed()[py.K_ESCAPE]:
                return True
            if py.key.get_pressed()[py.K_RETURN]:
                return False
  
if __name__ == "__main__":
    while True:
        #Spiel erstellen
        game = Game()
        #Canvas erstellen, wenn noch nicht da
        try: game.new_canvas() 
        except: pass
        #Das Spiel laufen lassen
        game.run()  
        #Wenn der Spieler nicht nochmal spielen will -> Spiel beenden
        if game.end() == True:
            quit()
        