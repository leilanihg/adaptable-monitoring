# Date - Friday August 31, 2018
# This system is built as part of the reasonableness monitoring system
# Author - LHG

import rdflib
from rdflib import Graph
from rdflib import URIRef
import pprint
import os
from datetime import date

# Noun is the actor - by default
def write_rdf(noun, verb, object, context, phrase_dict, fileName='log.n3'):
    graph = Graph()
    rdflib = Namespace('http://rdflib.net/test/')
    graph.bind("test", "http://rdflib.net/test/")

    graph.add((rdflib['pic:1'], rdflib['name'], Literal('Jane & Bob')))
    graph.add((rdflib['pic:2'], rdflib['name'], Literal('Squirrel in Tree')))
    graph.commit()

    print("Triples in RDF Log after add: %d"% len(graph))

    # display the graph in RDF/XML
    print(graph.serialize())
    
    graph.close()

    # Clean up the mkdtemp spoor to remove the Sleepycat database files...
    for f in os.listdir(path):
        os.unlink(path+'/'+f)
    os.rmdir(path)

def read_output(file='out.n3'):
    with open(file) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    rule = False
    info = []

    for line in content:
        if rule:
            if line == '\n': # we're done
                print("Detected a line")
                print(rules)
                rule = False
                rules = dict()
            else:            # Do some processing
                if '"' in line and line.endswith(');'):
                    start = line.find("\"")
                    end = line.find("\"", start+1)
                    quote = line[start+1:end]
                    rules['description'] = quote
                else:
                    tokens = line.split()
                    try:
                        if tokens[0] == 'a:rule':
                            rules['name'] = tokens[1]
                            print(rules)
                        elif tokens[0] == 'pml:inputdata':
                            rules['input'] = (tokens[1], tokens[2], tokens[3])
                        elif tokens[0] == 'pml:outputdata':
                            if 'non-compliant' in tokens[2]:
                                print("Found non-compliant activity!")
                                reasonable = False
                                rules['compliant'] = False
                            else:
                                rules['compliant'] = True
                            rules['output'] = (tokens[1], tokens[2], tokens[3])
                    except IndexError:
                        rule = False
                        info.append(rules)
                        rules = dict()
                        continue
        if line.startswith('run') and line.endswith('RuleApplication;'):
            rule = True
            rules = dict()
    pprint.pprint(info)
    return info

# TODO - formatting for Lalana
def write_output(act, file='in.n3'):
    raw = open(file, 'r+')
    contents = raw.read().split("\n")
    raw.seek(0)
    raw.truncate()

    # Header information
    raw.write("# Author:  lgilpin\n")
    raw.write("# Date: %s\n\n" % str(date.today()))
    raw.write("@prefix foo: <http://foo#>.\n")
    raw.write("@prefix ontology: <http://ontology#>.\n")
    raw.write("\n")
    
    raw.close()
    print(act)
    return

def explain(info, summary):
    sentence = make_sentence(summary)
    judgement = ''

    explanation = ""
    for item in info:
        print("next iteration")
        print(item)
        if 'compliant' in item:
            if item['compliant']:
                explanation += item['description']
                explanation += ". "
            else:
                judgement = 'unreasonable'
                explanation += item['description']
                explanation += ". "
        else:
            print("not compliant")
    if judgement == '':
        judgement = 'reasonable'

    print("This perception is %s" %judgement.upper())
    print("==========================================")
    print(explanation)
    print('So it is %s to perceive %s' %(judgement, sentence))

def make_sentence(summary):
    toRet = ''
    for word in summary:
        if toRet=='':
            toRet += word.lower()
        else:
            toRet += ' '
            toRet += word
    return toRet.strip()

def process_line(line):
    tokens = line.split("\\s")
    if 'description' in tokens:
        return true

# Read the RDF and get the descriptions
def read_rdf(file='out.n3'):
    g = Graph()
    g.parse('out.n3', format='n3')

    # What are we looking for
    car = URIRef('http://foo#my_car')
    justification = URIRef('http://dig.csail.mit.edu/2009/AIR/air#then')
    compliant = URIRef('http://dig.csail.mit.edu/TAMI/2007/amord/air#compliant-with')
    notCompliant = URIRef('http://dig.csail.mit.edu/TAMI/2007/amord/air#non-compliant-with')
    description = URIRef('http://dig.csail.mit.edu/2009/AIR/airjustification#description')
    ruleApplication = URIRef('http://dig.csail.mit.edu/2009/AIR/airjustification#RuleApplication')

    runs = []
    rulesFired = g.subject_predicates(ruleApplication)
    for stmt in rulesFired:
        runs.append(stmt[0])
        pprint.pprint(stmt)

    for stmt in runs:
        print("For the following")
        print(stmt)
        important = g.predicate_objects(URIRef(stmt))
        for thing in important:
            print(thing)

#    others = g.subject_objects(description)
#    for stmt in others:
#        pprint.pprint(stmt)

#    so = g.subject_objects(notCompliant)
#    for stmt in so:
#        pprint.pprint(stmt)
#
#    sp = g.subject_predicates(notCompliant)
#    for stmt in sp:
#        pprint.pprint(stmt)#

#    po = g.predicate_objects(notCompliant)
#    for stmt in po:
#        pprint.pprint(stmt)

    #for car in g.subjects(car):
    #    print("%s %p %o") %(s,p,o)

    print("wtf happened")
    print(len(g)) # prints 2
    print("     ")
    supports = []
    contradictions = []

    for stmt in g:
        pprint.pprint(stmt)

    if (None, notCompliant, None) in g:
        print("This perception is UNREASONABLE")
        print("============================================")
    else:
        print("This perception is REASONABLE")
        print("============================================")

    # 

    # Get the literal
    # if everything compliant, great then it's reasonable

    # if something is non-compliant, its not reasonable
