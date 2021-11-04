import sys

if __name__== "__main__" :
    
    tmp_test = 0 
    pivot_word = ""
    str_tmp = ""

    for line in sys.stdin:
        line = line.strip()
        if not line: continue

        line = line.replace("\n", "")
        Regtmp = line.split("\t")
        
        if len(pivot_word) == 0:
            pivot_word = Regtmp[0]
            str_tmp = line
        elif pivot_word == Regtmp[0]:
            str_tmp += "\t" + Regtmp[1]
        else:
            print(str_tmp)
            pivot_word = Regtmp[0]
            str_tmp = line
            
            
        tmp_test += 1
    
