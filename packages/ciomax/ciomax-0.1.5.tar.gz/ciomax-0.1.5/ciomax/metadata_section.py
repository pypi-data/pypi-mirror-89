from PySide2 import QtWidgets, QtGui, QtCore

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.key_value_grp import KeyValueGrpList


class MetadataSection(CollapsibleSection):
    ORDER = 70

    def __init__(self, dialog):
        super(MetadataSection, self).__init__(dialog, "Metadata")

        self.component = KeyValueGrpList()
        self.content_layout.addWidget(self.component)
        self.configure_signals()

    def configure_signals(self):
        """Write to store when values change"""
        self.component.edited.connect(self.on_edited)

    def on_edited(self):
        self.dialog.store.set_metadata(list(self.component))

    def populate_from_store(self):
        store = self.dialog.store
        self.component.set_entries(store.metadata())
