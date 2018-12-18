from .. import yacc
from .lexer import tokens, find_column
from .syntax import TmIf, TmSucc, TmPred, TmIsZero, TmTrue, TmFalse, TmZero
from .support import Info


def _get_info(p, n) -> Info:
    return Info(
        p.parser.file_name,
        p.lineno(n),
        find_column(p.parser.file_data, p.lexpos(n)),
    )


# The top level of a file is a sequence of commands, each terminated
# by a semicolon.
def p_toplevel_eof(p):
    'toplevel :'
    p[0] = []


def p_toplevel(p):
    'toplevel : Command SEMI toplevel'
    p[0] = [p[1]] + p[3]


# A top-level command
def p_command(p):
    'Command : Term'
    p[0] = p[1]


def p_term(p):
    'Term : AppTerm'
    p[0] = p[1]


def p_term_if(p):
    'Term : IF Term THEN Term ELSE Term'
    p[0] = TmIf(p[2], p[4], p[6], info=_get_info(p, 1))


def p_app_term(p):
    'AppTerm : ATerm'
    p[0] = p[1]


def p_app_term_succ(p):
    'AppTerm : SUCC ATerm'
    p[0] = TmSucc(p[2], info=_get_info(p, 1))


def p_app_term_pred(p):
    'AppTerm : PRED ATerm'
    p[0] = TmPred(p[2], info=_get_info(p, 1))


def p_app_term_iszero(p):
    'AppTerm : ISZERO ATerm'
    p[0] = TmIsZero(p[2], info=_get_info(p, 1))


# Atomic terms are ones that never require extra parentheses
def p_a_term(p):
    'ATerm : LPAREN Term RPAREN'
    p[0] = p[2]


def p_a_term_true(p):
    'ATerm : TRUE'
    p[0] = TmTrue(info=_get_info(p, 1))


def p_a_term_false(p):
    'ATerm : FALSE'
    p[0] = TmFalse(info=_get_info(p, 1))


def p_a_term_intv(p):
    'ATerm : INTV'
    info = _get_info(p, 1)

    def f(n):
        if n == 0:
            return TmZero(info=info)
        else:
            return TmSucc(f(n - 1), info=info)

    p[0] = f(p[1])


def p_error(t):
    print("Syntax error in input!")
    print(parser.file_data.split('\n')[t.lineno - 1])
    print(' ' * (find_column(parser.file_data, t.lexpos) - 1) + '^')


parser = yacc.yacc()


def test():
    code = 'if iszero 6 then 2 else 3;0;4;5;'
    assert ';'.join(map(str, parser.parse(code))) == code[:-1]

    import os
    with open(os.path.join(os.path.dirname(__file__), 'test.f')) as f:
        input_ = f.read()
    print(parser.parse(input_))
