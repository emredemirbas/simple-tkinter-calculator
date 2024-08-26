from stack import Stack

operators = {"+", "-", "*", "/", "(", ")"}


class Evaluator:
    def __init__(self):
        pass

    def is_expression_valid(self, expression):
        global operators
        stack = Stack()
        previous_char = None

        for i, char in enumerate(expression):
            if char == "(":
                stack.push(char)
            elif char == ")":
                if stack.is_empty() or stack.pop() != "(":
                    return False
            elif char in operators:
                if previous_char in operators and previous_char != "(" and char != "-":
                    # Invalid if two consecutive operators (unless it's a negative sign after an operator)
                    return False
            elif not self.is_operand(char):
                # If the character is not a digit and not in the operator list
                return False

            previous_char = char

        # Expression is invalid if there are unbalanced parentheses
        return stack.is_empty()

    def add_spaces_to_expression(self, expression):
        global operators
        result = ""

        for char in expression:
            if char in operators:
                result += " " + char + " "
            else:
                result += char

        return result

    def evaluate_infix_expression(self, expression):
        if not self.is_expression_valid(expression):
            raise Exception

        dummy_operator = "#"
        operator_stack = Stack()
        operand_stack = Stack()

        operator_stack.push(dummy_operator)

        for symbol in self.add_spaces_to_expression(expression).split():
            if symbol == " ":
                continue

            if self.is_operand(symbol):
                operand_stack.push(symbol)

            elif self.is_operator(symbol):
                popped_operator = operator_stack.pop()

                if self.get_operator_precedence(symbol) > self.get_operator_precedence(popped_operator):
                    operator_stack.push(popped_operator)
                    operator_stack.push(symbol)

                else:
                    while self.get_operator_precedence(symbol) <= self.get_operator_precedence(popped_operator):
                        try:
                            operand2 = operand_stack.pop()
                            operand1 = operand_stack.pop()
                            operand_stack.push(self.calculate(operand1, operand2, popped_operator))
                            popped_operator = operator_stack.pop()
                        except ZeroDivisionError:
                            print("FIX HERE!!!!!!!!!!!!!!!!!!!!")
                        operator_stack.push(popped_operator)
                        operator_stack.push(symbol)

        popped_operator = operator_stack.pop()

        while popped_operator != dummy_operator:
            try:
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                operand_stack.push(self.calculate(operand1, operand2, popped_operator))
                popped_operator = operator_stack.pop()
            except ZeroDivisionError:
                print("FIX HERE 2!!!!!!!!!!!!!!!!!!!!")

        return operand_stack.pop()

    def calculate(self, operand1, operand2, operator):
        operand1 = float(operand1)
        operand2 = float(operand2)
        result = None
        match operator:
            case "+":
                result = operand1 + operand2
            case "-":
                result = operand1 - operand2
            case "*":
                result = operand1 * operand2
            case "/":
                if operand2 == 0:
                    raise ZeroDivisionError
                result = operand1 / operand2
        return int(result) if result.is_integer() else round(result, 2)

    def is_operator(self, symbol):
        global operators
        return symbol in operators

    def is_operand(self, symbol):
        return not self.is_operator(symbol)

    # Note to myself: this method throws KeyError if what you pass in is not an actual operator.
    def get_operator_precedence(self, operator):
        precedences = {
            "#": 0,
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "(": 3,
            ")": 3
        }
        return precedences[operator]
