import sys

if __name__== "__main__" :
    
    dis_range = 5
    
    
    fw = open("skipgram.tsv", "w")
    tmp_test = 0 
    pivot_word = skip_word = ""
    pivot_cnt = 0
    pivot_list = [0] * (dis_range*2)
    
    for line in sys.stdin:
        line = line.strip()
        if not line: continue

        # [ TODO ] collect the output from shuffler and generate reducer output
        # Now you need to calculate the skip-gram frequency with its distance information.
        # Input: 
        #   "{pivot}\t{word}\t{distance}\t{count}"
        # Output: 
        #   "{pivot}\t{word}\t{total_freq}\t{-5}\t{-4}\t{-3}\t{-2}\t{-1}\t{1}\t{2}\t{3}\t{4}\t{5}"
        # Example:
        #   See the sample output file given by TA.
        # Steps: 
        #   1) Parse the input from shuffler
        #   2) Check if this is the same skipgram
        #   3) If so, add the frequency according to its distance
        #   4) If not, output the previous skipgram data
        line = line.replace("\n", "")
        Regtmp = line.split("\t")
        if len(Regtmp) != 4 : continue #排除不完整，奇怪的行數
            
        if len(pivot_word) == 0 and len(skip_word) == 0:
            pivot_word = Regtmp[0]
            skip_word = Regtmp[1]
               
        elif pivot_word == Regtmp[0] and skip_word == Regtmp[1]:
            a = 1
                
        else:
            tmp_print = pivot_word + "\t" + skip_word + "\t" + str(pivot_cnt) + "\t" 
            for i in range(dis_range*2):
                    tmp_print += str(pivot_list[i])
                    if i < (dis_range*2 - 1) :
                        tmp_print +=  "\t"
                    
            #if tmp_test < 30:
            print(tmp_print)
            #fw.write(tmp_print+"\n")
            pivot_word = Regtmp[0]
            skip_word = Regtmp[1]
            pivot_cnt = 0
            pivot_list = [0] * (dis_range*2)
            
        pivot_cnt += int(Regtmp[3])    
        if int(Regtmp[2]) < 0:
            pivot_list[int(Regtmp[2])+dis_range] += 1
        else:
            pivot_list[int(Regtmp[2])+dis_range-1] += 1
        
        tmp_test += 1
    fw.close()
