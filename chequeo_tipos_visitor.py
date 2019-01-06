
from string import lower


class ChequeoTipos(object):
    def __init__(self, archivo):
        self.errors_chequeo_tipos = archivo
        self.inicializadas = []

    def visit_program(self, program):
        for declaration in program.declarations_p:
            declaration.accept(self)

    def visit_var_declaration(self, var_declaration):
        var_declaration.tipo = var_declaration.variable.tipo

    def visit_fun_declaration(self, fun_declaration):
        if fun_declaration.params_p is not None:
            for param in fun_declaration.params_p:
                param.accept(self)
                if param.tipo == 'ERROR':
                    fun_declaration.tipo = param.tipo
        if fun_declaration.compound_stmt_p.local_declarations_p is not None or \
                        fun_declaration.compound_stmt_p.stmt_list_p is not None:
            fun_declaration.compound_stmt_p.accept(self)
        fun_declaration.tipo = fun_declaration.funcion.tipo

    def visit_simple_expression(self, simple_expresion):
        simple_expresion.additive_expression1_p.accept(self)
        if simple_expresion.additive_expression1_p.tipo != 'int':
            self.errors_chequeo_tipos.write('El lado izquierdo de la comparación debe ser de tipo entero.\n')
            simple_expresion.tipo = 'ERROR'
        simple_expresion.additive_expression2_p.accept(self)
        if simple_expresion.additive_expression2_p.tipo != 'int':
            self.errors_chequeo_tipos.write('El lado derecho de la comparación debe ser de tipo entero.\n')
            simple_expresion.tipo = 'ERROR'
        if simple_expresion.additive_expression1_p.tipo == 'int' and simple_expresion.additive_expression2_p.tipo == \
                'int':
            simple_expresion.tipo = 'int'