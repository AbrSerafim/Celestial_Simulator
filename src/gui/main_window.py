""" Main application window """

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
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

        self.dynamic_gui = DynamicGui(
            self.system,
            self.simulation
        )

        self.static_gui = StaticGui(
            self.system,
            self.simulation
        )

    def _create_layout(self):
        """ Arrange the GUI components """

        central_widget = QWidget()
        layout = QHBoxLayout()

        layout.addWidget(self.dynamic_gui.plot)
        layout.addWidget(self.static_gui)

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

        self.static_gui.reset_button.clicked.connect(
            self.reset_simulation
        )

        self.static_gui.step_button.clicked.connect(
            self.step_simulation
        )

        self.static_gui.add_body_button.clicked.connect(
            self.add_body_simulation
        )

        self.static_gui.remove_body_button.clicked.connect(
            self.remove_body_simulation
        )

    def start_simulation(self):
        """ Start the simulation """
        self.dynamic_gui.start()

    def pause_simulation(self):
        """ Pause the simulation """
        self.dynamic_gui.stop()

    def reset_simulation(self):
        print("Reset")

    def step_simulation(self):
        """ Advance the simulation by one step """
        self.dynamic_gui._step()


if __name__ == "__main__":
    pass