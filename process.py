# -*- coding: utf-8 -*-
import os
import xlrd
import csv
import os.path
import pandas as pd
import numpy as np

class Experiment(object):
	"""docstring for Experiment"""
	def __init__(self, name, directory):
		self.name = name
		self.directory = os.path.abspath(os.path.expanduser(directory)) + "/"

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
		from ggplot import *

		print ggplot(aes(x='time', y='cell1'), \
			data=self.data) +\
			theme_bw() +\
			stat_smooth(span=0.08, colour='navy')

if __name__ == '__main__':

	e = Experiment(
		name="test",
		directory = "~/Desktop/Ca"
	).plotTrace()