""" Code to handle the dynamical elements of the simulation (celestial system) """

import sys

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

import simulation.bodies as bodies
import simulation.physics as physics


class DynamicGui:
    """ Handles the simulation visualization """

    def __init__(self, system: bodies.CelestialSystem, simulation: physics.Simulation):

        self.system = system
        self.simulation = simulation

        # Create Qt Application
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

        # -----------------------------------
        # Create plot
        # -----------------------------------
        self.plot = pg.PlotWidget()

        self.plot.setWindowTitle(system.name)

        # Keep x/y scales equal
        self.plot.setAspectLocked(True)

        # Grid
        self.plot.showGrid(x=False, y=False)

        # Plot range
        self.plot.setRange(xRange=(-10, 10),
                           yRange=(-10, 10))

        # -----------------------------------
        # Store graphical objects
        # -----------------------------------
        self.body_items = []
        self._create_body_items()

        # -----------------------------------
        # Timer controls the simulation loop
        # -----------------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self._step)

    def _create_body_items(self):
        """ Create a graphical item for every celestial body """

        for body in self.system.bodies:

            item = pg.ScatterPlotItem(
                x=[body.pos[0]],
                y=[body.pos[1]],
                size=10
            )

            self.plot.addItem(item)
            self.body_items.append(item)

    def _step(self):
        """ Advance simulation and update visualization """

        # Physics
        self.simulation.step(system=self.system)

        # Visualization
        self.update()

    def update(self):
        """ Update graphical posistions from the system """

        for body, item in zip(
            self.system.bodies,
            self.body_items
        ):

            item.setData(
                x=[body.pos[0]],
                y=[body.pos[1]],
            )

    def start(self, fps: float = 60):
        """ Start simulation loop """
        self.timer.start(int(1000/fps)) # 60 fps (ms)

    def stop(self):
        """ Stop simulation loop """
        self.timer.stop()

    def show(self): # Equivalent to a while loop using event 
        """ Display GUI """
        self.plot.show() 
        self.start()
        self.app.exec()


if __name__ == "__main__":
    pass