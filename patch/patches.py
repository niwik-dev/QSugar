"""

The `patches.py` file stores solutions to problems that the framework can adapt certain classes or methods.
This file may become very large, so it may be split and categorized later.

If you find problems with control adaptation, feel free to raise an issue on GitHub.

"""

from qtpy.QtWidgets import QTextEdit, QPlainTextEdit


class UnmatchedSetterAndGetterPatch(object):
    """
    Normally, setter and getter methods are of the form 'setProp()' and 'prop()' or 'isProp()'
    Those that do not apply will be handled in this patch class.
    """
    @staticmethod
    def QTextEditPatch(clazz):
        __patch_version__ = '0.0.1'
        clazz.text = clazz.toPlainText
        return clazz

    QTextEditPatch(QTextEdit)

    @staticmethod
    def QPlainTextEditPatch(clazz):
        __patch_version__ = '0.0.1'
        clazz.setText = clazz.setPlainText
        clazz.text = clazz.toPlainText
        return clazz

    QPlainTextEditPatch(QPlainTextEdit)
