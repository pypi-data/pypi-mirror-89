def add(addend1, addend2):
    if(addend1 - int(addend1) == 0 and addend2 - int(addend2) == 0):
        return int(addend1) + int(addend2)
    if(addend1 - int(addend1) != 0 or addend1 - int(addend1) != 0):
        return float(addend1) + float(addend2)

def subtract(minuend, subtrahend):
    if(minuend - int(minuend) == 0 and subtrahend - int(subtrahend) == 0):
        return int(minuend) - int(subtrahend)
    if(minuend - int(minuend) != 0 or subtrahend - int(subtrahend) != 0):
        return float(minuend) - float(subtrahend)


def multiply(multiplier, multiplicand):
    if(multiplier - int(multiplier) == 0 and multiplicand - int(multiplicand) == 0):
        return int(multiplier) * int(multiplicand)
    if(multiplier - int(multiplier) != 0 or multiplicand - int(multiplicand) != 0):
        return float(multiplier) * float(multiplicand)
    
def divide(dividend, divisor):
    if(dividend - int(dividend) == 0 and divisor - int(divisor) == 0):
        return int(dividend) / int(divisor)
    if(dividend - int(dividend) != 0 or divisor - int(divisor) != 0):
        return float(dividend) / float(divisor)


def power(base, exponent):
    if(base - int(base) == 0 and exponent - int(exponent) == 0):
        return pow(int(base), int(exponent))
    if(base - int(base) != 0 or exponent - int(exponent) != 0):
        return pow(float(base), float(exponent))




def sub(minuend, subtrahend):
    if(minuend - int(minuend) == 0 and subtrahend - int(subtrahend) == 0):
        return int(minuend) - int(subtrahend)
    if(minuend - int(minuend) != 0 or subtrahend - int(subtrahend) != 0):
        return float(minuend) - float(subtrahend)

def mul(multiplier, multiplicand):
    if(multiplier - int(multiplier) == 0 and multiplicand - int(multiplicand) == 0):
        return int(multiplier) * int(multiplicand)
    if(multiplier - int(multiplier) != 0 or multiplicand - int(multiplicand) != 0):
        return float(multiplier) * float(multiplicand)

def div(dividend, divisor):
    if(dividend - int(dividend) == 0 and divisor - int(divisor) == 0):
        return int(dividend) / int(divisor)
    if(dividend - int(dividend) != 0 or divisor - int(divisor) != 0):
        return float(dividend) / float(divisor)

def pow(base, exponent):
    if(base - int(base) == 0 and exponent - int(exponent) == 0):
        return pow(int(base), int(exponent))
    if(base - int(base) != 0 or exponent - int(exponent) != 0):
        return pow(float(base), float(exponent))