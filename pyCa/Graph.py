from . import *

# Graphics Stuff
import matplotlib.pyplot as plt


class Graph(object):

    """docstring for Graph"""

    def __init__(self, Experiment):
        self.Experiment = Experiment
        self.numberOfStimulantsAdded = 0
        self.nameToUse = 0

    def plot(self):
        print ''
        log(self.Experiment.name, colour="yellow")
        log('==================', colour="yellow")

        for i, col in self.Experiment.data.iteritems():

            if i == 0:
                col.name = "time"

            if col.name == "time":
                continue

            fig, ax = plt.subplots(1)
            plt.plot(self.Experiment.data.time, col, '-')
            plt.title(col.name)
            ax.set_ylim(
                col.min() - (0.1 * col.min()), col.max() + (0.1 * col.max()))
            self.nameToUse = 0

            print ''
            log(col.name, colour="red")
            log('--------------------------------------', colour="red")

            def onclick(event):

                if self.numberOfStimulantsAdded == 0:
                    x1 = event.xdata
                    y1 = event.ydata

                    log(' > 1st point, adding x1:{} y1:{} to {}'.format(
                        x1, y1, self.Experiment.names[self.nameToUse]),
                        colour="black")

                    self.Experiment.currentCell.addFirstPoint(x1, y1)
                    self.numberOfStimulantsAdded = 1
                elif self.numberOfStimulantsAdded == 1:
                    x2 = event.xdata
                    y2 = event.ydata

                    log(' > 2nd point, adding x2:{} y2:{} to {}'.format(
                        x2, y2, self.Experiment.names[self.nameToUse]),
                        colour="black")

                    self.Experiment.currentCell.addSecondPointWithName(
                        x2, y2, self.Experiment.names[self.nameToUse])
                    self.numberOfStimulantsAdded = 0
                    self.nameToUse = self.nameToUse + 1

            fig.canvas.mpl_connect('button_press_event', onclick)

            for t in self.Experiment.times:
                plt.axvspan(t, t + 5, color='red', alpha=0.1)

            plt.show()

            self.Experiment.currentCell.cellname = col.name
            self.Experiment.cells.append(self.Experiment.currentCell)

            if self.Experiment.currentCell.describe() is not None:
                log(self.Experiment.currentCell.describe(),
                    colour="black")

            self.Experiment.currentCell = Cell()
