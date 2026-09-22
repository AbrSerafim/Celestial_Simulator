""" Main application window """

import numpy as np
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout
)

from gui.dynamic_gui import DynamicGui
from gui.static_gui import StaticGui

import simulation.bodies as bodies
import simulation.physics as physics

class MainWindow(QMainWindow):
    """ Main window """

    def __init__(self, system: bodies.CelestialSystem, simulation: physics.Simulation):
        super().__init__()

        self.system = system
        self.simulation = simulation

        self._create_gui()
        self._create_layout()
        self._connect_signals()

        self.setWindowTitle(system.name)

    def _create_gui(self):
        """ Create the GUI components """

        self.static_gui = StaticGui(
            self.system,
            self.simulation
        )
        
        self.dynamic_gui = DynamicGui(
            self.system,
            self.simulation,
            self.static_gui.update_information
        )

        self.static_gui.update_body_selector()
        self.static_gui.update_information()

    def _create_layout(self):
        """ Arrange the GUI components """

        central_widget = QWidget()

        layout = QVBoxLayout()
        row = QHBoxLayout()

        row.addLayout(self.static_gui.body_layout)
        row.addWidget(self.dynamic_gui.plot)

        layout.addLayout(row)
        layout.addWidget(self.static_gui.kinematics_group)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def _connect_signals(self):
        """ Connect GUI signlas to application actions """

        self.static_gui.start_button.clicked.connect(
            self.start_simulation
        )

        self.static_gui.pause_button.clicked.connect(
            self.pause_simulation
        )

        self.static_gui.step_button.clicked.connect(
            self.step_simulation
        )

        self.static_gui.add_button.clicked.connect(
            self.add_body
        )

        self.static_gui.remove_button.clicked.connect(
            self.remove_body
        )

    def start_simulation(self):
        """ Start the simulation """
        self.dynamic_gui.start()

    def pause_simulation(self):
        """ Pause the simulation """
        self.dynamic_gui.stop()

    def step_simulation(self):
        """ Advance the simulation by one step """
        self.dynamic_gui.step()
        self.static_gui.update_information()

    def add_body(self):
        """ Add a body to the simulation """

        name = self.static_gui.name_input.text()

        mass = float(self.static_gui.mass_input.text().replace(",","."))
        radius = float(self.static_gui.radius_input.text().replace(",","."))

        x = float(self.static_gui.x_input.text().replace(",","."))
        y = float(self.static_gui.y_input.text().replace(",","."))

        vx = float(self.static_gui.vx_input.text().replace(",","."))
        vy = float(self.static_gui.vy_input.text().replace(",","."))

        pos = np.array([x, y], dtype=np.float64)
        vel = np.array([vx, vy], dtype=np.float64)

        self.dynamic_gui.add_body(
            name=name,
            mass=mass,
            radius=radius,
            pos=pos,
            vel=vel
        )

        self.static_gui.update_body_selector()
        self.static_gui.update_information()

    def remove_body(self):
        """ Remove a body from the simulation """

        name = self.static_gui.body_selector.currentText()

        self.dynamic_gui.remove_body(name)

        self.static_gui.update_body_selector()
        self.static_gui.update_information()

if __name__ == "__main__":
    pass