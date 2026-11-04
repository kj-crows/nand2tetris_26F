class Symbols:
    def __init__(self):
        self.symbols = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "SCREEN": 16384, "KBD": 24576,
        }
        for i in range(16):
            self.symbols[f"R{i}"] = i

    def contains(self, item):
        return item in self.symbols

    def addEntry(self, item, address):
        self.symbols[item] = address

    def GetAddress(self, item):
        return self.symbols[item]