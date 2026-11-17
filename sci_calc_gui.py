import math
import os
import re
import tkinter as tk
from tkinter import messagebox, ttk
import sci_calc

def transform_factorials(expr: str) -> str:
    """Transforms arbitrary factorial expressions (including nested parentheses) into fact(...) calls."""
    while "!" in expr:
        idx = expr.index("!")
        if idx > 0 and expr[idx - 1] == ")":
            depth = 1
            j = idx - 2
            while j >= 0 and depth > 0:
                if expr[j] == ")":
                    depth += 1
                elif expr[j] == "(":
                    depth -= 1
                j -= 1
            inner = expr[j + 1 : idx]
            expr = expr[: j + 1] + f"fact({inner})" + expr[idx + 1 :]
        else:
            m = re.search(r'(\d+(?:\.\d+)?)\s*!$', expr[: idx + 1])
            if m:
                num_str = m.group(1)
                start = m.start(1)
                expr = expr[:start] + f"fact({num_str})" + expr[idx + 1 :]
            else:
                break
    return expr

def add_implicit_multiplication(expr: str) -> str:
    """Inserts multiplication operators for expressions like 2(5), 2pi, 3sqrt(9), and (2+3)(4+5)."""
    # Number followed by parenthesis, constant, or function name: 2( -> 2*(, 2pi -> 2*pi
    expr = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', expr)
    # Closing parenthesis followed by digit, opening parenthesis, constant, or function: )2 -> )*2, )( -> )*(
    expr = re.sub(r'\)\s*([0-9a-zA-Z(])', r')*\1', expr)
    return expr

class ScientificCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("640x520")
        self.root.minsize(580, 480)
        self.root.configure(bg="#1e1e2e")

        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "calculator.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self.angle_mode = "deg"  # "deg" or "rad"
        self.last_ans = ""
        self.expression = ""
        self.just_evaluated = False  # Flags when display holds fresh result for overwrite/chaining

        self.create_styles()
        self.create_layout()
        self.bind_events()

        # Set initial keyboard focus to root window for instant hotkeys
        self.root.focus_set()

    def create_styles(self):
        self.bg_color = "#1e1e2e"
        self.panel_bg = "#282a36"
        self.btn_bg = "#383a59"
        self.btn_fg = "#f8f8f2"
        self.btn_accent = "#6272a4"
        self.btn_op = "#ff79c6"
        self.btn_eq = "#50fa7b"
        self.btn_eq_fg = "#282a36"
        self.btn_clear = "#ff5555"

    def create_layout(self):
        # Configure Grid Weights
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

        # Top Display Container
        display_frame = tk.Frame(self.root, bg=self.panel_bg, bd=2, relief="sunken")
        display_frame.grid(row=0, column=0, columnspan=2, padx=12, pady=12, sticky="nsew")
        display_frame.columnconfigure(0, weight=1)

        # Expression Label (History / Previous step)
        self.expr_label = tk.Label(
            display_frame, text="", anchor="e", bg=self.panel_bg, fg="#8be9fd",
            font=("Consolas", 11)
        )
        self.expr_label.grid(row=0, column=0, padx=10, pady=(6, 0), sticky="ew")

        # Main Entry Display
        self.display = tk.Entry(
            display_frame, font=("Consolas", 22, "bold"), bg=self.panel_bg, fg="#f8f8f2",
            bd=0, justify="right", insertbackground="#f8f8f2", takefocus=True
        )
        self.display.grid(row=1, column=0, padx=10, pady=(0, 6), sticky="ew")
        self.display.insert(0, "0")

        # Keypad & History Frames
        keypad_frame = tk.Frame(self.root, bg=self.bg_color)
        keypad_frame.grid(row=1, column=0, padx=(12, 6), pady=(0, 12), sticky="nsew")

        history_frame = tk.Frame(self.root, bg=self.panel_bg, bd=1, relief="solid")
        history_frame.grid(row=1, column=1, padx=(6, 12), pady=(0, 12), sticky="nsew")
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)

        # History Header & Controls
        hist_header = tk.Frame(history_frame, bg=self.panel_bg)
        hist_header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        hist_header.columnconfigure(0, weight=1)

        tk.Label(hist_header, text="History", bg=self.panel_bg, fg="#f8f8f2", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w")
        btn_clr_hist = tk.Button(
            hist_header, text="Clear", command=self.clear_history, bg=self.btn_clear, fg="#ffffff",
            font=("Arial", 9, "bold"), bd=0, padx=6, pady=2, cursor="hand2", takefocus=True
        )
        btn_clr_hist.grid(row=0, column=1, sticky="e")

        # History Listbox + Scrollbar
        self.history_listbox = tk.Listbox(
            history_frame, bg="#21222c", fg="#f8f8f2", selectbackground="#44475a",
            selectforeground="#8be9fd", font=("Consolas", 10), bd=0, highlightthickness=0,
            takefocus=True
        )
        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        self.history_listbox.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)
        scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 5), pady=5)
        self.history_listbox.bind("<Double-Button-1>", self.recall_history)

        # Build Keypad Buttons Grid (Replaced duplicate 'rad' button with 'abs')
        buttons = [
            [("DEG", self.toggle_angle_mode, self.btn_accent), ("abs", lambda: self.add_func("abs"), self.btn_accent), ("sin", lambda: self.add_func("sin"), self.btn_accent), ("cos", lambda: self.add_func("cos"), self.btn_accent), ("tan", lambda: self.add_func("tan"), self.btn_accent), ("AC", self.all_clear, self.btn_clear)],
            [("asin", lambda: self.add_func("asin"), self.btn_accent), ("acos", lambda: self.add_func("acos"), self.btn_accent), ("atan", lambda: self.add_func("atan"), self.btn_accent), ("sec", lambda: self.add_func("sec"), self.btn_accent), ("cosec", lambda: self.add_func("cosec"), self.btn_accent), ("cot", lambda: self.add_func("cot"), self.btn_accent)],
            [("log", lambda: self.add_func("log"), self.btn_accent), ("ln", lambda: self.add_func("ln"), self.btn_accent), ("sqrt", lambda: self.add_func("sqrt"), self.btn_accent), ("exp", lambda: self.add_func("exp"), self.btn_accent), ("!", lambda: self.add_symbol("!"), self.btn_accent), ("⌫", self.backspace, self.btn_clear)],
            [("(", lambda: self.add_symbol("("), self.btn_accent), (")", lambda: self.add_symbol(")"), self.btn_accent), ("^", lambda: self.add_symbol("^"), self.btn_accent), ("%", lambda: self.add_symbol("%"), self.btn_accent), ("//", lambda: self.add_symbol("//"), self.btn_accent), ("/", lambda: self.add_symbol("/"), self.btn_op)],
            [("7", lambda: self.add_symbol("7"), self.btn_bg), ("8", lambda: self.add_symbol("8"), self.btn_bg), ("9", lambda: self.add_symbol("9"), self.btn_bg), ("π", lambda: self.add_symbol("pi"), self.btn_accent), ("e", lambda: self.add_symbol("e"), self.btn_accent), ("*", lambda: self.add_symbol("*"), self.btn_op)],
            [("4", lambda: self.add_symbol("4"), self.btn_bg), ("5", lambda: self.add_symbol("5"), self.btn_bg), ("6", lambda: self.add_symbol("6"), self.btn_bg), ("Ans", self.add_ans, self.btn_accent), ("x²", lambda: self.add_symbol("^2"), self.btn_accent), ("-", lambda: self.add_symbol("-"), self.btn_op)],
            [("1", lambda: self.add_symbol("1"), self.btn_bg), ("2", lambda: self.add_symbol("2"), self.btn_bg), ("3", lambda: self.add_symbol("3"), self.btn_bg), (".", lambda: self.add_symbol("."), self.btn_bg), ("0", lambda: self.add_symbol("0"), self.btn_bg), ("+", lambda: self.add_symbol("+"), self.btn_op)],
        ]

        for r in range(len(buttons) + 1):
            keypad_frame.rowconfigure(r, weight=1)
        for c in range(6):
            keypad_frame.columnconfigure(c, weight=1)

        self.mode_btn = None
        for r_idx, row in enumerate(buttons):
            for c_idx, (text, cmd, color) in enumerate(row):
                btn = tk.Button(
                    keypad_frame, text=text, command=cmd, bg=color, fg=self.btn_fg,
                    font=("Arial", 10, "bold"), bd=0, relief="flat", cursor="hand2",
                    activebackground="#6272a4", activeforeground="#ffffff", takefocus=True
                )
                btn.grid(row=r_idx, column=c_idx, padx=2, pady=2, sticky="nsew")
                if text == "DEG":
                    self.mode_btn = btn

        # Equals button spanning bottom row
        eq_btn = tk.Button(
            keypad_frame, text="=", command=self.evaluate, bg=self.btn_eq, fg=self.btn_eq_fg,
            font=("Arial", 12, "bold"), bd=0, cursor="hand2", activebackground="#8be9fd",
            takefocus=True
        )
        eq_btn.grid(row=len(buttons), column=0, columnspan=6, padx=2, pady=2, sticky="nsew")

    def bind_events(self):
        """Binds keyboard shortcuts and handles direct typing smoothly."""
        self.root.bind("<Return>", lambda e: self.evaluate())
        self.root.bind("<KP_Enter>", lambda e: self.evaluate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.all_clear())
        self.root.bind("<Key>", self.handle_key_press)

    def handle_key_press(self, event):
        """Global keyboard handler for digits, operators, shortcuts, and navigation."""
        char = event.char
        keysym = event.keysym

        # If user types directly in Entry, sanitize leading zero / errors
        if event.widget == self.display:
            if keysym in ("Return", "KP_Enter"):
                self.evaluate()
                return "break"
            if keysym == "Escape":
                self.all_clear()
                return "break"
            cur = self.get_display_text()
            if cur in ["0", "Error: Division by zero.", "Error: Invalid input.", "Error: Undefined.", "Error: Overflow.", "Error: Complex result."]:
                if char in "0123456789":
                    self.set_display_text(char)
                    return "break"
                elif char in "+-*/%^":
                    self.set_display_text(f"0{char}")
                    return "break"
            return

        if char in "0123456789.":
            self.add_symbol(char)
            return "break"
        elif char in "+-*/%()^!":
            self.add_symbol(char)
            return "break"
        elif char == "=":
            self.evaluate()
            return "break"
        elif char.lower() == "c":
            self.all_clear()
            return "break"
        elif char.lower() == "d":
            self.toggle_angle_mode()
            return "break"

    def toggle_angle_mode(self):
        if self.angle_mode == "deg":
            self.set_angle_mode("rad")
        else:
            self.set_angle_mode("deg")

    def set_angle_mode(self, mode):
        self.angle_mode = mode
        if self.mode_btn:
            self.mode_btn.configure(
                text="RAD" if mode == "rad" else "DEG",
                bg="#ffb86c" if mode == "rad" else self.btn_accent
            )

    def get_display_text(self):
        return self.display.get()

    def set_display_text(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(text))

    def add_symbol(self, symbol):
        current = self.get_display_text()

        # If previous operation completed and user types a digit or '.', start fresh
        if self.just_evaluated:
            self.just_evaluated = False
            if symbol.startswith(("+", "-", "*", "/", "%", "^")):
                # Chain operator directly onto existing result
                pass
            else:
                # Fresh new expression
                if symbol == ".":
                    self.set_display_text("0.")
                else:
                    self.set_display_text(symbol)
                return

        # Replace initial 0 or previous error display cleanly
        if current in ["0", "Error: Division by zero.", "Error: Invalid input.", "Error: Undefined.", "Error: Overflow.", "Error: Complex result."]:
            if symbol == ".":
                self.set_display_text("0.")
            elif symbol.startswith(("+", "-", "*", "/", "%", "^")):
                self.set_display_text(f"0{symbol}")
            else:
                self.set_display_text(symbol)
        else:
            self.display.insert(tk.END, symbol)

    def add_func(self, func_name):
        current = self.get_display_text()

        if self.just_evaluated:
            self.just_evaluated = False
            self.set_display_text(f"{func_name}(")
            return

        if current in ["0", "Error: Division by zero.", "Error: Invalid input.", "Error: Undefined.", "Error: Overflow.", "Error: Complex result."]:
            self.set_display_text(f"{func_name}(")
        else:
            self.display.insert(tk.END, f"{func_name}(")

    def add_ans(self):
        if self.last_ans != "":
            self.add_symbol(str(self.last_ans))

    def backspace(self):
        self.just_evaluated = False
        current = self.get_display_text()
        if len(current) > 1 and not current.startswith("Error:"):
            self.set_display_text(current[:-1])
        else:
            self.set_display_text("0")

    def all_clear(self):
        self.just_evaluated = False
        self.set_display_text("0")
        self.expr_label.configure(text="")

    def clear_history(self):
        self.history_listbox.delete(0, tk.END)

    def recall_history(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            if "=" in item:
                val = item.split("=")[-1].strip()
                self.set_display_text(val)
                self.just_evaluated = True

    def evaluate(self):
        expr = self.get_display_text()
        if not expr:
            return

        self.expr_label.configure(text=f"{expr} =")
        try:
            # Environment for expression evaluation using sci_calc module
            eval_env = {
                "math": math,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "sin": lambda x: sci_calc.sine(x, self.angle_mode),
                "cos": lambda x: sci_calc.cosine(x, self.angle_mode),
                "tan": lambda x: sci_calc.tangent(x, self.angle_mode),
                "sec": lambda x: sci_calc.sec(x, self.angle_mode),
                "cosec": lambda x: sci_calc.cosec(x, self.angle_mode),
                "cot": lambda x: sci_calc.cot(x, self.angle_mode),
                "asin": lambda x: sci_calc.arcsin(x, self.angle_mode),
                "acos": lambda x: sci_calc.arccos(x, self.angle_mode),
                "atan": lambda x: sci_calc.arctan(x, self.angle_mode),
                "sqrt": sci_calc.square_root,
                "log": sci_calc.logarithm,
                "ln": sci_calc.natural_log,
                "exp": sci_calc.exponential,
                "fact": sci_calc.factorial,
            }
            
            # 1. Transform ^ to Python exponentiation **
            eval_expr = expr.replace("^", "**")
            
            # 2. Add implicit multiplication: 2pi -> 2*pi, 2(5) -> 2*(5), (2+3)(4+5) -> (2+3)*(4+5)
            eval_expr = add_implicit_multiplication(eval_expr)

            # 3. Transform factorial notation to fact(...) including nested parentheses and numbers
            eval_expr = transform_factorials(eval_expr)

            result = eval(eval_expr, {"__builtins__": None, "sci_calc": sci_calc}, eval_env)
            
            if isinstance(result, (float, int)):
                if isinstance(result, float):
                    result = round(result, 6)
                    if result.is_integer():
                        result = int(result)
                res_str = str(result)
            else:
                res_str = str(result)

            self.set_display_text(res_str)
            if not res_str.startswith("Error:"):
                self.last_ans = res_str
                self.just_evaluated = True
                self.history_listbox.insert(tk.END, f"{expr} = {res_str}")
                self.history_listbox.yview(tk.END)
            else:
                self.just_evaluated = False

        except ZeroDivisionError:
            self.set_display_text("Error: Division by zero.")
            self.just_evaluated = False
        except Exception:
            self.set_display_text("Error: Invalid input.")
            self.just_evaluated = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculatorGUI(root)
    root.mainloop()
