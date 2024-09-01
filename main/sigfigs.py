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
        self.val = str(num)
        self.getSigFigs()
        self.LeastSigDig()

    def getSigFigs(self):
        '''
        This method determines the number of sig figs in the number. It is called in the constructor and is thus calculated upon instantiation.
        '''
        num = self.val
        #print(num)
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
                    print(index, digit)
                    first_nonzero = index
                    print(first_nonzero)
                    break
            print(first_nonzero)   
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
        try:                                                            # Try suite for floats. If exception is raised, they're ints
            num1 = int(self.val)
        except ValueError:
            num1 = float(self.val)
        
        try:                                                            # Second try suite to check int vs. float of values
            num2 = int(other.val)
        except ValueError:
            num2 = float(other.val)

        prod = str(num1 * num2)
        sf = SigFig(prod).sigFigs
        is_neg = False
        
        if prod.find('-') != -1:                                        # Negative number check
            is_neg = True
            prod = prod.replace('-', '')

        # 3 cases: no decimal point (e.g., 3500), |prod| < 1 (e.g., 0.0045), or generic float (e.g., 3.45)
        if prod.find('.') == -1:                                        #IF there's no decimal point (i.e., an int like 3500)
            prod = round(int(prod), -1*sf)

        else:
            dec_indx = prod.index('.')
            if abs(float(prod)) >= 1:                                       # If it's greater than one (i.e., don't worry about leading zeros)
                prod = round(float(prod), sf - dec_indx)

            else:                                                         # If you do worry about leading zeros...
                for index, digit in enumerate(prod):                        # Checking for first nonzero digit
                    if digit != '0':
                        first_nonzero = index
                        break
                prod = round(float(prod), first_nonzero + sf - dec_indx)

        if is_neg:
            prod = '-' + prod

        prod = SigFig(prod)
        return prod

    def __div__(self, other):
        neg_other = SigFig(str(1/float(other.val)))
        return self.__mul__(neg_other)

    def __pow__(self, other):
        pass

    def __repr__(self):
        return f'{self.val}'


a = SigFig(-3)
b = SigFig(700)

c = SigFig(-0.501)
d = SigFig(-0.04)
e = SigFig(-5.23)
f = SigFig(-2.345)
print(a - e)
#print(_21.sigFigs)
#print(a+b)


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
