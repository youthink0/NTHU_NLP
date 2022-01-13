## Environment Set Up
 * pip install -r /path/to/requirements.txt
 * this cmd can get all python package that need to use in all HW
## lab1_Ngram_Frequency
## lab2_Find_Academic_Keyword_List
## lab3_Simple_Language_Model
## lab4_Error_Correction  
* get bnc.prune.arpa : https://drive.google.com/drive/folders/1Yg63ivIQoiY8T4KG9Vkkd9Sws3LEIGVF  
## lab5_SkipgramAndMapReduce  
* get wiki1G.txt : https://drive.google.com/drive/folders/1vKxr--sLd2J4kdsXUzJDBZdG3AmV4NGl  
## lab6_Collocation_Extraction
* get AKL_skipgram.tsv : https://drive.google.com/drive/folders/17BtzXxHy6khXpXoctydi8mNUkFmp6VQN
## lab7_Linggle_DIY  
* 執行code: (environment : Python 3.6.9)
  * time python mapper.py < nc.10.txt | pv -cN 'mapper to sort' | sort -k1,1 -t$'\t' | pv -cN 'sort to reducer' | python reducer.py | pv -cN 'to output file' > testgram.txt
  * python linggle.py testgram.txt
## lab8_Phrase Classification
* get train.tsv & test.tsv & GoogleNews-vectors-negative300.bin.gz : https://drive.google.com/drive/folders/13MraQoHdzY6lJSQJ0ETUPhDgaOP_IqzR
## lab9_Word_Sense_Disambiguation
* use party.train.txt & party.test.txt in data folder & GoogleNews-vectors-negative300.bin.gz as same as above link
## lab10_Example_Sentences_Classification
* use train.jsonl & test.jsonl in data folder
## lab11_Sequence_Classification_with_BERT
* use evp.test.csv & evp.train.csv in data folder
