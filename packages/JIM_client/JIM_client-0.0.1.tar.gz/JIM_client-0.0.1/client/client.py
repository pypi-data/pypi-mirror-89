import sys

from PyQt5.QtWidgets import QApplication

from client.client_gui import AuthForm


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = AuthForm()
    sys.exit(app.exec_())
