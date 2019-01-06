# coding=utf-8
import sys

import ply.yacc as yacc

from scanner import tokens

import nodos
from build_symbol_table_visitor import BuildTablaSimbolosVisitor
from dibujar_AST_visitor import Visitor


def p_programa(p):
    """programa : lista_decl"""
    p[0] = nodos.Programa(p[1])

def p_lista_decl1(p):
    """lista_decl : lista_decl declaracion """
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[2], list):
        p[0].extend(p[2])
    else:
        p[0].extend([p[2]])


def p_lista_decl2(p):
    """lista_decl : declaracion"""
    p[0] = p[1]

def p_declaracion1(p):
    """declaracion : declaracion_var"""
    p[0] = p[1]

def p_declaracion2(p):
    """declaracion : declaracion_fun"""
    p[0] = p[1]

def p_declaracion_var1(p):
    """declaracion_var : def_tipo ID SEMICOLON"""
    p[0] = nodos.DeclaracionVar(p[1],p[2], None)

def p_declaracion_var2(p):
    """declaracion_var : def_tipo ID LANGLE NUMBER RANGLE SEMICOLON"""
    p[0] = nodos.DeclaracionVar(p[1],p[2],p[4])

def p_def_tipo1(p):
    """def_tipo : VACUO"""
    p[0] = p[1]


def p_def_tipo2(p):
    """def_tipo : ENT"""
    p[0] = p[1]
def p_declaracion_fun(p):
    """declaracion_fun : def_tipo ID LSQUARE parametros RSQUARE sentencia_comp"""
    p[0] = nodos.DeclaracionFun(p[1],p[2],p[4],p[6])

def p_parametros1(p):
    """parametros : lista_parametros"""
    p[0] = p[1]


def p_parametros2(p):
    """parametros : VACUO"""
    p[0] = p[1]

def p_lista_parametros1(p):
    """lista_parametros : lista_parametros COMMA param"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[3], list):
        p[0].extend(p[3])
    else:
        p[0].extend([p[3]])

def p_lista_parametros2(p):
    """lista_parametros : param"""
    p[0] = p[1]

def p_param(p):
    """param : def_tipo ID
             | def_tipo ID LANGLE RANGLE"""
    p[0] = nodos.Param(p[1],p[2])

def p_sentencia_comp(p):
    """sentencia_comp : LPARENT declaraciones_locales lista_sentencias RPARENT """
    p[0] = nodos.SentenciaComp(p[2], p[3])

def p_declaraciones_locales1(p):
    """declaraciones_locales : declaraciones_locales declaracion_var"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[2], list):
        p[0].extend(p[2])
    else:
        p[0].extend([p[2]])


def p_declaraciones_locales2(p):
    """declaraciones_locales : empty """
    pass

def p_lista_sentencias1(p):
    """lista_sentencias : lista_sentencias sentencia """
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[2], list):
        p[0].extend(p[2])
    else:
        p[0].extend([p[2]])

def p_lista_sentencias2(p):
    """lista_sentencias : empty """
    pass

def p_sentencia(p):
    """sentencia : sentencia_expr
                 | sentencia_comp
                 | sentencia_seleccion
                 | sentencia_iteracion
                 | sentencia_retorno"""
    p[0] = p[1]


def p_sentencia_expr1(p):
    """sentencia_expr : expresion SEMICOLON """
    p[0] = p[1]

def p_sentencia_expr2(p):
    """sentencia_expr : SEMICOLON """
    pass

def p_sentencia_seleccion1(p):
    """sentencia_seleccion : SI LSQUARE expresion RSQUARE sentencia """
    p[0] = nodos.SentenciaSeleccion(p[3],p[5], None)

def p_sentencia_seleccion2(p):
    """sentencia_seleccion : SI LSQUARE expresion RSQUARE sentencia SINO sentencia """
    p[0] = nodos.SentenciaSeleccion(p[3], p[5], p[7])


def p_sentencia_iteracion1(p):
    """sentencia_iteracion : MIENTRAS LSQUARE expresion RSQUARE sentencia """
    p[0] = nodos.SentenciaIteracion1(p[3], p[5])

def p_sentencia_iteracion2(p):
    """sentencia_iteracion : REP sentencia_comp """
    p[0] = nodos.SentenciaIteracion2(p[2])

def p_sentencia_retorno1(p):
    """sentencia_retorno : RET SEMICOLON """
    p[0] = p[1]

def p_sentencia_retorno2(p):
    """sentencia_retorno : RET expresion SEMICOLON """
    p[0] = nodos.SentenciaRetorno(p[2])

