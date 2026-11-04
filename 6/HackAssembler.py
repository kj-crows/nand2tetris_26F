from Parser import Parser, InstructionType
from CodeModule import Code
from Symbols import Symbols
import os
import sys

def assembleNoL(filename):
    parse = Parser(filename)
    code = Code()
    symbols = Symbols()

    print(f'{filename} has {len(parse.lines)} code lines.\n')

    # pass 1
    romAddress = 0
    while parse.hasMoreLines():
        parse.advance()
        if parse.instructionType() is InstructionType.L_INSTRUCTION:
            symbols.addEntry(parse.symbol(), romAddress)   # label add to symbols w/ next instruction
        else:
            romAddress += 1 #increment

    # pass 2
    parse.reset()
    nextVariable = 16
    outlines = []
    while parse.hasMoreLines():
        parse.advance()
        findType = parse.instructionType()

        if findType is InstructionType.A_INSTRUCTION:
            symbolFound = parse.symbol()
            if symbolFound.isdigit():
                value = int(symbolFound)
            elif symbols.contains(symbolFound):
                value = symbols.GetAddress(symbolFound)
            else:                                   # new variable
                value = nextVariable
                symbols.addEntry(symbolFound, value)
                nextVariable += 1
            outlines.append(f'{value:016b}')

        elif findType is InstructionType.C_INSTRUCTION: 
            dest = parse.dest() if parse.dest() else '000' # is there a destination? 
            jump = parse.jump() if parse.jump() else '000' # is there a jump?
            outlines.append('111' + code.comp(parse.comp()) # add the top 111, compute from code module
                            + code.dest(dest) + code.jump(jump))
        # L_INSTRUCTIONs produce no output

    #output file
    basename, ext = os.path.splitext(filename)
    outfilename = basename + '.hack'
    with open(outfilename, 'w') as outfile:
        for line in outlines:
            outfile.write(line + '\n')
    print(f'Wrote {len(outlines)} lines to {outfilename}.\n')

if __name__ == '__main__':
    assembleNoL(sys.argv[1])