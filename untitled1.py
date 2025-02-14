
import tkinter as tk
import math


# Backend class for calculator operations
class CalculatorBackend:
    def calculate_expression(self, expression):
        """
        Calculate the result of a given arithmetic expression.
        :param expression: The arithmetic expression to be calculated.
        :return: The result of the calculation or "Error" if an exception occurs.
        """
        try:
            # Define operators and their corresponding calculation functions
            operators = {'+': lambda x, y: x + y,
                         '-': lambda x, y: x - y,
                         '*': lambda x, y: x * y,
                         '/': lambda x, y: x / y if y != 0 else float('inf')}
            # Define operator precedence
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

            def apply_operator(operators_stack, values_stack):
                """
                Apply the operator on top of the operators stack to the top two values on the values stack.
                :param operators_stack: Stack storing operators.
                :param values_stack: Stack storing values.
                """
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

            result = values[-1]
            # Check if the result is a float and its decimal part is 0, convert it to an integer if true
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return result
        except Exception:
            return "Error"

    def calculate_trig(self, func, num):
        """
        Calculate trigonometric functions for a given number.
        :param func: The trigonometric function name (e.g., "sin", "cos", etc.).
        :param num: The input number.
        :return: The result of the trigonometric calculation or "Error" if an exception occurs.
        """
        try:
            if func == "sin":
                result = math.sin(math.radians(num))
            elif func == "cos":
                result = math.cos(math.radians(num))
            elif func == "tan":
                result = math.tan(math.radians(num))
            elif func == "asin":
                if -1 <= num <= 1:
                    result = math.degrees(math.asin(num))
                else:
                    return "Error"
            elif func == "acos":
                if -1 <= num <= 1:
                    result = math.degrees(math.acos(num))
                else:
                    return "Error"
            elif func == "atan":
                result = math.degrees(math.atan(num))
            # Check if the result is a float and its decimal part is 0, convert it to an integer if true
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return result
        except ValueError:
            return "Error"

    def calculate_square(self, num):
        """
        Calculate the square of a given number.
        :param num: The input number.
        :return: The square of the number or "Error" if an exception occurs.
        """
        try:
            result = num ** 2
            # Check if the result is a float and its decimal part is 0, convert it to an integer if true
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return result
        except ValueError:
            return "Error"

    def calculate_sqrt(self, num):
        """
        Calculate the square root of a given number.
        :param num: The input number.
        :return: The square root of the number or "Error" if the input is invalid or an exception occurs.
        """
        try:
            if num >= 0:
                result = math.sqrt(num)
                # Check if the result is a float and its decimal part is 0, convert it to an integer if true
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                return result
            else:
                return "Error"
        except ValueError:
            return "Error"


# Front - end GUI class for the calculator
class CalculatorGUI:
    def __init__(self, root):
        """
        Initialize the calculator GUI.
        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Calculator")
        self.backend = CalculatorBackend()

        # Variable to hold the display content
        self.display_var = tk.StringVar()
        # Entry widget to display input and results
        self.display = tk.Entry(root, textvariable=self.display_var, font=("Arial", 24), bd=10, insertwidth=4, width=14,
                                justify="right", state="readonly")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Define the layout of calculator buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('sin', 5, 1), ('cos', 5, 2), ('tan', 5, 3),
            ('asin', 6, 0), ('acos', 6, 1), ('atan', 6, 2),
            ('Square', 7, 0), ('Square Root', 7, 1)
        ]

        # Create and place calculator buttons
        for (text, row, col) in buttons:
            button = tk.Button(
                root, text=text, font=("Arial", 18), padx=20, pady=20,
                command=lambda symbol=text: self.button_click(symbol)
            )
            button.grid(row=row, column=col, padx=5, pady=5)

    def button_click(self, symbol):
        """
        Handle button click events.
        :param symbol: The symbol on the clicked button.
        """
        current = self.display_var.get()

        if symbol == "C":
            # Clear the display
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
            # Append the symbol to the current display content
            self.display_var.set(current + symbol)


if __name__ == "__main__":
    root = tk.Tk()
    # Create an instance of the calculator GUI
    calculator_gui = CalculatorGUI(root)
    root.mainloop()