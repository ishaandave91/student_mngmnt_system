import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QComboBox
from PyQt6 import QtGui


class AgeCalculator(QWidget):
    metric_system = "Metric (km)"
    imperial_system = "Imperial (mile)"

    def __init__(self):
        super().__init__()

        # Configure Window title bar
        self.setWindowTitle("Average Speed Calculator")
        self.setWindowIcon(QtGui.QIcon('img/avg_speed.png'))
        grid = QGridLayout()

        # Create widgets
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        self.metric_selected = QComboBox()
        self.metric_selected.addItems([self.metric_system, self.imperial_system])

        time_label = QLabel("Time (hours)")
        self.time_line_edit = QLineEdit()

        calculate_btn = QPushButton("Calculate")
        calculate_btn.clicked.connect(self.calculate_average_speed)
        self.output_label = QLabel("")

        # Add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.metric_selected, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_btn, 2, 1)   # row 2, column 0, span = 1 row & 2 columns
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_average_speed(self):
        metric_selection = self.metric_selected.currentText()
        match metric_selection:
            case self.metric_system:
                avg_speed = float(self.distance_line_edit.text()) / float(self.time_line_edit.text())
                unit = "km/h"
            case self.imperial_system:
                avg_speed = float(self.distance_line_edit.text()) / float(self.time_line_edit.text()) / 1.609
                unit = "mph"
        self.output_label.setText(f'Average Speed: {str(round(avg_speed, 2))} {unit}')


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())