#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
# 
# Name:         Arnav Garg
# Class:        CSE 4308 - 001
# ID:           1001039593
#
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):

    # print expression

    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

# Extracting all the symbols in this function.
def extract_symbols(expression, symbols):

    if expression.symbol[0]:
        symbols.append(expression.symbol[0])

    for subexpression in expression.subexpressions:
        extract_symbols(subexpression, symbols)

# A function for extending the dictionary.
# Pretty useless but essential because... Python
def extend_model(model, key, value):
    model[key] = value
    return model

# TT-CHECK-ALL FUNCTION. 
def tt_check_all(kb, alpha, symbols, model):

    if not symbols:
        # If true in the knowledge base
        if pl_true(kb, model):
            # return the value for the sentence for that model
            return pl_true(alpha, model)
        else:
            return True
    
    # Getting the first symbol
    p = symbols[0]
    # Storing the rest of the symbol
    rest = symbols[1:]

    return tt_check_all( kb, alpha, rest, extend_model(model, p, True) ) \
           and tt_check_all( kb, alpha, rest, extend_model(model, p, False) )

# PL TRUE FUNCTION
def pl_true(expression, model):
    # Check for connective AND
    if expression.connective[0].lower() == 'and':
        # A boolean value that will return the value for this expression
        bool_value = True
        # Going over all the subexpressions and AND-ing them.
        for i, subexpression in enumerate(expression.subexpressions):
            # Finding the inital value of the bool.
            if(i == 0):
                bool_value = pl_true(subexpression, model)
                continue;
            bool_value = bool_value and pl_true(subexpression, model)
        # Returning the value of all the AND subexpressions.
        return bool_value

    # Check for connective OR
    elif expression.connective[0].lower() == 'or':
        bool_value = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                bool_value = pl_true(subexpression, model)
                continue;
            bool_value = bool_value or pl_true(subexpression, model)
        return bool_value

    # Check for the connective NOT
    elif expression.connective[0].lower() == 'not':
        # A boolean value that will return the value for this expression
        # Here, we are just concerned with the not of the value.
        bool_value = not pl_true(expression.subexpressions[0], model)
        return bool_value

    # Check for the connective XOR
    elif expression.connective[0].lower() == 'xor':
        bool_value = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                bool_value = pl_true(subexpression, model)
                continue;
            # taking the XOR
            bool_value = bool_value ^ pl_true(subexpression, model)
        return bool_value

    elif expression.connective[0].lower() == 'if':
        bool_value = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                bool_value = pl_true(subexpression, model)
                continue;
            bool_value = (not bool_value) or pl_true(subexpression, model)
        return bool_value

    elif expression.connective[0].lower() == 'iff':
        bool_value = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                bool_value = pl_true(subexpression, model)
                continue;
            bool_value = not (bool_value ^ pl_true(subexpression, model))
        return bool_value
    
    # return the value of the symbol from the model dictionary
    return model[expression.symbol[0]]

def testing(expression):

    for i, subexpression in enumerate(expression.subexpressions):
        print subexpression.connective
        print subexpression.symbol
        print '-----------------------------'
        testing(subexpression)
