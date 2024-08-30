

def decimalCount(num):
    '''
    Determines the number of decimal places in the mantissa of a number to ensure proper precision.
    '''
    num = str(num)
    num_len = len(num)
    dot_indx = num.find('.')
    mantissa = num_len - dot_indx - 1
    return mantissa



# Making a class whose objects are sig figs coupled with error (for proper addition properties)
class SigFigNum:
    '''
    This class creates sig fig objects
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
