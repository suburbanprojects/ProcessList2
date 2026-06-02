from PyQt6.QtWidgets import QApplication
import sys
from ui import ProcessList


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ProcessList()
    main_window.show()
    sys.exit(app.exec())
