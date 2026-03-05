
import os, sys, math  # E401: multiple imports on one line

def add_numbers(a, b)
    result = a + b  # SyntaxError: missing colon above
    return result

x = 5
y = 10
print(add_numbers(x y))  # SyntaxError: missing comma
