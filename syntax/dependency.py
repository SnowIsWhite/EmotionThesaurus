"""This code outputs dependency relations
1. input files:
    1) novels from project gutenberg: json file
    2) emotion thesaurus: txt file
    3) idioms: txt file
2. output files:
    1) json file
    2) json file
    3) json file

We use state-of-the-art dependency parser: Parsey McParseface
"""

import sys, json
sys.path.append('../')
sys.path.append('../utils')
from utils import*
import en

gutenbergDir = '../preprocess/results/gutenberg_dic.json'
thesaurusDir = '../preprocess/results/EmotionThesaurus.txt'
idiomsDir = '../preprocess/results/idioms.txt'
thesaurusAllDir = '../preprocess/results/EmotionThesaurus_all.txt'


def get_gutenberg_dependency(bodyparts):
    #gutenberg
    gutenbergDic = {}
    for bp in bodyparts:
        gutenbergDic[bp] = {'sentence':[], 'dependency':[]}
    with open(gutenbergDir, 'r') as f:
        gutenbergData = json.load(f)
    f.close()

    for key in gutenbergData:
        gutenbergDic[key]['sentence'] = gutenbergData[key]

    for keybp in gutenbergDic:
        for phrase in gutenbergDic[keybp]['sentence']:
            print(phrase)
            res = get_stanford_dependency(phrase, '../utils')
            print(res)
            gutenbergDic[keybp]['dependency'].append(res)
        print("dependency parsing for gutenberg, " + keybp + " is done.")
        with open('./results/gutenberg_dependency.json', 'w') as f:
            json.dump(gutenbergDic, f)
        f.close()

    print("gutenberg done.")

def get_thesaurus_dependency(bodyparts):
    #emotion thesaurus
    thesaurusDic = {}
    for bp in bodyparts:
        thesaurusDic[bp] = {'sentence': [], 'dependency': []}
    with open(thesaurusDir, 'r') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            line = line.replace(u'\u2019', u'\'').encode('ascii', 'ignore')
            if not isEnglish(line):
                continue
            for word in line.split():
                for bp in bodyparts:
                    if (en.noun.singular(word.lower())) == bp.lower():
                        if line not in thesaurusDic[bp]['sentence']:
                            thesaurusDic[bp]['sentence'].append(line)
    for keybp in thesaurusDic:
        for phrase in thesaurusDic[keybp]['sentence']:
            print(phrase)
            thesaurusDic[keybp]['dependency'].append(get_stanford_dependency(phrase, '../utils'))
        print("dependency parsing for thesaurus," + keybp + " is done.")
        with open('./results/thesaurus_dependency.json', 'w') as f:
            json.dump(thesaurusDic, f)
        f.close()

    print("thesaurus done")

def get_idioms_dependency():
    #idioms
    idiomsDic = {'sentence': [], 'dependency': []}
    with open(idiomsDir, 'r') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            line = line.replace(u'\u2019', u'\'').encode('ascii', 'ignore')
            if not isEnglish(line):
                continue
            idiomsDic['sentence'].append(line)
    f.close()

    for phrase in idiomsDic['sentence']:
        idiomsDic['dependency'].append(get_stanford_dependency(phrase, '../utils'))

    with open('./results/idioms_dependency.json', 'w') as f:
        json.dump(idiomsDic, f)
    f.close()

    print("idioms done")

def get_thesaurus_all_dependency():
    #emotion thesaurus
    thesaurusDic = {}
    thesaurusDic = {'sentence': [], 'dependency': []}
    with open(thesaurusAllDir, 'r') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            line = line.replace(u'\u2019', u'\'').encode('ascii', 'ignore')
            if not isEnglish(line):
                continue
            thesaurusDic['sentence'].append(line)
    cnt = 0
    for phrase in thesaurusDic['sentence']:
        print(phrase)
        thesaurusDic['dependency'].append(get_stanford_dependency(phrase, '../utils'))
        cnt += 1
        if cnt %20 ==0:
            print("dependency parsing for thesaurus," +str(cnt/(len(thesaurusDic['sentence'])*1.)*100)+ "percent is done.")
            with open('./results/thesaurus_all_dependency.json', 'w') as f:
                json.dump(thesaurusDic, f)
            f.close()

    print("thesaurus_all done")

def split_idioms_dependency_into_bodyparts(bodyparts):
    with open('./results/idioms_dependency.json', 'r') as f:
        idiomsJson = json.load(f)
    f.close()

    result = {}
    for bp in bodyparts:
        result[bp] = {'dependency': [], 'sentence': []}

    for bp in bodyparts:
        for idx, phrase in enumerate(idiomsJson['sentence']):
            for word in phrase.split():
                if en.noun.singular(word.lower()) == bp.lower():
                    result[bp]['dependency'].append(idiomsJson['dependency'][idx])
                    result[bp]['sentence'].append(phrase)
                    break

    with open('./results/idioms_bp_dependency.json', 'w') as f:
        json.dump(result, f)
    print("idioms bodyparts done")

if __name__ == "__main__":
    bodyparts = get_bodyparts(bpDir = '../data/bodyparts.txt')
    get_thesaurus_dependency(bodyparts)
    #get_idioms_dependency()
    #split_idioms_dependency_into_bodyparts(bodyparts)
    #get_thesaurus_all_dependency()
