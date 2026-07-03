from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.scanner import ModScanner


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.scanner = ModScanner()

        self.setWindowTitle("BeamNG Career Editor")

        self.resize(950, 600)

        self.open_button = QPushButton("Open Mod")

        self.info_label = QLabel(
            "Select a BeamNG mod (.zip) or extracted folder."
        )

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Version",
                "JPG",
                "PC",
                "Info"
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()

        layout.addWidget(self.open_button)
        layout.addWidget(self.info_label)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        self.open_button.clicked.connect(self.open_mod)

    # ---------------------------------------------------------

    def open_mod(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open BeamNG Mod",
            "",
            "BeamNG Mod (*.zip)"
        )

        if not filename:
            return

        self.info_label.setText(filename)

        versions = self.scanner.scan(filename)

        self.table.setRowCount(len(versions))

        for row, version in enumerate(versions):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(version.name)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem("✓" if version.jpg_exists else "")
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem("✓" if version.pc_exists else "")
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem("✓" if version.info_exists else "")
            )

        self.statusBar().showMessage(
            f"{len(versions)} version(s) found."
        )