import sys
from collections import deque

class SquareValidator:

	sqrDist = lambda a, b :  (a.x - b.x)**2 + (a.y - b.y)**2

	class Point:
		
		def __init__(self, x, y):
			self.x = x
			self.y = y
			self.inf = sys.float_info.max
		
		def hashCoords(self):
			return 397 * self.x + self.y

		def gradient(self, p):
			dx = self.x - p.x
			if dx == 0:
				return self.inf
			else:
				return (self.y - p.y) / dx


		def dotProd(self, p1, p2):
			return (p1.x - self.x) * (p2.x - self.x) + (p1.y - self.y) * (p2.y - self.y)
		

		def crossProd(self, p1, p2):
			return (p1.x - self.x) * (p2.y - self.y) - (p1.y - self.y) * (p2.x - self.x)
		

		def isRightAngDot(self, p1, p2):
			return self.dotProd(p1, p2) == 0
		

		def isRightAngGrad(self, p1, p2):
			gradient_a = self.gradient(p1)
			gradient_b = self.gradient(p2)
			if (gradient_a == 0):
				return gradient_b == self.inf
			if (gradient_b == 0):
				return gradient_a == self.inf
			return (gradient_a * gradient_b) == -1.0
		

		def equalDistances(self, p1, p2):
			return SquareValidator.sqrDist(self, p1) == SquareValidator.sqrDist(self, p2)
		
	
	@staticmethod
	def isDivisible(d, div):
		return (d % div) == 0

	@staticmethod
	def arePointsDistinct(numPoints, *points):
		pointsSet = set([p.hashCoords() for p in points])
		return len(pointsSet) == numPoints
	
	@classmethod
	def calculateSqrDistances(cls, p1, p2, p3, p4):
		sqr_d12 = cls.sqrDist(p1, p2)
		sqr_d13 = cls.sqrDist(p1, p3)
		sqr_d14 = cls.sqrDist(p1, p4)
		return sqr_d12, sqr_d13, sqr_d14

	def isSquareGradient(self, p1, p2, p3, p4):
		if not self.arePointsDistinct(4, p1, p2, p3, p4):
			return False
		sqr_d12, sqr_d13, sqr_d14 = SquareValidator.calculateSqrDistances(p1, p2, p3, p4)
		if sqr_d12 == 0 or sqr_d13 == 0 or sqr_d14 == 0:
			return False

		area = min(min(sqr_d12, sqr_d13), sqr_d14)
		if sqr_d14 == 2 * area:
			return p2.isRightAngGrad(p1, p4) and p3.isRightAngGrad(p1, p4)
		if sqr_d13 == 2 * area:
			return p2.isRightAngGrad(p1, p3) and p4.isRightAngGrad(p1, p3)
		if sqr_d12 == 2 * area:
			return p3.isRightAngGrad(p1, p2) and p4.isRightAngGrad(p1, p2)
		return False
	

	def isSquareDot(self, p1, p2, p3, p4):
		sqr_d12, sqr_d13, sqr_d14 = SquareValidator.calculateSqrDistances(p1, p2, p3, p4)
		if sqr_d12 == 0 or sqr_d13 == 0 or sqr_d14 == 0:
			return False
		area = min(min(sqr_d12, sqr_d13), sqr_d14)
		if sqr_d14 == 2 * area:
			return p1.isRightAngDot(p2, p3) and p4.isRightAngDot(p2, p3)
		if sqr_d13 == 2 * area:
			return p1.isRightAngDot(p2, p4) and p3.isRightAngDot(p2, p4)
		if sqr_d12 == 2 * area:
			return p1.isRightAngDot(p3, p4) and p2.isRightAngDot(p3, p4)
		return False
	

	def isSquareCross(self, p1, p2, p3, p4):
		if not SquareValidator.arePointsDistinct(4, p1, p2, p3, p4):
			return False
		if p1.crossProd(p2, p3) == -p1.crossProd(p2, p4): # ( p1, p2) is possible diagonal
			return p3.isRightAngDot(p1, p2) and p4.isRightAngDot(p1, p2) and p3.equalDistances(p1, p2)
		if p1.crossProd(p3, p2) == -p1.crossProd(p3, p4): # ( p1, p3) is possible diagonal
			return p2.isRightAngDot(p1, p3) and p4.isRightAngDot(p1, p3) and p2.equalDistances(p1, p3)
		if p1.crossProd(p4, p2) == -p1.crossProd(p4, p3): # ( p1, p4) is possible diagonal
			return p2.isRightAngDot(p1, p4) and p3.isRightAngDot(p1, p4) and p2.equalDistances(p1, p4)
		return False
	

	def isSquare(self, p1, p2, p3, p4):
		cls = SquareValidator
		sqr_d12, sqr_d13, sqr_d14 = cls.calculateSqrDistances(p1, p2, p3, p4)
		if sqr_d12 == 0 or sqr_d13 == 0 or sqr_d14 == 0:
			return False
		area = min(min(sqr_d12, sqr_d13), sqr_d14)
		if (not cls.isDivisible(sqr_d12, area) or 
			not cls.isDivisible(sqr_d13, area) or 
			not cls.isDivisible(sqr_d14, area) or 
			not ((sqr_d12 + sqr_d13 + sqr_d14) == 4 * area)):
			return False
		
		if sqr_d12 == 2 * area:
			return cls.sqrDist(p4, p3) == 2 * area and cls.sqrDist(p3, p2) == area and cls.sqrDist(p4, p2) == area
		if sqr_d13 == 2 * area:
			return cls.sqrDist(p4, p2) == 2 * area and cls.sqrDist(p2, p3) == area and cls.sqrDist(p4, p3) == area
		if sqr_d14 == 2 * area:
			return cls.sqrDist(p3, p2) == 2 * area and cls.sqrDist(p2, p4) == area and cls.sqrDist(p3, p4) == area
		return False
	

	def isSquareGeeksForGeeks(self, p1, p2, p3, p4):
		cls = SquareValidator
		d2 = cls.sqrDist(p1, p2) # from p1 to p2
		d3 = cls.sqrDist(p1, p3) # from p1 to p3
		d4 = cls.sqrDist(p1, p4) # from p1 to p4
		if d2 == 0 or d3 == 0 or d4 == 0:
			return False
		# f lengths if (p1, p2) and (p1, p3) area:same, then
		# following conditions must met to form a square.
		# 1) Square of length of (p1, p4) is same as twice
		# the square of (p1, p2)
		# 2) Square of length of (p2, p3) is same
		# as twice the square of (p2, p4)
		if (d2 == d3 and 2 * d2 == d4 and 2 * cls.sqrDist(p2, p4) == cls.sqrDist(p2, p3)):
			return True
		
		# The below two cases are similar to above case
		if (d3 == d4 and 2 * d3 == d2 and 2 * cls.sqrDist(p3, p2) == cls.sqrDist(p3, p4)):
			return True
		
		if (d2 == d4 and 2 * d2 == d3 and 2 * cls.sqrDist(p2, p3) == cls.sqrDist(p2, p4)):
			return True
		
		return False
	


