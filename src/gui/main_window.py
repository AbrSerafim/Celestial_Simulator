""" Main application window """

import numpy as np
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QInputDialog
)

from gui.dynamic_gui import DynamicGui
from gui.static_gui import StaticGui

import simulation.bodies as bodies
import simulation.physics as physics

from database.database import Database

class MainWindow(QMainWindow):
    """ Main window """

    def __init__(self, system: bodies.CelestialSystem, simulation: physics.Simulation):
        super().__init__()

        self.system = system
        self.simulation = simulation
        self.database = Database()

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

        self.static_gui.save_button.clicked.connect(
            self.save_system
        )

        self.static_gui.load_button.clicked.connect(
            self.load_system
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

    def save_system(self):
        """ Save the current system state to the database """

        system_name, accepted = QInputDialog.getText(
            self,
            "Save System",
            "System name:"
        )

        if not accepted:
            return 

        system_name = system_name.strip()

        if not system_name:
            return

        # Update system name
        self.system.name = system_name

        # Update windows title
        self.setWindowTitle(system_name)

        # Save to database
        self.database.save_system(self.system)

    def load_system(self):
        """ Load a saved system from the database """

        systems = self.database.get_systems()

        if not systems:
            return

        system_name = [
            system[1]
            for system in systems
        ]

        selected_name, accepted = QInputDialog.getItem(
            self,
            "Load System",
            "Select a system:",
            system_name,
            0,
            False
        )

        if not accepted:
            return

        # Find selected system ID
        selected_id = None

        for system in systems:
            if system[1] == selected_name:
                selected_id = system[0]
                break

        if selected_id is None:
            return

        # Load system from database
        loaded_system = self.database.load_system(
            selected_id
        )

        if self.load_system is None:
            return

        # Stop current simulation
        self.dynamic_gui.stop()

        # Replace system
        self.system = loaded_system

        # Replace system used by static GUI
        self.static_gui.system = loaded_system

        # Rebuild dynamic GUI
        self.dynamic_gui.reload_system(loaded_system)
        self.simulation.update_accelerations(loaded_system)

        # Update GUI
        self.static_gui.update_body_selector()
        self.static_gui.update_information()

        # Update window titles
        self.setWindowTitle(loaded_system.name)

    def add_body(self):
        """ Add a body to the simulation """

        name = self.static_gui.name_input.text()

        mass = float(self.static_gui.mass_input.text().replace(".",".").replace(",",".").replace("","0"))
        radius = float(self.static_gui.radius_input.text().replace(".",".").replace(",",".").replace("","0"))

        x = float(self.static_gui.x_input.text().replace(".",".").replace(",",".").replace("","0"))
        y = float(self.static_gui.y_input.text().replace(".",".").replace(",",".").replace("","0"))

        vx = float(self.static_gui.vx_input.text().replace(".",".").replace(",",".").replace("","0"))
        vy = float(self.static_gui.vy_input.text().replace(".",".").replace(",",".").replace("","0"))

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