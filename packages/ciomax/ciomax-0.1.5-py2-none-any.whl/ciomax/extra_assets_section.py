from PySide2 import QtWidgets
from ciomax.collapsible_section import CollapsibleSection


class ExtraAssetsSection(CollapsibleSection):
    ORDER = 65

    def __init__(self,dialog):
        super(ExtraAssetsSection, self).__init__(dialog,"Extra Assets")

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        for button in [
            {"label": "Clear", "func": self.clear},
            {"label": "Remove selected", "func": self.remove_selected},
            {"label": "Browse files", "func": self.browse_files},
            {"label": "Browse directory", "func": self.browse_dir},
        ]:

            btn = QtWidgets.QPushButton(button["label"])
            btn.clicked.connect(button["func"])
            self.button_layout.addWidget(btn)

        self.content_layout.addLayout(self.button_layout)

        # List
        self.list_component = QtWidgets.QListWidget()
        self.list_component.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_component.setFixedHeight(140)
        self.content_layout.addWidget(self.list_component)
 

    def entries(self):
        result = []
        for i in range(self.list_component.count() ):
            result.append(self.list_component.item(i).text())
        return result

    def clear(self):
        self.list_component.clear()
        self.dialog.store.set_assets([])

    def remove_selected(self):
        model = self.list_component.model()
        for row in sorted([index.row() for index in self.list_component.selectionModel().selectedIndexes()], reverse=True):
            model.removeRow(row)

        self.dialog.store.set_assets( self.entries() )

    def browse_files(self):
        result = QtWidgets.QFileDialog.getOpenFileNames(
            parent=None, caption="Select files to upload")
        if len(result) and len(result[0]):
            self.list_component.addItems(result[0])
            self.dialog.store.set_assets( self.entries() )

    def browse_dir(self):
        result = QtWidgets.QFileDialog.getExistingDirectory(
            parent=None, caption="Select a directory to upload")
        if result:
            self.list_component.addItem(result)
            self.dialog.store.set_assets( self.entries() )

    def populate_from_store(self):
        self.list_component.addItems(self.dialog.store.assets())

    # def resolve(self):
    #     pass
