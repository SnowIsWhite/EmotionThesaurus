"""This code make overlapping frequency lists on dependency sequences:
1. input file:
    - thesaurus, for each body parts
    - thesaurus, entire
    - thesaurus, for all body parts
    vs.
    - idioms, entire
"""

import sys, csv
sys.path.append('../')
from utils import *
resultDir = './results/overlaps/'

thesaurus = {}
thesaurus_entire = []
thesaurus_all_bp = []
idioms = []
bodyparts = get_bodyparts('../data/bodyparts.txt')


def get_overlaps(list1, list2, fname):
    result = []
    rank1 = 1
    max1 = float(list1[0][1])
    for idx1, line1 in enumerate(list1):
        dependency1 = line1[0]
        if float(line1[1]) < max1:
            rank1 += 1
            max1 = float(line1[1])
        rank2 = 1
        max2 = float(list2[0][1])
        for idx2, line2 in enumerate(list2):
            dependency2 = line2[0]
            if float(line2[1]) < max2:
                rank2 += 1
                max2 = float(line2[1])
            arr = []
            if dependency1 == dependency2:
                arr.append(dependency1)
                arr.append(line1[1]) #frequency
                arr.append(line2[1])
                arr.append(line1[2]) #norm
                arr.append(line2[2])
                arr.append(rank1) #rank
                arr.append(rank2)
                arr.append(line1[3]) #samples
                arr.append(line2[3])
                result.append(arr)

    fieldname = ['dependency', 'frequency1', 'frequency2', 'norm1', 'norm2', 'rank1', 'rank2', 'samples1', 'samples2']
    with open(fname, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldname)
        writer.writerows(result)
    return result

def get_non_overlaps(list_, overlapList, fname):
    result = []
    rank1 = 1
    max1 = float(list_[0][1])
    for idx1, line1 in enumerate(list_):
        dependency1 = line1[0]
        if float(line1[1]) < max1:
            rank1 += 1
            max1 = float(line1[1])
        flag = 0
        for idx2, line2 in enumerate(overlapList):
            dependency2 = line2[0]
            if dependency1 == dependency2:
                flag = 1
                break
        if flag ==0:
            arr = []
            arr.append(dependency1)
            arr.append(line1[1])
            arr.append(line1[2])
            arr.append(rank1)
            arr.append(line1[3])
            result.append(arr)
    fieldname = ['nonoverlapping dependency', 'frequency', 'norm', 'rank', 'samples']
    with open(fname, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldname)
        writer.writerows(result)

if __name__ == "__main__":
    #read csv
    for bp in bodyparts:
        thesaurus[bp] = []
        thesaurusName = './results/frequency/thesaurus_' + bp + '.csv'
        with open(thesaurusName, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for idx, line in enumerate(reader):
                if idx > 0:
                    thesaurus[bp].append(line)
        csvfile.close()

    thesaurus_all_name = './results/frequency/thesaurus_all_bp.csv'
    with open(thesaurus_all_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for idx, line in enumerate(reader):
            if idx > 0:
                thesaurus_all_bp.append(line)
    csvfile.close()

    thesaurus_entire_name = './results/frequency/thesaurus_entire.csv'
    with open(thesaurus_entire_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for idx, line in enumerate(reader):
            if idx > 0:
                thesaurus_entire.append(line)
    csvfile.close()

    idiomsName = './results/frequency/idioms_entire.csv'
    with open(idiomsName, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for idx, line in enumerate(reader):
            if idx > 0:
                idioms.append(line)
    csvfile.close()

    #get overlaps
    #thesaurus each body parts vs. entire idioms
    for bp in bodyparts:
        if len(thesaurus[bp]) == 0:
            continue
        if float(thesaurus[bp][0][1]) > 4:
            fname = resultDir + 'thesaurus_' + bp + '_vs_idioms_entire.csv'
            overlaps = get_overlaps(thesaurus[bp], idioms, fname)
            fname = resultDir + 'thesaurus_' + bp + '_non_overlaps.csv'
            get_non_overlaps(thesaurus[bp], overlaps, fname)
            fname = resultDir + 'idioms_' + bp + '_non_overlaps.csv'
            get_non_overlaps(idioms, overlaps, fname)

    #thesaurus for all body parts vs. entire idioms
    fname = resultDir + 'thesaurus_all_bp_vs_idioms_entire.csv'
    overlaps = get_overlaps(thesaurus_all_bp, idioms, fname)
    fname = resultDir + 'thesaurus_all_bp_non_overlaps.csv'
    get_non_overlaps(thesaurus_all_bp, overlaps, fname)
    fname = resultDir + 'idioms_t_all_bp_non_overlaps.csv'
    get_non_overlaps(idioms, overlaps, fname)

    #thesaurus entire vs idioms entire
    fname = resultDir + 'thesaurus_entire_vs_idioms_entire.csv'
    overlaps = get_overlaps(thesaurus_entire, idioms, fname)
    fname = resultDir + 'thesaurus_entire_non_overlaps.csv'
    get_non_overlaps(thesaurus_entire, overlaps, fname)
    fname = resultDir + 'idioms_t_enire_non_overlaps.csv'
    get_non_overlaps(idioms, overlaps, fname)
