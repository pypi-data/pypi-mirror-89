from PySide2 import QtWidgets, QtGui, QtCore

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.key_value_grp import KeyValueGrpList


class EnvironmentSection(CollapsibleSection):
    ORDER = 60

    def __init__(self, dialog):
        super(EnvironmentSection, self).__init__(dialog, "Extra Environment")

        self.component = KeyValueGrpList(
            checkbox_label="Excl", key_label="Name")
        self.content_layout.addWidget(self.component)
        self.configure_signals()

    def configure_signals(self):
        """Write to store when values change"""
        self.component.edited.connect(self.on_edited)

    def on_edited(self):
        self.dialog.store.set_extra_environment(list(self.component))

    def populate_from_store(self):
        store = self.dialog.store
        self.component.set_entries(store.extra_environment())

    # def resolve(self, expander):
    #     inst_type_desc = self.instance_type_component.combobox_machine.currentText()
    #     return {
    #         "job_title": expander.evaluate(self.title_component.field.text()),
    #         "output_path": self.destination_component.field.text(),
    #         "project": self.project_component.combobox.currentText(),
    #         "instance_type": inst_type_desc,
    #         "preemptible": self.instance_type_component.checkbox.isChecked()
    #     }
