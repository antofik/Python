__author__ = 'anton'

from PySide.QtGui import QItemDelegate
from PySide.QtCore import *
from PySide.QtGui import *


class tournament_delegate(QItemDelegate):
    def __init__(self, parent=None, *args, **kwargs):
        QItemDelegate.__init__(self, *args, **kwargs)

    def paint2(self, painter, option, index):
        painter.save()
        # set background color
        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.yellow))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        # set text color
        painter.setPen(QPen(Qt.green))
        value = index.data(Qt.DisplayRole)
        tooltip = index.data(Qt.ToolTipRole)
        painter.drawText(option.rect, Qt.AlignLeft, value)
        painter.drawText(option.rect, Qt.AlignRight, tooltip)

        painter.restore()
