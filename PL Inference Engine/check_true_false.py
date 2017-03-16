#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Notes:       *Ported by Christopher Conly from C++ code supplied by Dr. 
#               Vassilis Athitsos.
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so I put it in a list, which
#               is passed by reference.
#              *Written to be Python 2.4 compliant for omega.uta.edu

# Name: Arnav Garg
# Class: CSE 4308 - 001
# ID: 1001039593

#-------------------------------------------------------------------------------

import sys
from logical_expression import *

def check_true_false(knowledge_base, statement, m_dict):
    try:
        output_file = open('result.txt', 'w')
    except:
        print('failed to create output file')
    
    kb_symbols = []
    s_symbols = []

    model = m_dict.copy();

    # extracting all the symbols from the KB
    extract_symbols(knowledge_base, kb_symbols)
    extract_symbols(statement, s_symbols)

    # removing the repeated ones
    kb_symbols = list(set(kb_symbols))
    s_symbols = list(set(s_symbols))

    # Extending the kb_list with the alpha symbol list
    kb_symbols.extend(s_symbols)
    # Removing the duplicates
    symbols = list(set(kb_symbols))

    # removing the symbols I know are true
    
    for key in model.keys():
        try:
            symbols.remove(key)
        except Exception:
            print 'TODO.. symbols are different'

    
    print symbols        
    # Doing the TT check
    result = tt_check_all(knowledge_base, statement, symbols, model)

    output_file.write('result unknown')    
    output_file.close()


def tt_check_all(kb, alpha, symbols, model):
    pass

def main(argv):    
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'rb')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)

    # This is basically for optimizing the TT-Entails.    
    m_dict = {}

    # Create the knowledge base with wumpus rules
    print '\nLoading wumpus rules...'
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue

        counter = [0]  # A mutable counter so recursive calls don't just make a copy

        subexpression = read_expression(line.rstrip('\r\n'), counter)

        if subexpression.connective[0] == '':
            m_dict[subexpression.symbol[0]] = True

        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'rb')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print 'Loading additional knowledge...'
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # a mutable counter
        subexpression = read_expression(line.rstrip('\r\n'), counter)

        if subexpression.connective == '':
            m_dict[subexpression.symbol[0]] = True

        knowledge_base.subexpressions.append(subexpression)

    input_file.close()

    ## TODO: REMOVE DEBUG CODE.
    # print knowledge_base.connective
    # print knowledge_base.symbol
    # print '------------------------'

    # for subexpressions in knowledge_base.subexpressions:
    #     print subexpressions.connective

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # I had left this line out of the original code. If things break, comment out.
    print_expression(knowledge_base, '\n')

    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'rb')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print 'Loading statement...'
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    
    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print '\nChecking statement: ',
    print_expression(statement, '')
    print    

    print m_dict

    # Run the statement through the inference engine
    check_true_false(knowledge_base, statement, m_dict
)

    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)