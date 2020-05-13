# Date - Friday August 31, 2018
# This system is built as part of the reasonableness monitoring system
# Author - LHG

import argparse
import requests
import sys
import logging as log

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer

from .primitives import *
from .primitives import representation as rep
from .primitives import verbs
#from .search import *
from .verbs import *
from linked import process

import rdflib
#from process import *

# TODO - Need verbose
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sentence', nargs='+',
                    help='Sentence')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help='This is the same as debug right now')
    args = parser.parse_args()

    if args.verbose:
        log.basicConfig(stream=sys.stdout, format="%(levelname)s: %(message)s",
                        level=log.DEBUG)
        log.info("Verbose output.")

    print(args.sentence)
    # Sanity check here....
    tree = rep.parse_with_regex(args.sentence)
    (noun, noun_phrase, adjectives) = rep.get_noun_phrase(tree)
    (verb, object, context, phrase_dict) = rep.get_verbs(tree, args.verbose)
    if not adjectives == '':
        if 'adverb' in phrase_dict:
            phrase_dict['adverb'].append(adjectives)
        else:
            phrase_dict['adverb'] = [adjectives.strip()]
    phrase_dict['noun'] = noun_phrase

    
    # WRITE RDFS HERE
    # Actor
    # Primitive
    # Object
    # Context
    
    # get verb type
    act = verbs.get_verb_type(verb, noun, object, context, phrase_dict, args.verbose)

    process.write_output(act)
    #process.write_rdf(noun, verb, object, context, phrase_dict)
    info = process.read_output()
    process.explain(info, args.sentence)
#consistent = act.check_constraints()
    #act.print_summary(consistent)

if __name__ == "__main__":
    main()

