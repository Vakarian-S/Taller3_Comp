class Visitor(object):
    def __init__(self):
        self.ast = ''
        self.id_programa = 0
        self.id_declaracion_var = 0
        self.id_declaracion_fun = 0
        self.id_parametros = 0
        self.id_sentencia_comp = 0
        self.id_sentencia_expr = 0
        self.id_sentencia_seleccion = 0
        self.id_sentencia_iteracion = 0
        self.id_sentencia_retorno = 0
        self.id_expresion = 0;
        self.id_var = 0
        self.id_expresion_negada = 0
        self.id_expresion_logica = 0
        self.id_expresion_simple = 0
        self.id_expresion_aditiva = 0
        self.id_term = 0
        self.id_invocacion = 0
        self.id_terminales = 0;

    def visit_programa(self, programa):
        self.id_programa += 1
        id_programa = self.id_programa
        if programa.lista_decl is not None:
            if isinstance(programa.lista_decl, list):
                aux = programa.lista_decl
            else:
                aux = [programa.lista_decl]
            for stmt in aux:
                if stmt is not None:
                    self.ast += '\t"lista-decl ' + str(id_programa) + '" '
                    stmt.accept(self)
        self.ast = 'digraph G {\n' + self.ast + '}'

    def visit_declaracion_var(self, declaracion_var):
        self.id_declaracion_var += 1
        id_declaracion_var = self.id_declaracion_var
        self.ast += '-> "Declaracion-var ' + str(id_declaracion_var) + '"' + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + declaracion_var.def_tipo_p + '"]\n'
        self.ast += '\t"Declaracion-var ' + str(id_declaracion_var) + '" -> ' + str(self.id_terminales) + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + declaracion_var.ID_t + '"]\n'
        self.ast += '\t"Declaracion-var ' + str(id_declaracion_var) + '" -> ' + str(self.id_terminales) + '\n'
        if declaracion_var.NUM_t is not None:
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + declaracion_var.NUM_t + '"]\n'
            self.ast += '\t"Declaracion-var ' + str(id_declaracion_var) + '" -> ' + str(self.id_terminales) + '\n'

    def visit_declaracion_fun(self, declaracion_fun):
        self.id_declaracion_fun += 1
        id_declaracion_fun = self.id_declaracion_fun
        self.ast += '-> "Declaracion-fun ' + str(id_declaracion_fun) + '"' + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + declaracion_fun.def_tipo_p + '"]\n'
        self.ast += '\t"Declaracion-fun ' + str(id_declaracion_fun) + '" -> ' + str(self.id_terminales) + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + declaracion_fun.ID_t + '"]\n'
        self.ast += '\t"Declaracion-fun ' + str(id_declaracion_fun) + '" -> ' + str(self.id_terminales) + '\n'
        if isinstance(declaracion_fun.parametros_p, list):
            for stmt in declaracion_fun.parametros_p:
                if stmt is not None:
                    self.ast += '\t"Declaracion-fun ' + str(id_declaracion_fun) + '" '
                    stmt.accept(self)
        else:
            if isinstance(declaracion_fun.parametros_p,str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + declaracion_fun.parametros_p + '"]\n'
                self.ast += '\t"Declaracion-fun ' + str(id_declaracion_fun) + '" -> ' + str(self.id_terminales) + '\n'
            else:
                self.ast += '\t"Declaracion-fun ' + str(id_declaracion_fun) + '" '
                declaracion_fun.parametros_p.accept(self)
        # Revisar si sentencia comp es nulo, o si es simpelmente parentesis vacios
        if declaracion_fun.sentencia_comp_p is not None:
            if not (declaracion_fun.sentencia_comp_p.declaraciones_locales_p is None
                    and declaracion_fun.sentencia_comp_p.lista_sentencias_p is None):
                self.ast += '\t"Declaracion-fun ' + str(id_declaracion_fun) + '" '
                declaracion_fun.sentencia_comp_p.accept(self)


    def visit_param(self, param):
        self.id_parametros += 1
        id_parametros = self.id_parametros
        self.ast += '-> "Parametros ' + str(id_parametros) + '"' + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + param.def_tipo_p + '"]\n'
        self.ast += '\t"Parametros ' + str(id_parametros) + '" -> ' + str(self.id_terminales) + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + param.ID_t + '"]\n'
        self.ast += '\t"Parametros ' + str(id_parametros) + '" -> ' + str(self.id_terminales) + '\n'

    def visit_sentencia_comp(self, sentencia_comp):
        self.id_sentencia_comp += 1
        id_sentencia_comp = self.id_sentencia_comp
        self.ast += '-> "Sentencia-comp ' + str(id_sentencia_comp) + '"' + '\n'

        if sentencia_comp.declaraciones_locales_p is not None:
            if isinstance(sentencia_comp.declaraciones_locales_p, list):
                for stmt in sentencia_comp.declaraciones_locales_p:
                    if stmt is not None:
                        self.ast += '\t"Sentencia-comp ' + str(id_sentencia_comp) + '" '
                        stmt.accept(self)
            else:
                self.ast += '\t"Sentencia-comp ' + str(id_sentencia_comp) + '" '
                sentencia_comp.declaraciones_locales_p.accept(self)

        if sentencia_comp.lista_sentencias_p is not None:
            if isinstance(sentencia_comp.lista_sentencias_p, list):
                for stmt in sentencia_comp.lista_sentencias_p:
                    if stmt is not None:
                        if isinstance(stmt,str):
                            self.id_terminales += 1
                            self.ast += '\t' + str(
                                self.id_terminales) + ' [label="' + str(stmt) + '"]\n'
                            self.ast += '\t"Sentencia-comp ' + str(id_sentencia_comp) + '" -> ' + str(
                                self.id_terminales) + '\n'
                        else:
                            self.ast += '\t"Sentencia-comp ' + str(id_sentencia_comp) + '" '
                            stmt.accept(self)
            else:
                self.ast += '\t"Sentencia-comp ' + str(id_sentencia_comp) + '" '
                sentencia_comp.lista_sentencias_p.accept(self)

    def visit_sentencia_expr(self, sentencia_expr):
        self.id_sentencia_expr += 1
        id_sentencia_expr = self.id_sentencia_expr
        self.ast += '-> "Sentencia-expr ' + str(id_sentencia_expr) + '"' + '\n'
        if sentencia_expr.expresion_p is not None:
            if isinstance(sentencia_expr.expresion_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + sentencia_expr.expresion_p + '"]\n'
                self.ast += '\t"Sentencia-expr ' + str(id_sentencia_expr) + '" -> ' + str(self.id_terminales) + '\n'
            else:
                self.ast += '\t"Sentencia-expr ' + str(id_sentencia_expr) + '" '
                sentencia_expr.expresion_p.accept(self)

    def visit_sentencia_seleccion(self, sentencia_seleccion):
        self.id_sentencia_seleccion += 1
        id_sentencia_seleccion = self.id_sentencia_seleccion
        if sentencia_seleccion.sentencia2_p is not None:
            self.ast += '-> "Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO"' + '\n'
            if isinstance(sentencia_seleccion.expresion_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(
                    self.id_terminales) + ' [label="' + str(sentencia_seleccion.expresion_p) + '"]\n'
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO" -> ' + str(
                    self.id_terminales) + '\n'
            else:
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO" '
                sentencia_seleccion.expresion_p.accept(self)
            if isinstance(sentencia_seleccion.sentencia_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(
                    self.id_terminales) + ' [label="' + str(sentencia_seleccion.sentencia_p) + '"]\n'
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO" -> ' + str(
                    self.id_terminales) + '\n'
            else:
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO" '
                sentencia_seleccion.sentencia_p.accept(self)
            if isinstance(sentencia_seleccion.sentencia2_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(
                    self.id_terminales) + ' [label="' + str(sentencia_seleccion.sentencia2_p) + '"]\n'
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO" -> ' + str(
                    self.id_terminales) + '\n'
            else:
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI SINO" '
                sentencia_seleccion.sentencia2_p.accept(self)
        else:
            self.ast += '-> "Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI"' + '\n'
            if isinstance(sentencia_seleccion.expresion_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(
                    self.id_terminales) + ' [label="' + str(sentencia_seleccion.expresion_p) + '"]\n'
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI" -> ' + str(
                    self.id_terminales) + '\n'
            else:
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI" '
                sentencia_seleccion.expresion_p.accept(self)
            if isinstance(sentencia_seleccion.sentencia_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(
                    self.id_terminales) + ' [label="' + str(sentencia_seleccion.sentencia_p) + '"]\n'
                self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI" -> ' + str(
                    self.id_terminales) + '\n'
            else:
                if sentencia_seleccion.sentencia_p is not None:
                    self.ast += '\t"Sentencia-seleccion ' + str(id_sentencia_seleccion) + ': SI" '
                    sentencia_seleccion.sentencia_p.accept(self)


    def visit_sentencia_iteracion1(self, sentencia_iteracion):
        self.id_sentencia_iteracion += 1
        id_sentencia_iteracion = self.id_sentencia_iteracion
        self.ast += '-> "Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': MIENTRAS" ' + '\n'
        if sentencia_iteracion.expresion_p is not None:
            self.ast += '\t"Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': MIENTRAS" '
            sentencia_iteracion.expresion_p.accept(self)
        if sentencia_iteracion.sentencia_p is not None:
            self.ast += '\t"Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': MIENTRAS" '
            sentencia_iteracion.sentencia_p.accept(self)

    def visit_sentencia_iteracion2(self, sentencia_iteracion):
        self.id_sentencia_iteracion += 1
        id_sentencia_iteracion = self.id_sentencia_iteracion
        self.ast += '-> "Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': REP"' + '\n'
        if sentencia_iteracion.sentencia_comp_p is not None:
            self.ast += '\t"Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': REP" '
            sentencia_iteracion.sentencia_comp_p.accept(self)

    def visit_sentencia_retorno(self, sentencia_retorno):
        self.id_sentencia_retorno += 1
        id_sentencia_retorno = self.id_sentencia_retorno
        self.ast += '-> "Sentencia-retorno ' + str(id_sentencia_retorno) + ': RET"' + '\n'
        if sentencia_retorno.expresion_p is not None:
            if isinstance(sentencia_retorno.expresion_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + sentencia_retorno.expresion_p + '"]\n'
                self.ast += '\t"Sentencia-retorno ' + str(id_sentencia_retorno) + ': RET" -> ' + str(self.id_terminales) + '\n'
            else:
                self.ast += '\t"Sentencia-retorno ' + str(id_sentencia_retorno) + ': RET" '
                sentencia_retorno.expresion_p.accept(self)


    def visit_expresion(self, expresion):
        self.id_expresion += 1
        id_expresion = self.id_expresion
        self.ast += '-> "Expresion ' + str(id_expresion) + ': ="' + '\n'
        if expresion.var_p is not None:
            if isinstance(expresion.var_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + expresion.var_p + '"]\n'
                self.ast += '\t"Expresion ' + str(id_expresion) + ': =" -> ' + str(self.id_terminales) + '\n'
            else:
                if expresion.var_p.expresion_p is None:
                    self.id_terminales += 1
                    self.ast += '\t' + str(self.id_terminales) + ' [label="' + expresion.var_p.ID_t + '"]\n'
                    self.ast += '\t"Expresion ' + str(id_expresion) + ': =" -> ' + str(self.id_terminales) + '\n'
                else:
                    self.ast += '\t"Expresion ' + str(id_expresion) + ': =" '
                    expresion.var_p.accept(self)

        if isinstance(expresion.expresion_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + expresion.expresion_p + '"]\n'
            self.ast += '\t"Expresion ' + str(id_expresion) + ': =" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Expresion ' + str(id_expresion) + ': =" '
            expresion.expresion_p.accept(self)

    def visit_var(self, var):
        self.id_var += 1
        id_var = self.id_var
        self.ast += '-> "Var ' + str(id_var) + ': ="'  '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + var.ID_t + '"]\n'
        self.ast += '\t"Var ' + str(id_var) + ': =" -> ' + str(self.id_terminales) + '\n'
        if isinstance(var.expresion_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + var.expresion_p + '"]\n'
            self.ast += '\t"Var ' + str(id_var) + ': =" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Var ' + str(id_var) + ': =" '
            var.expresion_p.accept(self)


    def visit_expresion_negada(self, expresion_negada):
        self.id_expresion_negada += 1
        id_expresion_negada = self.id_expresion_negada
        self.ast += '-> "Expresion-negada ' + str(id_expresion_negada) + ': !"'  '\n'
        self.ast += '\t"Expresion-negada ' + str(id_expresion_negada) + ': !" '
        expresion_negada.expresion_logica_p.accept(self)

    def visit_expresion_logica(self, expresion_logica):
        self.id_expresion_logica += 1
        id_expresion_logica = self.id_expresion_logica
        if expresion_logica.expresion_logica_p is not None:
            if expresion_logica.NOT_t is not None:
                signos = ': && !"'
            else:
                signos = ': &&"'
            self.ast += '-> "Expresion-logica ' + str(id_expresion_logica) + signos + '\n'
            if isinstance(expresion_logica.expresion_logica_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + expresion_logica.expresion_logica_p + '"]\n'
                self.ast += '\t"Expresion-logica ' + str(id_expresion_logica) + \
                            signos + ' -> ' + str(self.id_terminales) + '\n'
            else:
                self.ast += '\t"Expresion-logica ' + str(id_expresion_logica) + signos
                expresion_logica.expresion_logica_p.accept(self)
            if isinstance(expresion_logica.expresion_simple_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + expresion_logica.expresion_simple_p + '"]\n'
                self.ast += '\t"Expresion-logica ' + str(id_expresion_logica) + \
                            signos + ' -> ' + str(self.id_terminales) + '\n'
            else:
                self.ast += '\t"Expresion-logica ' + str(id_expresion_logica) + signos
                expresion_logica.expresion_simple_p.accept(self)
        else:
            self.ast += '-> "Expresion-logica ' + str(id_expresion_logica) + ': !"'  '\n'
            if isinstance(expresion_logica.expresion_simple_p, str):
                self.id_terminales += 1
                self.ast += '\t' + str(self.id_terminales) + ' [label="' + expresion_logica.expresion_simple_p + '"]\n'
                self.ast += '\t"Expresion-logica ' + str(id_expresion_logica) + \
                            ': !" -> ' + str(self.id_terminales) + '\n'
            else:
                self.ast += '\t"Expresion-logica ' + str(id_expresion_logica) + ': !"'
                expresion_logica.expresion_simple_p.accept(self)


    def visit_expresion_simple(self, expresion_simple):
        self.id_expresion_simple += 1
        id_expresion_simple = self.id_expresion_simple
        self.ast += '-> "Expresion-simple ' + str(id_expresion_simple) + ': ' + str(expresion_simple.relop_t) +\
                    '"' + '\n'
        if isinstance(expresion_simple.expresion_simple_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(expresion_simple.expresion_simple_p) \
                        + '"]\n'
            self.ast += '\t"Expresion-simple ' + str(id_expresion_simple) + ': ' + str(expresion_simple.relop_t) + \
                        '" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Expresion-simple ' + str(id_expresion_simple) + ': ' + str(expresion_simple.relop_t) + '" '
            expresion_simple.expresion_simple_p.accept(self)

        if isinstance(expresion_simple.expresion_aditiva_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(expresion_simple.expresion_aditiva_p) \
                        + '"]\n'
            self.ast += '\t"Expresion-simple ' + str(id_expresion_simple) + ': ' + str(expresion_simple.relop_t) + \
                        '" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Expresion-simple ' + str(id_expresion_simple) + ': ' + str(expresion_simple.relop_t) + '" '
            expresion_simple.expresion_aditiva_p.accept(self)

    def visit_expresion_aditiva(self, expresion_aditiva):
        self.id_expresion_aditiva += 1
        id_expresion_aditiva = self.id_expresion_aditiva
        self.ast += '-> "Expresion-aditiva ' + str(id_expresion_aditiva) + ': '+ str(expresion_aditiva.addop_t) +\
                    '"' + '\n'
        if isinstance(expresion_aditiva.expresion_aditiva_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(expresion_aditiva.expresion_aditiva_p)\
                        + '"]\n'
            self.ast += '\t"Expresion-aditiva ' + str(id_expresion_aditiva) + ': ' + str(expresion_aditiva.addop_t) +\
                        '" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Expresion-aditiva ' + str(id_expresion_aditiva) + ': '+ str(expresion_aditiva.addop_t)\
            + '" '
            expresion_aditiva.expresion_aditiva_p.accept(self)

        if isinstance(expresion_aditiva.term_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(expresion_aditiva.term_p)\
                        + '"]\n'
            self.ast += '\t"Expresion-aditiva ' + str(id_expresion_aditiva) + ': ' + str(expresion_aditiva.addop_t) +\
                        '" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Expresion-aditiva ' + str(id_expresion_aditiva) + ': '+ str(expresion_aditiva.addop_t)\
            + '" '
            expresion_aditiva.term_p.accept(self)

    def visit_term(self, term):
        self.id_term += 1
        id_term = self.id_term
        self.ast += '-> "Term ' + str(id_term) + ': ' + str(term.mulop_t) + '"' + '\n'
        if isinstance(term.term_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(term.term_p) + '"]\n'
            self.ast += '\t"Term ' + str(id_term) + ': ' + str(term.mulop_t) + '" -> ' + str(self.id_terminales) + '\n'
        else:
            self.ast += '\t"Term ' + str(id_term) + ': ' + str(term.mulop_t) + '"'
            term.term_p.accept(self)
        if isinstance(term.factor_p, str):
            self.id_terminales += 1
            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(term.factor_p) + '"]\n'
            self.ast += '\t"Term ' + str(id_term) + ': ' + str(term.mulop_t) + '" -> ' + str(self.id_terminales) + '\n'
        else:
            term.factor_p.accept(self)

    def visit_invocacion(self, invocacion):
        self.id_invocacion += 1
        id_invocacion = self.id_invocacion
        self.ast += '-> "Invocacion ' + str(id_invocacion) + '"' + '\n'
        self.id_terminales += 1
        self.ast += '\t' + str(self.id_terminales) + ' [label="' + invocacion.ID_t + '"]\n'
        self.ast += '\t"Invocacion ' + str(id_invocacion) + '" -> ' + str(self.id_terminales) + '\n'
        if invocacion.argumentos_p is not None:
            if isinstance(invocacion.argumentos_p, list):
                for stmt in invocacion.argumentos_p:
                    if stmt is not None:
                        if isinstance(stmt, str):
                            self.id_terminales += 1
                            self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(stmt) + '"]\n'
                            self.ast += '\t"Invocacion ' + str(id_invocacion) + '" -> ' + str(self.id_terminales) + '\n'
                        else:
                            self.ast += '\t"Invocacion ' + str(id_invocacion) + '" '
                            stmt.accept(self)
            else:
                if isinstance(invocacion.argumentos_p, str):
                    self.id_terminales += 1
                    self.ast += '\t' + str(self.id_terminales) + ' [label="' + str(invocacion.argumentos_p) + '"]\n'
                    self.ast += '\t"Invocacion ' + str(id_invocacion) + '" -> ' + str(self.id_terminales) + '\n'
                else:
                    self.ast += '\t"Invocacion ' + str(id_invocacion) + '" '
                    invocacion.argumentos_p.accept(self)

