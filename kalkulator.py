"""
Nama : Danang Adiwijaya
NIM  : F1D02310044
Kelas: D
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShortcut, QKeySequence

STYLE_VALID = """
    QLineEdit {
        border: 2px solid #4A90D9;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        background: white;
        color: #1a1a1a;
    }
    QLineEdit:focus {
        border-color: #2176c7;
    }
"""

STYLE_INVALID = """
    QLineEdit {
        border: 2px solid #E53E3E;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        background: #fff5f5;
        color: #1a1a1a;
    }
"""

STYLE_MAIN = """
    QMainWindow {
        background-color: #2b2d3a;
    }
    QWidget#centralWidget {
        background-color: #2b2d3a;
    }
    QWidget#card {
        background-color: #f0f2f5;
        border-radius: 8px;
    }
    QLabel#sectionLabel {
        font-size: 12px;
        color: #555;
        font-weight: 600;
    }
    QLabel#errorLabel {
        font-size: 11px;
        color: #E53E3E;
    }
    QLabel#resultLabel {
        font-size: 14px;
        color: #333;
        background: white;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 10px;
        qproperty-alignment: AlignCenter;
    }
    QLabel#statusError {
        font-size: 11px;
        color: #E53E3E;
        background: #fff5f5;
        border-top: 1px solid #fcc;
        padding: 6px 12px;
    }
    QComboBox {
        border: 2px solid #ccc;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        background: white;
        color: #1a1a1a;
    }
    QComboBox:focus {
        border-color: #4A90D9;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox QAbstractItemView {
        background-color: white;       
        color: #1a1a1a;                
        selection-background-color: #4A90D9; 
        selection-color: white;        
        border: 1px solid #ccc;
        outline: none;                 
    }
    QPushButton#btnHitung {
        background-color: #9e9e9e;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton#btnHitung:enabled {
        background-color: #4A90D9;
    }
    QPushButton#btnHitung:enabled:hover {
        background-color: #2176c7;
    }
    QPushButton#btnClear {
        background-color: #E53E3E;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton#btnClear:hover {
        background-color: #c53030;
    }
    QLabel#titleBar {
        font-size: 13px;
        font-weight: bold;
        color: white;
    }
