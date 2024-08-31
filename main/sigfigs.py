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


# Classes
class SigFig:
    '''
    This class defines the rules for significant figure objects, chiefly their operations with respect to each other.

    Please make sure the value passed is a string. I've accommodated for if it's not, but if you enter 5.000 as a float, only 5.0 will be registered.
    '''

    def __init__(self, num):
        self.val = num
        if type(self.val) == float or type(self.val) == int:
            self.val = str(self.val)

        self.getSigFigs()

    def getSigFigs(self):
        '''
        This method determines the number of sig figs in the number. It is called in the constructor and is thus calculated upon instantiation.
        '''
        num = self.val
        # 3 cases: no decimal point (e.g., 3500), |prod| < 1 (e.g., 0.0045), or float (e.g., 3.45)
        if num.find('.') != -1:                                         # If there's a decimal...
            new_num = num.replace('-', '')                              # Creating a new number without decimal or negative sign
            new_num = new_num.replace('.', '')

            if abs(float(num)) >= 1:                                    # If it's greater than one (i.e., don't worry about leading zeros)
                sf = len(new_num)

            else:                                                       # If you do worry about leading zeros...
                for index, digit in enumerate(new_num):                 # Checking for first nonzero digit
                    if digit != '0':
                        first_nonzero = index
                        break
                sf = len(new_num) - first_nonzero

        else:
            new_num = num.replace('-', '')                              # Removing any potential negative signs
            reverse_num = new_num[::-1]                                 # Reversing the number
            for index, digit in enumerate(reverse_num):                 # Checking for first nonzero digit
                if digit != '0':
                    first_nonzero = index
                    break
            sf = len(new_num) - first_nonzero
        
        self.sigFigs = sf

    def __add__(self, other):
        '''
        This function specifies adding and subtracting using proper significant figures.
        '''
        num1, num2 = self.val, other.val
        print(num1, num2)
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
                        break
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
    
        sum = SigFig(sum)                                                              # Make the product another SigFig object
        return sum
    
    def __sub__(self, other):
        '''
        Defines the subtraction operation using significant figures. In subtraction, the minimum significant power of ten is kept 
        (i.e., 4.7 - 0.732 = 4.0).
        '''
        neg_other = SigFig(str(-float(other.val)))
        return self.__add__(neg_other)

    def __mul__(self, other):
        '''
        Defines multiplication operation using significant figures. In multiplication, the minimum number of significant figures between the
        binary operators is conserved in the product.
        '''
        num1, num2 = float(self.val, other.val)
        prod = str(num1 * num2)
        sf = SigFig(prod).sigFigs
        # 3 cases: no decimal point (e.g., 3500), |prod| < 1 (e.g., 0.0045), or generic float (e.g., 3.45)
        if prod.find('.') != -1:                                         # If there's a decimal...
            new_num = prod.replace('-', '')


            if abs(float(prod)) >= 1:                                    # If it's greater than one (i.e., don't worry about leading zeros)
                dec_indx = new_num.index('.')
                if dec_indx > sf:
                    pass

            else:                                                       # If you do worry about leading zeros...
                for index, digit in enumerate(new_num):                 # Checking for first nonzero digit
                    if digit != '0':
                        first_nonzero = index
                        break
                sf = len(new_num) - first_nonzero

        else:                                                           # No decimal point case (e.g., 5000)
            prod = round(float(prod), -1 * sf)

        prod = SigFig(prod)
        return prod

    def __div__(self, other):
        neg_other = SigFig(str(1/float(other.val)))
        return self.__mul__(neg_other)

    def __pow__(self, other):
        pass


class SigFigData(SigFig):
    '''
    This subclass creates sig fig objects with an associated error. It propagates error AND sig figs correctly.

    If there is no error, enter '0' for the error.
    '''
    def __init__(self, num, err):
        SigFig.__init__(self, num)
        self.err = err
    
    def __add__(self, other):
        num1, num2 = self.val, other.val
        sum = add_precision(num1, num2)
        new_err = (self.err**2 + other.err**2)**0.5         #Calculating error
        new_err = round(new_err, decimalCount(sum))         #Rounding error to sum's precision
        sum_obj = SigFigData(sum, new_err)
        return sum_obj
    
    def __sub__(self, other):
        num1, num2 = self.val, -1 * other.val
        diff = add_precision(num1, num2)
        new_err = (self.err**2 + other.err**2)**0.5         #Calculating error
        new_err = round(new_err, decimalCount(sum))         #Rounding error to sum's precision
        diff_obj = SigFigData(diff, new_err)
        return diff_obj

    def __mul__(self, other):
        num1, num2 = self.val, other.val

    def __div__(self, other):
        num1, num2 = self.val, other.val

    def __pow__(self, other):
        num, pow = self.val, other
