# -*- coding: utf-8 -*-
import os
import xlrd
import csv
import os.path
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

from mpltools import style
from mpltools import layout
style.use('ggplot')

from helpers import namedTuple

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

	def gradient(self):
		return (float(self.p2.y) - self.p1.y) / (self.p2.x - self.p1.x)

	def basalToPeak(self):
		return (float(self.p2.y) - self.p1.y)

class Cell(object):
	"""docstring for Cell"""
	def __init__(self):
		self.stimulants = {}

	def addStimulant(self, event):
		s = Stimulant()

		s.p1.x = x1
		s.p1.y = y1
		s.p2.x = x2
		s.p2.y = y2

		self.stimulants[name] = s

class Experiment(object):
	"""docstring for Experiment"""
	def __init__(self, name, directory):
		self.name = name
		self.directory = os.path.abspath(os.path.expanduser(directory)) + "/"

		self.cells = []

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

	def onclick(event):
	    #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
	    #    event.button, event.x, event.y, event.xdata, event.ydata)
		i = 0
		if i == 0:
	    	x1, y1 = event.xdata, event.ydata
	    	i = 1
	    elif i == 1:
			x2, y2 = event.xdata, event.ydata
			c = Cell()
			c.addStimulant('Test', x1, y1, x2, y2)
			x1, y1, x2, y2 = None, None, None, None
			i = 0


	def plotTrace(self):
		fig, ax = plt.subplots(1)
		plt.plot(self.data.time, self.data.cell1, '-')




		cid = fig.canvas.mpl_connect('button_press_event', onclick)
		plt.axvspan(200, 220, color='red', alpha=0.1)

		plt.show()
		self.cells.append(c)


	def split(self):
		for i in self.data.cell1:
			print i

if __name__ == '__main__':

	e = Experiment (
		name="test",
		directory = "~/Desktop/Ca"
	).plotTrace()