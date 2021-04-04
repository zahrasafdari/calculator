from operator import pow, truediv, mul, add, sub
import re


operators = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow,
}


def turn_to_number(element):
    #   this function use regex to detect if given string
    #   is number (and if it is imaginary or real) or not
    imag = re.match(r'^(-|\+)?\d+(?:\.\d+)?(j|i)?$', element)
    real = re.match(r'^(-|\+)?\d+(?:\.\d+)?$', element)
    if real:
        return float(element)
    if imag:
        # python determain complex numbers with j
        # so we must change all i to j
        element = element.replace('i', 'j')
        return complex(element)
    return None


def get_index(li, idx, default):
    if idx < 0:
        return default
    try:
        return li[idx]
    except IndexError:
        return default

def find(li, condition, from_=0):
    li = li[from_:]
   
    for i, e in enumerate(li):
        if condition(e):
            return i+from_

    return None