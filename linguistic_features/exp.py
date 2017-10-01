import re
import os

read_data_dir = '/Users/jaeickbae/Documents/projects/EmotionThesaurus/data/Gutenberg/'
windowsize = 2000
data = ''
for root, dirs, files in os.walk(read_data_dir):
    for file in files:
        if file.endswith('.txt'):
            fname = os.path.join(root,file)
            with open(fname, 'r') as f:
                data = '\n'.join([data, f.read().lower()])

regex_list = [r'((\b(hold|holding|held)\b)(.*?)(\belbows?\b)(.*?)(\bfrom\b))', r'((\blegs?\b)(.*?)(\b(wide|widen|widened)\b))',\
            r'((\b(cross|crossing|crossed)\b)(.*?)(\barms?\b))', r'((\b(stand|standing|stood)\b)(.*?)(\b(wide|widen|widened)\b))',\
            r'((\b(crack|cracking|cracked)\b)(.*?)(\bknuckles?\b))', r'((\b(arms?))(.*?)(\b(cross|crossed|crossing)\b))',\
            r'((\b(pound|pounding|pounded)\b)(.*?)(\bfists?\b))']
            #r'((\bface\b)(.*?)(\bred+\b))'

substring = []
for pattern in regex_list:
    res = [(m.start(0), m.end(0)) for m in re.finditer(pattern, data)]
    print(res)
    if len(res) > 0:
        for tup in res:
            substring.append(data[tup[0] - windowsize : tup[1] + windowsize])

with open('result.txt', 'w') as f:
    for substr in substring:
        f.write(substr)
        f.write('\n\n\n======================================================\n\n\n')
