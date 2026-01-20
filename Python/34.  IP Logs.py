import re
file = r'/home/acts/Mohit/PGD-HPCSA/Python/access.log'
with open (file, 'r') as f:
    output = f.read()
print(output)
pattern = r'/d/d/d.'
out = re.findall(pattern=pattern, string=output)
print(out)