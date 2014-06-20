# -*- coding: utf-8 -*-
import os, sys
import xlrd
import csv
import os.path
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl

from mpltools import style
from mpltools import layout
style.use('ggplot')

class Point(dict):
	"""Python Objects that act like Javascript Objects"""
	def __init__(self, *args, **kwargs):
		super(Point, self).__init__(*args, **kwargs)
		self.__dict__ = self

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


numberOfStimulantsAdded = 0
nameToUse = 0

class Experiment(object):
	"""docstring for Experiment"""
	def __init__(self, name, directory):
		self.name = name
		self.directory = os.path.abspath(os.path.expanduser(directory)) + "/"
		self.cells = []
		self.names = []
		self.currentCell = Cell()
		self.times = []

		try:
			with open(self.directory + self.name+'.csv') as file:
				self.data = pd.read_csv(file)
			pass
		except IOError as e:
			self.convertXLSX()
			with open(self.directory + self.name+'.csv') as file:
				self.data = pd.read_csv(file)
			pass

	def convertXLSX(self):
			wb = xlrd.open_workbook(self.directory + self.name+".xlsx")
			sh = wb.sheet_by_name('Data1')
			your_csv_file = open(self.directory + self.name+'.csv', 'wb')
			wr = csv.writer(your_csv_file)

			for rownum in xrange(sh.nrows):
				wr.writerow(sh.row_values(rownum))

			print 'Converted'

	def plotTrace(self):
		for i, col in self.data.iteritems():

			if col.name == "time":
				continue

			fig, ax = plt.subplots(1)
			plt.plot(self.data.time, col, '-')
			plt.title(col.name)
			global nameToUse
			nameToUse = 0

			def onclick(event):
				global numberOfStimulantsAdded
				global nameToUse

				if numberOfStimulantsAdded == 0:
					x1 = event.xdata
					y1 = event.ydata

					#print '1st point, adding x1:{} y1:{}'.format(x1,y1)
					self.currentCell.addFirstPoint(x1, y1)
					numberOfStimulantsAdded = 1
				elif numberOfStimulantsAdded == 1:
					x2 = event.xdata
					y2 = event.ydata

					#print '2nd point, adding x2:{} y2:{} to {} out of {} with nametouse: {}'.format(x2,y2,self.names[nameToUse], self.names, nameToUse)

					self.currentCell.addSecondPointWithName(x2, y2, self.names[nameToUse])
					numberOfStimulantsAdded = 0
					nameToUse = nameToUse + 1

			if nameToUse == len(self.names):
				continue

			cid = fig.canvas.mpl_connect('button_press_event', onclick)

			for t in self.times:
				plt.axvspan(t, t+15, color='blue', alpha=0.1)

			plt.show()
			self.currentCell.cellname = col.name
			self.cells.append(self.currentCell)
			self.currentCell = Cell()

	def save_csv(self, concat, type):
		concat.to_csv(self.directory + self.name + "-compiled-"+ type.upper() +".csv")
		print concat

	def combineAllCsvsInDir(self):
		bigDF = []

		for f in glob.glob(self.directory+"*compiled-GRADIENT.csv"):
			df = pd.read_csv(f)
			bigDF.append(df)

		concat = pd.concat(bigDF)
		concat = concat.replace([np.inf, -np.inf], np.nan).dropna()

		concat.to_csv(self.directory + self.name + "-aggregated-GRADIENT.csv")
		del(concat)
		del(bigDF)
		bigDF = []

		for f in glob.glob(self.directory+"*compiled-BP.csv"):
			df = pd.read_csv(f)
			bigDF.append(df)

		concat = pd.concat(bigDF)
		concat = concat.replace([np.inf, -np.inf], np.nan).dropna()

		concat.to_csv(self.directory + self.name + "-aggregated-BP.csv")

if __name__ == '__main__':

	experiment = Experiment (
		name="Cond Media - n=1 - 18th June",
		directory = "/Users/garethprice/Desktop/5. 5mM CM CM+ab M ~ 10uM/Conditioned Media"
	)

	experiment.names = ['ADP', 'ATP', 'UTP']
	experiment.times = [101, 299, 682]
	experiment.plotTrace()

	gdfs = []
	bpdfs = []
	for e in experiment.cells:

		print ''
		print e.cellname
		print '-------------------'
		print e.describe()
		gdfs.append(e.makePandasDF()['g'])
		bpdfs.append(e.makePandasDF()['bp'])

	experiment.save_csv( pd.concat(gdfs, axis=1).T, 'gradient')
	experiment.save_csv( pd.concat(bpdfs, axis=1).T, 'bp')

	experiment.combineAllCsvsInDir()

	sys.exit()
