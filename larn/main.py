import sys
import collections

import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui

WinPosition = collections.namedtuple('WinPosition', 'left top')
WinSize = collections.namedtuple('WinSize', 'height width')

MAP_COLS, MAP_LINES = 65, 17
EFFECTS_COLS, EFFECTS_LINES = 17, 17

STATS_COLS = MAP_COLS + EFFECTS_COLS
STATS_LINES = 2

MESSAGE_COLS = STATS_COLS
MESSAGE_LINES = 5

INVENTORY_COLS = 34
INVENTORY_LINES = MAP_LINES + STATS_LINES + MESSAGE_LINES

def horizontal_layout():
    hl = QtWidgets.QHBoxLayout()
    hl.setContentsMargins(0, 0, 0, 0)
    hl.setSpacing(0)
    return hl

def vertical_layout():
    vl = QtWidgets.QVBoxLayout()
    vl.setContentsMargins(0, 0, 0, 0)
    vl.setSpacing(0)
    return vl


class TextView(QtWidgets.QWidget):
    def __init__(self, columns=None, fillchar=' ', lines=None):
        super().__init__()

        if columns is None: 
            columns = self.COLS
        if lines is None:
            lines = self.LINES

        self.text = [fillchar * columns] * lines
        vbox = self.vbox = vertical_layout()

        for line in self.text:
            lbl = QtWidgets.QLabel()
            lbl.setAlignment(QtCore.Qt.AlignLeft)
            lbl.setStyleSheet(f"background-color: rgb(28, 43, 255); color: rgb(127,127,127);")
            vbox.addWidget(lbl)

        self.setLayout(vbox)
        self.refresh()

    def refresh(self):
        vbox = self.vbox

        for i, line in enumerate(self.text):
            lbl = vbox.itemAt(i).widget()
            lbl.setText(line)


class MapView(TextView):
    COLS = 65
    LINES = 17

    def __init__(self, **kwargs):
        super().__init__(fillchar='#', **kwargs)


class EffectsView(TextView):
    COLS = 17
    LINES = MapView.LINES


class StatsView(TextView):
    COLS = MapView.COLS + EffectsView.COLS
    LINES = 2


class MessageView(TextView):
    COLS = StatsView.COLS
    LINES = 5


class InventoryView(TextView):
    COLS = 34
    LINES = MapView.LINES + StatsView.LINES + MessageView.LINES


class MainView(QtWidgets.QWidget):
    def __init__(self, title='', position=None, size=None):
        super().__init__()

        self.title = title

        if position is not None:
            self.position = position
        else:
            self.position = WinPosition(0, 0)

        if size is not None:
            self.size = size
        else:
            self.size = WinSize(300, 300)

        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(self.title)
        pos, size = self.position, self.size
        #self.setGeometry(pos.left, pos.top, size.width, size.height)
        
        self.effects = EffectsView()
        self.inventory = InventoryView()
        self.map = MapView()
        self.messages = MessageView()
        self.stats = StatsView()

        map_fx = horizontal_layout()
        map_fx.addWidget(self.map)
        map_fx.addWidget(self.effects)
        map_fx.addStretch()

        map_group = vertical_layout()
        map_group.addLayout(map_fx)
        map_group.addWidget(self.stats)
        map_group.addWidget(self.messages)
        map_group.addStretch()

        outer_layout = horizontal_layout()
        outer_layout.addLayout(map_group)
        outer_layout.addWidget(self.inventory)
        outer_layout.addStretch()

        self.setLayout(outer_layout)
        self.setContentsMargins(5, 5, 5, 5)
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Set default font for entire application
    font = QtGui.QFont("", 14)
    font.setStyleHint(QtGui.QFont.TypeWriter)
    app.setFont(font)

    view = MainView()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
