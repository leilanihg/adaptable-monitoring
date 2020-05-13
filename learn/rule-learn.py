"""rule_learn.py: Rule learning file."""

__author__      = "Leilani H. Gilpin"

import argparse

debug = True
TEST_LOG_FILE = '../test/racecar_cone_test/'
RULE_KEYWORDS = ['before', 'after', 'because'] 
ERROR_KEYWORDS = ['ERROR']

def read_errors(file="../test/error.txt"):
    # Open file    
    fileHandler = open (file, "r")
    listOfLines = fileHandler.readlines()
    logs = []
    log = []
    for line in listOfLines:
        if not line.isspace():
            log.append(line.strip())
        else:
            logs.append(log)
            log = []
    return logs

# Just a printer for testing sake
def print_errors(items):
    for item in items:
        print(item)

# Right now, it just processes the repeats, but in the future it will
# also do other types of analysis.
def find_new_rules(elements):
    return process_repeats(elements)

# Find the repeated elements 
def process_repeats(elements):
    seen = set()
    unique = []
    for element in elements:
        event = element[0]
        if isinstance(event, (list,)):
            new_event = ''.join(map(str, event))
        else:
            new_event = event
        if is_explanation(new_event):
            if new_event not in unique:
                unique.append(new_event)
            else:
                seen.add(new_event)
    if debug and len(seen)>0:
        print("The following events are repeats and should be new rules")
        for item in seen:
            print(item)
    return seen

# This will have to be expanded to something that is a good explanation
def is_explanation(event):
    items = event.split(' ')
    if len(items) >= 3:
        return True
    else: return False

def remove_keywords(explanation):
    for word in ERROR_KEYWORDS:
        explanation = explanation.replace(word, "")
    return explanation.strip()
    
def parse_explanation(description):
    if debug:
        print("Found the explanation ", description)
    tokens = remove_keywords(description).split()
    splitter = None
    for token in tokens:
        if token in RULE_KEYWORDS:
            splitter = tokens.index(token)
    return [tokens[0], tokens[splitter], tokens[splitter+1]]
            

def make_rule(triple, prefix="foo", ontology="ontology"):
    first = prefix+":"+triple[0]
    action = ontology+":"+triple[1]
    second = prefix+":"+triple[2]
    return first+" "+action+" "+second
    

def make_new_rule(description, policy, count, prefix="foo"):
    rule_triple = parse_explanation(description)
    if debug:
        print("Found triple")
        print(rule_triple)
    new_rule_text = ":added-rule-"+ str(count) + " a air:Belief-rule;\n" 
    new_rule_text+= "    rdfs:comment \"Trying this out .\";\n" # This is  test
    new_rule_text+= "    air:if {\n"
    new_rule_text+= "        "+make_rule(rule_triple)+". };\n"
    new_rule_text+= "    air:then[\n"
    new_rule_text+= "        air:description (\""+description+"\"); \n"
    new_rule_text+= "        air:assert[air:statement{foo:cone  air:compliant-with " + policy + " .}]] ;\n"
    new_rule_text+= "    air:else [\n"
    new_rule_text+= "        air:assert[air:statement{foo:cone  air:non-compliant-with " + policy + " .}]] ;\n"
    return new_rule_text

# Given a natural language description, parse it into an Air Policy
# Rule
# Adding a count for labeling the rules
def parse_into_rules(descriptions, reason="event occured multiple times"):
    rule_text = ""
    policy = ":learned_policy"
    policy_text = policy+" a air:Policy"
    policy_end = "rdsf:label \"Learned tactic by "+reason
    added_count = 1
    for description in descriptions:
        rule_text+=make_new_rule(description, policy, added_count)
        added_count += 1
    return rule_text

def main():
    parser = argparse.ArgumentParser(description='Process explanations') 
    parser.add_argument('log', nargs='*', default = "",
                        help='The log file to read in')
    parser.add_argument('--debug', action='store_true',
                        help='print debug messages to stderr')
    args = parser.parse_args()

    """ Right now, we only parse one error file at a time"""
    if(args.log):
        error = TEST_LOG_FILE+args.log[0]+'.txt'
        elements = read_errors(error)
    else:
        elements = read_errors()
    new_rules = find_new_rules(elements)
    print(parse_into_rules(new_rules))

if __name__=="__main__":
    main()
