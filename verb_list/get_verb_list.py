"""This code does the followings:
1. Functions
    find verb corresponding to the body parts -> count frequency -> calculate pmi values -> write
2. Input files
    1) gutenberg dependency
    2) emotion thesaurus dependency
3. Output files
    1) gutenberg: for each body parts, csv file
    2) emotion thesaurus: for each body parts, csv file
    * order by pmi values
    * csv file format: verb, frequency, pmi, sentences
4. file directory:
    results > gutenberg > csv > hand, arm,...
                        plot > graphs that have sufficient number
            > thesaurus > hand, arm,...
                        plot > grpah s that have sufficient number
"""
import nltk, os, sys, json, csv
import numpy as np
sys.path.append('../utils')
sys.path.append('../')
import en
from utils import*

def find_verbs(jsonData):
    res = {}
    for bp in jsonData:
        res[bp] = {}
        depArr = jsonData[bp]['dependency']
        sentArr = jsonData[bp]['sentence']
        for idx, dependency in enumerate(depArr):
            for triples in dependency:
                if (((bp.lower() in (en.noun.singular(triples[0][0].lower()))) and ('N' in triples[0][1])) or ((bp.lower() == (en.noun.singular(triples[2][0].lower())) and ('N' in triples[2][1])))) and (('V' in triples[0][1]) or ('V' in triples[2][1])) and ('subj' in triples[1] or 'obj' in triples[1]):
                    if 'V' in triples[0][1]:
                        try:
                            verb = en.verb.present(str(triples[0][0]).lower())
                        except KeyError:
                            verb = str(triples[0][0])
                    else:
                        try:
                            verb = en.verb.present(str(triples[2][0]).lower())
                        except KeyError:
                            verb = str(triples[2][0])
                    if verb in res[bp]:
                        res[bp][verb]['freq'] += 1.
                        res[bp][verb]['norm'] += 1./(len(depArr)*1.)
                        res[bp][verb]['sentence'].append(sentArr[idx])
                        res[bp][verb]['dependency'].append(dependency)
                    else:
                        res[bp][verb] = {'freq': 1., 'norm': 1./(len(depArr)*1.), 'pmi': 0., 'sentence': [sentArr[idx]], 'dependency': [dependency]}
    return res

def get_pmi(dic):
    #make vocab list
    vocab = []
    for bp in dic:
        for verb in dic[bp]:
            if verb not in vocab:
                vocab.append(verb)
    Vlen = len(vocab)
    Nlen = len(dic)

    #make matrix (log probability)
    weightMat = np.ones((Vlen, Nlen))
    for j, bp in enumerate(dic):
        for i, verb in enumerate(vocab):
            if verb in dic[bp]:
                weightMat[i][j] += dic[bp][verb]['freq']
    Vsum = np.sum(weightMat, axis = 1)
    Nsum = np.sum(weightMat, axis = 0)
    totSum = np.sum(Nsum, axis = 0)

    weightMat = np.log(weightMat) - np.log(Nsum) + np.log(totSum)
    weightMat = np.transpose(np.transpose(weightMat) - np.log(np.transpose(Vsum)))
    weightMat[weightMat<0] = 0

    #add pmi to the dic
    for j, bp in enumerate(dic):
        for i, verb in enumerate(vocab):
            if verb in dic[bp]:
                dic[bp][verb]['pmi'] = weightMat[i][j]
    return dic

def save_in_csv(dic, fdir):
    fieldname = ['verb', 'frequency', 'norm', 'pmi', 'samples']
    for bp in dic:
        fname = fdir + str(bp)+ '_verb_freq.csv'
        sortedDic = sorted(dic[bp].items(), key= lambda (k,v): v['norm'], reverse = True)
        csvArr = []
        for (x,y) in sortedDic:
            temp = []
            temp.append(x)
            temp.append(str(y['freq']))
            temp.append(str(y['norm']))
            temp.append(str(y['pmi']))
            temp.append('\t\t'.join(y['sentence']))
            csvArr.append(temp)

        with open(fname, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldname)
            writer.writerows(csvArr)

def call_functions(jsonData, fdir):
    result = {}
    #given dependency, find verb
    result = find_verbs(jsonData)
    #get pmi
    result = get_pmi(result)
    #sort by pmi value and save in csv file
    save_in_csv(result, fdir)

if __name__ == "__main__":
    #gutenberg
    with open('../syntax/results/gutenberg_dependency.json', 'r') as f:
        gutenbergData = json.load(f)
    f.close()
    fdir = './results/gutenberg/csv/'
    call_functions(gutenbergData, fdir)
    print('gutenberg comlete')

    #thesaurus
    with open('../syntax/results/thesaurus_dependency.json', 'r') as f:
        thesaurusData = json.load(f)
    f.close()
    fdir = './results/thesaurus/csv/'
    call_functions(thesaurusData, fdir)
    print('thesaurus complete')
