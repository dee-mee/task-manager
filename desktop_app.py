import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                           QComboBox, QSpinBox, QDateEdit, QTableWidget, 
                           QTableWidgetItem, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QDate

class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle("Add Task" if not task else "Edit Task")
        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        if self.task:
            self.title_input.setText(self.task[1])
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)

        # Description
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        if self.task:
            self.desc_input.setText(self.task[2])
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        # Due Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Due Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if self.task and self.task[3]:
            self.date_input.setDate(QDate.fromString(self.task[3], "yyyy-MM-dd"))
        else:
            self.date_input.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)

        # Status
        status_layout = QHBoxLayout()
        status_label = QLabel("Status:")
        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "In Progress", "Completed"])
        if self.task:
            self.status_input.setCurrentText(self.task[4])
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_input)
        layout.addLayout(status_layout)

        # Priority
        priority_layout = QHBoxLayout()
        priority_label = QLabel("Priority:")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        if self.task:
            self.priority_input.setCurrentText(self.task[5])
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_input)
        layout.addLayout(priority_layout)

        # Progress
        progress_layout = QHBoxLayout()
        progress_label = QLabel("Progress:")
        self.progress_input = QSpinBox()
        self.progress_input.setRange(0, 100)
        self.progress_input.setSuffix("%")
        if self.task:
            self.progress_input.setValue(self.task[6])
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_input)
        layout.addLayout(progress_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_task_data(self):
        return {
            'title': self.title_input.text(),
            'description': self.desc_input.toPlainText(),
            'due_date': self.date_input.date().toString("yyyy-MM-dd"),
            'status': self.status_input.currentText(),
            'priority': self.priority_input.currentText(),
            'progress': self.progress_input.value()
        }

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.setup_db()
        self.load_tasks()

    def setup_db(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT,
                priority TEXT,
                progress INTEGER,
                created_date TEXT,
                updated_date TEXT
            )
        ''')
        self.conn.commit()

    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Header with Add Task button
        header_layout = QHBoxLayout()
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        header_layout.addStretch()
        header_layout.addWidget(add_button)
        layout.addLayout(header_layout)

        # Tasks table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Title", "Description", "Due Date", "Status", 
            "Priority", "Progress", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

    def load_tasks(self):
        self.cursor.execute('SELECT * FROM tasks ORDER BY due_date')
        tasks = self.cursor.fetchall()
        self.table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task[1]))
            self.table.setItem(row, 1, QTableWidgetItem(task[2]))
            self.table.setItem(row, 2, QTableWidgetItem(str(task[3])))
            self.table.setItem(row, 3, QTableWidgetItem(task[4]))
            self.table.setItem(row, 4, QTableWidgetItem(task[5]))
            progress_item = QTableWidgetItem(f"{task[6]}%")
            self.table.setItem(row, 5, progress_item)

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)

            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, t=task: self.edit_task(t))
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, t=task: self.delete_task(t))

            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.table.setCellWidget(row, 6, actions_widget)

        self.table.resizeColumnsToContents()

    def add_task(self):
        dialog = TaskDialog(self)
        if dialog.exec():
            task_data = dialog.get_task_data()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''
                INSERT INTO tasks (title, description, due_date, status, priority, 
                                 progress, created_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_data['title'], task_data['description'], task_data['due_date'],
                task_data['status'], task_data['priority'], task_data['progress'],
                now, now
            ))
            self.conn.commit()
            self.load_tasks()

    def edit_task(self, task):
        dialog = TaskDialog(self, task)
        if dialog.exec():
            task_data = dialog.get_task_data()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''
                UPDATE tasks 
                SET title=?, description=?, due_date=?, status=?, priority=?, 
                    progress=?, updated_date=?
                WHERE id=?
            ''', (
                task_data['title'], task_data['description'], task_data['due_date'],
                task_data['status'], task_data['priority'], task_data['progress'],
                now, task[0]
            ))
            self.conn.commit()
            self.load_tasks()

    def delete_task(self, task):
        reply = QMessageBox.question(
            self, 'Delete Task',
            f'Are you sure you want to delete "{task[1]}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.cursor.execute('DELETE FROM tasks WHERE id=?', (task[0],))
            self.conn.commit()
            self.load_tasks()

    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())
