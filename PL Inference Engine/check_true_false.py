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


'''
@description: This function checks for the statement and the not_statement and returns
              if the statements entail KB.

@Params: knowledge_base: The knowledge
         statement: alpha
         not_statement: negation of alpha
         m_dict: All the known truth values 
'''
def check_true_false(knowledge_base, statement, not_statement, m_dict):
    
    try:
        output_file = open('result.txt', 'w')
    except:
        print('failed to create output file')
    
    # Storing all the knowledge_base symbols.
    kb_symbols = []
    # Storing all the sentence variables
    # NOTE: not_setence and sentence will have the same variables.
    s_symbols = []

    # Making a shallow copy of the m_dict and storing the values
    # in the model
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

            print
            print 'Sentence contains symbols not present in the KB'
            sys.exit(0)

    # Doing the TT check for alpha
    result_alpha = tt_check_all(knowledge_base, statement, symbols, model)

    # Doing the TT check for negation of alpha
    result_not_alpha = tt_check_all(knowledge_base, not_statement, symbols, model)
    
    print                 
    print 'ANSWER: ', 

    # Different answers depending on the values of alpha and not alpha
    if result_alpha == True and result_not_alpha == False:
        output_file.write('definitely true') 
        print 'definitely true'
    elif result_alpha == False and result_not_alpha == True:
        output_file.write('definitely false')
        print 'definitely false'
    elif result_alpha == False and result_not_alpha == False:
        output_file.write('possibly true, possibly false')
        print 'possibly true, possibly false'
    elif result_alpha == True and result_not_alpha == True:
        output_file.write('both true and false')
        print 'both true and false'
    else:
        output_file.write('Error in the code')    
        
    print 
    output_file.close()


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

    not_statement = '(not '+ statement + ')'

    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)

    # Cause this makes my code work.
    counter = [0]

    # Convert statement into a logical expression and verify it is valid 
    not_statement = read_expression(not_statement, counter)

    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print '\nChecking statement alpha: ',
    print_expression(statement, '')
    print
    print '\nChecking statement NOT alpha: ',
    print_expression(not_statement, '')
    print    

    # Run the statement through the inference engine
    check_true_false(knowledge_base, statement, not_statement, m_dict)

    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)
