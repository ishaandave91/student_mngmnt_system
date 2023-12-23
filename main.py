# ToDo:
# Once edit-delete btn are added they stay on, should be removed if any cell is not selected
# Organize code esp insert and edit classes


import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QToolBar, QStatusBar, QDialogButtonBox, QMessageBox
from PyQt6.QtGui import QAction, QIcon, QFont
import sqlite3


class MainWindow(QMainWindow):
    window_width = 700
    window_height = 500

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QIcon('img/student-management-icon.png'))
        self.setMinimumSize(self.window_width, self.window_height)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon('img/add.png'), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction(QIcon('img/search.png'), "Search", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole)     # for mac devices if 'Help' menu doesn't show
        about_action.triggered.connect(self.about)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)   # Hide row count default column
        self.setCentralWidget(self.table)

        # Create toolbar and populate with elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create Status bar and populate with elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect click on cell
        self.table.cellClicked.connect(self.cell_clicked)
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.edit_btn.clicked.connect(self.edit)
        self.delete_btn.clicked.connect(self.delete)

        self.table.clearSelection()

    def cell_clicked(self):
        self.statusbar.addWidget(self.edit_btn)
        self.statusbar.addWidget(self.delete_btn)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("Select * from students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    window_width = 230
    window_height = 250

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setWindowIcon(QIcon('img/add.png'))
        self.setFixedWidth(self.window_width)
        self.setFixedHeight(self.window_height)

        layout = QVBoxLayout()

        # Create dialog box widgets
        self.student_name_line_edit = QLineEdit()
        self.student_name_line_edit.setPlaceholderText("Name")

        self.courses_name = QComboBox()
        courses = ['Astronomy', 'Biology', 'Math', 'Physics', 'Chemistry']
        self.courses_name.addItems(courses)

        self.mobile_line_edit = QLineEdit()
        self.mobile_line_edit.setPlaceholderText("Mobile")

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.add_student)

        # Add widgets to the layout
        layout.addWidget(self.student_name_line_edit)
        layout.addWidget(self.courses_name)
        layout.addWidget(self.mobile_line_edit)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name_line_edit.text()
        course = self.courses_name.currentText()
        mobile = self.mobile_line_edit.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("Insert into students (name, course, mobile) Values(?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()


class EditDialog(QDialog):
    window_width = 230
    window_height = 250

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        # Get student name from the selected row
        self.index = main_window.table.currentRow()
        if self.index >= 0:
            self.setWindowTitle("Update Student Data")
            self.setWindowIcon(QIcon('img/edit.png'))
            self.setFixedWidth(self.window_width)
            self.setFixedHeight(self.window_height)

            current_name = main_window.table.item(self.index, 1).text()

            # Create dialog box widgets
            self.student_name_line_edit = QLineEdit(current_name)
            self.student_name_line_edit.setPlaceholderText("Name")

            current_course_name = main_window.table.item(self.index, 2).text()
            self.courses_name = QComboBox()
            courses = ['Astronomy', 'Biology', 'Math', 'Physics', 'Chemistry']
            self.courses_name.addItems(courses)
            self.courses_name.setCurrentText(current_course_name)

            current_mobile = main_window.table.item(self.index, 3).text()
            self.mobile_line_edit = QLineEdit(current_mobile)
            self.mobile_line_edit.setPlaceholderText("Mobile")

            self.submit_btn = QPushButton("Update")
            self.submit_btn.clicked.connect(self.edit_student)

            # Add widgets to the layout
            layout.addWidget(self.student_name_line_edit)
            layout.addWidget(self.courses_name)
            layout.addWidget(self.mobile_line_edit)
            layout.addWidget(self.submit_btn)

            self.setLayout(layout)
        else:
            self.window_width = 300
            self.window_height = 80
            self.setWindowTitle("WARNING!")
            self.setWindowIcon(QIcon('img/warning.png'))
            self.setFixedWidth(self.window_width)
            self.setFixedHeight(self.window_height)

            message = QLabel("Please select a record!")
            font = QFont()
            font.setPointSize(13)
            message.setFont(font)
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Add widgets to the layout
            layout.addWidget(message)
            self.setLayout(layout)

    def edit_student(self):
        name = self.student_name_line_edit.text()
        course = self.courses_name.currentText()
        mobile = self.mobile_line_edit.text()
        student_row_id = main_window.table.item(self.index, 0).text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("Update students Set name = ?, course = ?, mobile = ? "
                       "where id = ?",
                       (name, course, mobile, student_row_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    window_width = 400
    window_height = 120

    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        # Get student name from the selected row
        self.index = main_window.table.currentRow()
        if self.index >= 0:
            self.setWindowTitle("Delete Student Record")
            self.setWindowIcon(QIcon('img/delete.png'))
            self.setFixedWidth(self.window_width)
            self.setFixedHeight(self.window_height)

            q_buttons = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.Cancel
            self.buttonBox = QDialogButtonBox(q_buttons)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
            selected_student_name = main_window.table.item(self.index, 1).text()
            message = QLabel(f"Are you sure you want to delete record of student: {selected_student_name}")

            # Add widgets to the layout
            layout.addWidget(message, 0, 0, 1, 2)
            layout.addWidget(self.buttonBox)

            self.setLayout(layout)
        else:
            self.window_width = 300
            self.window_height = 80
            self.setWindowTitle("WARNING!")
            self.setWindowIcon(QIcon('img/warning.png'))
            self.setFixedWidth(self.window_width)
            self.setFixedHeight(self.window_height)

            message = QLabel("Please select a record!")
            font = QFont()
            font.setPointSize(13)
            message.setFont(font)
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Add widgets to the layout
            layout.addWidget(message, 0, 0)
            self.setLayout(layout)

    def accept(self):
        row_id = main_window.table.item(self.index, 0).text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("Delete from students where id=?",
                       (row_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setWindowIcon(QIcon('img/success.png'))
        confirmation_widget.setText("The student record was deleted successfully.")
        confirmation_widget.exec()


class SearchDialog(QDialog):
    window_width = 230
    window_height = 250

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setWindowIcon(QIcon('img/search.png'))
        self.setFixedWidth(self.window_width)
        self.setFixedHeight(self.window_height)

        layout = QVBoxLayout()

        # Create dialog box widgets
        self.search_name_line_edit = QLineEdit()
        self.search_name_line_edit.setPlaceholderText("Name...")

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search)

        # Add widgets to layout
        layout.addWidget(self.search_name_line_edit)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def search(self):
        main_window.load_data()
        search_name = self.search_name_line_edit.text()
        items = main_window.table.findItems(search_name,
                                            Qt.MatchFlag.MatchFixedString)
        for item in items:
            for column in range(main_window.table.columnCount()):
                main_window.table.item(item.row(), column).setSelected(True)     # item.row() = index of the row

        self.close()
        main_window.table.scrollToItem(item)


class AboutDialog(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This code was created during course Python mega course.
        Lorem ipsum
        Blah.Blah.Blah
        """
        self.setText(content)



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())