import sys
import os
from string import punctuation

def preprocess(text):
    # preprocess/tokenize the sentence
    line = ''.join([i if ord(i) < 128 else ' ' for i in text]) #remove non-ascii
    line = line.lower()
    Regtmp = line.split(" ")
    Regtmp = filter(None, Regtmp) # remove None from the List
    Reg = [i.strip(punctuation) for i in Regtmp]
    processed_data = Reg
    return processed_data

def _map(text: str, fw):
    tokens = preprocess(text)
    
    dis_range = 5
    cnt = 1
    # [ TODO ] generate the mapper output
    # Output: "{pivot}\t{word}\t{distance}\t{count}"
    # Example: 
    #   predict is  -3  1
    #   predict used    -2  1
    #   predict the -1  1
    #   predict the 1   1
    #   ...
    token_length = len(tokens)
    
    for idx in range(token_length):
        for i in reversed(range(dis_range)):
            tmp_str = str(tokens[idx]) + "\t"
            if idx-i-1 < 0:
                continue
            else:
                tmp_str += str(tokens[idx-i-1]) + "\t" + str(-i-1) + "\t" + str(cnt)
                print(tmp_str)
                fw.write(tmp_str+"\n")
        for i in range(dis_range):
            tmp_str = str(tokens[idx]) + "\t"
            if idx+i+1 >= token_length:
                continue
            else:
                tmp_str += str(tokens[idx+i+1]) + "\t" + str(i+1) + "\t" + str(cnt)
                print(tmp_str)
                fw.write(tmp_str+"\n")
          
    
if __name__== "__main__" :
    
    tmp = 0
    fw = open("mapper_test.tsv", "w")
    for line in sys.stdin:
        _map(line, fw)
        tmp += 1
        #if tmp > 100:
        #    break;
    fw.close()