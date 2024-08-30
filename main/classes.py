# Imports




# Necessary Functions
def decimalCount(num):
    '''
    Determines the number of decimal places in the mantissa of a number to ensure proper precision.
    '''
    num = str(num)
    num_len = len(num)
    dot_indx = num.find('.')
    mantissa = num_len - dot_indx - 1
    return mantissa

def add_precision(num1, num2):
    num1, num2 = str(num1), str(num2)
    prec_list = [0, 0]
    count = 0
    for num in [num1, num2]:
        if num.find('.') != -1:
            prec_list[count] = -1 * decimalCount(float(num1))
        else:
            reverse_num = num[::-1]
            for index, digit in enumerate(reverse_num):                 #Checking for first nonzero digit
                if digit != '0':
                    prec_list[count] = index

    pass





# Classes
class SigFigNum:
    '''
    This class creates sig fig objects with an associated error. It propagates error and sig figs correctly.

    If there is no error, enter '0' for the error.
    '''
    def __init__(self, num, err):
        self.val = num
        self.err = err
    
    def __add__(self, other):
        sum = self.val + other.val
        new_err = (self.err**2 + other.err**2)**0.5         #Calculating error
        new_err = round(new_err, decimalCount(sum))         #Rounding error to sum's precision
        sum_obj = SigFigNum(sum, new_err)
        return sum_obj
    
    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __div__(self, other):
        pass
