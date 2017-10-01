import os, sys, subprocess
from nltk import DependencyGraph
from nltk.parse.stanford import StanfordDependencyParser

class Tree(object):
    "Generic tree node."
    def __init__(self, name= 'root', pos = 'VB', relation = 'root', children=None, parent = None):
        self.name = name
        self.pos = pos
        self.relation = relation
        self.children = []
        self.parent = parent
        if children is not None:
            for child in children:
                self.add_child(child)
    def get_item(self):
        return [self.name, self.pos, self.relation]
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    def get_children(self):
        return self.children
    def get_parent(self):
        return self.parent

def get_stanford_dependency(sentence, path_to_utils):#Stanford Dependency Parser
    path_to_jar = path_to_utils + '/stanford-parser-full-2017-06-09/stanford-parser.jar'
    path_to_models_jar = path_to_utils + '/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    parsed = dependency_parser.raw_parse(sentence)
    dep = parsed.next()
    res = list(dep.triples())
    return res

def get_syntaxnet_dependency(sentenceList):
    all_sentences = '\n'.join(sentenceList)
    FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(
        'cd  /Users/jaeickbae/Documents/projects/utils/models/syntaxnet; '
        'echo \'%s\' | syntaxnet/demo.sh ' % all_sentences,
        shell=True,
        universal_newlines=False,
        stdout=subprocess.PIPE,
        stderr=FNULL)
    output = process.communicate()

    processed_sentences = []
    sentence = []
    for line in output[0].split("\n"):
        if len(line) == 0:
            processed_sentences.append(sentence)
            sentence = []
        else:
            word = line.split("\t")
            sentence.append(word)

    deps = []
    for sentence in processed_sentences:
        s = ''
        for line in sentence:
            s += "\t".join(line) + '\n'
        deps.append(s)

    result = []
    print(deps)
    for sent_dep in deps:
        if len(sent_dep) == 0:
            continue
        tmp = []
        try:
            graph = DependencyGraph(tree_str=sent_dep.decode("utf8"))
            for triple in graph.triples():
                tmp.append(triple)
            result.append(tmp)
        except ValueError:
            result.append(tmp)
    return result

def get_bodyparts(bpDir = './data/bodyparts.txt'):
    with open(bpDir, 'r') as f:
        bp = []
        for line in f.readlines():
            for word in line.split():
                bp.append(word)
    return bp

def isEnglish(phrase):
    try:
        phrase.decode('ascii')
    except UnicodeDecodeError:
        return False
    return True
