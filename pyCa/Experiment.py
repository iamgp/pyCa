# System Stuff
import os
import os.path
import glob

# Data Stuff
import xlrd
import csv
import yaml

# Maths Stuff
import pandas as pd
import numpy as np

# pyCa Stuff
from Helpers import *
from Cell import *
from Stimulant import *
from Graph import Graph

# Globals
numberOfStimulantsAdded = 0
nameToUse = 0


def aggregateData(directory):
    directory = os.path.abspath(os.path.expanduser(directory)) + "/"

    # variables
    bigDF = []
    for f in glob.glob(directory + "*compiled-BP.csv"):
        df = pd.read_csv(f)
        bigDF.append(df)

    concat = pd.concat(bigDF)
    concat = concat.replace([np.inf, -np.inf], np.nan).dropna()
    concat.to_csv(directory + "aggregated-BP.csv")


def scanDirAndSetUpExperiments(directory):
    with open(os.path.abspath(os.path.expanduser(directory))) as f:
        y = yaml.load(f)

    for index, a in enumerate(y):
        test = os.path.abspath(
            os.path.dirname(directory) + "/" + a[
                'name'] + "-compiled-BP.csv"
        )
        if os.path.exists(test):
            print 'skipping ' + a['name']
            continue

        names, times = [], []
        stimulants = sorted(a['stimulants'], key=lambda k: k['time'])
        for b in stimulants:
            names.append(b['name'])
            times.append(b['time'])

        e = Experiment(
            name=a['name'],
            directory=os.path.dirname(directory)
        )
        e.names = names
        e.times = times
        e.plotTrace()

        gdfs = []
        bpdfs = []
        for expt in e.cells:
            gdfs.append(expt.makePandasDF()['g'])
            bpdfs.append(expt.makePandasDF()['bp'])

        e.save_csv(pd.concat(gdfs, axis=1).T, 'gradient')
        e.save_csv(pd.concat(bpdfs, axis=1).T, 'bp')

        if (index + 1) == len(y):
            e.combineAllCsvsInDir()


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
            with open(self.directory + self.name + '.csv') as file:
                self.data = pd.read_csv(file)
            pass
        except IOError:
            self.convertXLSX()
            with open(self.directory + self.name + '.csv') as file:
                self.data = pd.read_csv(file)
            pass

    def convertXLSX(self):
        wb = xlrd.open_workbook(self.directory + self.name + ".xlsx")
        sh = wb.sheet_by_name('Sheet1')
        your_csv_file = open(self.directory + self.name + '.csv', 'wb')
        wr = csv.writer(your_csv_file)

        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        print 'Converted'

    def plotTrace(self):
        g = Graph(Experiment=self)
        g.plot()

    def save_csv(self, concat, type):
        concat.to_csv(
            self.directory + self.name + "-compiled-" + type.upper() + ".csv")

    def combineAllCsvsInDir(self):
        bigDF = []

        for f in glob.glob(self.directory + "*compiled-GRADIENT.csv"):
            df = pd.read_csv(f)
            bigDF.append(df)

        concat = pd.concat(bigDF)
        concat = concat.replace([np.inf, -np.inf], np.nan).dropna()

        concat.to_csv(self.directory + "aggregated-GRADIENT.csv")
        del (concat)
        del (bigDF)
        bigDF = []

        for f in glob.glob(self.directory + "*compiled-BP.csv"):
            df = pd.read_csv(f)
            bigDF.append(df)

        concat = pd.concat(bigDF)
        concat = concat.replace([np.inf, -np.inf], np.nan).dropna()

        concat.to_csv(self.directory + "aggregated-BP.csv")
