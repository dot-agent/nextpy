import pyparsing as pp
from pyparsing import ParseException, ParseSyntaxException

from ..parsing._grammar import grammar
def parse_program( program):
    try:
        parse_tree = grammar.parse_string(program._text)
        return parse_tree
    except (pp.ParseException, pp.ParseSyntaxException) as e:
        initial_str = program._text[max(0, e.loc-40):e.loc]
        initial_str = initial_str.split("\n")[-1] # trim off any lines before the error
        next_str = program._text[e.loc:e.loc+40]
        error_string = str(e)
        if next_str.startswith("{{#") or next_str.startswith("{{~#"):
            error_string += "\nPerhaps the block command was not correctly closed?"
        msg = error_string + "\n\n"+initial_str
            # msg += "\033[91m" + program._text[e.loc:e.loc+40] + "\033[0m\n"
        msg += program._text[e.loc:e.loc+40] + "\n"
        msg += " " * len(initial_str) + "^\n"

        raise SyntaxException(msg, e) from None
class CustomParseException(Exception):
    def __init__(self, error_context, original_exception):
        super().__init__(error_context)
        self.original_exception = original_exception
class SyntaxException(Exception):
    def __init__(self, msg, pyparsing_exception=None):
        super().__init__(msg)
        self.pyparsing_exception = pyparsing_exception

