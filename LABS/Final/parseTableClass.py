class ParseTable:
    _parseTable = {}

    def put(self, key1, key2, value):
        self._parseTable[(key1, key2)] = value
    
    def getParseTable(self):  
        return self._parseTable
    
    def __str__(self):
        str = ""
        for keys in self._parseTable.keys():
            str += "M["+",".join(keys)+"] = ["
            str += ", ".join(self._parseTable[keys]) + "]"
            str += "\n"
        return str