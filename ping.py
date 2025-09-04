import os


working = []
not_working = []

for i in range(1,253):
    ping_ip = os.system("ping -n 1 -w 300 192.168.160." +str(i)) 
    print(ping_ip)
    if ping_ip == 0:
        working.append("192.168.160."+str(i))
        
    else:
        not_working.append("192.168.160."+str(i))
        


print(working)
print(len(working))

print("------------------")

print(not_working)
print(len(not_working))