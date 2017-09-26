# Untested
def evaluate(exp, env):
    cur = exp["type"]
    if (cur == 'num'):
        return cur['value']
    elif (cur == 'str'):
        return cur['value']
    elif (cur == 'bool'):
        return cur['value']
    elif (cur == 'var'):
        return env.get(exp["value"])
    elif (cur == "assign"):
        if (exp["left"]["type"] != 'var'):
            print("error")
        else:
            return env.set(exp["left"]["value"], evaluate(exp["right"], env))
    elif (cur == "binary"):
        return applyOp(exp["operator"], evaluate(exp["left"], env), evaluate(exp["right"], env))
    elif (cur == "lambda"):
        return makeFunction(env, exp)
    elif (cur =="if"):
        cond = evaluate(exp.cond, env)
        if (cond != False):
            return evaluate(exp["then"], env)
        if "else" in exp:
            return evaluate(exp["else"], env)
        return False
    elif (cur == "prog"):
        val = False
        def inner(x):
            val = evaluate(x, env)
        for i in exp[prog]:
            inner(i)
        return val
    elif (cur == 'call'):
        fun = evaluate(exp["func"], env)
        a = []
        for i in exp["args"]:
            a.append(evaluate(arg, env))
        return fun(a)
    else:
        print("Fallthrough Error")
        
    
