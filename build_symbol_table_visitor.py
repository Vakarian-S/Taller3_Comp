# coding=utf-8
#from string import lower

from nodos import *
#from symbol_table.nodo_funcion import NodoFuncion
from symbol_table import NodoSymbolTable
#from symbol_table.nodo_variable import NodoVariable
from symbol_table import ScopedSymbolTable
from symbols import VarSymbol, ProcedureSymbol
import re


class BuildTablaSimbolosVisitor(object):
    def __init__(self, archivo):
        # La tabla de simbolos.
        self.tabla_simbolos = ScopedSymbolTable(scope_name='global', scope_level=1)
        # Lista de las funciones.
        self.funciones = []
        # Nodo que se encuentra siendo modificado, se va cambiando cuando se crea otro.
        self.nodo = NodoSymbolTable()
        self.errors_tabla_simbolos = archivo
        self.current_scope = None

    def visit_programa(self, programa):
        print('ENTER scope: global')
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope,  # None
        )
        global_scope._init_builtins()
        self.current_scope = global_scope


        #--------- Creacion input e output base----------

        proc_input = 'input'
        input_type_name = 'ENT'
        input_type_symbol = self.current_scope.lookup(input_type_name)
        proc_input_symbol = ProcedureSymbol(proc_input, type=input_type_symbol);
        proc_input_symbol.params = 'VACUO'
        self.current_scope.insert(proc_input_symbol)
        
        proc_output = 'output'
        output_type_name = 'VACUO'
        output_type_symbol = self.current_scope.lookup(output_type_name)
        proc_output_symbol = ProcedureSymbol(proc_output, type=output_type_symbol);
        param_type = self.current_scope.lookup('ENT')
        param_name = 'x'
        var_symbol = VarSymbol(param_name, param_type)
        proc_output_symbol.params.append(var_symbol)
        self.current_scope.insert(proc_output_symbol)

        # Crear el nodo raiz y agregarlo.
        self.nodo = NodoSymbolTable()
        self.tabla_simbolos.root = self.nodo
        # Expanir el arbol para seguir el analisis.
        if programa.lista_decl is not None:
            if isinstance(programa.lista_decl, list):
                aux = programa.lista_decl
            else:
                aux = [programa.lista_decl]
            for stmt in aux:
                if stmt is not None:
                    stmt.accept(self)

        print(global_scope)

        self.current_scope = self.current_scope.enclosing_scope
        print('LEAVE scope: global')

    def visit_declaracion_var(self, declaracion_var):
        type_name = declaracion_var.def_tipo_p
        type_symbol = self.current_scope.lookup(type_name)
        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = declaracion_var.ID_t
        var_symbol = VarSymbol(var_name, type_symbol)
        # Signal an error if the table alrady has a symbol
        # with the same name
        error_var = self.current_scope.lookup(var_name, current_scope_only=True)
        if error_var:
            self.errors_tabla_simbolos.write('error en declaracion de variable: '
             + str(type_name) +' ' + str(var_name) + ', ya fue declarada anteriormente'+'\n')
        else:
            self.current_scope.insert(var_symbol)

        #error_var = self.current_scope.lookup(declaracion_var.ID_t);
        #if error_var is None:
            # Añadir la declaracion al nodo de la tabla de simbolos.
            #var_symbol = VarSymbol(var_name, type_symbol)
            #self.current_scope.insert(var_symbol)
        #else:
            # Indicar el error.
            #self.errors_tabla_simbolos.write('error en declaracion de variable: '
                                             #+ str(type_name) +' ' + str(var_name) + ', ya fue declarada anteriormente como: '
                                             #+ str(error_var) + '\n')

    def visit_declaracion_fun(self, declaracion_fun):
        proc_name = declaracion_fun.ID_t
        type_name = declaracion_fun.def_tipo_p
        type_symbol = self.current_scope.lookup(type_name)
        error_var_nombre = self.current_scope.lookup(proc_name,current_scope_only=True)
        if error_var_nombre:
            # - Caso especial parametro VACUO --#
            if isinstance(declaracion_fun.parametros_p,str):
                for funcion in error_var_nombre:
                    if funcion.params == 'VACUO':
                        self.errors_tabla_simbolos.write('error en declaracion de funcion: '
                                            + str(proc_name) + ', ya fue declarada anteriormente' + '\n')
            else:
                # ------------ Crear una lista con los parametros a usar --------
                tipos_params = []
                if declaracion_fun.parametros_p is not None:
                    if isinstance(declaracion_fun.parametros_p, list):
                        params = declaracion_fun.parametros_p
                    else:
                        params = [declaracion_fun.parametros_p]
                    for param in params:
                        if param is not None:
                            tipos_params.append(param.def_tipo_p)

                # -- Revisar cada parametro
                for funcion in error_var_nombre:

                    # ------------ Checkear si es una sobrecarga o un duplicado -------

                    # -- Checkeo por cantidad de parametros
                    if (len(funcion.params) == len(tipos_params)):
                        # -- Checkeo por tipos de parametro
                        match = True
                        for tipo in range(len(funcion.params)):
                            if str(funcion.params[tipo].type) != tipos_params[tipo]:
                                match = False
                                break
                        if match == True:
                            self.errors_tabla_simbolos.write('error en declaracion de funcion: '
                                                             + str(proc_name) + ', ya fue declarada anteriormente' + '\n')

        proc_symbol = ProcedureSymbol(proc_name, type=type_symbol)
        self.current_scope.append(proc_symbol)

        print('ENTER scope: %s' % proc_name)
        # Scope for parameters and local variables
        procedure_scope = ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope

        if declaracion_fun.parametros_p is not None:
            if isinstance(declaracion_fun.parametros_p, str):
                proc_symbol.params = 'VACUO'
            else:
                if isinstance(declaracion_fun.parametros_p, list):
                    params = declaracion_fun.parametros_p
                else:
                    params = [declaracion_fun.parametros_p]
                for param in params:
                    if param is not None:
                        param_type = self.current_scope.lookup(param.def_tipo_p)
                        param_name = param.ID_t
                        var_symbol = VarSymbol(param_name, param_type)
                        error_symbol = self.current_scope.lookup(name=param_name,current_scope_only=True)
                        if error_symbol:
                            self.errors_tabla_simbolos.write('error en declaracion de parametros: '
                                                             + str(param_type) +  ' ' + str(param_name)
                            + ', ya fue declarado anteriormente' + '\n')
                        else:
                            self.current_scope.insert(var_symbol)
                            proc_symbol.params.append(var_symbol)


        declaracion_fun.sentencia_comp_p.accept(self)

        print(procedure_scope)

        self.current_scope = self.current_scope.enclosing_scope
        print('LEAVE scope: %s' % proc_name)

    def visit_sentencia_comp(self, sentencia_comp):

        if sentencia_comp.declaraciones_locales_p is not None:
            if isinstance(sentencia_comp.declaraciones_locales_p, list):
                aux = sentencia_comp.declaraciones_locales_p
            else:
                aux = [sentencia_comp.declaraciones_locales_p]
            for dclr in aux:
                if dclr is not None:
                    dclr.accept(self)

        if sentencia_comp.lista_sentencias_p is not None:
            if isinstance(sentencia_comp.lista_sentencias_p, list):
                aux = sentencia_comp.lista_sentencias_p
            else:
                aux = [sentencia_comp.lista_sentencias_p]
            for stmt in aux:
                if stmt is not None:
                    if isinstance(stmt, str):
                        # --- Un string o es un numero, RET, o un id
                        numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                        retRegex = re.compile(r'(?i:ret)')
                        if not (numRegex.match(stmt) or retRegex.match(stmt)):
                            var_name = stmt
                            var_symbol = self.current_scope.lookup(var_name)
                            if var_symbol is None:
                                self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                                 + str(var_name) +
                                                             ', la variable no ha sido declarada' + '\n')
                    else:
                        stmt.accept(self)


    def visit_sentencia_expr(self, sentencia_expr):
        if sentencia_expr.expresion_p is not None:
            if isinstance(sentencia_expr.expresion_p, str):
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                if not (numRegex.match(sentencia_expr.expresion_p)):
                    var_name2 = sentencia_expr.expresion_p
                    var_symbol2 = self.current_scope.lookup(var_name2)
                    if var_symbol2 is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name2) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                sentencia_expr.expresion_p.accept(self)


    def visit_expresion(self, expresion):
        if expresion.var_p is not None:
            if isinstance(expresion.var_p, str):
                var_name = expresion.var_p
            else:
                var_name = expresion.var_p.ID_t
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.errors_tabla_simbolos.write('error en llamado a variable: '
                                             + str(var_name) +
                                             ', la variable no ha sido declarada' + '\n')
        if isinstance(expresion.expresion_p, str):
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(expresion.expresion_p)):
                var_name2 = expresion.expresion_p
                var_symbol2 = self.current_scope.lookup(var_name2)
                if var_symbol2 is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                 + str(var_name2) +
                                                 ', la variable no ha sido declarada' + '\n')
        else:
            expresion.expresion_p.accept(self)

    def visit_expresion_aditiva(self, expresion_aditiva):
        if isinstance(expresion_aditiva.expresion_aditiva_p, str):
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(expresion_aditiva.expresion_aditiva_p)):
                var_name2 = expresion_aditiva.expresion_aditiva_p
                var_symbol2 = self.current_scope.lookup(var_name2)
                if var_symbol2 is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name2) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            expresion_aditiva.expresion_aditiva_p.accept(self)

        if isinstance(expresion_aditiva.term_p, str):
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(expresion_aditiva.term_p)):
                var_name2 = expresion_aditiva.term_p
                var_symbol2 = self.current_scope.lookup(var_name2)
                if var_symbol2 is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name2) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            expresion_aditiva.term_p.accept(self)



    def visit_sentencia_seleccion(self, sentencia_seleccion):
        if isinstance(sentencia_seleccion.expresion_p, str):
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(sentencia_seleccion.expresion_p)):
                var_name2 = sentencia_seleccion.expresion_p
                var_symbol2 = self.current_scope.lookup(var_name2)
                if var_symbol2 is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name2) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            sentencia_seleccion.expresion_p.accept(self)

        if isinstance(sentencia_seleccion.sentencia_p, str):
            # --- Un string o es un numero, RET, o un id
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            retRegex = re.compile(r'(?i:ret)')
            if not (numRegex.match(sentencia_seleccion.sentencia_p) or retRegex.match(sentencia_seleccion.sentencia_p)):
                var_name = sentencia_seleccion.sentencia_p
                var_symbol = self.current_scope.lookup(var_name)
                if var_symbol is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            sentencia_seleccion.sentencia_p.accept(self)

        if sentencia_seleccion.sentencia2_p is not None:
            if isinstance(sentencia_seleccion.sentencia2_p, str):
                # --- Un string o es un numero, RET, o un id
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                retRegex = re.compile(r'(?i:ret)')
                if not (numRegex.match(sentencia_seleccion.sentencia2_p) or retRegex.match(
                        sentencia_seleccion.sentencia2_p)):
                    var_name = sentencia_seleccion.sentencia2_p
                    var_symbol = self.current_scope.lookup(var_name)
                    if var_symbol is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                sentencia_seleccion.sentencia2_p.accept(self)

    def visit_sentencia_iteracion1(self, sentencia_iteracion):
        if sentencia_iteracion.expresion_p is not None:
            if isinstance(sentencia_iteracion.expresion_p, str):
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                if not (numRegex.match(sentencia_iteracion.expresion_p)):
                    var_name2 = sentencia_iteracion.expresion_p
                    var_symbol2 = self.current_scope.lookup(var_name2)
                    if var_symbol2 is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name2) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                sentencia_iteracion.expresion_p.accept(self)

        if sentencia_iteracion.sentencia_p is not None:
            if isinstance(sentencia_iteracion.sentencia_p, str):
                # --- Un string o es un numero, RET, o un id
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                retRegex = re.compile(r'(?i:ret)')
                if not (numRegex.match(sentencia_iteracion.sentencia_p) or retRegex.match(
                        sentencia_iteracion.sentencia_p)):
                    var_name = sentencia_iteracion.sentencia_p
                    var_symbol = self.current_scope.lookup(var_name)
                    if var_symbol is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                sentencia_iteracion.sentencia_p.accept(self)

    def visit_sentencia_iteracion2(self, sentencia_iteracion):
        if sentencia_iteracion.sentencia_comp_p is not None:
            sentencia_iteracion.sentencia_comp_p.accept(self)


    def visit_sentencia_retorno(self, sentencia_retorno):
        if sentencia_retorno.expresion_p is not None:
            if isinstance(sentencia_retorno.expresion_p, str):
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                if not (numRegex.match(sentencia_retorno.expresion_p)):
                    var_name2 = sentencia_retorno.expresion_p
                    var_symbol2 = self.current_scope.lookup(var_name2)
                    if var_symbol2 is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name2) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                sentencia_retorno.expresion_p.accept(self)


    def visit_expresion_negada(self, expresion_negada):
        print('here')
        if isinstance(expresion_negada.expresion_logica_p, str):
            print('here2')
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(expresion_negada.expresion_logica_p)):
                var_name2 = expresion_negada.expresion_logica_p
                var_symbol2 = self.current_scope.lookup(var_name2)
                if var_symbol2 is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name2) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            expresion_negada.expresion_logica_p.accept(self)

    def visit_expresion_logica(self, expresion_logica):
        if expresion_logica.expresion_logica_p is not None:
            if isinstance(expresion_logica.expresion_logica_p, str):
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                if not (numRegex.match(expresion_logica.expresion_logica_p)):
                    var_name = expresion_logica.expresion_logica_p
                    var_symbol = self.current_scope.lookup(var_name)
                    if var_symbol is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                expresion_logica.expresion_logica_p.accept(self)

        if expresion_logica.expresion_simple_p is not None:
            if isinstance(expresion_logica.expresion_simple_p, str):
                numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
                if not (numRegex.match(expresion_logica.expresion_simple_p)):

                    var_name = expresion_logica.expresion_simple_p
                    var_symbol = self.current_scope.lookup(var_name)
                    if var_symbol is None:
                        self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                         + str(var_name) +
                                                         ', la variable no ha sido declarada' + '\n')
            else:
                expresion_logica.expresion_simple_p.accept(self)



    def visit_expresion_simple(self, expresion_simple):
        if isinstance(expresion_simple.expresion_simple_p, str):
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(expresion_simple.expresion_simple_p)):
                var_name = expresion_simple.expresion_simple_p
                var_symbol = self.current_scope.lookup(var_name)
                if var_symbol is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            expresion_simple.expresion_simple_p.accept(self)

        if isinstance(expresion_simple.expresion_aditiva_p, str):
            numRegex = re.compile(r'(([0-9]|[a-f])+\#16)|[0-7]+\#8|[0-9]+')
            if not (numRegex.match(expresion_simple.expresion_aditiva_p)):
                var_name = expresion_simple.expresion_aditiva_p
                var_symbol = self.current_scope.lookup(var_name)
                if var_symbol is None:
                    self.errors_tabla_simbolos.write('error en llamado a variable: '
                                                     + str(var_name) +
                                                     ', la variable no ha sido declarada' + '\n')
        else:
            expresion_simple.expresion_aditiva_p.accept(self)

    #----------------------------------

    def visit_declaracion_funa(self, declaracion_fun):
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

    def visit_sentencia_compa(self, sentencia_comp):
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

    def visit_sentencia_expra(self, sentencia_expr):
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

    def visit_sentencia_selecciona(self, sentencia_seleccion):
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


    def visit_sentencia_iteracion1a(self, sentencia_iteracion):
        self.id_sentencia_iteracion += 1
        id_sentencia_iteracion = self.id_sentencia_iteracion
        self.ast += '-> "Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': MIENTRAS" ' + '\n'
        if sentencia_iteracion.expresion_p is not None:
            self.ast += '\t"Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': MIENTRAS" '
            sentencia_iteracion.expresion_p.accept(self)
        if sentencia_iteracion.sentencia_p is not None:
            self.ast += '\t"Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': MIENTRAS" '
            sentencia_iteracion.sentencia_p.accept(self)

    def visit_sentencia_iteracion2a(self, sentencia_iteracion):
        self.id_sentencia_iteracion += 1
        id_sentencia_iteracion = self.id_sentencia_iteracion
        self.ast += '-> "Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': REP"' + '\n'
        if sentencia_iteracion.sentencia_comp_p is not None:
            self.ast += '\t"Sentencia-iteracion ' + str(id_sentencia_iteracion) + ': REP" '
            sentencia_iteracion.sentencia_comp_p.accept(self)

    def visit_sentencia_retornoa(self, sentencia_retorno):
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


    def visit_expresiona(self, expresion):
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


    def visit_expresion_negadaa(self, expresion_negada):
        self.id_expresion_negada += 1
        id_expresion_negada = self.id_expresion_negada
        self.ast += '-> "Expresion-negada ' + str(id_expresion_negada) + ': !"'  '\n'
        self.ast += '\t"Expresion-negada ' + str(id_expresion_negada) + ': !" '
        expresion_negada.expresion_logica_p.accept(self)

    def visit_expresion_logicaa(self, expresion_logica):
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


    def visit_expresion_simplea(self, expresion_simple):
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

    def visit_expresion_aditivaa(self, expresion_aditiva):
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




