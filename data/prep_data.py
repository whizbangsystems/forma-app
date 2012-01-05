import sys, os


"""
drop country ecoid gadm coastdist modh modv sample line prob200512
drop if prob201108 < 50 & hansen == 0
outsheet using "/Users/robin/Dropbox/code/forma-app/data/IDN.csv", comma noquote replace
"""

def parse_line(line):
    vals = line.split(",")
    
    # just for reference
    lat, lon = vals[:2]
    
    # field #3
    hansen = vals[2]
    
    # rest of fields
    prob_data = vals[3:]
    
    # this gets us the period without having to worry about the date!
    for i in range(len(prob_data)):
        if hansen > 0:
            return 254
        elif prob_data[i] >= 50:
            return i
        else:
            return 0

fp = open(sys.argv[1], 'r')
path, fname = os.path.split(sys.argv[1])
out_fp = open(os.path.join(path, os.path.splitext(fname)[0] + "_fixed.csv"), "w")

n = 0

for line in fp:
    if n == 0:
        out_fp.write(line.strip() + "\n")
        n += 1
        continue
        
    vals = line.strip().split(",")
    probs = [int(i) for i in vals[2:]]
    
    if 1 in probs:
        out_fp.write(",".join(vals) + "\n")

    if n % 1000 == 0:
        print "%i lines processed" % n
        
    n += 1
