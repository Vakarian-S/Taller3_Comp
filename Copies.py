
def p_expression_stmt1(p):
    """expression_stmt : expression PUNTOC"""
    p[0] = p[1]

def p_expression_stmt2(p):
    """expression_stmt : PUNTOC"""
    pass

def p_expression1(p):
    """expression : NUM ASIGN expression"""
    p[0] = nodos.Expression(p[1], p[3])

def p_expression2(p):
    """expression : simple_expression"""
    p[0] = p[1]

def p_simple_expression1(p):
    """simple_expression : additive_expression relop additive_expression"""
    p[0] = nodos.SimpleExpression(p[1], p[2], p[3])

def p_simple_expression2(p):
    """simple_expression : additive_expression"""
    p[0] = p[1]

def p_relop1(p):
    """relop : MENORI"""
    p[0] = p[1]

def p_relop2(p):
    """relop : MENOR"""
    p[0] = p[1]

def p_relop3(p):
    """relop : MAYOR"""
    p[0] = p[1]

def p_relop4(p):
    """relop : MAYORI"""
    p[0] = p[1]

def p_relop5(p):
    """relop : IGUAL"""
    p[0] = p[1]

def p_relop6(p):
    """relop : DIST"""
    p[0] = p[1]

def p_additive_expression1(p):
    """additive_expression : additive_expression addop term"""
    p[0] = nodos.AdditiveExpression(p[1], p[2], p[3])

def p_additive_expression2(p):
    """additive_expression : term"""
    p[0] = p[1]

def p_addop1(p):
    """addop : SUMA"""
    p[0] = p[1]

def p_addop2(p):
    """addop : RESTA"""
    p[0] = p[1]

def p_term1(p):
    """term : term mulop factor"""
    p[0] = nodos.Term(p[1], p[2], p[3])

def p_term2(p):
    """term : factor"""
    p[0] = p[1]

def p_mulop1(p):
    """mulop : MULTI"""
    p[0] = p[1]

def p_mulop2(p):
    """mulop : DIVI"""
    p[0] = p[1]

def p_factor1(p):
    """factor : IPAREN expression DPAREN"""
    p[0] = p[2]

def p_factor2(p):
    """factor : NUM"""
    p[0] = nodos.Num(p[1])
