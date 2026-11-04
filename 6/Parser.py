from enum import Enum

class InstructionType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3
    NO_TYPE = 4

class Parser(object):
    def __init__(self, input_file):
        self.lines = []
        self.cur = -1
        self.inputfile = input_file
        self.curtype = InstructionType.NO_TYPE
        self.curdest = None
        self.cursymbol = None
        self.curcomp = None
        self.curjump = None
        self.preprocessFile()

    def hasMoreLines(self):
        return self.cur + 1 < len(self.lines)

    def advance(self):
        if self.hasMoreLines():
            self.cur += 1
            self.interpretLine()

    def reset(self):
        '''Go back to the start so we can do a second pass.'''
        self.cur = -1
        self.curtype = InstructionType.NO_TYPE

    def instructionType(self):
        return self.curtype

    def curLine(self):
        assert 0 <= self.cur < len(self.lines), 'No current line to report'
        return self.lines[self.cur]

    def symbol(self):
        assert self.curtype in (InstructionType.A_INSTRUCTION,
                                InstructionType.L_INSTRUCTION), \
            f'symbol only for A or L type, not {self.lines[self.cur]}'
        return self.cursymbol

    def dest(self):
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'dest only for C-type, not {self.lines[self.cur]}'
        return self.curdest

    def comp(self):
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'comp only for C-type, not {self.lines[self.cur]}'
        return self.curcomp

    def jump(self):
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'jump only for C-type, not {self.lines[self.cur]}'
        return self.curjump

    def preprocessFile(self):
        try:
            with open(self.inputfile, 'r') as f:
                all_lines = f.read().split('\n')
        except FileNotFoundError:
            print(f'Read Error: could not read {self.inputfile}.')
            return
        for line in all_lines:
            line = line.split('//')[0]          # strip inline/full-line comments
            line = ''.join(line.split())        # strip ALL whitespace
            if line == '':
                continue
            self.lines.append(line)

    def interpretLine(self):
        line = self.lines[self.cur]
        # reset everything so nothing carries over from the previous line
        self.cursymbol = self.curdest = self.curcomp = self.curjump = None

        if line[0] == '@':
            self.curtype = InstructionType.A_INSTRUCTION #get just A
            self.cursymbol = line[1:]
        elif line[0] == '(':
            self.curtype = InstructionType.L_INSTRUCTION # get just label
            self.cursymbol = line[1:-1]
        else:
            self.curtype = InstructionType.C_INSTRUCTION # split C instructions
            rest = line
            if '=' in rest:
                self.curdest, rest = rest.split('=', 1)
            if ';' in rest:
                rest, self.curjump = rest.split(';', 1)
            self.curcomp = rest