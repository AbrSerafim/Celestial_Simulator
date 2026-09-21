""" Code to handle the static elements of the GUI """

from PySide6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox
)

class StaticGui(QWidget):
    """ Handles the static controls and info of the GUI """

    def __init__(self, system, simulation):
        super().__init__()

        self.system = system
        self.simulation = simulation

        self.setMinimumWidth(280)
        self.setMaximumWidth(350)

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):
        """ Create the GUI widgets """

        # Simulation controls
        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")

        # Simulation group
        self.simulation_group = QGroupBox("Simulation")

    def _create_layout(self):
        """ Create and arrange the GUI layout """

        # -----------------------------------
        # Simulation controls
        # -----------------------------------

        simulation_layout = QHBoxLayout()

        simulation_layout.addWidget(self.start_button)
        simulation_layout.addWidget(self.pause_button)
        simulation_layout.addWidget(self.reset_button)

        self.simulation_group.setLayout(simulation_layout)

        # -----------------------------------
        # Main layout
        # -----------------------------------

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.simulation_group)

        # Push everything to the top
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _connect_signals(self):
        """ Connect widget signals to their action """

        self.start_button.clicked.connect(self.start)
        self.start_button.clicked.connect(self.pause)
        self.start_button.clicked.connect(self.reset)

    def start(self):
        print("Start")

    def pause(self):
        print("Pause")

    def reset(self):
        print("Reset")


if __name__ == "__main__":
    pass