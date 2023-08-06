# built-in
from typing import Optional

# app
from .common import TOKENS, Extractor, Token
from .value import UNKNOWN, get_value


get_asserts = Extractor()


@get_asserts.register(*TOKENS.ASSERT)
def handle_assert(expr) -> Optional[Token]:
    value = get_value(expr=expr.test)
    if value is UNKNOWN:
        return None
    if value:
        return None
    return Token(value=value, line=expr.lineno, col=expr.col_offset + 7)
