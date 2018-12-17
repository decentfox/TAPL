from .syntax import Term, TmZero, TmSucc, TmTrue, TmFalse


def is_numeric_val(t: Term) -> bool:
    return isinstance(t, TmZero) or \
           isinstance(t, TmSucc) and is_numeric_val(t._value)


def is_val(t: Term) -> bool:
    return isinstance(t, (TmTrue, TmFalse)) or is_numeric_val(t)


def test_numeric():
    assert is_numeric_val(TmZero())
    assert is_numeric_val(TmSucc(TmZero()))
    assert is_numeric_val(TmSucc(TmSucc(TmZero())))

    assert not is_numeric_val(TmTrue())
    assert not is_numeric_val(TmSucc(TmTrue()))
    assert not is_numeric_val(TmSucc(TmSucc(TmTrue())))
