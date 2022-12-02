class Production:
    _left = 0
    _rules = {}

    def __init__(self, start, rules):
        self._left = start
        self._rules = rules
        
    def getRightHandSide(self):
        return self._rules

    def getLeftHandSide(self):
        return self._left
    
    def __str__(self):
        temp = self._left+"-> "
        for i, rule in enumerate(self._rules):
            for rul in rule:
                if(rul.find("\n") != -1):
                    rul = rul[:rul.find("\n")]
                temp += rul + " "
            if(i == len(self._rules)-1):
                continue
            temp += '| '
        return temp
