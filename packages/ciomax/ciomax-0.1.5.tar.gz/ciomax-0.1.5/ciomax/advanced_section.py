from PySide2 import QtCore, QtWidgets

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.text_field_grp import TextFieldGrp
from ciomax.components.checkbox_grp import CheckboxGrp

from ciomax.components.int_field_grp import IntFieldGrp


class AdvancedSection(CollapsibleSection):
    ORDER = 100

    def __init__(self, dialog):
        super(AdvancedSection, self).__init__(dialog, "Advanced")

        self.autosave_component = TextFieldGrp(
            label="Autosave",
            checkbox=True,
            check_label="Clean up",
            hidable=True)
        self.content_layout.addWidget(self.autosave_component)

        self.task_template_component = TextFieldGrp(
            label="Task template",
            enablable=True)
        self.content_layout.addWidget(self.task_template_component)

        self.retry_preempted_component = IntFieldGrp(
            label="Preempted retries", default=1, minimum=0)
        self.content_layout.addWidget(self.retry_preempted_component)

        self.notification_component = TextFieldGrp(
            label="Send Notifications",
            enablable=True)
        self.content_layout.addWidget(self.notification_component)

        self.location_component = TextFieldGrp(
            label="Location tag")
        self.content_layout.addWidget(self.location_component)

        upload_options_component = CheckboxGrp(
            checkboxes=2,
            sublabels=["Use daemon", "Upload only"]
        )
        self.use_daemon_checkbox = upload_options_component.checkboxes[0]
        self.upload_only_checkbox = upload_options_component.checkboxes[1]
        self.content_layout.addWidget(upload_options_component)

        separator = QtWidgets.QFrame()
        separator.setLineWidth(1)
        separator.setFrameStyle(QtWidgets.QFrame.HLine |
                                QtWidgets.QFrame.Raised)
        self.content_layout.addWidget(separator)

        diagnostics_options_grp = CheckboxGrp(
            checkboxes=2,
            sublabels=["Show tracebacks", "Use fixtures"]
        )

        self.tracebacks_checkbox = diagnostics_options_grp.checkboxes[0]
        self.fixtures_checkbox = diagnostics_options_grp.checkboxes[1]
        self.content_layout.addWidget(diagnostics_options_grp)

        # self.autosave_component.checkbox.setEnabled(False)

        self.configure_signals()

    def configure_signals(self):
        """Write to store when values change"""

        # AUTOSAVE
        self.autosave_component.field.editingFinished.connect(
            self.on_autosave_change)

        self.autosave_component.checkbox.stateChanged.connect(
            self.on_autosave_cleanup_change)

        self.autosave_component.display_checkbox.stateChanged.connect(
            self.on_use_autosave_change)

        # TASK TEMPLATE
        self.task_template_component.field.editingFinished.connect(
            self.on_task_template_change)

        self.task_template_component.display_checkbox.stateChanged.connect(
            self.on_override_task_template_change)

        self.retry_preempted_component.field.valueChanged.connect(
            self.on_retry_preempted_change)

        self.notification_component.field.editingFinished.connect(
            self.on_notification_change)

        self.notification_component.display_checkbox.stateChanged.connect(
            self.on_use_notification_change)

        self.location_component.field.editingFinished.connect(
            self.on_location_change)

        # DAEMON
        self.use_daemon_checkbox.clicked.connect(self.on_use_daemon_change)

        self.upload_only_checkbox.clicked.connect(self.on_upload_only_change)

        self.tracebacks_checkbox.clicked.connect(
            self.on_show_tracebacks_change)

        self.fixtures_checkbox.clicked.connect(
            self.on_use_fixtures_change)

    def on_autosave_change(self):
        self.dialog.store.set_autosave_filename(
            self.autosave_component.field.text())

    def on_autosave_cleanup_change(self, value):
        self.dialog.store.set_autosave_cleanup(value > 0)

    def on_use_autosave_change(self, value):
        self.dialog.store.set_use_autosave(value > 0)

    def on_task_template_change(self):
        self.dialog.store.set_task_template(
            self.task_template_component.field.text())

    def on_override_task_template_change(self, value):
        self.dialog.store.set_override_task_template(value > 0)

    def on_retry_preempted_change(self, value):
        self.dialog.store.set_retries_when_preempted(value)

    def on_notification_change(self):
        self.dialog.store.set_emails(self.notification_component.field.text())

    def on_use_notification_change(self, value):
        self.dialog.store.set_use_emails(value > 0)

    def on_location_change(self):
        self.dialog.store.set_location_tag(
            self.location_component.field.text())

    def on_use_daemon_change(self, value):
        self.dialog.store.set_use_upload_daemon(value > 0)
        self.autosave_component.checkbox.setEnabled(not value)

    def on_upload_only_change(self, value):
        self.dialog.store.set_upload_only(value > 0)

    def on_show_tracebacks_change(self, value):
        self.dialog.store.set_show_tracebacks(value > 0)

    def on_use_fixtures_change(self, value):
        self.dialog.store.set_use_fixtures(value > 0)

    def populate_from_store(self):
        store = self.dialog.store
        self.autosave_component.field.setText(store.autosave_filename())

        self.autosave_component.set_active(store.use_autosave())
        self.autosave_component.checkbox.setChecked(store.autosave_cleanup())

        self.task_template_component.field.setText(store.task_template())
        self.task_template_component.set_active(store.override_task_template())

        self.retry_preempted_component.field.setValue(
            store.retries_when_preempted())

        self.notification_component.field.setText(store.emails())
        self.notification_component.set_active(store.use_emails())

        self.location_component.field.setText(store.location_tag())

        self.upload_only_checkbox.setChecked(store.upload_only())

        # USE DAEMON: Autosave cleanup must be disabled if use daemon
        use_daemon = store.use_upload_daemon()
        self.use_daemon_checkbox.setChecked(use_daemon)
        self.autosave_component.checkbox.setEnabled(not use_daemon)

        self.tracebacks_checkbox.setChecked(store.show_tracebacks())
        self.fixtures_checkbox.setChecked(store.use_fixtures())

        return
    # def resolve(self):
    #     pass
