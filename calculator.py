import sys
import tkinter as tk

window = tk.Tk()
window.title("Calculator")
window.geometry("350x500")
window.resizable(False, False)
window.configure(bg="#1b2838")

expression = ""

display = tk.Entry(
    window,
    font=("Arial", 24),
    bg="#171a21",
    fg="#c7d5e0",
    insertbackground="#66c0f4",
    justify="right",
    bd=0
)

display.pack(
    fill="x",
    padx=15,
    pady=20,
    ipady=20
)

MOD_MASK = 0x8 if sys.platform == "darwin" else 0x4
ALLOWED_CHARS = "0123456789.+-*/"

def block_keys(event):
    if event.keysym.isdigit() or event.keysym.startswith("KP_"):
        return "break"
    if event.state & MOD_MASK and event.keysym.lower() in ("c", "a", "v"):
        return None
    return "break"

def update_display():
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def paste(event=None):
    global expression
    try:
        text = window.clipboard_get()
    except tk.TclError:
        return "break"
    text = "".join(ch for ch in text if ch in ALLOWED_CHARS)
    if text:
        expression += text
        update_display()
    return "break"

display.bind("<Key>", block_keys)
display.bind("<<Paste>>", paste)
display.bind("<<PasteSelection>>", lambda e: "break")

def button_click(value):
    global expression
    expression += str(value)
    update_display()

def clear():
    global expression
    expression = ""
    update_display()

def backspace():
    global expression
    expression = expression[:-1]
    update_display()

def calculate():
    global expression
    try:
        result = eval(expression)
        display.delete(0, tk.END)
        display.insert(tk.END, str(result))
        expression = str(result)
    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "ERROR")
        expression = ""

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

button_frame = tk.Frame(
    window,
    bg="#1b2838"
)

button_frame.pack(
    expand=True,
    fill="both",
    padx=10,
    pady=5
)

clear_button = tk.Button(
    button_frame,
    text="C",
    font=("Arial", 18, "bold"),
    bg="#c94c4c",
    fg="white",
    activebackground="#e06060",
    activeforeground="white",
    bd=0,
    command=clear
)

clear_button.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="nsew",
    padx=4,
    pady=4
)

backspace_button = tk.Button(
    button_frame,
    text="⌫",
    font=("Arial", 18, "bold"),
    bg="#417a9b",
    fg="white",
    activebackground="#5a9cc0",
    activeforeground="white",
    bd=0,
    command=backspace
)

backspace_button.grid(
    row=0,
    column=2,
    columnspan=2,
    sticky="nsew",
    padx=4,
    pady=4
)

for row_index, row in enumerate(buttons, start=1):
    for col_index, value in enumerate(row):
        if value == "=":
            command = calculate
            color, text_color, hover = "#5c7e10", "white", "#a4d007"
        elif value in ["+", "-", "*", "/"]:
            command = lambda v=value: button_click(v)
            color, text_color, hover = "#66c0f4", "#171a21", "#8fd3ff"
        else:
            command = lambda v=value: button_click(v)
            color, text_color, hover = "#2a475e", "#c7d5e0", "#316282"

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 18, "bold"),
            bg=color,
            fg=text_color,
            activebackground=hover,
            activeforeground=text_color,
            bd=0,
            command=command
        )

        button.grid(
            row=row_index,
            column=col_index,
            sticky="nsew",
            padx=4,
            pady=4
        )

for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

window.mainloop()
