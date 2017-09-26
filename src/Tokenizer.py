import InputStream

class TokenStream:
    def __init__(self, inp):
        self.input = InStream(inp)
        self.current = None
        self.keywords = ["if", "then", "else", "lambda", "@", "true", "false"]
    def is_keyword(self,x):
        return x in self.keywords
    def is_digit(self, ch):
        return ch.isdigit()
    def is_id_start(self, ch):
        return ch.isalpha() or ch in "@_"
    def is_id(self, ch):
        return self.is_id_start(ch) or ch in "?!-<>=0123456789"
    def is_op_char(self, ch):
        return ch in "+-*/%=&|<>!"
    def is_punc(self,ch):
        return ch in ",;(){}[]"
    def is_whitespace(self,ch):
        return ch in " \t\n"
    def read_while(self, pred):
        s = ""
        while not self.input.eof() and pred(self.input.peek()):
            s = s + self.input.nextCh();
        return s
    def read_number(self):
        has_dot = False
        def inner(ch):
            if (ch == "."):
                if has_dot:
                    return False
                has_dot = True
                return True
            return ch.isdigit()
        
        number = self.read_while(inner)
        return {"type": "num", "value" : int(number)}
    def read_ident(self):
        id = self.read_while(self.is_id)
        t = "var"
        if self.is_keyword(id):
            t = "kw"
        return {"type": t, "value" : id}
    def read_escaped(self, end):
        escaped = False
        s = ""
        self.input.nextCh()
        while(not self.input.eof()):
            ch = self.input.nextCh()
            if (escaped):
                s = s + ch
            elif (ch == "\\"):
                escaped = True
            elif (ch == end):
                break
            else:
                s += ch
        return s
    def read_string(self):
        return {"type":"str", "value" : self.read_escaped('"')}
    def skip_comment(self):
        self.read_while(lambda ch: ch != "\n")
        self.input.nextCh()
    def read_next(self):
        self.read_while(self.is_whitespace)
        if (self.input.eof()):
            return None
        ch = self.input.peek()
        if (ch == "#"):
            self.skip_comment()
            return read_next()
        if ch =='"':
            return self.read_string()
        if self.is_digit(ch):
            return self.read_number()
        if self.is_id_start(ch):
            return self.read_ident()
        if self.is_punc(ch):
            return {"type": "punc", "value": self.read_while(self.is_punc)}
        if self.is_op_char(ch):
            return {"type": "op", "value" : self.read_while(self.is_op_char)}
        self.input.croak("Can't Handle: " + ch)
    def peek(self):
        if self.current != None:
            return self.current
        self.current = self.read_next()
        return self.current
    def nextOne(self):
        token = self.current
        self.current = None
        if token != None:
            return token
        return self.read_next()
    def eof(self):
        return self.peek() == None
    def croak(self, msg):
        self.input.croak(msg)
        