# built-in
import ast
from textwrap import dedent

# external
import astroid
import pytest

# project
from deal.linter._extractors import get_contracts


@pytest.mark.parametrize('text, expected', [
    ('@deal.post(lambda x: x>0)', ('post', )),
    ('@deal.pure', ('pure', )),
    ('@deal.pure()', ('pure', )),
    ('@deal.chain(deal.pure)', ('pure', )),
    ('@deal.chain(deal.pure, deal.post(lambda x: x>0))', ('pure', 'post')),
])
def test_get_contracts_decorators(text, expected):
    text += '\ndef f(x): pass'

    tree = astroid.parse(text)
    print(tree.repr_tree())
    decos = tree.body[-1].decorators.nodes
    returns = tuple(cat for cat, _ in get_contracts(decos))
    assert returns == expected

    tree = ast.parse(text)
    print(ast.dump(tree))
    decos = tree.body[-1].decorator_list
    returns = tuple(cat for cat, _ in get_contracts(decos))
    assert returns == expected


def test_get_contracts_infer():
    text = """
        from io import StringIO
        import deal

        contracts = deal.chain(deal.pure, deal.post(lambda x: x>0))

        @contracts
        def f(x):
            return x

        with StringIO() as contracts2:
            @contracts2
            def f(x):
                return x
    """

    tree = astroid.parse(dedent(text))
    print(tree.repr_tree())
    decos = tree.body[-2].decorators.nodes
    returns = tuple(cat for cat, _ in get_contracts(decos))
    assert returns == ('pure', 'post')
