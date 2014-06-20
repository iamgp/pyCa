from Stimulant import *
import pandas as pd


class Cell(object):
	"""docstring for Cell"""
	def __init__(self):
		self.stimulants = {}
		self.stimulant = Stimulant()

		self.p1 = Point()
		self.p2 = Point()

		self.p1.x = 0
		self.p1.y = 0
		self.p2.x = 0
		self.p2.y = 0

		self.cellname = ''

	def reset(self):
		self.p1 = Point()
		self.p2 = Point()

		self.p1.x = 0
		self.p1.y = 0
		self.p2.x = 0
		self.p2.y = 0

	def addFirstPoint(self, x, y):
		self.p1.x = x
		self.p1.y = y
		self.stimulant.p1 = self.p1

	def addSecondPointWithName(self, x, y, name):
		self.p2.x = x
		self.p2.y = y
		self.stimulant.p2 = self.p2
		self.stimulant.name = name

		self.stimulants[name] = self.stimulant

		del(self.stimulant)
		del(self.p1)
		del(self.p2)
		self.stimulant = Stimulant()
		self.p1 = Point()
		self.p2 = Point()

	def makePandasDF(self):
		bpdict = {}
		gdict = {}
		for s in self.stimulants:
			bpdict[self.stimulants[s].name] = self.stimulants[s].basalToPeak()
			gdict[self.stimulants[s].name] = self.stimulants[s].gradient()
		return {'bp':pd.DataFrame.from_dict({self.cellname: bpdict}), 'g':pd.DataFrame.from_dict({self.cellname: gdict})}

	def describe(self):
		for s in self.stimulants:
			print self.stimulants[s].description()
