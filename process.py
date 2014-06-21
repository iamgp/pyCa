# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import yaml

from pyCa import *

if __name__ == '__main__':

	exp_folder = ''
	treatment_folder = exp_folder + ''

	scanDirAndSetUpExperiments(treatment_folder + 'settings.yaml')