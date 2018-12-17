from .support import FileInfo


class Term:
    def __init__(self, info: FileInfo = None):
        self._info = info

    @property
    def info(self) -> FileInfo:
        return self._info

    def stringify_term(self) -> str:
        return self.stringify_app_term()

    def stringify_app_term(self) -> str:
        return self.stringify_a_term()

    def stringify_a_term(self) -> str:
        return f'({self.stringify_term()})'

    def __repr__(self) -> str:
        return self.stringify_term()


class TmTrue(Term):
    def stringify_a_term(self) -> str:
        return 'true'


class TmFalse(Term):
    def stringify_a_term(self) -> str:
        return 'false'


class TmIf(Term):
    def __init__(self, condition: Term, true_val: Term, false_val: Term,
                 info: FileInfo = None):
        super().__init__(info)
        self._condition = condition
        self._true_val = true_val
        self._false_val = false_val

    def stringify_term(self) -> str:
        return (f'if {self._condition.stringify_term()} '
                f'then {self._true_val.stringify_term()} '
                f'else {self._false_val.stringify_term()}')


class TmZero(Term):
    def stringify_a_term(self) -> str:
        return '0'


class TmSucc(Term):
    def __init__(self, value: Term, info: FileInfo = None):
        super().__init__(info)
        self._value = value

    def stringify_a_term(self) -> str:
        def f(n, t: Term):
            if isinstance(t, TmZero):
                return str(n)
            elif isinstance(t, TmSucc):
                return f(n + 1, t._value)
            else:
                return f'(succ {t.stringify_a_term()})'

        return f(1, self._value)


class TmPred(Term):
    def __init__(self, value: Term, info: FileInfo = None):
        super().__init__(info)
        self._value = value

    def stringify_app_term(self) -> str:
        return f'pred {self._value.stringify_a_term()}'


class TmIsZero(Term):
    def __init__(self, value: Term, info: FileInfo = None):
        super().__init__(info)
        self._value = value

    def stringify_app_term(self) -> str:
        return f'iszero {self._value.stringify_a_term()}'


def test_consts():
    assert repr(TmTrue()) == 'true'
    assert repr(TmFalse()) == 'false'
    assert repr(TmZero()) == '0'


def test_succ():
    n = TmZero()
    for i in range(10):
        assert repr(n) == str(i)
        n = TmSucc(n)

    assert repr(TmSucc(TmTrue())) == '(succ true)'
    assert repr(TmSucc(TmSucc(TmTrue()))) == '(succ true)'


def test_iszero():
    assert repr(TmIsZero(TmZero())) == 'iszero 0'
    assert repr(TmIsZero(TmTrue())) == 'iszero true'
    assert repr(TmIsZero(TmFalse())) == 'iszero false'
