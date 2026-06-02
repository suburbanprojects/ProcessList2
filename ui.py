from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QListWidget, QLineEdit, QLabel)
from process_manager import get_all_processes, terminate_by_target


class ProcessList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Process List')
        self.setGeometry(100, 100, 550, 525)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # set up the layout and text area to show process information
        self.layout = QVBoxLayout(self.central_widget)
        # using QListWidget instead of QTextEdit to display process information in a more structured way
        self.show_process_entry = QListWidget(self)
        self.layout.addWidget(self.show_process_entry)

        # set bottom button to quit the application and input field to specify which process to kill
        button_layout_2 = QHBoxLayout()
        # input field accepts either a PID or a process name
        self.process_to_kill = QLineEdit(self)
        self.layout.addWidget(self.process_to_kill)
        # status label shows feedback after kill attempts
        self.status_label = QLabel('Enter a PID or process name and click Kill Process.', self)
        self.status_label.setWordWrap(True)
        self.layout.addWidget(self.status_label)
        # add buttons to kill process and quit application
        self.kill_process = QPushButton('Kill Process', self)
        self.kill_process.clicked.connect(self.killProcess)
        button_layout_2.addWidget(self.kill_process)

        self.quit_application = QPushButton('Quit Application', self)
        self.quit_application.clicked.connect(self.quitApplication)
        button_layout_2.addWidget(self.quit_application)
        self.layout.addLayout(button_layout_2)

        # Refresh the process list every 1.5 seconds without blocking the GUI thread.
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.showProcesses)
        self.refresh_timer.start(1500)

        # Load the initial process list immediately when the window opens.
        self.showProcesses()

    def showProcesses(self):
        """Show process information in the list widget."""
        self.show_process_entry.clear()
        processes = get_all_processes()
        for info in processes:
            self.show_process_entry.addItem(
                f"PID: {info['pid']}, Name: {info['name']}, CPU: {info['cpu_percent']}%, "
                f"Memory: {info['memory_percent']:.2f}%, User: {info['username']}"
            )
        self.show_process_entry.addItem("Waiting 1.5 seconds before the next refresh...")

    def killProcess(self):
        """Kill a process by entering either its PID or name."""
        target_text = self.process_to_kill.text().strip()
        if not target_text:
            self.status_label.setText('Enter a PID or process name first.')
            return

        success, message = terminate_by_target(target_text)
        self.status_label.setText(message)

        if success:
            self.process_to_kill.clear()
            self.showProcesses()

    def quitApplication(self):
        QApplication.quit()
