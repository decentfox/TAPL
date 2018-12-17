from .syntax import Term, TmZero, TmSucc, TmTrue, TmFalse, TmIf, TmPred, \
    TmIsZero


class NoRuleApplies(Exception):
    pass


def is_numeric_val(t: Term) -> bool:
    return isinstance(t, TmZero) or \
           isinstance(t, TmSucc) and is_numeric_val(t._value)


def is_val(t: Term) -> bool:
    return isinstance(t, (TmTrue, TmFalse)) or is_numeric_val(t)


def eval1(t: Term) -> Term:
    if isinstance(t, TmIf):
        if isinstance(t._condition, TmTrue):
            return t._true_val
        elif isinstance(t._condition, TmFalse):
            return t._false_val
        else:
            return TmIf(eval1(t._condition), t._true_val, t._false_val,
                        info=t.info)
    elif isinstance(t, TmSucc):
        return TmSucc(eval1(t._value), info=t.info)
    elif isinstance(t, TmPred):
        if isinstance(t._value, TmZero):
            return TmZero()
        elif isinstance(t._value, TmSucc) and is_numeric_val(t._value._value):
            return t._value._value
        else:
            return TmPred(eval1(t._value), info=t.info)
    elif isinstance(t, TmIsZero):
        if isinstance(t._value, TmZero):
            return TmTrue()
        elif isinstance(t._value, TmSucc) and is_numeric_val(t._value._value):
            return TmFalse()
        else:
            return TmIsZero(eval1(t._value), info=t.info)
    else:
        raise NoRuleApplies()


def evaluate(t: Term) -> Term:
    try:
        return evaluate(eval1(t))
    except NoRuleApplies:
        return t


def test_numeric():
    assert is_numeric_val(TmZero())
    assert is_numeric_val(TmSucc(TmZero()))
    assert is_numeric_val(TmSucc(TmSucc(TmZero())))

    assert not is_numeric_val(TmTrue())
    assert not is_numeric_val(TmSucc(TmTrue()))
    assert not is_numeric_val(TmSucc(TmSucc(TmTrue())))


def test_evalate():
    for t in TmTrue(), TmFalse(), TmZero(), TmSucc(TmZero()):
        assert evaluate(t) is t
