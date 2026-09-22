""" Code to handle the static elements of the GUI """

from PySide6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSizePolicy,
    QPushButton,
    QGroupBox
)

import simulation.bodies as bodies
import simulation.physics as physics

class StaticGui(QWidget):
    """ Handles the static controls and info of the GUI """

    def __init__(self, system: bodies.CelestialSystem, simulation: physics.Simulation):
        super().__init__()

        self.system = system
        self.simulation = simulation

        self.setMinimumWidth(280)
        self.setMaximumWidth(350)

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        """ Create the GUI widgets """

        # Simulation group
        self.simulation_group = QGroupBox("Simulation")

        # Simulation controls
        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")
        self.step_button = QPushButton("Step")
        self.add_body_button = QPushButton("Add Body")
        self.remove_body_button = QPushButton("Remove Body")


    def _create_layout(self):
        """ Create and arrange the GUI layout """

        # -----------------------------------
        # Simulation controls
        # -----------------------------------

        simulation_row = QHBoxLayout()

        simulation_row.addWidget(self.start_button)
        simulation_row.addWidget(self.pause_button)
        simulation_row.addWidget(self.reset_button)
        simulation_row.addWidget(self.step_button)

        body_row = QHBoxLayout()

        body_row.addWidget(self.add_body_button)
        body_row.addWidget(self.remove_body_button)
        self.add_body_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        self.remove_body_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        simulation_layout = QVBoxLayout()

        simulation_layout.addLayout(simulation_row)
        simulation_layout.addLayout(body_row)

        self.simulation_group.setLayout(simulation_layout)

        # -----------------------------------
        # Main layout
        # -----------------------------------

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.simulation_group)

        # Push everything to the top
        main_layout.addStretch()

        self.setLayout(main_layout)


if __name__ == "__main__":
    pass