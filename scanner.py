import sys

from ply import lex
import io


tokens = ('SINO', 'SI', 'ENT', 'VACUO',
          'RET', 'MIENTRAS', 'REP', 'MULT',
          'PLUS', 'DIV', 'MINUS',
          'LT', 'EQ', 'AND', 'NOT',
          'ASSIGN', 'LSQUARE', 'RSQUARE', 'LANGLE',
          'RANGLE', 'LPARENT', 'RPARENT', 'SCOMMENT',
          'LCOMMENT', 'NUMBER',
          'COMMA', 'SEMICOLON', 'ID')


def t_SINO(t):
    # Funcion que define la regla de expresion regular para el token SINO

    r'(?i:sino)'
    return t


def t_SI(t):
    # Funcion que define la regla de expresion regular para el token SI

    r'(?i:si)'
    return t


# ENT
def t_ENT(t):
    # Funcion que define la regla de expresion regular para el token ENT

    r'(?i:ent)'
    return t


def t_VACUO(t):
    # Funcion que define la regla de expresion regular para el token VACUO

    r'(?i:vacuo)'
    return t


def t_RET(t):
    # Funcion que define la regla de expresion regular para el token RET

    r'(?i:ret)'
    return t


def t_MIENTRAS(t):
    # Funcion que define la regla de expresion regular para el token MIENTRAS

    r'(?i:mientras)'
    return t


def t_REP(t):
    # Funcion que define la regla de expresion regular para el token REP

    r'(?i:rep)'
    return t


def t_MULT(t):
    # Funcion que define la regla de expresion regular para el token ++

    r'\+\+'
    return t


def t_PLUS(t):
    # Funcion que define la regla de expresion regular para el token +

    r'\+'
    return t


def t_DIV(t):
    # Funcion que define la regla de expresion regular para el token --

    r'--'
    return t


def t_MINUS(t):
    # Funcion que define la regla de expresion regular para el token -

    r'-'
    return t


def t_LT(t):
    # Funcion que define la regla de expresion regular para el token LT

    r'LT'
    return t


def t_EQ(t):
    # Funcion que define la regla de expresion regular para el token EQ

    r'EQ'
    return t


def t_AND(t):
    # Funcion que define la regla de expresion regular para el token &&

    r'&&'
    return t


def t_NOT(t):
    # Funcion que define la regla de expresion regular para el token !

    r'!'
    return t


def t_ASSIGN(t):
    # Funcion que define la regla de expresion regular para el token =

    r'='
    return t


def t_LSQUARE(t):
    # Funcion que define la regla de expresion regular para el token [

    r'\['
    return t


def t_RSQUARE(t):
    # Funcion que define la regla de expresion regular para el token ]

    r']'
    return t


def t_LANGLE(t):
    # Funcion que define la regla de expresion regular para el token <

    r'<'
    return t


def t_RANGLE(t):
    # Funcion que define la regla de expresion regular para el token >

    r'>'
    return t


def t_LPARENT(t):
    # Funcion que define la regla de expresion regular para el token (

    r'\('
    return t


def t_RPARENT(t):
    # Funcion que define la regla de expresion regular para el token )

    r'\)'
    return t


def t_COMMA(t):
    # Funcion que define la regla de expresion regular para el token ,

    r','
    return t


def t_SEMICOLON(t):
    # Funcion que define la regla de expresion regular para el token ;

    r';'
    return t


def t_NUMBER(t):
    # Funcion que define la regla de expresion regular para el token NUMBER, en sus
    # 3 formas posibles (Octagonal, Hexadecimal y Decimal)

    r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+'
    return t


def t_SCOMMENT(t):
    # Funcion que define la regla de expresion regular para el token SCOMMENT, este token
    # es ignorado por el scanner

    r'\#.*'
    pass


def t_LCOMMENT(t):
    # Funcion que define la regla de expresion regular para el token LCOMMENT, este token
    # es ignorado por el scanner

    r'(\*/(.|\n)*?/\*)'
    pass


def t_ID(t):
    # Funcion que define la regla de expresion regular para el token ID

    r'[a-z](\$?[a-zA-Z])*\$?[0-9]*'
    return t


t_ignore = ' \t\n'  # Ignorar esto!


def t_error(t):
    # Funcion que define imprime un mensaje de erroe al encontrar un caracter invalido

    print("Illegal character '{0}' at line {1}".format(t.value[0], t.lineno))
    # Tratamiento de errores.
    t.lexer.skip(1)

# build the lexer

fileName = str(sys.argv[1])
lexer = lex.lex()

out = open('parser_examples/out1.dot', 'w')
with open(fileName, 'r') as arch:
    contents = arch.read()
    result = lexer.input(contents)
    for token in lexer:
        print("Token:", token)

