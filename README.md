# wordCount
Counting words in annotated sets of data

## Input

File(s) annotated as tag<tab>example

## Output 
All words associated to an intent key (word cloud) OR all intents associated to a word

python3 filename.py -d directory -k intentKey -w word

Must use k or w
* -k = Occurrences of words associated to a key
* i.e. intentKeyA: wordA(numOccurrences), word...N
* -w = intentKeys associated to a word and its occurrences 
* i.e. wordA: intentKeyA(numOccurrences), intentKey...N
