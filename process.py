# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import yaml

from pyCa import *

if __name__ == '__main__':

	exp_folder = '~/Dropbox/PhD/Data/Calcium Microfluorimetry/5. 5mM CM CM+ab M ~ 10uM/'
	treatment_folder = exp_folder + 'Conditioned Media/'

	scanDirAndSetUpExperiments(treatment_folder + 'settings.yaml')