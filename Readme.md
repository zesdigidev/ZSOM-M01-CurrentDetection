# Abnormal Current Detection for ZES ZSOM-M01

This Arduino-based program is designed for use with the **ZES ZSOM-M01** and the accompanying **ZSOM-M01-CS01 evaluation board**. It monitors current drawn by onboard resistors and detects abnormal current patterns based on a configurable thresholds. A Python-based GUI is included for easy visualization of normal and abnormal current logs and patterns.

---

## 🔍 Overview

- The program supports **real-time current monitoring** and **logging**.
- **Normal and abnormal current profiles** are stored in the TMR FRAMs onboard the ZSOM-M01.
- A **Python-based GUI** (included in this repository) allows users to view or retrieve stored current profiles.

---

## 🧪 Demo/Test Instructions

1. Power on the board and activate **one resistor path** only.
2. Upload and run the program on the ZSOM-M01.
3. After the program starts, toggle additional resistor paths — either individually or multiple at once.
4. The system will detect current jump as **abnormal** and log it accordingly.

---

## 📁 Repository Contents

- `ZSOM_CurrentDetection/` — Arduino sketch files
- `python_gui/` — Python GUI application for data viewing
- `images/` — Picture of the board (ZSOM-M01 + ZSOM-M01-CS01 eval board)
- `README.md` — This documentation
- `LICENSE.txt` — License file

---

## 🛠️ Requirements

- ZES ZSOM-M01 board
- ZSOM-M01-CS01 evaluation board
- Arduino IDE
- Python 3.x
- PySide6
- pyqtgraph
- pyserial
- numpy

---

## 📜 License

[MIT License](LICENSE) 

---

## ✍️ Author

- Zero-Error Systems Pte. Ltd.
