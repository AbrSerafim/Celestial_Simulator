""" Main application window """

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
)

from gui.dynamic_gui import DynamicGui
from gui.static_gui import StaticGui

class MainWindow(QMainWindow):
    """ Main window """

    def __init__(self, system, simulation):
        super().__init__()

        self.system = system
        self.simulation = simulation

        self._create_gui()
        self._create_layout()

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


if __name__ == "__main__":
    pass