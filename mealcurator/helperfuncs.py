# Holds helper functions for various things that need solutions

# Check for blanks and if found default value
def check_blank(input, default):
    if input == '':
        return default
    else:
        return input
