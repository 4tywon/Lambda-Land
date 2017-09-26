import Tokenizer
import InputStream
class Parser:
    PRECEDENCE = {
        "=": 1,
        "||": 2,
        "&&": 3,
        "<": 7, ">": 7, "<=": 7, ">=": 7, "==": 7, "!=": 7,
        "+": 10, "-": 10,
        "*": 20, "/": 20, "%": 20,
    }
    
    FALSE = { "type": "bool", "value": False }
    
    def __init__(self, inp):
        self.input = TokenStream(inp + " ") # TokenStream
    
    def is_punc(self, ch):
        tok = self.input.peek()
        if tok != None and tok['type'] == 'punc' and (not ch or tok['value'] == ch):
            return tok
        return False
    def is_kw(self, ch):
        tok = self.input.peek()
        if tok != None and tok['type'] == 'kw' and (not ch or tok['value'] == ch):
            return tok
        return False
    def is_op(self, ch):
        tok = self.input.peek()
        if tok != None and tok['type'] == 'op' and (not ch or tok['value'] == ch):
            return tok
        return False
    def skip_punc(self, ch):
        if (self.is_punc(ch)):
            self.input.nextOne()
        else:
            self.input.croak("Expecting Operator: \"" + str(ch) + "\"")
    def skip_kw(self, ch):
        if (self.is_kw(ch)):
            self.input.nextOne()
        else:
            self.input.croak("Expecting keyword: \"" + str(ch) + "\"")
    def skip_op(self, ch):
        if (self.is_op(ch)):
            self.input.nextOne()
        else:
            self.input.croak("Expecting Operator: \"" + str(ch) + "\"")
    def unexpected(self):
        self.input.croak("Idk what this is: " + str(self.input.peek()))
    def maybe_binary(self, left, my_prec):
        tok = self.is_op('')
        if (tok):
            his_prec = self.PRECEDENCE[tok['value']]
            if his_prec > my_prec:
                self.input.nextOne()
                return self.maybe_binary({
                    "type" : "assign" if tok["value"] == "=" else "binary",
                    "operator": tok["value"],
                    "left" : left,
                    "right" : self.maybe_binary(self.parse_atom(), his_prec)
                }, my_prec)
        return left
    def delimited(self,start, stop, separator, parser):
        a = []
        first = True
        self.skip_punc(start)
        while(not self.input.eof()):
            if self.is_punc(stop):
                break
            if first:
                first = False
            else:
                self.skip_punc(separator)
            if (self.is_punc(stop)):
                break
            a.append(parser())
        self.skip_punc(stop)
        return a
    def parse_call(self, func):
        return {"type": "call", "func": func, "args" : self.delimited("(", ")", ",", self.parse_expression)
               }
    def parse_varname(self):
        name = self.input.nextOne()
        if name["type"] != "var":
            self.input.croak("Expecting variable name")
        return name['value']
    
    def parse_if(self):
        self.skip_kw("if")
        cond = self.parse_expression()
        if (not self.is_punc("{")):
            self.skip_kw("then")
        then = self.parse_expression()
        ret = {"type": "if", "cond": cond, "then" : then}
        if (self.is_kw("else")):
            self.input.nextOne()
            ret["else"] = self.parse_expression()
        return ret
    
    def parse_lambda(self):
        return {"type": "lambda", "vars" : self.delimited("(", ")", "," , self.parse_varname),
               "body": self.parse_expression()}
    
    def parse_bool(self):
        return {"type" : "bool", "value" : self.input.nextOne()["value"] == "true"}
    
    def maybe_call(self, expr):
        expr = expr()
        return self.parse_call(expr) if self.is_punc("(") else expr
    def parse_atom(self):
        def inner():
            if self.is_punc("("):
                self.input.nextOne()
                exp = self.parse_expression()
                self.skip_punc(")")
                return exp
            if self.is_punc("{"):
                return self.parse_prog()
            if self.is_kw("if"):
                return self.parse_if()
            if self.is_kw("true") or self.is_kw("false"):
                return self.parse_bool()
            if self.is_kw("lambda") or self.is_kw("@"):
                self.input.nextOne()
                return self.parse_lambda()
            tok = self.input.nextOne()
            if (tok["type"] == "var" or tok["type"] == "num" or tok["type"] == 'str'):
                return tok
            self.unexpected()
        return self.maybe_call(inner)
    def parse_toplevel(self):
        prog = []
        while(not self.input.eof()):
            prog.append(self.parse_expression())
            if not self.input.eof():
                self.skip_punc(";")
        return {"type" : "prog", "prog" : prog}
    def parse_prog(self):
        prog = self.delimited("{", "}", ";", self.parse_expression)
        if prog["length"] == 0:
            return FALSE
        if prog["length"] == 1:
            return prog[0]
        return {"type": "prog", "prog" : prog}
    def parse_expression(self):
        def inner():
            return self.maybe_binary(self.parse_atom(), 0)
        return self.maybe_call(inner)
    
    
    