def p_expresion1(p):
    """expresion : var ASSIGN expresion """
    p[0] = nodos.Expresion(p[1], p[3])

def p_expresion2(p):
    """expresion : expresion_negada """
    p[0] = p[1];

def p_var1(p):
    """var : ID """
    p[0] = p[1]

def p_var2(p):
    """var : ID LANGLE expresion RANGLE"""
    p[0] = nodos.Var(p[1], p[3])


def p_expresion_negada1(p):
    """expresion_negada : NOT LSQUARE expresion_logica RSQUARE """
    p[0] = nodos.ExpresionNegada(p[3])

def p_expresion_negada2(p):
    """expresion_negada : expresion_logica """
    p[0] = p[1]

def p_expresion_logica1(p):
    """expresion_logica : expresion_logica AND expresion_simple """
    p[0] = nodos.ExpresionLogica(p[1], None , p[3] )

def p_expresion_logica2(p):
    """expresion_logica : expresion_logica AND NOT LSQUARE expresion_simple RSQUARE """
    p[0] = nodos.ExpresionLogica(p[1], p[3], p[5])

def p_expresion_logica3(p):
    """expresion_logica : expresion_simple """
    p[0] = p[1]

def p_expresion_logica4(p):
    """expresion_logica : NOT LSQUARE expresion_simple RSQUARE """
    p[0] = nodos.ExpresionLogica(None, p[1], p[3])

def p_expresion_simple1(p):

    """expresion_simple :  expresion_simple relop expresion_aditiva  """
    p[0] = nodos.ExpresionSimple(p[1], p[2], p[3])

def p_expresion_simple2(p):
    """expresion_simple : expresion_aditiva  """
    p[0] = p[1]

def p_relop1(p):
    """relop : LT"""
    p[0] = p[1]

def p_relop2(p):
    """relop : EQ"""
    p[0] = p[1]

def p_expresion_aditiva1(p):
    """expresion_aditiva : expresion_aditiva addop term  """
    p[0] = nodos.ExpresionAditiva(p[1], p[2], p[3])

def p_expresion_aditiva2(p):
    """expresion_aditiva : term """
    p[0] = p[1]

def p_addop1(p):
    """addop : PLUS"""
    p[0] = p[1]

def p_addop2(p):
    """addop : MINUS"""
    p[0] = p[1]

def p_term1(p):
    """term : term mulop factor"""
    p[0] = nodos.Term(p[1], p[2], p[3])

def p_term2(p):
    """term : factor"""
    p[0] = p[1]

def p_mulop1(p):
    """mulop : MULT"""
    p[0] = p[1]

def p_mulop2(p):
    """mulop : DIV"""
    p[0] = p[1]

def p_factor1(p):
    """factor : LSQUARE expresion RSQUARE """
    p[0] = p[2]

def p_factor2(p):
    """factor : var """
    p[0] = p[1]

def p_factor3(p):
    """factor : invocacion """
    p[0] = p[1]

def p_factor4(p):
    """factor : NUMBER """
    p[0] = p[1]

def p_invocacion(p):
    """invocacion : ID LSQUARE argumentos RSQUARE  """
    p[0] = nodos.Invocacion(p[1], p[3])

def p_argumentos1(p):
    """argumentos : lista_arg """
    p[0] = p[1]

def p_argumentos2(p):
    """argumentos : empty"""
    pass

def p_lista_arg1(p):
    """lista_arg : lista_arg COMMA expresion """
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[3], list):
        p[0].extend(p[3])
    else:
        p[0].extend([p[3]])

def p_lista_arg2(p):
    """lista_arg : expresion """
    p[0] = p[1]

#--------------------------------------

def p_empty(p):
    'empty :'
    pass

# Errores en la sintaxis.
def p_error(p):
    print('Error de sintaxis! ')
    if p is not None:
        print('Error en el ' + str(p.type) + '\n')
    else:
        print('El archivo de entrada esta vacío\n')


# Build the parser
fileName = str(sys.argv[1])
parser = yacc.yacc()

out = open('parser_examples/out.dot', 'w')
outErrors = open('parser_examples/errores.dot', 'w')
with open(fileName, 'r') as arch:
    contents = arch.read()
    result = parser.parse(contents)
    if result is not None:
        visitor_tipos = Visitor()
        visitor_symbols = BuildTablaSimbolosVisitor(outErrors)
        nodos.Programa.accept(result, visitor_tipos)
        out.write(visitor_tipos.ast)
        nodos.Programa.accept(result, visitor_symbols)

    else:
        out.write('Error al realizar el parse.')



