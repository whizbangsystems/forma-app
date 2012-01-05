import sys, os


"""
drop if prob201108 == .
drop country ecoid gadm coastdist modh modv sample line prob200512
drop if prob201108 < 50 & hansen == 0
outsheet using "/Users/robin/Dropbox/code/forma-app/data/IDN.csv", comma noquote replace
"""

def parse_line(line):
    vals = line.split(",")
    lat, lon = vals[:2]
    # field #3
    hansen = vals[2]
    # rest of fields
    # this gets us the period without having to worry about the date!
    # assumes the 4th field is where probs start, and that they start at 200601
    prob_data = [int(val) for val in vals[3:]
    period = 0
    if hansen > 0:
        period = 254
    else:
        for i in range(len(prob_data)):
            if prob_data[i] >= 50:
                period = i
                break    
    return dict(lat=lat, lon=lon, period=period)

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
