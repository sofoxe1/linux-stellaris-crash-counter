import re
f = open("stellaris.log", "r")
lines = f.readlines()
errors=[]
errors_c=[]
r=False
depth = 1
_depth = 0
crash_c = 0

def error_log(fline,_depth,r):
    global crash_c
    
    _depth += 1
    if not re.search('|'.join(["CPdxCrashReporter","libstdc++.so.6","libc.so.6", "libpops_api.so","CString::CString","std"]), line):
        crash_c +=1
        if fline not in errors:
            errors.append(fline)
            errors_c.append(1)
        else:
            errors_c[errors.index(fline)]+=1
    
    if _depth == depth:
        _depth = 0
        r = False
    
    return _depth, r

for line in lines:
    
    if "Demangled Stack Trace:" in line:
        r = True
    elif "Original Stack Trace:" in line:
        r = False
    
    
    elif r:
        
        if "./stellaris" in line:
            fline=line.split(" ")[22:]
            # print(line)
            if fline[0] != "(":
                raise Exception(f"string formating is incorrect for {line}")
            fline.pop(0)
            if fline[0] in ["main", "_start","RunGame(int,"]:
                continue
            fline=fline[0]
            _depth,r = error_log(fline,_depth,r)
        elif ".so" in line:
            
            fline=line.split(" ")[2:][0].split("/")[-1]
            if ".so" not in fline:
                raise Exception(f"string formating is incorrect for")
            _depth,r = error_log(fline,_depth,r)
                
            
            
for i in range(len(errors)): 
    # print(errors_c[i])
    errors[i]=f"{errors_c[i]} {errors[i]}  {round(errors_c[i]/crash_c*100,1)}%"
   
print("\n".join(sorted(errors, reverse=True)))

