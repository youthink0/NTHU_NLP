#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from itertools import product
from heapq import nlargest
import logging


MAX_LEN = 5


def parse_ngramstr(text):
    ngram, count = text.rsplit(maxsplit=1)
    
    return ngram, int(count)


def parse_line(line):
    query, *ngramcounts = line.strip().split('\t')
    
    return query, tuple(map(parse_ngramstr, ngramcounts))


def expand_query(query):
    # TODO: write your query expansion, e.g.,
    #  "in/at afternoon" -> ["in afternoon", "at afternoon"]
    #  "listen ?to music" -> ["listen music", "listen to music"]
    sample = query
    sample = sample.split(" ")
    possible_cnt = -1
    flag = 0

    for i in range(len(sample)):
        if "/" in sample[i]:
            or_tmp = sample[i].split('/')
            possible_cnt = i
            flag = 1
        if "?" in sample[i]:
            optional = ["", sample[i].strip("?")]
            possible_cnt = i
            flag = 2
    query = []
    before_tmp = ""
    for i in range(len(sample)):
        if i != possible_cnt:
            before_tmp += sample[i] + " "
        else:
            if flag == 1 :
                for j in or_tmp:
                    tmp = before_tmp
                    tmp += j + " "
                    if possible_cnt == len(sample)-1:
                        query.append(tmp.strip())
                    else:
                        query.append(tmp)
            elif  flag == 2:
                for j in optional:
                    tmp = before_tmp
                    if j != "":
                        tmp += j + " "
                    if possible_cnt == len(sample)-1:
                        query.append(tmp.strip())
                    else:
                        query.append(tmp)
            
            break     
    if flag != 0:
        after_tmp = ""
        for i in range(possible_cnt+1, len(sample)):
            after_tmp += sample[i] + " "
        after_tmp = after_tmp.strip(" ")  
        result = [s + after_tmp for s in query]
    else:
        result = [before_tmp.strip(" ")]

    #for i in result:
    #    print(i)
            
    return result


def extend_query(query):
    # TODO: write your query extension, 
    # e.g., can tolerate missing/unnecessary determiners
    sentence = query.split(" ")
    pos_holder = ["", "_", "_ _", "_ _ _", "_ _ _ _", "_ _ _ _ _"] #I assume 5 ways to face wildcard * in this implement
    candidate = []  
    tmp = []
        
    for i in range(len(sentence)):
        if sentence[i] == "*":
            tmp.insert(i, pos_holder)
        else:
            tmp.insert(i, [sentence[i]])

    total_possible_len = 1
    for i in range(len(sentence)): 
        total_possible_len = total_possible_len * len(tmp[i])

    #每個有候選字的都跑for迴圈，每個字都要重複total_possible_len/(後面所有候選字次數相乘)次
    #can_len : 本身candidate在輪流
    #next_turn_len : 每組candidate輪
    can_len = total_possible_len
    for i in range(len(sentence)): 
        next_turn_len = int(total_possible_len/can_len)
        can_len = int(can_len/len(tmp[i]))

        if not candidate:  #第一個字的特殊狀況
            for j in range(len(tmp[i])):
                for k in range(can_len):
                    if str(tmp[i][j]) == "":
                        candidate.append(str(tmp[i][j]))
                    else:
                        candidate.append(str(tmp[i][j]) + " ")
        else:
            for z in range(next_turn_len):
                for j in range(len(tmp[i])):
                    for k in range(can_len):
                        if str(tmp[i][j]) == "":
                            candidate[z*len(tmp[i])*can_len + j*can_len + k] = candidate[z*len(tmp[i])*can_len + j*can_len + k] + str(tmp[i][j])
                        else:
                            candidate[z*len(tmp[i])*can_len + j*can_len + k] = candidate[z*len(tmp[i])*can_len + j*can_len + k] + str(tmp[i][j]) + " "

    result = [s.strip() for s in candidate]

    #for i in result:                    
    #    print(i)
    return result


def load_data(lines):
    logging.info('Loading...', end='')
    # read linggle data
    linggle_table = {query: ngramcounts for query, ngramcounts in map(parse_line, lines)}
    logging.info('ready.')
    return linggle_table


def linggle(linggle_table):
    '''
    max_length = 0
    for query in linggle_table:
        #print(query, len(query.split(" ")))
        if len(query.split(" ")) > max_length:
            max_length = len(query.split(" "))
        
    print(max_length)
    '''
    q = input('linggle> ')

    # exit execution keyword: exit()
    if q == 'exit()':
        return

    # extend and expand query
    queries = [
        simple_query
        for query in extend_query(q)
        for simple_query in expand_query(query)
    ]
    # gather results
    ngramcounts = {item for query in queries if query in linggle_table for item in linggle_table[query]}
    # output 10 most common ngrams
    ngramcounts = nlargest(10, ngramcounts, key=itemgetter(1))

    if len(ngramcounts) > 0:
        print(*(f"{count:>7,}: {ngram}" for ngram, count in ngramcounts), sep='\n')
    else:
        print(' '*8, 'no result.')
    print()

    return True


if __name__ == '__main__':
    import fileinput
    # If the readline module was loaded, then input() will use it to provide elaborate line editing and history features.
    # https://docs.python.org/3/library/functions.html#input
    import readline

    linggle_table = load_data(fileinput.input())
    while linggle(linggle_table):
        pass
