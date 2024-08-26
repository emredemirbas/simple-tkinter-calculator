import tkinter as tk
from tkinter import ttk
from evaluator import Evaluator

ev = Evaluator()


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator App")
        self.geometry("640x480")

        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 16))

        self.columnconfigure(0, weight=90)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=15)

        self.left_frame = InputFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.right_frame = HistoryFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


class InputFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        for i in range(4):
            self.columnconfigure(i, weight=1)

        for i in range(9):
            self.rowconfigure(i, weight=1)

        self.entry = ttk.Entry(self, font=("Helvetica", 16, "bold"))
        self.entry.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.entry.bind("<Return>", self.display_result)

        self.add_numeric_buttons()
        self.add_operator_buttons()
        self.add_trivial_buttons()

    def get_expression(self):
        return self.entry.get()

    def get_result(self):
        return ev.evaluate_infix_expression(self.get_expression())

    def display_result(self, event=None):
        expression = self.entry.get()
        result = ev.evaluate_infix_expression(expression)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, result)

        self.master.right_frame.add_to_expression_list(f"{expression} = {result}")

    def button_click(self, button_val):
        self.entry.insert(len(self.entry.get()), button_val)
        # print(self.entry.get())

    def backspace(self):
        self.entry.delete(len(self.entry.get()) - 1)

    def negate(self):
        expr = self.entry.get()
        if not expr:
            return
        if not expr.startswith("-"):
            self.entry.insert(0, "-")
        else:
            self.entry.delete(0)

    def add_numeric_buttons(self):
        num = 1
        row_index = 2

        while row_index >= 0:
            for column_index in range(3):
                button = ttk.Button(self, text=num, command=lambda x=num: self.button_click(x))
                button.grid(row=row_index + 1, column=column_index, sticky="nsew", padx=1, pady=1)
                num += 1
            row_index -= 1

        zero_button = ttk.Button(self, text=0, command=lambda: self.button_click(0))
        zero_button.grid(row=4, column=1, sticky="nsew", padx=1, pady=1)

    def add_operator_buttons(self):
        operators = ["/", "*", "-", "+", "(", ")"]

        row_index = 1
        for op in operators:
            ttk.Button(self, text=op, command=lambda operator=op: self.button_click(operator)).grid(row=row_index,
                                                                                                    column=3,
                                                                                                    sticky="nsew")
            row_index += 1

    def add_trivial_buttons(self):
        ttk.Button(self, text="⌫", command=self.backspace).grid(row=0, column=3, sticky="nsew")
        ttk.Button(self, text="NEG", command=self.negate).grid(row=4, column=0, sticky="nsew")
        ttk.Button(self, text=".", command=lambda: self.button_click(".")).grid(row=4, column=2, sticky="nsew")
        ttk.Button(self, text="=", command=self.display_result).grid(row=7, column=3,
                                                                     sticky="nsew")
        ttk.Button(self, text="DEL", command=lambda: self.entry.delete(0, tk.END)).grid(row=8, column=3, sticky="nsew")


class HistoryFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.dummy_text = "There's no history yet"

        self.label = ttk.Label(self, text="History")
        self.label.grid(row=0, column=0, sticky="w")

        self.delete_button = ttk.Button(self, text="🗑", command=self.clear_expression_list)
        self.delete_button.grid(row=5, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.expression_list = tk.Listbox(self)
        self.expression_list.grid(row=1, column=0, sticky="nsew")
        self.expression_list.insert(0, self.dummy_text)

    def add_to_expression_list(self, expression):
        if expression:
            self.expression_list.insert(0, expression)
            if self.expression_list.get(tk.END) == self.dummy_text:
                self.expression_list.delete(tk.END)

    def clear_expression_list(self):
        self.expression_list.delete(0, tk.END)
        self.expression_list.insert(0, "There's no history yet")


# TEMPLATE
class InputForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=0, sticky="ew")

        self.entry.bind("<Return>", self.add_to_list)

        self.entry_btn = ttk.Button(self, text="Add", command=self.add_to_list)
        self.entry_btn.grid(row=0, column=1)

        self.entry_btn2 = ttk.Button(self, text="Clear", command=self.clear_list)
        self.entry_btn2.grid(row=0, column=2)

        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=1, column=0, columnspan=3, sticky="nsew")

    def add_to_list(self, event=None):
        text = self.entry.get()
        if text:
            self.text_list.insert(tk.END, text)
            self.entry.delete(0, tk.END)

    def clear_list(self):
        self.text_list.delete(0, tk.END)


if __name__ == "__main__":
    main()
