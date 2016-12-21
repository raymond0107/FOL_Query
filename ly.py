import ply.lex as lex
import ply.yacc as yacc
from helper import *

tokens = ('NAME', 'IMPLY', 'VAR')

literals = [ '&', '|', '~', '(', ')', ',']

# Regular expression rules for simple tokens
t_NAME   = r'[A-Z][a-zA-Z]*'
t_IMPLY = r'\=\>'
t_VAR = r'[a-z]+'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n\r'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lex.lex()

def p_term1_imply(p):
    'term1 : term1 IMPLY term2'
    p[0] = (p[1].do_not()).do_or(p[3])

def p_term1_term2(p):
    'term1 : term2'
    p[0] = p[1]

def p_term2_and(p):
    '''term2 : term2 '&' term3'''
    p[0] = p[1].do_and(p[3])

def p_term2_or(p):
    '''term2 : term2 '|' term3'''
    p[0] = p[1].do_or(p[3])

def p_term2_term3(p):
    'term2 : term3'
    p[0] = p[1]

def p_term3_factor(p):
    'term3 : factor'
    p[0] = Conjunction([Clause([p[1]])])

def p_term3_not(p):
    '''term3 : '~' term3'''
    p[0] = p[2].do_not()

def p_term3_term1(p):
    '''term3 : '(' term1 ')' '''
    p[0] = p[2]

def p_factor_name(p):
    '''factor : NAME '(' args ')' '''
    p[0] = Predicate(p[1], p[3])

def p_args_var(p):
    '''args : NAME
            | VAR
    '''
    p[0] = [p[1]]

def p_args_combine(p):
    '''args : args ',' NAME
            | args ',' VAR
    '''
    p[1].append(p[3])
    p[0] = p[1]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()