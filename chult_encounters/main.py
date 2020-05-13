from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTextBrowser,
    QLabel,
    QHBoxLayout,
    QGroupBox,
    QRadioButton,
)

from model import Model, EncounterTime, EncounterFrequency


class QEncounterDisplay(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setOpenExternalLinks(True)


class QEncounterFrequency(QRadioButton):
    def __init__(self, frequency):
        super().__init__(frequency.name.title())
        self.frequency = frequency


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.setWindowTitle("Chult Encounters")

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.interface_layout = QHBoxLayout()
        self.interface_layout.addWidget(self.get_generate_encounter_button())
        self.interface_layout.addWidget(self.get_encounter_frequency_selectors())

        self.encounter_displays = {
            EncounterTime.MORNING: QEncounterDisplay(),
            EncounterTime.AFTERNOON: QEncounterDisplay(),
            EncounterTime.EVENING: QEncounterDisplay(),
        }

        self.main_layout.addLayout(self.interface_layout)
        self.add_encounter_text_layout()
        self.setup_window()

    def get_encounter_frequency_selectors(self):
        def on_click(button_frequency):
            self.model.encounter_frequency = button_frequency

        group = QGroupBox("Encounter Frequency")
        layout = QVBoxLayout()
        for frequency in EncounterFrequency:
            button = QEncounterFrequency(frequency)
            button.toggled.connect(lambda: on_click(button.frequency))
            if button.frequency == self.model.encounter_frequency:
                button.setChecked(True)
            layout.addWidget(button)
        group.setLayout(layout)
        return group

    def get_generate_encounter_button(self):
        def on_click():
            self.model.generate_encounters()
            for time in self.encounter_displays:
                self.encounter_displays[time].setHtml(self.model.encounters[time])

        button = QPushButton("Generate Encounters")
        button.clicked.connect(on_click)
        return button

    def add_encounter_text_layout(self):
        layout = QVBoxLayout()
        labels = [QLabel(label) for label in ["Morning", "Afternoon", "Evening"]]
        for label, text_box in zip(labels, self.encounter_displays.values()):
            layout.addWidget(label)
            layout.addWidget(text_box)
        self.main_layout.addLayout(layout)

    def setup_window(self):
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
