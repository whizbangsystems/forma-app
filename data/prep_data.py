import sys, os

fp = open(sys.argv[1], 'r')
path, fname = os.path.split(sys.argv[1])
out_fp = open(os.path.join(path, os.path.splitext(fname)[0] + "_fixed.csv"), "w")

n = 0

for line in fp:
    if n == 0:
        n += 1
        continue
        
    vals = line.strip().split(",")
    probs = [int(i) for i in vals[2:]]
    
    if 1 in probs:
        out_fp.write(",".join(vals) + "\n")

    if n % 1000 == 0:
        print "%i lines processed" % n
        
    n += 1
