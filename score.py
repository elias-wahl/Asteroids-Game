import parameters as p
import stddraw as std

"""
Score() ist die Klasse, die die Punkte des Spielers managed. Sowohl die aktuellen als auch den Highscore.
"""
class Score():
    def __init__(self):
        #Der highscore wrid der highscore.txt entnommen, wo immer der aktuelle highscore gespeichert ist.
        with open('highscore.txt') as f:
            highscore = int(f.readline())
        self.highscore = highscore   
        self.score = 0
    
    #zeigt die Punkte am unteren Bildschirmrand an
    def draw(self):
        std.setPenColor(std.color.WHITE)
        std.text(p.SEEN_CANVAS_WIDTH * 0.25, p.SEEN_CANVAS_HEIGHT * 0.12, "HIGHSCORE: " + str(self.highscore))
        std.text(p.SEEN_CANVAS_WIDTH * 0.9, p.SEEN_CANVAS_HEIGHT * 0.12, "SCORE: " + str(self.score))

       