if __name__ == '__main__':
	sqr = SquareValidator()
	squares = ((sqr.Point(20, 10), sqr.Point(10, 20), sqr.Point(20, 20), sqr.Point(10, 10)),
				(sqr.Point(1, 0), sqr.Point(4, 1), sqr.Point(3, 4), sqr.Point(0, 3)),
				(sqr.Point(0, 0), sqr.Point(3, 1), sqr.Point(2, 4), sqr.Point(-1, 3)),
				(sqr.Point(0, 0), sqr.Point(1, 0), sqr.Point(1, 1), sqr.Point(0, 1)),
				(sqr.Point(0, -1), sqr.Point(3, 0), sqr.Point(2, 3), sqr.Point(-1, 2)),
				(sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(3, 4), sqr.Point(1, 2)),
				(sqr.Point(0, 0), sqr.Point(2, 0), sqr.Point(2, 2), sqr.Point(0, 2)),
				(sqr.Point(0, 0), sqr.Point(2, 1), sqr.Point(3, -1), sqr.Point(1, -2)),
				(sqr.Point(0, -2), sqr.Point(2, 0), sqr.Point(0, 2), sqr.Point(-2, 0)))

	notSquares = ((sqr.Point(20, 10), sqr.Point(10, 20), sqr.Point(20, 20), sqr.Point(30, 10)),
				(sqr.Point(20, 10), sqr.Point(10, 20), sqr.Point(20, 20), sqr.Point(-10, 10)),
				(sqr.Point(20, 10), sqr.Point(20, 10), sqr.Point(20, 10), sqr.Point(20, 10)),
				(sqr.Point(3, 0), sqr.Point(0, 0), sqr.Point(6, -3), sqr.Point(0, 3)),
				(sqr.Point(3, 0), sqr.Point(3, 3), sqr.Point(0, 6), sqr.Point(0, 3)),
				(sqr.Point(3, 0), sqr.Point(3, 3), sqr.Point(3, 6), sqr.Point(0, 3)),
				(sqr.Point(3, 0), sqr.Point(3, 3), sqr.Point(6, 6), sqr.Point(6, 3)),
				(sqr.Point(-3, 6), sqr.Point(3, 3), sqr.Point(0, 0), sqr.Point(0, 3)),
				(sqr.Point(3, 0), sqr.Point(-3, -3), sqr.Point(0, 0), sqr.Point(0, 3)),
				(sqr.Point(3, 0), sqr.Point(3, 3), sqr.Point(6, 6), sqr.Point(0, 3)),
				(sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(-1, 0), sqr.Point(1, 2)),
				(sqr.Point(3, 0), sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(1, 2)),
				(sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(3, 0), sqr.Point(1, 2)),
				(sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(1, 2), sqr.Point(3, 0)),
				(sqr.Point(1, 0), sqr.Point(0, 1), sqr.Point(0, 0), sqr.Point(0, 0)),
				(sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(5, 2), sqr.Point(1, 2)),
				(sqr.Point(3, 0), sqr.Point(5, 2), sqr.Point(1, 2), sqr.Point(5, 2)),
				(sqr.Point(3, 0), sqr.Point(1, 2), sqr.Point(5, 2), sqr.Point(5, 2)),
				(sqr.Point(0, 0), sqr.Point(0, 0), sqr.Point(0, 0), sqr.Point(0, 0)),
				(sqr.Point(3, -1), sqr.Point(5, 2), sqr.Point(3, 4), sqr.Point(1, 2)),
				(sqr.Point(3, -1), sqr.Point(5, 2), sqr.Point(3, 5), sqr.Point(1, 2)),
				(sqr.Point(3, 0), sqr.Point(6, 2), sqr.Point(3, 4), sqr.Point(0, 2)),
				(sqr.Point(0, 0), sqr.Point(2, 0), sqr.Point(2, 1), sqr.Point(0, 1)),
				(sqr.Point(0, 2), sqr.Point(2, 1), sqr.Point(2, 3), sqr.Point(0, 4)),
				(sqr.Point(-1, 0), sqr.Point(2, 0), sqr.Point(2, 1), sqr.Point(-1, 1)),
				(sqr.Point(0, -2), sqr.Point(2, 2), sqr.Point(0, 2), sqr.Point(-3, 1)),
				(sqr.Point(1, 1), sqr.Point(4, 1), sqr.Point(3, 4), sqr.Point(0, 3)),
				(sqr.Point(0, 0), sqr.Point(-3, 1), sqr.Point(2, 4), sqr.Point(-1, 3)),
				(sqr.Point(0, 0), sqr.Point(1, 0), sqr.Point(1, 1), sqr.Point(1, 1)),
				(sqr.Point(0, -1), sqr.Point(3, 0), sqr.Point(2, 3), sqr.Point(1, 2)),
				(sqr.Point(3, 0), sqr.Point(3, 2), sqr.Point(3, 4), sqr.Point(1, 2)),
				(sqr.Point(0, 0), sqr.Point(3, 0), sqr.Point(2, 2), sqr.Point(0, 2)),
				(sqr.Point(0, -2), sqr.Point(2, 0), sqr.Point(0, 2), sqr.Point(-2, 1)))

	FalseNegs = 0
	FalsePostvs = 0
	# print("Squares: ")
	for points in squares:
		for i in range(4): 
			points = deque(points) 
			points.rotate(i) 
			points = list(points) 
			# print(["({}, {})".format(p.x, p.y) for p in points])
			assert sqr.isSquare(points[0], points[1], points[2], points[3])
			assert sqr.isSquareCross(points[0], points[1], points[2], points[3])
			assert sqr.isSquareDot(points[0], points[1], points[2], points[3])
			assert sqr.isSquareGradient(points[0], points[1], points[2], points[3])
			if not sqr.isSquareGeeksForGeeks(points[0], points[1], points[2], points[3]):
				FalseNegs += 1

	# print("Not Squares: ")
	for points in notSquares:
		for i in range(4): 
			points = deque(points) 
			points.rotate(i) 
			points = list(points) 
			# print(["({}, {})".format(p.x, p.y) for p in points])
			assert not sqr.isSquare(points[0], points[1], points[2], points[3])
			assert not sqr.isSquareCross(points[0], points[1], points[2], points[3])
			assert not sqr.isSquareDot(points[0], points[1], points[2], points[3])
			assert not sqr.isSquareGradient(points[0], points[1], points[2], points[3])
			if sqr.isSquareGeeksForGeeks(points[0], points[1], points[2], points[3]):
				FalsePostvs += 1		
	print("Errors in GeeksForGeeks solution:")
	print("False positives: {}".format(FalsePostvs))
	print("False negatives: {}".format(FalseNegs))
  
