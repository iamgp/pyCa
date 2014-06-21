from Tkinter import *
import tkFileDialog

class GUI(object):
	"""docstring for GUI"""
	def __init__(self):
		self.root = Tk()

	def setUp(self):
		Label(self.root, text='Hi').pack()

		self.root.withdraw()
