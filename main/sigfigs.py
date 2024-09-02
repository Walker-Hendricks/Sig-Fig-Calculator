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
        '''
        This constructor automatically finds the number of sig figs and the least significant digit in the number upon instantiation.
        '''
        self.val = str(num)
        self.getSigFigs()
        self.LeastSigDig()


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
            first_nonzero = len(reverse_num)
            for index, digit in enumerate(reverse_num):                 # Checking for first nonzero digit
                if digit != '0':
                    first_nonzero = index
                    break 
            sf = len(new_num) - first_nonzero
        
        self.sigFigs = sf

    def LeastSigDig(self):
        '''
        This function finds the least significant digit (lsd) in the sig fig. This is used in addition/subtraction with sig figs, as this is the
        final decimal to which precision is kept.

        This function is consistent with the round() function. That is, the ones position has an lsd value of 0, the tens position of -1, the tenths position 1, etc.
        A sample number is shown below, with the associated indices (lsd values) underneath:

        Number:      4  3  7  .  2  3  0  5
        lsd value:  -2 -1  0     1  2  3  4
        '''
        num = self.val
        try:                                                    # Checking if the number is an int
            num = str(int(num))
            reverse_num = num[::-1]                             # Reversing to find the first nonzero digit
            for index, digit in enumerate(reverse_num):
                if digit != '0':
                    lsd =  -1 * index
                    break

        except: 
            lsd = len(num) - num.find('.') - 1
            

        self.lsd = lsd

    def __add__(self, other):
        '''
        This function specifies adding and subtracting using proper significant figures.
        '''
        num1, num2 = self.val, other.val
        if self.lsd <=0 or other.lsd <= 0:                              # If the lsd is >= 0 (if one is an int)
            sum = int(round(float(num1))) + int(round(float(num2)))
        else:
            sum = float(num1) + float(num2)
        
        sum = SigFig(round(sum, min([self.lsd, other.lsd])))

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
        num1 = float(self.val)
        # Checking if this is two sig figs or a constant multiple
        if type(other) == SigFig:
            num2 = float(other.val)
        else:
            num2 = other

        prod = num1 * num2
        # Getting number of sig figs for product
        if type(other) == SigFig:
            sf = min([self.sigFigs, other.sigFigs])
        else:
            sf = self.sigFigs

        # Getting decimal point index
        dec_indx = str(prod).find('.')

        # If dec_indx > sf - 1, we need ints (decimal comes after the last sig fig):
        if dec_indx >= sf:
            prod = int(round(prod, sf - dec_indx))

        else:
            prod = round(prod, sf - dec_indx)

        return SigFig(prod)
    

    def __div__(self, other):
        neg_other = SigFig(str(1/float(other.val)))
        return self.__mul__(neg_other)
    

    def __pow__(self, other):
        '''
        This method is for when a sig fig is raised to an exponent. Even if the exponent is also a sig fig, convention dictates that 
        the number of sig figs in the base is the number of sig figs in the final result.
        '''
        num1 = float(self.val)
        if type(other) == SigFig:
            num2 = float(other.val)
        else:
            num2 = float(other)
        
        sf = self.sigFigs
        result = num1 ** num2

        # Getting decimal point index
        dec_indx = str(result).find('.')

        # If dec_indx > sf - 1, we need ints (decimal comes after the last sig fig):
        if dec_indx >= sf:
            result = int(round(result, sf - dec_indx))

        else:
            result = round(result, sf - dec_indx)

        return SigFig(result)

    def __rpow__(self, other):
        '''
        This function is for when a sig fig is used in the exponent, as opposed to the base. If both base and exponent are sig figs, see above;
        if just the exponent is a sig fig, the number of sig figs in the exponent should be the number of sig figs in the result.
        '''
        if type(other) == SigFig:
            result = other.__pow__(self)

        else:
            sf = self.sigFigs
            result = other**float(self.val)
            # Getting decimal point index
            dec_indx = str(result).find('.')

            # If dec_indx > sf - 1, we need ints (decimal comes after the last sig fig):
            if dec_indx >= sf:
                result = int(round(result, sf - dec_indx))

            else:
                result = round(result, sf - dec_indx)

        return SigFig(result)


    def __repr__(self):
        '''
        Determines the output of the print() function on a SigFig data type.
        '''
        return f'{self.val}'



class SigFigData(SigFig):
    '''
    This subclass creates sig fig objects with an associated error. It propagates error AND sig figs correctly.

    If there is no error, enter '0' for the error.
    '''
    def __init__(self, num, err):
        SigFig.__init__(self, num)
        self.err = err
    
    def __add__(self, other):
        sum = SigFig.__add__(other)
        new_err = (self.err**2 + other.err**2)**0.5         # Calculating error
        new_err = round(new_err, decimalCount(sum))         # Rounding error to sum's precision
        sum_obj = SigFigData(sum, new_err)
        return sum_obj
    
    def __sub__(self, other):
        diff = SigFig.__sub__(other)
        new_err = (self.err**2 + other.err**2)**0.5         # Calculating error
        new_err = round(new_err, decimalCount(diff))         # Rounding error to sum's precision
        diff_obj = SigFigData(diff, new_err)
        return diff_obj

    def __mul__(self, other):
        num1, num2 = self.val, other.val

    def __div__(self, other):
        num1, num2 = self.val, other.val

    def __pow__(self, other):
        num, pow = self.val, other

    def __repr__(self):
        return f'{self.val} +/- {self.err}'
