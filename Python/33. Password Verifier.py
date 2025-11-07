def Check_Length(password):
    if len(password) < 7:
        print("Password must be at least 7 characters long.")
        return False
    return True

def Check_Upper_Case(password):
    for i in password:
        if i.isupper():
            return True
    print("Password must contain at least one capital letter!")
    return False

def Check_Lower_Case(password):
    for j in password:
        if j.islower():
            return True
    print("Password must contain at least one small letter!")
    return False

def Check_Numeric_Case(password):
    for j in password:
        if j.isdigit():
            return True
    print("Password must contain at least one numeric character!")
    return False

def Check_Sym(password):
    special_symbols = "!@#$%^&*()-_+=[]{}|\\;:'\",.<>?/`~"
    for j in password:
        if j in special_symbols:
            return True
    print("Password must contain at least one special symbol!")
    return False

password = input("Enter the Password: ")

if (Check_Length(password) and
    Check_Upper_Case(password) and
    Check_Lower_Case(password) and
    Check_Numeric_Case(password) and
    Check_Sym(password)):
    print("Password is Strong!!!!")
else:
    print("Password is Weak.")
