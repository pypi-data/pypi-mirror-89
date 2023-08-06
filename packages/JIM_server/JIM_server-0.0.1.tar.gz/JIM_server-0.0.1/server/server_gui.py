import sys

from PyQt5.QtWidgets import QApplication
from server.server_gui import MainForm

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = ""
    app = QApplication(sys.argv)
    form = MainForm(db_file_name=file)
    sys.exit(app.exec_())
