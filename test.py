import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

# Initialize Qt Application
app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)

# Set up main window and plot
win = pg.GraphicsLayoutWidget(show=True, title="PyQtGraph Circular Objects")
win.resize(800, 600)

plot = win.addPlot(title="Circular Objects Overview")
plot.setAspectLocked(True)  # Keeps 1:1 aspect ratio so circles stay round
plot.showGrid(x=True, y=True)

# -------------------------------------------------------------------
# 1. Parametric Circle (Exact radius & center in plot units)
# -------------------------------------------------------------------
def add_circle(plot_item, cx, cy, radius, color='r', width=2):
    theta = np.linspace(0, 2 * np.pi, 200)
    x = cx + radius * np.cos(theta)
    y = cy + radius * np.sin(theta)
    pen = pg.mkPen(color=color, width=width)
    curve = pg.PlotCurveItem(x, y, pen=pen)
    plot_item.addItem(curve)

# Draw a red circle at (0, 0) with radius 5
add_circle(plot, cx=0, cy=0, radius=5, color=(255, 80, 80), width=2)


# -------------------------------------------------------------------
# 2. ScatterPlotItem (Circular markers/dots in pixel dimensions)
# -------------------------------------------------------------------
scatter = pg.ScatterPlotItem(
    pos=[(2, 2), (-4, 4), (6, -4)],
    size=[20, 35, 50],  # Marker sizes in pixels
    symbol='o',
    pen=pg.mkPen('w', width=1),
    brush=pg.mkBrush(100, 150, 255, 200)
)
plot.addItem(scatter)


# -------------------------------------------------------------------
# 3. CircleROI (Interactive draggable/resizable circle)
# -------------------------------------------------------------------
# pos is bounding box lower-left [x, y], size is [diameter, diameter]
roi = pg.CircleROI(pos=[-6, -8], size=[6, 6], pen=pg.mkPen('y', width=2))
plot.addItem(roi)


# -------------------------------------------------------------------
# 4. QGraphicsEllipseItem (Qt-native graphic element)
# -------------------------------------------------------------------
# Arguments: x, y, width, height (bounding rectangle)
ellipse = QtWidgets.QGraphicsEllipseItem(-10, -2, 4, 4)
ellipse.setPen(pg.mkPen('c', width=2))
ellipse.setBrush(pg.mkBrush(200, 100, 255, 120))
plot.addItem(ellipse)


if __name__ == '__main__':
    sys.exit(app.exec_())