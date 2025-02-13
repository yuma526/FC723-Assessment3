import tkinter as tk
import math

class CalculatorBackend:
    def calculate_expression(self, expression):
        try:
            operators = {'+': lambda x, y: x + y,
                         '-': lambda x, y: x - y,
                         '*': lambda x, y: x * y,
                         '/': lambda x, y: x / y if y != 0 else float('inf')}
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

            def apply_operator(operators_stack, values_stack):
                operator = operators_stack.pop()
                right_operand = values_stack.pop()
                left_operand = values_stack.pop()
                values_stack.append(operators[operator](left_operand, right_operand))

            values = []
            ops = []
            i = 0
            while i < len(expression):
                if expression[i].isdigit() or expression[i] == '.':
                    num_str = ""
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    values.append(float(num_str))
                    i -= 1
                elif expression[i] in operators:
                    while (ops and ops[-1] in operators and
                           precedence[ops[-1]] >= precedence[expression[i]]):
                        apply_operator(ops, values)
                    ops.append(expression[i])
                i += 1

            while ops:
                apply_operator(ops, values)

            return values[-1]
        except Exception:
            return "Error"

    def calculate_trig(self, func, num):
        try:
            if func == "sin":
                return math.sin(math.radians(num))
            elif func == "cos":
                return math.cos(math.radians(num))
            elif func == "tan":
                return math.tan(math.radians(num))
            elif func == "asin":
                if -1 <= num <= 1:
                    return math.degrees(math.asin(num))
                else:
                    return "Error"
            elif func == "acos":
                if -1 <= num <= 1:
                    return math.degrees(math.acos(num))
                else:
                    return "Error"
            elif func == "atan":
                return math.degrees(math.atan(num))
        except ValueError:
            return "Error"

    def calculate_square(self, num):
        try:
            return num ** 2
        except ValueError:
            return "Error"

    def calculate_sqrt(self, num):
        try:
            if num >= 0:
                return math.sqrt(num)
            else:
                return "Error"
        except ValueError:
            return "Error"

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.backend = CalculatorBackend()

        self.display_var = tk.StringVar()
        self.display = tk.Entry(root, textvariable=self.display_var, font=("Arial", 24), bd=10, insertwidth=4, width=14,
                                justify="right", state="readonly")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('sin', 5, 1), ('cos', 5, 2), ('tan', 5, 3),
            ('asin', 6, 0), ('acos', 6, 1), ('atan', 6, 2),
            ('Square', 7, 0), ('Square Root', 7, 1)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(
                root, text=text, font=("Arial", 18), padx=20, pady=20,
                command=lambda symbol=text: self.button_click(symbol)
            )
            button.grid(row=row, column=col, padx=5, pady=5)

    def button_click(self, symbol):
        current = self.display_var.get()

        if symbol == "C":
            self.display_var.set("")
        elif symbol == "=":
            result = self.backend.calculate_expression(current)
            self.display_var.set(result)
        elif symbol in ["sin", "cos", "tan", "asin", "acos", "atan"]:
            try:
                num = float(current)
                result = self.backend.calculate_trig(symbol, num)
                self.display_var.set(result)
            except ValueError:
                self.display_var.set("Error")
        elif symbol == "Square":
            try:
                num = float(current)
                result = self.backend.calculate_square(num)
                self.display_var.set(result)
            except ValueError:
                self.display_var.set("Error")
        elif symbol == "Square Root":
            try:
                num = float(current)
                result = self.backend.calculate_sqrt(num)
                self.display_var.set(result)
            except ValueError:
                self.display_var.set("Error")
        else:
            self.display_var.set(current + symbol)


if __name__ == "__main__":
    root = tk.Tk()
    calculator_gui = CalculatorGUI(root)
    root.mainloop()