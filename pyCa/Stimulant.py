from Point import *

class Stimulant(object):
	"""docstring for Stimulant"""
	def __init__(self):
		self.p1 = Point(x=None, y=None)
		self.p2 = Point(x=None, y=None)
		self.name = None

	def description(self):
		return '{0}: B-P: {1:.3},  G: {2:.3}'.format(self.name, self.basalToPeak(), self.gradient())

	def gradient(self):
		return (float(self.p2.y) - self.p1.y) / (self.p2.x - self.p1.x)

	def basalToPeak(self):
		return (float(self.p2.y) - self.p1.y)
