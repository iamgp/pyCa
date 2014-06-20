# -*- coding: utf-8 -*-
import os, sys
import pandas as pd

from pyCa import *

if __name__ == '__main__':

	experiment = Experiment (
		name="test",
		directory = "~/Desktop/Ca"
	)
	experiment.names = ['UTP', 'ATP', 'ADP']
	experiment.times = [100, 301,  408]
	experiment.plotTrace()
	gdfs = []
	bpdfs = []

	for e in experiment.cells:
		gdfs.append(e.makePandasDF()['g'])
		bpdfs.append(e.makePandasDF()['bp'])

	experiment.save_csv( pd.concat(gdfs, axis=1).T, 'gradient')
	experiment.save_csv( pd.concat(bpdfs, axis=1).T, 'bp')



	sys.exit()
	# experiment = Experiment (
	# 	name="Cond Media - n=1 - 18th June",
	# 	directory = "/Users/garethprice/Desktop/5. 5mM CM CM+ab M ~ 10uM/Conditioned Media"
	# )

	# experiment.names = ['ADP', 'ATP', 'UTP']
	# experiment.times = [101, 299,  508]

	experiment = Experiment (
		name="Cond Media - n=1 - 18th June",
		directory = "/Users/garethprice/Desktop/5. 5mM CM CM+ab M ~ 10uM/Conditioned Media"
	)

	experiment.names = ['UTP', 'ATP', 'ADP']
	experiment.times = [100, 301,  408]

	experiment = Experiment (
		name="Cond Media - n=1 - 18th June",
		directory = "/Users/garethprice/Desktop/5. 5mM CM CM+ab M ~ 10uM/Conditioned Media"
	)

	experiment.names = ['ATP', 'UTP', 'ADP']
	experiment.times = [97, 313,  566]

	experiment = Experiment (
		name="Cond Media - n=1 - 18th June",
		directory = "/Users/garethprice/Desktop/5. 5mM CM CM+ab M ~ 10uM/Conditioned Media"
	)

	experiment.names = ['ATP', 'ADP', 'UTP']
	experiment.times = [97, 292, 597]


	experiment.plotTrace()

	gdfs = []
	bpdfs = []
	for e in experiment.cells:

		# print ''
		# print e.cellname
		# print '-------------------'
		# print e.describe()
		gdfs.append(e.makePandasDF()['g'])
		bpdfs.append(e.makePandasDF()['bp'])

	experiment.save_csv( pd.concat(gdfs, axis=1).T, 'gradient')
	experiment.save_csv( pd.concat(bpdfs, axis=1).T, 'bp')

	#experiment.combineAllCsvsInDir()

	sys.exit()
