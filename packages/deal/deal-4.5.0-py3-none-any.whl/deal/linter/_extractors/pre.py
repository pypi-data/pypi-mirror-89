# built-in
import ast
from typing import Any, Dict, Iterator, Sequence

# external
import astroid

# app
from .common import Extractor, Token, infer
from .contracts import get_contracts
from .value import UNKNOWN, get_value


get_pre = Extractor()


@get_pre.register(astroid.Call)
def handle_call(expr: astroid.Call, context: Dict[str, ast.stmt] = None) -> Iterator[Token]:
    # app
    from .._contract import Category, Contract

    args = []
    for subnode in expr.args:
        value = get_value(expr=subnode)
        if value is UNKNOWN:
            return
        args.append(value)

    kwargs: Dict[str, Any] = {}
    for subnode in (expr.keywords or ()):
        value = get_value(expr=subnode.value)
        if value is UNKNOWN:
            return
        kwargs[subnode.arg] = value

    for func in infer(expr.func):
        if type(func) is not astroid.FunctionDef:
            continue
        if not func.decorators:
            continue
        code = 'def f({}):0'.format(func.args.as_string())
        func_args = ast.parse(code).body[0].args  # type: ignore

        for category, contract_args in get_contracts(func.decorators.nodes):
            if category != 'pre':
                continue

            contract = Contract(
                args=contract_args,
                category=Category.PRE,
                func_args=func_args,
                context=context,
            )
            try:
                result = contract.run(*args, **kwargs)
            except NameError:
                continue
            if result is False or type(result) is str:
                yield Token(
                    value=format_call_args(args, kwargs),
                    marker=result or None,
                    line=expr.lineno,
                    col=expr.col_offset,
                )


def format_call_args(args: Sequence, kwargs: Dict[str, Any]) -> str:
    sep = ', '
    args_s = sep.join(map(repr, args))
    kwargs_s = sep.join(['{}={!r}'.format(k, v) for k, v in kwargs.items()])
    if args and kwargs:
        return args_s + sep + kwargs_s
    return args_s + kwargs_s
