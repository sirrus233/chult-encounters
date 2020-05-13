from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QLabel,
)

from model import Model, EncounterTime


class QEncounterDisplay(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.setWindowTitle("Chult Encounters")

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.encounter_displays = {
            EncounterTime.MORNING: QEncounterDisplay(),
            EncounterTime.AFTERNOON: QEncounterDisplay(),
            EncounterTime.EVENING: QEncounterDisplay(),
        }

        self.add_generate_encounter_button()
        self.add_encounter_text_layout()
        self.setup_window()

    def add_generate_encounter_button(self):
        def x():
            self.model.generate_encounters()
            for time in self.encounter_displays:
                self.encounter_displays[time].setText(self.model.encounters[time])

        button = QPushButton("Generate Encounters")
        button.clicked.connect(x)
        self.main_layout.addWidget(button)

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
