# Untested
def applyOp(op, a, b):
    if (op == "+"):
        return a + b
    elif (op == "-"):
        return a - b
    elif (op == "*"):
        return a * b
    elif (op == '/'):
        return a / b
    elif (op == '%'):
        return a % b
    elif (op == "&&"):
        return a and b
    elif (op == "||"):
        return a or b
    elif (op == "<"):
        return a < b
    elif (op == ">"):
        return a > b
    elif (op == "<="):
        return a <= b
    elif (op == ">="):
        return a >= b
    elif (op == "=="):
        return a == b
    elif (op == "!="):
        return a != b
    else:
        print("apply fallthrough")
def makeFunction(env, exp):
    def inner(arguments):
        names = exp["vars"]
        scope = env.extend()
        for i in range(len(names)):
            second = False
            if i < len(arguments):
                second = arguments[i]
            scope.define(names[i], second)
            return evaluate(exp["body"], scope)
    return inner
