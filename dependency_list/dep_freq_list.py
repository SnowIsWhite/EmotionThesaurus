"""This code reads json files(containing information of dependency relations),
and make a flattened dependency sequence that will be exploited in making a frequency list of the dependency relations.

1. File to read:
2. Some metrics in making dependency sequences
    - does not consider determiners.
    - take a subtree which takes either verb or a body part noun as a root

3. output files
    (dependecny sequence list in json file):
    - Thesaurus for each body parts
    - enitre Thesaurus
    - entire idioms
    - idioms for each body parts

    (dependency frequency list in csv file):
    - Thesaurus for each body parts
    - Thesaurus for entire body parts
    - enitre Thesaurus
    - entire idioms
    - idioms for each body parts
    - idioms entire body parts

LATER: make overlapping frequency list based on analysis on his result.

4. functions:
    - get_dependency_json_file: call other necessary functions in order
    - get_parse_tree: make parse tree
    - get_flattened_sequence: make sequence
    - traverse_tree: Get subtree
"""
import json, csv, sys, nltk
sys.path.append('../')
sys.path.append('../utils')
import en
from utils import *

def __find_root(dependencySeq):
    return dependencySeq[0][0]

def __get_parse_tree(dependencySeq, tree):
    triple = dependencySeq[0]
    if triple[0][0] != tree.get_item()[0] or triple[0][1] != tree.get_item()[1]:
        return __get_parse_tree(dependencySeq, tree.get_parent())
    triple = dependencySeq.pop(0)
    child = Tree(name = triple[2][0], pos = triple[2][1], relation = triple[1], parent = tree)
    tree.add_child(child)
    if len(dependencySeq) == 0:
        return tree
    if dependencySeq[0][0][0] != child.get_item()[0]:
        return __get_parse_tree(dependencySeq, tree)
    else:
        __get_parse_tree(dependencySeq, child)
    return tree

def __get_subtree(tree, bp, subtree):
    if en.noun.singular((tree.get_item()[0]).lower()) == en.noun.singular(bp.lower()) and 'NN' in tree.get_item()[1]:
        subtree.append(tree)
        return subtree
    if len(tree.get_children()) == 0:
        subtree.append('')
        return subtree
    for child in tree.get_children():
        if en.noun.singular((child.get_item()[0]).lower()) == en.noun.singular(bp.lower()) and 'NN' in child.get_item()[1]:
            subtree.append(tree)
            break
        __get_subtree(child,bp,subtree)
    return subtree

def __get_flattened_sequence(tree, rep):
    if len(tree.get_children()) == 0:
        return rep
    for child in tree.get_children():
        if 'DT' in child.get_item()[1]:
            continue
        rep.append(tree.get_item()[1]) #insert head
        rep.append(child.get_item()[2]) # add relation
        rep.append(child.get_item()[1]) # add child node
        __get_flattened_sequence(child, rep)
    return rep

def __change_into_triple_form(seq):
    term = 3
    cnt = 0
    res = []
    for s in seq:
        cnt += 1
        if cnt % term == 1:
            res.append('(')
        if s == "NNS":
            res.append('NN')
        elif s == "NNPS":
            res.append("NNP")
        elif s == "VBD":
            res.append('VB')
        elif s == "VBP":
            res.append("VBN")
        else:
            res.append(s)
        if cnt % term == 0:
            res.append(')')
    return res

def get_dependency_json_file(dic, bp, fname):
    resultDic = {'dependency': [], 'sentence': []}
    for idx, dependencySeq in enumerate(dic['dependency']):
        if len(dependencySeq) == 0: #smiling, etc.
            pos = nltk.tag.pos_tag([dic['sentence'][idx]])[0][1]
            resultDic['dependency'].append(['(',pos, ')'])
            resultDic['sentence'].append(dic['sentence'][idx])
            continue
        #get parse tree
        root = __find_root(dependencySeq)
        tree = Tree(name = root[0], pos = root[1], relation = 'root')
        parseTree = __get_parse_tree(dependencySeq, tree)
        if bp != 'none':
            subTree = []
            subTree = __get_subtree(parseTree, bp, subTree)
            rep = []
            realtree = parseTree
            for item in subTree:
                if item != '':
                    realtree = item
            res = __get_flattened_sequence(realtree, rep) #array of string
        else:
            rep = []
            res = __get_flattened_sequence(parseTree, rep)
        #change representation form
        res = __change_into_triple_form(res)
        resultDic['dependency'].append(res)
        resultDic['sentence'].append(dic['sentence'][idx])
    with open(fname, 'w') as f:
        json.dump(resultDic, f)
    f.close()
    print(fname + ' is done.')
    return resultDic

def __convert_into_frequency_dic(dic):
    res = {}
    depArr = []
    sentArr = []
    for idx, dep in enumerate(dic['dependency']):
        depArr.append(' '.join(dep))
        sentArr.append(dic['sentence'][idx])

    for idx, sequence in enumerate(depArr):
        if sequence in res:
            res[sequence]['frequency'] += 1.
            res[sequence]['norm'] += 1./(len(depArr)*1.)
            res[sequence]['samples'].append(sentArr[idx])
        else:
            res[sequence] = {'frequency': 1., 'norm': 1./(len(depArr)*1.), 'samples': [sentArr[idx]]}
    return res

