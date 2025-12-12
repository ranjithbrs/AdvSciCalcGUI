import math
import tkinter as tk
from tkinter import messagebox

def clear_fields():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)

def clear_history():
    history_box.delete(0, tk.END)

def exit_app():
    root.destroy()

def calculate(operation):
    try:
        if operation == "sqrt":
            num = float(entry1.get())
            result = math.sqrt(num) if num >= 0 else "Error: Negative value."
        elif operation == "!":
            num = int(entry1.get())
            result = math.factorial(num) if num >= 0 else "Error: Negative value."
        elif operation == "log":
            num = float(entry1.get())
            base = float(entry2.get())
            result = math.log(num, base) if num > 0 and base > 1 else "Error: Invalid input."
        elif operation == "sin":
            result = round(math.sin(math.radians(float(entry1.get()))), 6)
        elif operation == "cos":
            result = round(math.cos(math.radians(float(entry1.get()))), 6)
        elif operation == "tan":
            angle = float(entry1.get())
            result = "Error: Undefined." if angle % 180 == 90 else round(math.tan(math.radians(angle)), 6)
        elif operation == "cot":
            angle = float(entry1.get())
            result = "Error: Undefined." if angle % 180 == 0 else round(1 / math.tan(math.radians(angle)), 6)
        elif operation == "sec":
            angle = float(entry1.get())
            result = "Error: Undefined." if angle % 180 == 90 else round(1 / math.cos(math.radians(angle)), 6)
        elif operation == "cosec":
            angle = float(entry1.get())
            result = "Error: Undefined." if angle % 180 == 0 else round(1 / math.sin(math.radians(angle)), 6)
        elif operation == "exp":
            result = round(math.exp(float(entry1.get())), 6)
        elif operation == "+":
            result = float(entry1.get()) + float(entry2.get())
        elif operation == "-":
            result = float(entry1.get()) - float(entry2.get())
        elif operation == "*":
            result = float(entry1.get()) * float(entry2.get())
        elif operation == "/":
            result = "Error: Division by zero." if float(entry2.get()) == 0 else float(entry1.get()) / float(entry2.get())
        elif operation == "**":
            result = float(entry1.get()) ** float(entry2.get())
        elif operation == "%":
            result = "Error: Division by zero." if float(entry2.get()) == 0 else float(entry1.get()) % float(entry2.get())
        elif operation == "//":
            result = "Error: Division by zero." if float(entry2.get()) == 0 else float(entry1.get()) // float(entry2.get())
        else:
            result = "Error: Invalid input."
        messagebox.showinfo("Result", f"Result: {result}")
        history_box.insert(tk.END, f"{operation} → {result}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Advanced Calculator")
root.configure(bg="#1e1e2f")

label_style = {"bg": "#1e1e2f", "fg": "#ffffff", "font": ("Arial", 12)}
entry_style = {"bg": "#2e2e3f", "fg": "#ffffff", "font": ("Arial", 12)}

tk.Label(root, text="First Number / Angle", **label_style).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry1 = tk.Entry(root, **entry_style)
entry1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

tk.Label(root, text="Second Number / Base", **label_style).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry2 = tk.Entry(root, **entry_style)
entry2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

frame_buttons = tk.Frame(root, bg="#1e1e2f")
frame_buttons.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

button_style = {
    "bg": "#4e4e6f", "fg": "#ffffff",
    "activebackground": "#6e6e8f", "activeforeground": "#ffffff",
    "font": ("Arial", 11), "width": 8, "height": 2
}

buttons = [
    ("+", "+"), ("-", "-"), ("*", "*"), ("/", "/"),
    ("**", "**"), ("sqrt", "sqrt"), ("%", "%"), ("log", "log"),
    ("!", "!"), ("//", "//"), ("sin", "sin"), ("cos", "cos"),
    ("tan", "tan"), ("cot", "cot"), ("sec", "sec"), ("cosec", "cosec"),
    ("exp", "exp"), ("Clear", "clear"), ("Clear History", "clear_history"), ("Exit", "exit")
]

row, col = 0, 0
for text, op in buttons:
    if op == "clear":
        cmd = clear_fields
    elif op == "clear_history":
        cmd = clear_history
    elif op == "exit":
        cmd = exit_app
    else:
        cmd = lambda o=op: calculate(o)
    tk.Button(frame_buttons, text=text, command=cmd, **button_style).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    col += 1
    if col > 3:
        col = 0
        row += 1

history_box = tk.Listbox(root, bg="#2e2e3f", fg="#ffffff", font=("Arial", 11), width=30, height=15)
history_box.grid(row=2, column=2, rowspan=6, padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()