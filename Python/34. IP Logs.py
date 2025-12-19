import re 

file = r'E:\Mohit\PGD-HPCSA\Python\access.log'
ip_list = []
c=0
with open(file, 'r') as f:
    for line in f:
        parts = line.split()
        ip_list.append(parts[0])


unique_ips = list(set(ip_list))
print(type(unique_ips))

out_file = r'E:\Mohit\PGD-HPCSA\Python\reports.log'
with open(out_file, 'w') as f:
    for i in range(len(unique_ips)):
        text = f"IP: {unique_ips[i]}\t: {ip_list.count(unique_ips[i])}\n"
        f.write(text)

print("Generated Report.log")

