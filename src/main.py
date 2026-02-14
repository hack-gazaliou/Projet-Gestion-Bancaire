import os
import sys

from PySide6.QtWidgets import QApplication

from Logger import logger

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from Vue.vue_principale import MainWindow  # noqa: E402


def main():
    logger.info("Application Starting...")
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    logger.info("MainWindow displayed.")
    exit_code = app.exec()

    logger.info(f"Application stopping with code {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
