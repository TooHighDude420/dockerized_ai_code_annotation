
def unused_variable_example():
    a = 10  # F841: local variable assigned but never used
    b = 20
    return b

def long_line_example():
    print("This is a very long line that exceeds the standard 79 character limit which will trigger E501 lint error")  # E501

def trailing_whitespace_example():    
    print("hello")  # W291 trailing whitespace
