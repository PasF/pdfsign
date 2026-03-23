import sys
import argparse

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def main():
    parser = argparse.ArgumentParser(description="PDFSign — Sign PDF documents")
    parser.add_argument("pdf", nargs="?", help="Path to a PDF file to open")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName("PDFSign")

    window = MainWindow()
    window.show()

    if args.pdf:
        window.open_pdf(args.pdf)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
