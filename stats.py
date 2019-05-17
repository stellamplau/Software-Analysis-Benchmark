
def compute(filename):
    ctrs = {}

    infile = open(filename, "r")
    for line in infile:
        x = line.split()
        basename = x[0][:-4]
        if basename not in ctrs:
            ctrs[basename] = [0,0,0]

        if "RESULT: SAT" in line:
            ctrs[basename][0] += 1
        elif "RESULT: UNSAT" in line:
            ctrs[basename][1] += 1
        else:
            ctrs[basename][2] += 1
    return ctrs

outfile = open("stats.md", "w")

infile_defects = "defects.txt"
infile_wo_defects = "wo_defects.txt"

outfile.write( "|name|w_sat|w_unsat|w_error|wo_sat|wo_unsat|wo_error|\n")

outfile.write( "|---|---|---|---|---|---|---|\n")

defects = compute(infile_defects)
wo_defects = compute(infile_wo_defects)



for k in sorted(defects):
    wlist = defects[k]

   
    if k not in wo_defects:
        wolist = [0,0,0]
    else:
        wolist = wo_defects[k]

    outfile.write( "| %s | %d | %d | %d | %d | %d | %d |\n" %(k, wlist[0], wlist[1], wlist[2], wolist[0], wolist[1], wolist[2]))


outfile.close()

