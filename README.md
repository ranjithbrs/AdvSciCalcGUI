# 🧮 Advanced Scientific Calculator (AdvSciCalcGUI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

A modern, dark-themed **scientific calculator application** built in Python with **Tkinter**.  
It features an expression display screen, an interactive scientific keypad, **DEG / RAD** angle mode switching, calculation history with click-to-recall, and an isolated backend math engine with full unit test coverage.

---

## 🚀 Features

- **Modern LCD Display**: Shows current mathematical expressions and live outputs directly without modal popup interruptions.
- **Arithmetic Operations**: Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`), Modulus (`%`), Floor Division (`//`), Exponentiation (`^`).
- **Scientific Functions**: Square Root (`sqrt`), Logarithm (`log`), Natural Log (`ln`), Exponential (`exp`), Factorial (`!`), Constants ($\pi$, $e$).
- **Trigonometry**: Sine (`sin`), Cosine (`cos`), Tangent (`tan`), Secant (`sec`), Cosecant (`cosec`), Cotangent (`cot`), plus inverse functions (`asin`, `acos`, `atan`).
- **Angle Modes**: Easy toggle between **DEG** (Degrees) and **RAD** (Radians) for trigonometric calculations.
- **History Panel**: Displays recent calculations with double-click recall functionality and a one-click **Clear History** button.
- **Keyboard Shortcuts**: Supports keyboard numeric input, `Enter` to evaluate, `Backspace` to delete, and `Escape` for All Clear (`AC`).
- **CLI & Module Architecture**: `sci_calc.py` serves as both an interactive CLI and an importable math backend.

---

## 📁 Repository Structure

```
AdvSciCalcGUI/
├── sci_calc.py        # Core scientific math library & interactive CLI
├── sci_calc_gui.py    # Tkinter graphical scientific calculator
├── test_sci_calc.py   # Unit test suite
├── calculator.ico     # Window application icon
└── README.md          # Project documentation
```

---

## 💻 Getting Started

### Prerequisites
- Python 3.8+ installed (Tkinter comes pre-installed with standard Python distributions).

### Running the GUI Application
```bash
python sci_calc_gui.py
```

### Running the Interactive CLI
```bash
python sci_calc.py
```

### Running Automated Tests
```bash
python -m unittest test_sci_calc.py
```

---

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author
**Ranjith**  
Computer Science & Business Systems Undergraduate | Python, Java, SQL, AI/ML Enthusiast
