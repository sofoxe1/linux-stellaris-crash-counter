import re
import argparse
from os import system,path
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path',help='stellaris log path',default=f"{path.expanduser('~')}/.var/app/com.valvesoftware.Steam/.local/share/Paradox Interactive/Stellaris/crashes/")
parser.add_argument('-d', '--depth', help='stack trace depth, 0 to disable ',default=1,type=int) 
args = parser.parse_args()

lines=[]
for file_ in glob.glob(f"{args.path}/*/exception.txt"):
    f = open(file_, "r")
    lines.extend(f.readlines())
    f.close()


errors=[]
errors_c=[]

r=False
_depth = 0
crash_c = 0


def error_log(fline,_depth,r):
    global crash_c
    if "::" in fline or ".so" in fline: pass # lazy bugfix for element w/o a name
    else:
        return _depth, r
    
    
    _depth += 1
    
    if not re.search('|'.join(["libstdc++.so.6","libc.so.6", "libpops_api.so","std"]), line):
        crash_c +=1

        if fline not in errors:
            errors.append(fline)
            errors_c.append(1)
        else:
            errors_c[errors.index(fline)]+=1
    
    if _depth == args.depth:
        _depth = 0
        r = False
    
    return _depth, r

for line in lines:
    if line[0:21] == "Original Stack Trace:": r = False
    elif line[0:22] == "Demangled Stack Trace:": r = True
    
    
    elif r:
        if line[2:13] == "./stellaris":
            fline=line.split(" ")[22:]
            if fline[0] != "(": raise Exception(f"string formating is incorrect for: {line}")
            fline=fline[1]
            
            _depth,r = error_log(fline,_depth,r)


        elif ".so" in line:
            fline=line.split(" ")[2:][0].split("/")[-1]
            if ".so" not in fline: raise Exception(f"string formating is incorrect for: {line}")

            _depth,r = error_log(fline,_depth,r)
                
            
            
for i in range(len(errors)): 
    errors[i]=f"{errors_c[i]} {errors[i]}  {round(errors_c[i]/crash_c*100,1)}%"
   
print("\n".join(sorted(errors, reverse=True)))

