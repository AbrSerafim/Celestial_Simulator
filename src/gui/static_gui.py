""" Code to handle the static elements of the GUI """

from PySide6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QLabel,
    QLineEdit,
    QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator

import simulation.bodies as bodies
import simulation.physics as physics

def create_number_input(value):
    input_box = QLineEdit()

    validator = QDoubleValidator()
    validator.setNotation(QDoubleValidator.Notation.ScientificNotation)

    input_box.setValidator(validator)
    input_box.setText(f"{value:g}")

    return input_box

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

        # -----------------------------------------------------
        # Simulation controls
        # -----------------------------------------------------

        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.step_button = QPushButton("Step")

        # -----------------------------------------------------
        # Add body
        # -----------------------------------------------------

        self.name_input = QLineEdit()

        self.mass_input = create_number_input(1e10)
        self.radius_input = create_number_input(1e1)

        self.x_input = create_number_input(0.0)
        self.y_input = create_number_input(0.0)      

        self.vx_input = create_number_input(0.0)
        self.vy_input = create_number_input(0.0)

        self.add_button = QPushButton("Add Body")

        # -----------------------------------------------------
        # Remove body
        # -----------------------------------------------------

        self.body_selector = QComboBox()
        self.remove_button = QPushButton("Remove Body")

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        self.time_label = QLabel("Time: 0.00s")
        self.bodies_label = QLabel("Bodies: 0")

        # -----------------------------------------------------
        # Body information
        # -----------------------------------------------------

        self.x_label = QLabel("X: 0")
        self.y_label = QLabel("Y: 0")

        self.vx_label = QLabel("Vx: 0")
        self.vy_label = QLabel("Vy: 0")

        self.ax_label = QLabel("Ax: 0")
        self.ay_label = QLabel("Ay: 0")

    def _create_layout(self):
        """ Create GUI layout """

        # -----------------------------------------------------
        # Simulation group
        # -----------------------------------------------------

        simulation_group = QGroupBox("Simulation")
        simulation_layout = QHBoxLayout()

        simulation_layout.addWidget(self.start_button)
        simulation_layout.addWidget(self.pause_button)
        simulation_layout.addWidget(self.step_button)

        simulation_group.setLayout(simulation_layout)

        # -----------------------------------------------------
        # Add body group
        # -----------------------------------------------------

        add_group = QGroupBox("Add Body")
        add_layout = QVBoxLayout()

        # Name
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Name:"))
        name_row.addWidget(self.name_input)

        # Mass
        mass_row = QHBoxLayout()
        mass_row.addWidget(QLabel("Mass:"))
        mass_row.addWidget(self.mass_input)

        # Radius
        radius_row = QHBoxLayout()
        radius_row.addWidget(QLabel("Radius:"))
        radius_row.addWidget(self.radius_input)

        # Position
        position_label = QLabel("Position")

        x_row = QHBoxLayout()
        x_row.addWidget(QLabel("X:"))
        x_row.addWidget(self.x_input)

        y_row = QHBoxLayout()
        y_row.addWidget(QLabel("Y:"))
        y_row.addWidget(self.y_input)

        # Velocity
        velocity_label = QLabel("Velocity")

        vx_row = QHBoxLayout()
        vx_row.addWidget(QLabel("Vx:"))
        vx_row.addWidget(self.vx_input)

        vy_row = QHBoxLayout()
        vy_row.addWidget(QLabel("Vy:"))
        vy_row.addWidget(self.vy_input)

        # Layout construct
        add_layout.addLayout(name_row)
        add_layout.addLayout(mass_row)
        add_layout.addLayout(radius_row)

        add_layout.addWidget(position_label)
        add_layout.addLayout(x_row)
        add_layout.addLayout(y_row)

        add_layout.addWidget(velocity_label)
        add_layout.addLayout(vx_row)
        add_layout.addLayout(vy_row)

        add_layout.addWidget(self.add_button)

        add_group.setLayout(add_layout)

        # -----------------------------------------------------
        # Remove body group
        # -----------------------------------------------------

        remove_group = QGroupBox("Remove Body")
        remove_layout = QVBoxLayout()

        remove_layout.addWidget(QLabel("Body:"))
        remove_layout.addWidget(self.body_selector)
        remove_layout.addWidget(self.remove_button)

        remove_group.setLayout(remove_layout)

        # -----------------------------------------------------
        # Information group
        # -----------------------------------------------------

        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout()

        info_layout.addWidget(self.time_label)
        info_layout.addWidget(self.bodies_label)

        info_group.setLayout(info_layout)

        # -----------------------------------------------------
        # Body information group
        # -----------------------------------------------------

        self.kinematics_group = QGroupBox("Body information")
        kinematics_layout = QHBoxLayout()

        pos_info = QVBoxLayout()
        pos_info.addWidget(QLabel("Position"))
        pos_info.addWidget(self.x_label)
        pos_info.addWidget(self.y_label)

        vel_info = QVBoxLayout()
        vel_info.addWidget(QLabel("Velocity"))
        vel_info.addWidget(self.vx_label)
        vel_info.addWidget(self.vy_label)

        ac_info = QVBoxLayout()
        ac_info.addWidget(QLabel("Acceleration"))
        ac_info.addWidget(self.ax_label)
        ac_info.addWidget(self.ay_label)

        kinematics_layout.addLayout(pos_info)
        kinematics_layout.addLayout(vel_info)
        kinematics_layout.addLayout(ac_info)

        #kinematics_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.kinematics_group.setLayout(kinematics_layout)

        # -----------------------------------------------------
        # Layout
        # -----------------------------------------------------

        self.body_layout = QVBoxLayout()

        self.body_layout.addWidget(simulation_group)
        self.body_layout.addWidget(add_group)
        self.body_layout.addWidget(remove_group)
        self.body_layout.addWidget(info_group)

        self.body_layout.addStretch()  

    def update_body_selector(self):
        """ Update the remove-body dropdown """

        self.body_selector.clear()

        for body in self.system.bodies:
            self.body_selector.addItem(body.name)

    def update_information(self):
        """ Update simulation Information """

        self.time_label.setText(
            f"Time: {self.system.time:.2f} s"
        )

        self.bodies_label.setText(
            f"Bodies: {len(self.system.bodies)}"
        )

        name = self.body_selector.currentText()

        for body in self.system.bodies:
            if body.name == name:
                self.x_label.setText(f"X: {body.pos[0]:.6e}")
                self.y_label.setText(f"Y: {body.pos[1]:.6e}")

                self.vx_label.setText(f"Vx: {body.vel[0]:.6e}")
                self.vy_label.setText(f"Vy: {body.vel[1]:.6e}")

                self.ax_label.setText(f"Ax: {body.ac[0]:.6e}")
                self.ay_label.setText(f"Ay: {body.ac[1]:.6e}")

                

if __name__ == "__main__":
    pass