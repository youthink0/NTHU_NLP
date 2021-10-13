from collections import Counter, defaultdict
import math, re
import kenlm
import operator
import itertools

model = kenlm.Model('bnc.prune.arpa')

def words(text): return re.findall(r'\w+|[,.?]', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return float(WORDS[word] / N)


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def suggest(word):
    '''return top 5 words as suggestion, original_word as top1 when original_word is correct'''
    suggest_P = {}
    edits_set = edits1(word).union(set(edits2(word)))
    for candidate in known(edits_set):
        suggest_P[candidate] = P(candidate)
    if word in WORDS:
        suggest_P[word] = 1
    suggest_can = sorted(suggest_P, key=suggest_P.get, reverse=True)[:5]
    
    return suggest_can

###### Task1 ######
def spelling_check(sentence):
    sentence = sentence.split()
    candidate = []
    tmp = []
    ## TODO ##    
    for i in range(len(sentence)):
        if sentence[i] not in WORDS:
            tmp.insert(i, suggest(sentence[i]))
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
                    candidate.append(str(tmp[i][j]) + " ")
        else:
            for z in range(next_turn_len):
                for j in range(len(tmp[i])):
                    for k in range(can_len):
                        candidate[z*len(tmp[i])*can_len + j*can_len + k] = candidate[z*len(tmp[i])*can_len + j*can_len + k] + str(tmp[i][j]) + " "  
        
    best_candidate = ""
    best_score = 0
    for i in range(total_possible_len):
        score = model.score(candidate[i], bos=True, eos=True) / len(candidate[i])
        if best_score == 0:
            best_score = score
            best_candidate = candidate[i]
        elif score > best_score:
            best_score = score
            best_candidate = candidate[i]

    return best_candidate, candidate


print("Task 1 Spelling Check")
task1_input = 'he sold everythin escept the housee'
#task1_input = 'nobady knows thats thing'
print("Text:",task1_input,"\n")
print("Candidates:")
task1_result, task1_candidate = spelling_check(task1_input)
for i in task1_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task1_candidate))
print()
print("Result:", task1_result,"\n\n\n")



###### Task2 ######
atcs = ["", "the", "a", "an"]
preps = ["", "about", "at", "by", "for", "from", "in", "of", "on", "to", "with"]

def prep_check(sentence):
    sentence = sentence.split()
    candidate = []
    ## TODO ##    
    
    total_possible_len = 1
    for i in range(len(sentence)): 
        if sentence[i] in atcs:
            total_possible_len = total_possible_len * len(atcs)
        elif sentence[i] in preps:
            total_possible_len = total_possible_len * len(preps)
        else:
            total_possible_len = total_possible_len * 1
    
    #每個有候選字的都跑for迴圈，每個字都要重複total_possible_len/(後面所有候選字次數相乘)次
    can_len = total_possible_len
    for i in range(len(sentence)): 
        if sentence[i] in atcs:
            next_turn_len = int(total_possible_len/can_len)
            can_len = int(can_len/len(atcs))
            
            if not candidate: #第一個字的特殊狀況
                for j in range(len(atcs)):
                    for k in range(can_len):
                        candidate.append(str(atcs[j]) + " ")
            else:
                for z in range(next_turn_len):
                    for j in range(len(atcs)):
                        for k in range(can_len):
                            candidate[z*len(atcs)*can_len + j*can_len + k] = candidate[z*len(atcs)*can_len + j*can_len + k] + str(atcs[j]) + " "
                            
                            
        elif sentence[i] in preps:
            next_turn_len = int(total_possible_len/can_len)
            can_len = int(can_len/len(preps))
            
            if not candidate: #第一個字的特殊狀況
                for j in range(len(preps)):
                    for k in range(can_len):
                        candidate.append(str(preps[j]) + " ")
            else:
                for z in range(next_turn_len):
                    for j in range(len(preps)):
                        for k in range(can_len):
                            candidate[z*len(preps)*can_len + j*can_len + k] = candidate[z*len(preps)*can_len + j*can_len + k] + str(preps[j]) + " "
                            
        else:
            if not candidate: #第一個字的特殊狀況
                for j in range(total_possible_len):
                        candidate.append(str(sentence[i]) + " ")
            else:
                for j in range(total_possible_len):
                    candidate[j] = candidate[j] + str(sentence[i]) + " "
    
    
    bet_candidate = ""
    best_score = 0
    for i in range(total_possible_len):
        score = model.score(candidate[i], bos=True, eos=True) / len(candidate[i].split())
        #print(score, candidate[i])
        if best_score == 0:
            best_score = score
            best_candidate = candidate[i]
        elif score > best_score:
            best_score = score
            best_candidate = candidate[i]
    
    return best_candidate, candidate


print("Task 2 Preposition and Article Check")
task2_input = 'look on an picture in the right'
#task2_input = 'at an afternoon'
print("Text:",task2_input,"\n")
task2_result, task2_candidate = prep_check(task2_input)
print("Candidates:")
for i in task2_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task2_candidate))
print()
print("Result:", task2_result,"\n\n\n")


def process_sent(sent):
    ## TODO ##
    candidate1,_ = spelling_check(sent)
    candidate2,_ = prep_check(candidate1)
    return candidate2
    
    
print("Task 3 Combination")
task3_input = 'we descuss a possible meamin by that'
print("Text:",task3_input,"\n")
comb_result = process_sent(task3_input)
print("Result:", comb_result)