def __write_csv_file(freqList, fname):
    #dependency relations, frequency, norm, samples
    fieldname = ['dependency', 'frequency', 'norm', 'samples']
    sortedDic = sorted(freqList.items(), key = lambda (k,v): v['norm'], reverse = True)
    csvArr = []
    for (x,y) in sortedDic:
        tempArr = []
        tempArr.append(x)
        tempArr.append(str(y['frequency']))
        tempArr.append(str(y['norm']))
        tempArr.append('\n'.join(y['samples']))
        csvArr.append(tempArr)

    with open(fname, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldname)
        writer.writerows(csvArr)

def get_frequency_csv_file(dic, fname):
    freqList = __convert_into_frequency_dic(dic)
    __write_csv_file(freqList, fname)
    print(fname + ' done')
    return freqList

def frequency_analytics(dic, fname):
    user_bodyparts = get_bodyparts(bpDir = '../data/bodyparts.txt')
    maxlen = 0
    for bp in user_bodyparts:
        len_ = len(dic[bp])
        if len_ > maxlen:
            maxlen = len_
    compareDic = {}
    for bp in user_bodyparts:
        compareDic[bp] = []
        sortedDic = sorted(dic[bp].items(), key = lambda (k,v): v['norm'], reverse = True)
        for (x,y) in sortedDic:
            compareDic[bp].append(y['frequency'])

    for bp in user_bodyparts:
        if len(compareDic[bp]) < maxlen:
            for idx in range(maxlen - len(compareDic[bp])):
                compareDic[bp].append('')

    csvArr = []
    with open('./results/frequency/' + fname + '.csv', 'w') as csvfile:
        fieldname = []
        for bp in user_bodyparts:
            fieldname.append(bp.lower())
        for idx in range(maxlen):
            tempArr = []
            for bp in user_bodyparts:
                tempArr.append(compareDic[bp][idx])
            csvArr.append(tempArr)
        writer = csv.writer(csvfile)
        writer.writerow(fieldname)
        writer.writerows(csvArr)

if __name__ == '__main__':
    bodyparts = get_bodyparts(bpDir = '../data/bodyparts.txt')
    dependencyLoc = '../syntax/results/'
    #read json files
    with open(dependencyLoc + 'thesaurus_dependency.json', 'r') as f:
        thesaurusJson = json.load(f)
    f.close()
    with open(dependencyLoc + 'idioms_dependency.json', 'r') as f:
        idiomsJson = json.load(f)
    f.close()
    with open(dependencyLoc + 'idioms_bp_dependency.json', 'r') as f:
        idiomsJson_bp = json.load(f)
    f.close()
    with open(dependencyLoc + 'thesaurus_dependency_all.json', 'r') as f:
        thesaurus_allJson = json.load(f)
    f.close()

    #flattened dependency
    #thesaurus, for each bodyparts
    for bp in bodyparts:
        dic = thesaurusJson[bp]
        fname = './results/sequences/thesaurus_' + bp + '.json'
        thesaurusJson[bp] = get_dependency_json_file(dic, bp, fname)

    #entire thesaurus
    fname = './results/sequences/thesaurus_all.json'
    thesaurus_allJson = get_dependency_json_file(thesaurus_allJson, 'none', fname)

    #idioms, for each bodyparts
    for bp in bodyparts:
        fname = './results/sequences/idioms_' + bp + '.json'
        dic = idiomsJson_bp[bp]
        idiomsJson_bp[bp] = get_dependency_json_file(dic, bp, fname)

    #entire idioms
    fname = './results/sequences/idioms_all.json'
    idiomsJson = get_dependency_json_file(idiomsJson, 'none', fname)

    #frequency list
    thesaurusFreqList = {}
    idiomsFreqList = {}
    #thesaurus, for each body parts
    for bp in bodyparts:
        dic = thesaurusJson[bp]
        fname = './results/frequency/thesaurus_' + bp+ '.csv'
        thesaurusFreqList[bp] = get_frequency_csv_file(dic, fname)

    #thesaurus, all body parts
    fname = './results/frequency/thesaurus_all_bp.csv'
    tempDic = {'dependency': [], 'sentence': []}
    for bp in bodyparts:
        for idx, item in enumerate(thesaurusJson[bp]['dependency']):
            tempDic['dependency'].append(item)
            tempDic['sentence'].append(thesaurusJson[bp]['sentence'][idx])
    get_frequency_csv_file(tempDic, fname)

    #thesaurus, entire data
    fname = './results/frequency/thesaurus_entire.csv'
    get_frequency_csv_file(thesaurus_allJson, fname)

    #idioms, for each body parts
    for bp in bodyparts:
        fname = './results/frequency/idioms_' + bp + '.csv'
        dic = idiomsJson_bp[bp]
        idiomsFreqList[bp] = get_frequency_csv_file(dic, fname)

    #idioms, all body parts
    fname = './results/frequency/idioms_all_bp.csv'
    tempDic = {'dependency': [], 'sentence': []}
    for bp in bodyparts:
        for idx, item in enumerate(idiomsJson_bp[bp]['dependency']):
            tempDic['dependency'].append(item)
            tempDic['sentence'].append(idiomsJson_bp[bp]['sentence'][idx])
    get_frequency_csv_file(tempDic, fname)

    #idioms, entire data
    fname = './results/frequency/idioms_entire.csv'
    get_frequency_csv_file(idiomsJson, fname)

    ############################################
    ############################################
    ################SOME ANALYSIS###############
    ############################################
    ############################################
    frequency_analytics(thesaurusFreqList, 'thesaurus_all_freq_analysis')
    frequency_analytics(idiomsFreqList, 'idioms_all_freq_analysis')
