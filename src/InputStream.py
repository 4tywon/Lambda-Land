# Input Stream Object
class InStream:
    def __init__(self,inp):
        self.inp = inp
        self.pos = 0
        self.line = 1
        self.col = 1;
    def nextCh(self):
        if self.pos >= len(self.inp):
            self.croak("END")
            return
        ch = self.inp[self.pos]
        self.pos = self.pos + 1
        if ch == "\n":
            self.line = self.line + 1
            self.col = 0
        else:
            self.col = self.col + 1
        return ch
    def peek(self):
        if self.pos >= len(self.inp):
            self.croak("END")
            return
        return self.inp[self.pos]
    def eof(self):
        return self.peek() == ""
    def croak(self,msg):
        raise Exception(msg + "...Oh no you be clownin'!  (" + str(self.line) + ":" + str(self.col) + ")")
