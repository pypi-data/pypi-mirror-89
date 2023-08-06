# built-in
import ast
from textwrap import dedent

# external
import astroid

# project
from deal.linter._func import Func
from deal.linter._rules import (
    CheckAsserts, CheckImports, CheckMarkers, CheckPre, CheckRaises, CheckReturns, rules,
)


def test_error_codes():
    codes = [rule.code for rule in rules]
    assert len(codes) == len(set(codes))


def test_error_messages():
    messages = [rule.message for rule in rules]
    assert len(messages) == len(set(messages))


def test_check_pre():
    checker = CheckPre()
    text = """
    @deal.pre(lambda x: x > 0)
    def example(x):
        return -x

    @deal.raises()
    def caller():
        return example(-3)

    # ignore funcs without contracts
    def caller():
        return example(-3)
    """
    text = dedent(text).strip()
    funcs = Func.from_astroid(astroid.parse(text))
    assert len(funcs) == 3
    actual = []
    for func in funcs:
        actual.extend(tuple(err) for err in checker(func))
    expected = [(7, 11, 'DEAL011 pre contract error (-3)')]
    assert actual == expected


def test_check_returns():
    checker = CheckReturns()
    text = """
    @deal.post(lambda x: x > 0)
    def test(a):
        if a:
            return 1
        else:
            return -1
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(6, 15, 'DEAL012 post contract error (-1)')]
        assert actual == expected


def test_check_returns_with_message():
    checker = CheckReturns()
    text = """
    @deal.post(lambda x: x > 0 or 'oh no!')
    def test(a):
        if a:
            return 1
        else:
            return -1
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(6, 15, 'DEAL012 oh no! (-1)')]
        assert actual == expected


def test_check_returns_ok_unresolved():
    checker = CheckReturns()
    text = """
    @deal.post(unknown)
    def test(a):
        return 1
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = tuple(checker(func))
        assert not actual


def test_check_raises():
    checker = CheckRaises()
    text = """
    @deal.raises(ValueError)
    def test(a):
        raise ValueError
        raise KeyError
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(4, 10, 'DEAL021 raises contract error (KeyError)')]
        assert actual == expected


def test_check_raises_without_allowed():
    checker = CheckRaises()
    text = """
    @deal.raises()
    def test(a):
        raise ValueError
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(3, 10, 'DEAL021 raises contract error (ValueError)')]
        assert actual == expected


def test_check_raises_unknown():
    checker = CheckRaises()
    text = """
    @deal.raises()
    def test(a):
        raise UnknownError
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(3, 10, 'DEAL021 raises contract error (UnknownError)')]
        assert actual == expected


def test_check_raises_inherited():
    checker = CheckRaises()
    text = """
    @deal.raises(LookupError)
    def test(a):
        raise KeyError
        raise ValueError
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(4, 10, 'DEAL021 raises contract error (ValueError)')]
        assert actual == expected


def test_check_prints():
    checker = CheckMarkers()
    text = """
    @deal.pure
    def test(a):
        print(1)
        return 1
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(3, 4, 'DEAL046 missed marker (stdout)')]
        assert actual == expected


def test_check_pure():
    checker = CheckMarkers()
    text = """
    @deal.pure
    @deal.post(lambda x: x)  # skip other contracts
    def test(a):
        global b
        return b
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(4, 4, 'DEAL041 missed marker (global)')]
        assert actual == expected


def test_check_pure_no_returns():
    checker = CheckMarkers()
    text = """
    @deal.pure
    def test(a):
        a + 3
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        assert len(actual) == 1
        expected = 'DEAL043 missed marker (io)'
        assert actual[0][2] == expected


def test_check_has_io():
    checker = CheckMarkers()
    text = """
    @deal.pre(lambda a: len(a) > 2)
    @deal.has('io')
    @deal.post(lambda result: result is not None)
    def test(a):
        import sys
        sys.stdout.write(a)
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        assert len(actual) == 1
        expected = 'DEAL042 missed marker (import)'
        assert actual[0][2] == expected


def test_check_has_custom_markers():
    checker = CheckMarkers()
    text = """
    import deal

    @deal.has('database')
    def inner():
        return 1

    @deal.has()
    def outer():
        return inner()
    """
    text = dedent(text).strip()
    funcs = Func.from_astroid(astroid.parse(text))
    func = funcs[-1]
    actual = [tuple(err) for err in checker(func)]
    assert len(actual) == 1
    expected = 'DEAL040 missed marker (database)'
    assert actual[0][2] == expected


def test_check_has_no_has():
    checker = CheckMarkers()
    text = """
    @deal.pre(lambda a: len(a) > 2)
    @deal.post(lambda result: result is not None)
    @deal.raises(ValueError)
    def test(a):
        import sys
        sys.stdout.write(a)
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        assert actual == []


def test_check_asserts():
    checker = CheckAsserts()
    text = """
    def example(a):
        assert False, "oh no!"
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = [tuple(err) for err in checker(func)]
        expected = [(2, 11, 'DEAL031 assert error (False)')]
        assert actual == expected


def test_skip_asserts_in_tests():
    checker = CheckAsserts()
    text = """
    def test_example(a):
        assert False, "oh no!"
    """
    text = dedent(text).strip()
    funcs1 = Func.from_ast(ast.parse(text))
    funcs2 = Func.from_astroid(astroid.parse(text))
    for func in (funcs1[0], funcs2[0]):
        actual = list(checker(func))
        assert actual == []


def test_check_imports():
    checker = CheckImports()
    text = """
    import deal
    from deal import pre
    from not_a_deal import pre
    from .deal import pre
    """
    text = dedent(text).strip()
    for tree in (ast.parse(text), astroid.parse(text)):
        actual = [tuple(err) for err in checker(tree)]
        expected = [(2, 0, 'DEAL001 ' + CheckImports.message)]
        assert actual == expected
