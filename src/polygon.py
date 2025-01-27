""" 
CLASS: Polygon
DESCRIPTION: A polygon is a sequence of points in space defined by a set of
             such points, an offset, and a rotation. The offset is the
             distance between the origin and the center of the shape.
             The rotation is measured in degrees, 0-360.
USAGE: You are intended to instantiate this class with a set of points that
       forever defines its shape, and then modify it by repositioning and
       rotating that shape. In defining the shape, the relative positions
       of the points you provide are used, in other words: {(0,1),(1,1),(1,0)}
       is the same shape as {(9,10),(10,10),(10,9)}.
NOTE: You don't need to worry about the "magic math" details.
 """
from point import Point
import math

class Polygon:
	def __init__(self, shape, position, rotation, size):
		if len(shape)<2:
			raise ValueError('Polygon must have at least two vertices')
		self._shape=shape# A list of points
		self._pos=position# The offset mentioned above
		self._rot=rotation# Zero degrees is due east
		self._size = size

		#~ First, we find the shape's top-most left-most boundary, its origin.
		origin=Point(self._shape[0].x, self._shape[0].y)
		for p in self._shape:
			if p.x<origin.x: origin.x=p.x
			if p.y<origin.y: origin.y=p.y

		#~ Then, we orient all of its points relative to the real origin.
		for p in self._shape:
			p.x-=origin.x
			p.y-=origin.y
	def getSize(self):
		return self._size
	def getShape(self):
		return self._shape

	def getPosition(self):
		return self._pos

	def getRotation(self):
		return self._rot

	def setPosition(self, position):
		self._pos=position

	def setRotation(self, degrees):
		self._rot=degrees%360

	def move(self, x=0, y=0):
		self._pos.x+=x
		self._pos.y+=y

	def rotate(self, degrees=0):
		self._rot=(self._rot+degrees)%360

	#~ "getPoints" applies the rotation and offset to the shape of the polygon.
	def getPoints(self):
		import stdarray
		center=self._findCenter()
		points=stdarray.create1D(len(self._shape))
		for i in range(len(self._shape)):
			p=self._shape[i]
			x=self._size*(((p.x-center.x)*math.cos(math.radians(self._rot)))-((p.y-center.y)*math.sin(math.radians(self._rot)))+center.x/2)+self._pos.x
			y=self._size*(((p.x-center.x)*math.sin(math.radians(self._rot)))+((p.y-center.y)*math.cos(math.radians(self._rot)))+center.y/2)+self._pos.y
			points[i]=Point(x, y)
		return points

	#~ "contains" implements some magical math (i.e. the ray-casting algorithm).
	def contains(self, point):
		points=self.getPoints()
		crossingNumber=0
		for i in range(-1, len(self._shape)-1):
			if (((points[i].x<point.x) and (point.x<=points[i+1].x)) or ((points[i+1].x<point.x) and (point.x<=points[i].x))) and (point.y>points[i].y+(points[i+1].y-points[i].y)/(points[i+1].x-points[i].x)*(point.x - points[i].x)):
				crossingNumber+=1
		return crossingNumber%2==1

    #~ "findArea" implements some more magic math.
	def findArea(self):
		return self._findArea()
    
    #~ "findArea" implements some more magic math.
	def _findArea(self):
		sum=0
		for i in range(-1, len(self._shape)-1):
			sum+=self._shape[i].x*self._shape[i+1].y-self._shape[i+1].x*self._shape[i].y
		return abs(sum/2)
    #~ "findArea" implements some more magic math.
	def findCenter(self):
		return self._findCenter()
    
	#~ "findCenter" implements another bit of math.
	def _findCenter(self):
		sum=Point(0, 0)
		for i in range(-1, len(self._shape)-1):
			sum.x+=(self._shape[i].x+self._shape[i+1].x)*(self._shape[i].x*self._shape[i+1].y-self._shape[i+1].x*self._shape[i].y)
			sum.y+=(self._shape[i].y+self._shape[i+1].y)*(self._shape[i].x*self._shape[i+1].y-self._shape[i+1].x*self._shape[i].y)
		area=self._findArea()
		return Point(abs(sum.x/(6*area)), abs(sum.y/(6*area)))
