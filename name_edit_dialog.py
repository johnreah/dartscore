from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLineEdit

class NameEditDialog(QDialog):
    name_edit_dialog_ok = Signal(str)

    def __init__(self, parent, name: str):
        super().__init__(parent = parent)

        self.name = name
        self.result = None
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Dialog)

        vLayout = QVBoxLayout(self)

        self.edName = QLineEdit(self.name, self)
        self.edName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edName.setReadOnly(False)
        self.edName.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                padding: 10px;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
        """)
        vLayout.addWidget(self.edName)

        dbb = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(dbb)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(lambda: self.name_edit_dialog_ok.emit(self.edName.text()))

        vLayout.addWidget(self.buttonBox)

        self.edName.selectAll()

    # def showEvent(self, event):
    #     super().showEvent(event)
    #     if self.parentWidget():
    #         parent_geo = self.parentWidget().window().geometry()
    #         geo = self.geometry()
    #         x = parent_geo.x() + (parent_geo.width() - geo.width()) // 2
    #         y = parent_geo.y() + (parent_geo.height() - geo.height()) // 6
    #         self.move(x, y)
