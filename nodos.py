class Nodo():
    pass


class Programa(Nodo):
    def __init__(self, lista_decl_p):
        self.lista_decl = lista_decl_p

    def accept(self, visitor):
        visitor.visit_programa(self)


class DeclaracionVar(Nodo):
    def __init__(self, def_tipo_p, ID_t, NUM_t):
        self.def_tipo_p = def_tipo_p
        self.ID_t = ID_t
        self.NUM_t = NUM_t

    def accept(self, visitor):
        visitor.visit_declaracion_var(self)


class DeclaracionFun(Nodo):
    def __init__(self, def_tipo_p, ID_t, parametros_p, sentencia_comp_p):
        self.def_tipo_p = def_tipo_p
        self.ID_t = ID_t
        self.parametros_p = parametros_p
        self.sentencia_comp_p = sentencia_comp_p

    def accept(self, visitor):
        visitor.visit_declaracion_fun(self)


class Param(Nodo):
    def __init__(self, def_tipo_p, ID_t):
        self.def_tipo_p = def_tipo_p
        self.ID_t = ID_t

    def accept(self, visitor):
        visitor.visit_param(self)


class SentenciaComp(Nodo):
    def __init__(self, declaraciones_locales_p, lista_sentencias_p):
        self.declaraciones_locales_p = declaraciones_locales_p
        self.lista_sentencias_p = lista_sentencias_p

    def accept(self, visitor):
        visitor.visit_sentencia_comp(self)

class SentenciaSeleccion(Nodo):
    def __init__(self, expresion_p, sentencia_p, sentencia2_p):
        self.expresion_p = expresion_p
        self.sentencia_p = sentencia_p
        self.sentencia2_p = sentencia2_p

    def accept(self, visitor):
        visitor.visit_sentencia_seleccion(self)


class SentenciaIteracion1(Nodo):
    def __init__(self, expresion_p, sentencia_p):
        self.expresion_p = expresion_p
        self.sentencia_p = sentencia_p

    def accept(self, visitor):
        visitor.visit_sentencia_iteracion1(self)


class SentenciaIteracion2(Nodo):
    def __init__(self, sentencia_comp_p):
        self.sentencia_comp_p = sentencia_comp_p

    def accept(self, visitor):
        visitor.visit_sentencia_iteracion2(self)


class SentenciaRetorno(Nodo):
    def __init__(self, expresion_p):
        self.expresion_p = expresion_p

    def accept(self, visitor):
        visitor.visit_sentencia_retorno(self)


class Var(Nodo):
    def __init__(self, ID_t, expresion_p):
        self.ID_t = ID_t
        self.expresion_p = expresion_p

    def accept(self, visitor):
        visitor.visit_var(self)


class Expresion(Nodo):
    def __init__(self, var_p, expresion_p):
        self.var_p = var_p
        self.expresion_p = expresion_p

    def accept(self, visitor):
        visitor.visit_expresion(self)


class ExpresionNegada(Nodo):
    def __init__(self, expresion_logica_p, ):
        self.expresion_logica_p = expresion_logica_p

    def accept(self, visitor):
        visitor.visit_expresion_negada(self)


class ExpresionLogica(Nodo):
    def __init__(self, expresion_logica_p, NOT_t, expresion_simple_p):
        self.expresion_logica_p = expresion_logica_p
        self.NOT_t = NOT_t
        self.expresion_simple_p = expresion_simple_p

    def accept(self, visitor):
        visitor.visit_expresion_logica(self)


class ExpresionAditiva(Nodo):
    def __init__(self, expresion_aditiva_p, addop_t, term_p):
        self.expresion_aditiva_p = expresion_aditiva_p
        self.addop_t = addop_t
        self.term_p = term_p

    def accept(self, visitor):
        visitor.visit_expresion_aditiva(self)


class Term(Nodo):
    def __init__(self, term_p, mulop_t, factor_p):
        self.term_p = term_p
        self.mulop_t = mulop_t
        self.factor_p = factor_p

    def accept(self, visitor):
        visitor.visit_term(self)


class ExpresionSimple(Nodo):
    def __init__(self, expresion_simple_p, relop_t, expresion_aditiva_p):
        self.expresion_simple_p = expresion_simple_p
        self.relop_t = relop_t
        self.expresion_aditiva_p = expresion_aditiva_p

    def accept(self, visitor):
        visitor.visit_expresion_simple(self)


class ExpresionAditiva(Nodo):
    def __init__(self, expresion_aditiva_p, addop_t, term_p):
        self.expresion_aditiva_p = expresion_aditiva_p
        self.addop_t = addop_t
        self.term_p = term_p

    def accept(self, visitor):
        visitor.visit_expresion_aditiva(self)


class Invocacion(Nodo):
    def __init__(self, ID_t, argumentos_p):
        self.ID_t = ID_t
        self.argumentos_p = argumentos_p

    def accept(self, visitor):
        visitor.visit_invocacion(self)

# ----------------------------------------------
