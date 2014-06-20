
# System Stuff
import os, sys
import os.path
import glob

# Data Stuff
import xlrd
import csv

# Maths Stuff
import pandas as pd
import numpy as np

# Graphics Stuff
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpltools import style
style.use('ggplot')

# pyCa Stuff
from Helpers import *
from Cell import *
from Stimulant import *

# Globals
numberOfStimulantsAdded = 0
nameToUse = 0

class Experiment(object):
	"""docstring for Experiment"""
	def __init__(self, name, directory):

		# Initialise properties
		self.name = name
		self.directory = os.path.abspath(os.path.expanduser(directory)) + "/"
		self.cells = []
		self.names = []
		self.currentCell = Cell()
		self.times = []

		# Let's get our data
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
			ax.set_ylim(col.min() - (0.1*col.min()), col.max() + (0.1*col.max()))
			global nameToUse
			nameToUse = 0

			print ''
			log(col.name, colour="red")
			log('-------------------', colour="red")


			def onclick(event):
				global numberOfStimulantsAdded
				global nameToUse

				if numberOfStimulantsAdded == 0:
					x1 = event.xdata
					y1 = event.ydata

					log('1st point, adding x1:{} y1:{} to {}'.format(x1,y1,self.names[nameToUse]), colour="black")

					self.currentCell.addFirstPoint(x1, y1)
					numberOfStimulantsAdded = 1
				elif numberOfStimulantsAdded == 1:
					x2 = event.xdata
					y2 = event.ydata

					log('2nd point, adding x2:{} y2:{} to {}'.format(x2,y2,self.names[nameToUse]), colour="black")

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

			if self.currentCell.describe() is not None:
				log(self.currentCell.describe(), colour="blue")

			self.currentCell = Cell()

	def save_csv(self, concat, type):
		concat.to_csv(self.directory + self.name + "-compiled-"+ type.upper() +".csv")

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