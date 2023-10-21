import re
import numbers
from openpyxl import *


class Helper():
    """docstring for Helper"""

    def __init__(self, inputfile):

        wb = load_workbook(inputfile)
        ws = wb.active
        columns = tuple(ws.columns)
        rows = tuple(ws.rows)

        self.columns = {columns[i][0].value:
                        [cell.value for cell in columns[i]][1:]
                        for i in range(len(columns))}

        self.rows = [[cell.value for cell in rows[i]]
                     for i in range(len(rows))][1:]

        for col in ['C1_Anion','C2_Anion','C3_Anion','C4_Anion','C5_Anion','C1_Cation','C2_Cation','C3_Cation','C4_Cation','C5_Cation']:
            for i, val in enumerate(self.columns[col]):
                if val is None:
                    self.columns[col][i] = ""
                try:
                    tempstr = str(self.columns[col][i]).strip()
                    # print ord(tempstr[-1])
                    if ord(tempstr[-1]) == 32:
                        self.columns[col][i] = tempstr[:-1]
                    else:
                        self.columns[col][i] = tempstr
                except:
                    pass
                    # print "asd"
                    # print self.columns[col][i]

        for col in ['Ph', 'S_a', 'S_b', 'S_c']:
            for i, val in enumerate(self.columns[col]):
                # print val, type(val)
                if self.columns[col][i] is None or self.columns[col][i] == ' ':
                    self.columns[col][i] = None
                else:
                    self.columns[col][i] = self.floatify(self.columns[col][i])
                if self.columns[col][i] == -2:
                    self.columns[col][i] = 0.0
                # print self.columns[col][i], type(self.columns[col][i])

        for col in ['C1_M', 'C2_M']:
            for i, val in enumerate(self.columns[col]):
                # print val
                if val is None or val == ' ':
                    self.columns[col][i] = self.columns[col[:2]+'_Conc'][i]

                if self.columns[col][i] is None or self.columns[col][i] == ' ':
                    self.columns[col][i] = 0.0
                else:
                    self.columns[col][i] = self.floatify(self.columns[col][i])

    def equals(self, num1, num2):
        print num1, type(num1)
        print num2, type(num2)
        return num1 == num2

    def floatify(self, number):
        # print "-- ", number, type(number)
        if number is None:
            return 0.0

        if isinstance(number, numbers.Real):
            return number

        regex = re.findall("\d+\.?\d*", number)
        if not regex:
            return 0.0

        if number[0] == "'":
            return float(number[1:])

        return float(regex[0])
        # return float(number)

    def size(self):
        return len(self.rows)
