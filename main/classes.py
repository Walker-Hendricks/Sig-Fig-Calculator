        num1, num2 = self.val + other.val
        sum = add_precision(num1, num2)
        new_err = (self.err**2 + other.err**2)**0.5         #Calculating error
        new_err = round(new_err, decimalCount(sum))         #Rounding error to sum's precision
        sum_obj = SigFigNum(sum, new_err)
        return sum_obj
