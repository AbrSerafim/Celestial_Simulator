""" Orchestrator of the project """

import sys

from PySide6.QtWidgets import QApplication
from pathlib import Path

from gui.main_window import MainWindow

import simulation.bodies as bodies
import simulation.physics as physics

class Controller:
    """ Controls the application """

    def __init__(self):

        self.app = QApplication(sys.argv)

        # Load stylesheet
        stylesheet_path = (
            Path(__file__).parent
            / "gui"
            / "styles"
            / "dark.qss"
        )

        with open(stylesheet_path, "r", encoding="utf-8") as file:
            self.app.setStyleSheet(file.read())

        self.system = bodies.CelestialSystem(name="Simulador Celeste")
        self.simulation = physics.Simulation()

        self.main_window = MainWindow(
            system=self.system,
            simulation=self.simulation
        )

    def run(self):
        """ Start the application """

        self.main_window.show()

        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = Controller()
    controller.run()