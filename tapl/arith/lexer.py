from .. import lex

tokens = [
    'IF',
    'THEN',
    'ELSE',
    'TRUE',
    'FALSE',
    'SUCC',
    'PRED',
    'ISZERO',
    'INTV',
    'LPAREN',
    'RPAREN',
    'SEMI',
]

t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_TRUE = r'true'
t_FALSE = r'false'
t_SUCC = r'succ'
t_PRED = r'pred'
t_ISZERO = r'iszero'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'

t_ignore = ' \t'
t_ignore_COMMENT = r'(/\*(.|\n)*?\*/)|(//.*)'


def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)


def t_INTV(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def find_column(input_, lexpos):
    line_start = input_.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1


lexer = lex.lex()


def test():
    import os
    with open(os.path.join(os.path.dirname(__file__), 'test.f')) as f:
        input_ = f.read()
    lexer.input(input_)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        tok.lexpos = find_column(input_, tok.lexpos)
        print(tok)
