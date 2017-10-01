"""This code extract sentences from data in a form we need:
1. Used data:
    1) novels from Gutenberg project:
        - txt, and json
    2) EmotionThesaurus:
        - different txt files
    3) idioms:
        - txt files
    4) EmotionThesaurus_all:
        - all physical signal phrases in emotion thesaurus
"""
import sys, os, json, textract, csv
sys.path.append('../')
sys.path.append('../utils/')
from utils import *
import en

resultDir = './results/'
#Gutenberg
def gutenberg(bodyparts):
    resultTxt = []
    resultDic = {}
    for bp in bodyparts:
        if bp not in resultDic:
            resultDic[bp] = []
    data = []
    dataDir = '../data/Gutenberg/'
    punctuation = [',','.','!','?','--','(',')',':',';','\xe2\x80\x9d','\xe2\x80\x9c','\xe2\x80\x98','\xe2\x80\x99']
    #read whole text data
    #save list of words
    for dirpath, dirname, filenames in os.walk(dataDir):
        for file_ in filenames:
            if file_.endswith('.txt'):
                with open(os.path.join(dirpath,file_), 'r') as f:
                    book = f.read()
                    for word in book.split():
                        data.append(word)
                f.close()
    #extract phrases that start and end with delimiters
    for idx, word in enumerate(data):
        if not isEnglish(word):
            continue
        if any(punc in word for punc in punctuation):
            pivot1 = idx + 1 #where phrase starts
        temp = []
        foundbp = 0
        for bp in bodyparts:
            if (en.noun.singular(word)).lower() == bp.lower():
                pivot2 = idx #where body part word is located
                otherLanguage = 0
                while (all(punc not in data[pivot2] for punc in punctuation)) and (pivot2 < len(data)):
                    pivot2 += 1 #put pivot at the end of the sentence
                for idx2 in range(pivot2 - pivot1 + 1):
                    put = data[pivot1 + idx2]
                    if not isEnglish(put):
                        otherLanguage = 1
                        break
                    for punc in punctuation:
                        if punc in put:
                            put = put.replace(punc, '')
                    temp.append(put)
                if otherLanguage == 0:
                    print(' '.join(temp))
                    resultTxt.append(' '.join(temp))
                    resultDic[bp].append(' '.join(temp))
    fname = resultDir + 'gutenberg_list.txt'
    with open(fname, 'w') as f:
        for phrase in resultTxt:
            f.write(phrase)
            f.write('\n')
    f.close()

    fname = resultDir + 'gutenberg_dic.json'
    with open(fname, 'w') as f:
        json.dump(resultDic, f)

def EmotionThesaurus(bodyparts):
    resultTxt = []
    pdfDir = '../data/thesaurus/EmotionThesaurus.pdf'
    text = textract.process(pdfDir)

    start = 0
    for line in text.split('\n'):
        if line == 'PHYSICAL SIGNALS:':
            start = 1
        if start == 1 and line not in resultTxt:
            for word in line.split():
                for bp in bodyparts:
                    if (en.noun.singular(word)).lower() == bp.lower():
                        temp = []
                        paranthesis = 0
                        for word in line.split():
                            if '(' in word:
                                paranthesis = 1
                            if paranthesis == 0:
                                temp.append(word)
                            if ')' in word:
                                paranthesis = 0
                        if ' '.join(temp) not in resultTxt:
                            resultTxt.append(' '.join(temp))
        if start ==1 and len(line) == 0:
            start = 0

    fname = resultDir + 'EmotionThesaurus.txt'
    with open(fname, 'w') as f:
        for phrase in resultTxt:
            f.write(phrase)
            f.write('\n')
    f.close()

def english_idioms():
    resultTxt = []
    csvDir = '../data/idioms/FAMILIARITY-Table 1.csv'
    with open(csvDir, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        next(reader) #skip first line
        for row in reader:
            resultTxt.append(row[0])
    csvfile.close()

    fname = resultDir + 'idioms.txt'
    with open(fname, 'w') as f:
        for phrase in resultTxt:
            f.write(phrase)
            f.write('\n')
    f.close()

def EmotionThesaurus_all():
    resultTxt = []
    pdfDir = '../data/thesaurus/EmotionThesaurus.pdf'
    text = textract.process(pdfDir)
    start = 0
    for line in text.split('\n'):
        if line == 'PHYSICAL SIGNALS:':
            start = 1
            continue
        if start == 1 and line not in resultTxt:
            resultTxt.append(line)
        if start ==1 and len(line) == 0:
            start = 0

    fname = resultDir + 'EmotionThesaurus_all.txt'
    with open(fname, 'w') as f:
        for phrase in resultTxt:
            f.write(phrase)
            f.write('\n')
    f.close()

if __name__ == "__main__":
    bp = get_bodyparts(bpDir = '../data/bodyparts.txt')
    #gutenberg(bp)
    #print("Gutenberg done")
    #EmotionThesaurus(bp)
    #print("Emotion done")
    #english_idioms()
    #print("idioms done")
    EmotionThesaurus_all()
    print("thesaurus done")
