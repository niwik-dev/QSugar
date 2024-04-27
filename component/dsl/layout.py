from qtpy.QtCore import QObject, Qt
from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout

from QSugar.proxy.dsl import DSL


def Row(
        *args,
        children: list[QObject],
        spacing: int = 8,
        direction: QBoxLayout.Direction = QBoxLayout.Direction.LeftToRight,
        alignment: Qt.Alignment = Qt.AlignmentFlag.AlignLeft,
        **kwargs):
    """
    Make sub widgets on the same row.
    """
    return DSL(QWidget)(
        *args,
        **kwargs,
        child=DSL(QHBoxLayout)(
            children=children,
            spacing=spacing,
            direction=direction,
            alignment=alignment
        )
    )


def Column(
        *args,
        children: list[QObject],
        spacing: int = 8,
        direction: QBoxLayout.Direction = QBoxLayout.Direction.TopToBottom,
        alignment: Qt.Alignment = Qt.AlignmentFlag.AlignLeft,
        **kwargs):
    """
    Make sub widgets on the same column.
    """
    return DSL(QWidget)(
        *args,
        **kwargs,
        child=DSL(QVBoxLayout)(
            children=children,
            spacing=spacing,
            direction=direction,
            alignment=alignment
        )
    )


def RowCol(*args,
           children: list,
           vSpacing: int = 8,
           hSpacing: int = 8,
           **kwargs):
    """
    Arrange child widgets by row and column with row-major.
    """
    colChildren = []
    for item in children:
        if isinstance(item, QObject):
            colChildren.append(item)
        if isinstance(item, list):
            colChildren.append(
                Row(*args, children=item, spacing=vSpacing, **kwargs)
            )
    return Column(*args, children=colChildren, spacing=hSpacing, **kwargs)


def ColRow(*args,
           children: list,
           vSpacing: int = 8,
           hSpacing: int = 8,
           **kwargs):
    """
    Arrange child widgets by row and column with column-major.
    """
    rowChildren = []
    for item in children:
        if isinstance(item, QObject):
            rowChildren.append(item)
        if isinstance(item, list):
            rowChildren.append(
                Column(*args, children=item, spacing=hSpacing, **kwargs)
            )
    return Row(*args, children=rowChildren, spacing=vSpacing, **kwargs)
