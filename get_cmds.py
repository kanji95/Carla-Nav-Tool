import os

dpath = "_out"

for d in [os.path.join(dpath,str(d)) for d in sorted([int(di) for di in os.listdir(dpath)])]:
    cmd = open(os.path.join(d,'command.txt'),'r').read().strip()
    print(f"{d}\t{cmd}")
