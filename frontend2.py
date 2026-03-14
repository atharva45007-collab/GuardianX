import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class GuardianX(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("GuardianX - Cybersecurity Dashboard")
        self.setGeometry(200, 100, 900, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b1f3a;
                color: white;
                font-family: Arial;
            }

            QPushButton {
                background-color: #00ff9c;
                color: black;
                padding: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #00cc7a;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("🛡 GuardianX")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        tagline = QLabel("Your Shield Against Ransomware & Data Leaks")
        tagline.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(tagline)

        self.tabs = QTabWidget()

        self.tabs.addTab(self.home_tab(), "Home")
        self.tabs.addTab(self.ransomware_tab(), "Ransomware Detection")
        self.tabs.addTab(self.leak_tab(), "Data Leak Check")
        self.tabs.addTab(self.report_tab(), "Reports")

        layout.addWidget(self.tabs)

        self.setLayout(layout)

    # ---------------- HOME TAB ----------------

    def home_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        status = QLabel("System Status: Monitoring Files and Network Activity")
        status.setFont(QFont("Arial", 14))

        threats = QLabel("Threats Scanned Today: 1245")
        ransomware = QLabel("Ransomware Detected: 2")
        leaks = QLabel("Data Leaks Found: 1")

        layout.addWidget(status)
        layout.addWidget(threats)
        layout.addWidget(ransomware)
        layout.addWidget(leaks)

        tab.setLayout(layout)

        return tab

    # ---------------- RANSOMWARE TAB ----------------

    def ransomware_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Run a scan to detect ransomware activity")

        scan_btn = QPushButton("Start Scan")
        scan_btn.clicked.connect(self.ransomware_alert)

        layout.addWidget(label)
        layout.addWidget(scan_btn)

        tab.setLayout(layout)

        return tab

    def ransomware_alert(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Security Alert")
        msg.setText("⚠️ Ransomware Activity Detected!")
        msg.setInformativeText("Suspicious file encryption behavior identified.")
        msg.exec_()

    # ---------------- DATA LEAK TAB ----------------

    def leak_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(3)
        table.setColumnCount(2)

        table.setHorizontalHeaderLabels(["File Name", "Risk Level"])

        table.setItem(0, 0, QTableWidgetItem("customer_data.csv"))
        table.setItem(0, 1, QTableWidgetItem("HIGH"))

        table.setItem(1, 0, QTableWidgetItem("passwords.txt"))
        table.setItem(1, 1, QTableWidgetItem("MEDIUM"))

        table.setItem(2, 0, QTableWidgetItem("report.pdf"))
        table.setItem(2, 1, QTableWidgetItem("SAFE"))

        layout.addWidget(table)

        tab.setLayout(layout)

        return tab

    # ---------------- REPORT TAB ----------------

    def report_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Generate system security report")

        report_btn = QPushButton("Generate Report")
        report_btn.clicked.connect(self.report_message)

        layout.addWidget(label)
        layout.addWidget(report_btn)

        tab.setLayout(layout)

        return tab

    def report_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Report")
        msg.setText("Security Report Generated Successfully")
        msg.exec_()


# ---------------- RUN APPLICATION ----------------

app = QApplication(sys.argv)

window = GuardianX()
window.show()

sys.exit(app.exec_())