"""

class ValidatedLineEdit(QLineEdit):
    validityChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_valid = False
        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str):
        was_valid = self._is_valid
        self._is_valid = self._validate(text)

        if text == "":
            self.setStyleSheet(STYLE_VALID) 
        elif self._is_valid:
            self.setStyleSheet(STYLE_VALID)
        else:
            self.setStyleSheet(STYLE_INVALID)

        if was_valid != self._is_valid:
            self.validityChanged.emit(self._is_valid)

    @staticmethod
    def _validate(text: str) -> bool:
        if text.strip() == "":
            return False
        try:
            float(text)
            return True
        except ValueError:
            return False

    def is_valid(self) -> bool:
        return self._is_valid

class Kalkulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator")
        self.setFixedSize(480, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._drag_pos = None

        self._build_ui()
        self._connect_signals()
        self._setup_shortcuts()
        self._update_hitung_button()

    def _build_ui(self):
        self.setStyleSheet(STYLE_MAIN)

        central = QWidget(objectName="centralWidget")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #1e2030;")
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(12, 0, 8, 0)

        icon_label = QLabel("🧮")
        icon_label.setStyleSheet("font-size: 16px;")
        title_label = QLabel("Kalkulator", objectName="titleBar")

        btn_min = QPushButton("─")
        btn_min.setFixedSize(28, 28)
        btn_min.setStyleSheet(
            "QPushButton{color:white;background:transparent;border:none;font-size:14px;}"
            "QPushButton:hover{background:#444;border-radius:4px;}"
        )
        btn_min.clicked.connect(self.showMinimized)

        btn_max = QPushButton("□")
        btn_max.setFixedSize(28, 28)
        btn_max.setStyleSheet(
            "QPushButton{color:white;background:transparent;border:none;font-size:14px;}"
            "QPushButton:hover{background:#444;border-radius:4px;}"
        )

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(28, 28)
        btn_close.setStyleSheet(
            "QPushButton{color:white;background:transparent;border:none;font-size:13px;}"
            "QPushButton:hover{background:#E53E3E;border-radius:4px;}"
        )
        btn_close.clicked.connect(self.close)

        tb_layout.addWidget(icon_label)
        tb_layout.addSpacing(6)
        tb_layout.addWidget(title_label)
        tb_layout.addStretch()
        tb_layout.addWidget(btn_min)
        tb_layout.addWidget(btn_max)
        tb_layout.addWidget(btn_close)
        root.addWidget(title_bar)

        card = QWidget(objectName="card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(14)

        lbl1 = QLabel("Angka Pertama", objectName="sectionLabel")
        self.input1 = ValidatedLineEdit()
        self.input1.setPlaceholderText("Masukkan angka pertama…")
        self.input1.setStyleSheet(STYLE_VALID)
        self.err1 = QLabel("⚠ Input harus berupa angka", objectName="errorLabel")
        self.err1.setVisible(False)

        lbl_op = QLabel("Operasi", objectName="sectionLabel")
        self.combo_op = QComboBox()
        self.combo_op.addItems(["+ Tambah", "− Kurang", "× Kali", "÷ Bagi"])

        lbl2 = QLabel("Angka Kedua", objectName="sectionLabel")
        self.input2 = ValidatedLineEdit()
        self.input2.setPlaceholderText("Masukkan angka kedua…")
        self.input2.setStyleSheet(STYLE_VALID)
        self.err2 = QLabel("⚠ Input harus berupa angka", objectName="errorLabel")
        self.err2.setVisible(False)

        btn_layout = QHBoxLayout()
        self.btn_hitung = QPushButton("Hitung (Enter)", objectName="btnHitung")
        self.btn_hitung.setEnabled(False)
        self.btn_clear = QPushButton("Clear (Esc)", objectName="btnClear")
        btn_layout.addWidget(self.btn_hitung)
        btn_layout.addWidget(self.btn_clear)

        self.lbl_result = QLabel("Hasil: —", objectName="resultLabel")

        card_layout.addWidget(lbl1)
        card_layout.addWidget(self.input1)
        card_layout.addWidget(self.err1)
        card_layout.addWidget(lbl_op)
        card_layout.addWidget(self.combo_op)
        card_layout.addWidget(lbl2)
        card_layout.addWidget(self.input2)
        card_layout.addWidget(self.err2)
        card_layout.addLayout(btn_layout)
        card_layout.addWidget(self.lbl_result)

        root.addWidget(card, stretch=1)

        self.status_error = QLabel(
            "⚠ Input tidak valid — tombol Hitung dinonaktifkan",
            objectName="statusError"
        )
        self.status_error.setVisible(False)
        root.addWidget(self.status_error)

    def _connect_signals(self):
        self.input1.textChanged.connect(self._on_input1_changed)
        self.input2.textChanged.connect(self._on_input2_changed)

        self.btn_hitung.clicked.connect(self._hitung)
        self.btn_clear.clicked.connect(self._clear)

    def _setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key_Return), self).activated.connect(self._hitung)
        QShortcut(QKeySequence(Qt.Key_Enter), self).activated.connect(self._hitung)
        QShortcut(QKeySequence(Qt.Key_Escape), self).activated.connect(self._clear)

    def _on_input1_changed(self, text: str):
        is_valid = self.input1.is_valid()
        self.err1.setVisible(bool(text) and not is_valid)
        self._update_hitung_button()

    def _on_input2_changed(self, text: str):
        is_valid = self.input2.is_valid()
        self.err2.setVisible(bool(text) and not is_valid)
        self._update_hitung_button()

    def _update_hitung_button(self):
        both_valid = self.input1.is_valid() and self.input2.is_valid()
        self.btn_hitung.setEnabled(both_valid)
        self.status_error.setVisible(
            bool(self.input1.text() or self.input2.text()) and not both_valid
        )

    def _hitung(self):
        if not self.btn_hitung.isEnabled():
            return

        a = float(self.input1.text())
        b = float(self.input2.text())
        op_index = self.combo_op.currentIndex()

        ops = {
            0: ("+", lambda x, y: x + y),
            1: ("−", lambda x, y: x - y),
            2: ("×", lambda x, y: x * y),
            3: ("÷", lambda x, y: x / y if y != 0 else None),
        }

        simbol, fungsi = ops[op_index]
        hasil = fungsi(a, b)

        if hasil is None:
            self.lbl_result.setText("⚠ Error: Pembagian dengan nol!")
            self.lbl_result.setStyleSheet(
                "font-size:14px;color:#E53E3E;background:#fff5f5;"
                "border:1px solid #fcc;border-radius:6px;padding:10px;"
                "qproperty-alignment: AlignCenter;"
            )
        else:
            hasil_str = int(hasil) if hasil == int(hasil) else round(hasil, 10)
            self.lbl_result.setText(
                f"Hasil: {hasil_str}"
            )
            self.lbl_result.setStyleSheet(
                "font-size:14px;color:#1a5e20;background:#f1f8e9;"
                "border:1px solid #a5d6a7;border-radius:6px;padding:10px;"
                "qproperty-alignment: AlignCenter;"
            )

    def _clear(self):
        self.input1.clear()
        self.input2.clear()
        self.input1.setStyleSheet(STYLE_VALID)
        self.input2.setStyleSheet(STYLE_VALID)
        self.err1.setVisible(False)
        self.err2.setVisible(False)
        self.lbl_result.setText("Hasil: —")
        self.lbl_result.setStyleSheet(
            "font-size:14px;color:#333;background:white;"
            "border:1px solid #ddd;border-radius:6px;padding:10px;"
            "qproperty-alignment: AlignCenter;"
        )
        self.status_error.setVisible(False)
        self._update_hitung_button()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Konfirmasi Keluar",
            "Apakah Anda yakin ingin menutup aplikasi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Kalkulator()
    window.show()
    sys.exit(app.exec())