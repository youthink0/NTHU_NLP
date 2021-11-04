import sys
import os
from string import punctuation

def preprocess(text):
    # preprocess/tokenize the sentence
    line = ''.join([i if ord(i) < 128 else ' ' for i in text]) #remove non-ascii
    Regtmp = line.split("\t")
    Regtmp = filter(None, Regtmp) # remove None from the List
    Reg = [i.strip(punctuation) for i in Regtmp]
    processed_data = Reg
    return processed_data

def _map(text: str):
    tokens = preprocess(text)
    
    token_length = len(tokens)
    cnt = tokens[token_length-1]  
    tmp_gram = tokens[0].split(" ")

    combs = [] #find all possible query
    for i in range(1, 2**len(tmp_gram)):
        # pat : 生成二進制，0代表不取1代表取，以此列出所有query可能性，而zfill則是填充左側缺失的部分為0
        pat = "{0:b}".format(i).zfill(len(tmp_gram))
        tmp = ""
        for c, b in zip(tmp_gram, pat):
            if int(b): 
                tmp += c + " "
            else: # if 0 then fill with placeholder
                tmp += "_" + " "
        tmp = tmp.strip() #delete space from begin and end string
        combs.append(tmp)  
        #combs.append(' '.join(c for c, b in zip(tmp_gram, pat) if int(b)))
    for i in combs:
        tmp = i
        tmp += "\t" + tokens[0] + " " + str(cnt)   
        print(tmp) 
        
    #print(combs)
if __name__== "__main__" :
    tmp = 0
    for line in sys.stdin:
        #print(line)
        _map(line)
        #tmp += 1
        if tmp > 1000:
            break;
