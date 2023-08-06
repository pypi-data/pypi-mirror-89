# built-in
import doctest
import re
import sys
from itertools import chain
from unittest.mock import Mock

# external
import pytest

# project
import deal._aliases
import deal._testing
from deal._state import state


rex = re.compile(r'deal\.(\w*ContractError)')


class Checker(doctest.OutputChecker):
    def __init__(self):
        self.diff = []

    def check_output(self, want: str, got: str, optionflags: int) -> bool:
        got = rex.sub(r'\1', got)
        ok = super().check_output(want=want, got=got, optionflags=optionflags)
        if not ok:
            self.diff.append((got, want))
        return ok


finder = doctest.DocTestFinder(exclude_empty=True)


@pytest.mark.parametrize('test', chain(
    finder.find(deal._aliases),
    finder.find(deal._testing),
))
def test_doctest(test):
    state.color = False
    sys.modules['atheris'] = Mock()
    try:
        runner = doctest.DocTestRunner(checker=Checker(), optionflags=doctest.ELLIPSIS)
        runner.run(test)
        result = runner.summarize(verbose=False)
        if result.failed:
            print('Kinda diff:')
            print(*runner._checker.diff, sep='\n')
        assert not result.failed
    finally:
        state.color = True
        del sys.modules['atheris']
