#!/usr/bin/python3.5
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Base_Desktop_Dial_Meter and CPU_Monitor created by Grorco <Grorco.Linux@gmail.com> 2018
# Main trunk at https://github.com/Grorco-Linux/Desktop_Widgets

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QAction
from PyQt5.QtGui import QPainter, QPolygon, QColor, QBrush
from PyQt5 import QtCore


class BaseDial(QWidget):
    """A base dial to use to monitor anything you would like"""
    def __init__(self, sidelength=100, refreshrate=100, pointercolor=QColor(250,100,100), ticklength=10,
                 tickcolor=QColor(100, 250, 100), monitortext='CPU', textcolor=QColor(100,100,250)):
        super().__init__()
        self._sidelength = sidelength
        self.refreshrate = refreshrate
        self._pointercolor = pointercolor
        self._ticklength = ticklength
        self._tickcolor = tickcolor
        self._monitortext = monitortext
        self._textcolor = textcolor
        self.left = 1000
        self.top = 100
        self._width = self._sidelength
        self._height = self._sidelength
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self._width, self._height)

        # Create widget
        self.label = QLabel(self)

        self.pointer = QPolygon([
            QtCore.QPoint(2, 0),
            QtCore.QPoint(-2, 0),
            QtCore.QPoint(0, -(self._sidelength / 2))
        ])

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(self.refreshrate)


        self.label.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnBottomHint |
            QtCore.Qt.X11BypassWindowManagerHint

        )


        self.show()

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(sys.exit)
        self.addAction(quitAction)

    # Override this method to return whatever you want to monitor, must be an int or float
    def monitor(self):
        return 0

    def paintEvent(self, QPaintEvent):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self._width / 2, self._height / 2)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QBrush(self._pointercolor))

        painter.save()
        painter.rotate((2.88 * self.monitor()) + 216)
        painter.drawConvexPolygon(self.pointer)
        painter.restore()

        painter.setPen(self._textcolor)
        painter.save()
        painter.drawText(-10, (self._sidelength / 2), self._monitortext)
        painter.drawText(-10, (self._sidelength / 2) - 15, str(self.monitor()))
        painter.restore()

        painter.save()
        painter.setPen(self._tickcolor)
        painter.rotate(126)

        for i in range(17):
            painter.drawLine((self._sidelength / 2) - self._ticklength, 0, (self._sidelength / 2), 0)
            painter.rotate(18)
        painter.restore()

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        position = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + position.x(), self.y() + position.y())
        self.oldPosition = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BaseDial()
    sys.exit(app.exec_())