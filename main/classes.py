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
    '''
    This function specifies adding and subtracting using proper significant figures.
    '''
    num1, num2 = str(num1), str(num2)
    prec_list = [0, 0]
    count = 0
    for num in [num1, num2]:
        if num.find('.') != -1:
            prec_list[count] = -1 * decimalCount(float(num))
        else:
            reverse_num = num[::-1]
            for index, digit in enumerate(reverse_num):                 #Checking for first nonzero digit
                if digit != '0':
                    prec_list[count] = index
        count += 1
    print(prec_list)    
    mindex = -1 * max(prec_list)

    if mindex < 0:
        if float(num1) + float(num2) < 0:                                           # Not sure why this has to be here but it does
            sum = round(round(float(num1)) + round(float(num2)), mindex + 2)
        else:
            sum = round(round(float(num1)) + round(float(num2)), mindex + 1)
    else: 
        sum = round(float(num1) + float(num2), mindex)
    
    return sum



def mult_precision(num1, num2):
    '''
    This function specifies multiplying and dividing using proper significant figures.
    '''
    num1, num2 = str(num1), str(num2)
    sf_list = [0, 0]
    count = 0
    for num in [num1, num2]:
        if num.find('.') != -1:                                         # If there's a decimal...
            if abs(float(num)) >= 1:                                    # If it's greater than one (i.e., don't worry about leading zeros)
                new_num = num.replace('-', '')
                new_num = new_num.replace('.', '')
                sf_list[count] = len(new_num)
            else:
                pass
        else:
            reverse_num = num[::-1]
            for index, digit in enumerate(reverse_num):                 #Checking for first nonzero digit
                if digit != '0':
                    first_nonzero = index
            sf_list[count] = len(num) - first_nonzero

        count += 1

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
        num1, num2 = self.val, other.val
        sum = add_precision(num1, num2)
        new_err = (self.err**2 + other.err**2)**0.5         #Calculating error
        new_err = round(new_err, decimalCount(sum))         #Rounding error to sum's precision
        sum_obj = SigFigNum(sum, new_err)
        return sum_obj
    
    def __sub__(self, other):
        num1, num2 = self.val, -1 * other.val
        sum = add_precision(num1, num2)
        new_err = (self.err**2 + other.err**2)**0.5         #Calculating error
        new_err = round(new_err, decimalCount(sum))         #Rounding error to sum's precision
        sum_obj = SigFigNum(sum, new_err)
        return sum_obj

    def __mul__(self, other):
        num1, num2 = self.val, other.val

    def __div__(self, other):
        pass

    def __pow__(self, other):
        pass
