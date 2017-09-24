# IN PROGRESS BUGGY LEXER/PARSER

# Simple iterator over string input
class InStream:
    def __init__(self,inp):
	'''initializes the object and stores string and pointers'''
        self.inp = inp
        self.pos = 0
        self.line = 1
        self.col = 1;
    def nextCh(self):
	'''gets next char in the sequence'''
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
	'''looks at next char but doesnt dequeue it'''
        if self.pos >= len(self.inp):
            self.croak("END")
            return
        return self.inp[self.pos]
    def eof(self):
	'''checks for the end'''
        return self.pos >= len(inp)
    def croak(self,msg):
	'''special error protocol'''
        raise Exception(msg + "...Oh no you be clownin'!  (" + str(self.line) + ":" + str(self.col) + ")")

