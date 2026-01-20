import re

upper = r'[A-Z]'
lower = r'[a-z]'
digit = r'[1-9]'
spl = r'[!@#$%^&*]'
password = input("Enter the Password: ")

is_upper = re.search(pattern=upper, string=password)
is_lower = re.search(pattern=lower, string=password)
is_digit = re.search(pattern=digit, string=password)
is_spl = re.search(pattern=spl, string=password)

if is_upper and is_lower and is_digit and is_spl:
    print("Password is Strong")
else:
    print("Weak")