""" Code to handle the dynamical elements of the simulation (celestial system) """

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QTimer

import simulation.bodies as bodies
import simulation.physics as physics


class DynamicGui:
    """ Handles the simulation visualization """

    def __init__(self,
                 system: bodies.CelestialSystem,
                 simulation: physics.Simulation,
                 update_callback=None):

        self.system = system
        self.simulation = simulation

        self.update_callback = update_callback

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
        self.timer.timeout.connect(self.step)

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

    def step(self):
        """ Advance simulation and update visualization """

        # Physics
        self.simulation.step(system=self.system)

        # Visualization
        self.update()

        # Static GUI
        if self.update_callback is not None:
            self.update_callback()

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

    def add_body(
            self,
            name: str,
            mass: float,
            radius: float,
            pos: np.array,
            vel: np.array
    ):
        """ Add a body to the simulation and visualization """

        # Add body to simulation
        self.system.add_body(
            name=name,
            mass=mass,
            radius=radius,
            pos=pos,
            vel=vel
        )

        # Fetches newly created body
        body = self.system.bodies[-1]

        # Create graphical representation
        item = pg.ScatterPlotItem(
            x=[body.pos[0]],
            y=[body.pos[1]],
            size=10
        )

        self.plot.addItem(item)
        self.body_items.append(item)

    def remove_body(self, body_name: str):
        """ Remove a body from the simulation and visualization """

        for i, body in enumerate(self.system.bodies):
            if body.name == body_name:

                self.plot.removeItem(self.body_items.pop(i)) # Vis
                self.system.remove_body(body_name) # Sim

                break


if __name__ == "__main__":
    pass