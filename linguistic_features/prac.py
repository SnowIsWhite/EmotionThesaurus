import re

regex = r'((cross|crossed|crossing)(.*?)arms?)'

s = 'he crossed his fucking arms'
res = [(m.start(0), m.end(0)) for m in re.finditer(regex, s)]
print(res)
for tup in res:
    string = s[tup[0]:tup[1]]
    print(string)
