import sys, csv
sys.path.append('../utils')
sys.path.append('../')
from utils import *
import en
resultDir ='./results/verb_overlaps/'

bodyparts = get_bodyparts('../data/bodyparts.txt')
gutenbergData = {}
thesaurusData = {}
#read csv
for bp in bodyparts:
    gutenbergName = './results/gutenberg/csv/' + bp + '_verb_freq.csv'
    thesaurusName = './results/thesaurus/csv/' + bp + '_verb_freq.csv'
    gutenbergData[bp] = []
    with open(gutenbergName, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for idx, line in enumerate(reader):
            if idx > 0:
                gutenbergData[bp].append(line)
    csvfile.close()

    thesaurusData[bp] = []
    with open(thesaurusName, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for idx, line in enumerate(reader):
            if idx > 0:
                thesaurusData[bp].append(line)
    csvfile.close()



#get overlap
res = {}
for bp in bodyparts:
    res[bp] = []
    if len(gutenbergData[bp]) == 0:
        continue
    if float(gutenbergData[bp][0][1]) > 9:
        rank1 = 1
        max1= float(gutenbergData[bp][0][1])
        for idx, line in enumerate(gutenbergData[bp]):
            verb = line[0]
            if float(line[1]) < max1:
                rank1 += 1
                max1 = float(line[1])
            rank2 = 1
            max2 = float(thesaurusData[bp][0][1])
            for idx2, line2 in enumerate(thesaurusData[bp]):
                verb2 = line2[0]
                if float(line2[1]) < max2:
                    rank2 += 1
                    max2 = float(line2[1])
                arr = []
                try:
                    verb = en.verb.present(verb.lower())
                    verb2 = en.verb.present(verb2.lower())
                except KeyError:
                    continue
                if verb in verb2:
                    arr.append(verb)
                    arr.append(line[1])
                    arr.append(line2[1])
                    arr.append(rank1)
                    arr.append(rank2)
                    arr.append(line[4].replace('\t\t', '\n'))
                    arr.append(line2[4].replace('\t\t', '\n'))
                    res[bp].append(arr)

        #write file
        fname = './results/verb_overlaps/' + bp +'_overlaps.csv'
        fieldname = ['verb', 'freq_g', 'freq_t', 'rank_g', 'rank_t', 'sent_g', 'sent_t']
        with open(fname, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldname)
            writer.writerows(res[bp])
