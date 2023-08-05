"""
Parsing module.

Here are all the parsers declared.
"""

from pyparsing import Word, nums, alphas, Combine, Optional, oneOf, Group, delimitedList, Keyword, Suppress, \
    pyparsing_common, printables, Forward, ZeroOrMore, SkipTo, LineEnd, restOfLine, quotedString,nestedExpr, StringEnd
import bagheera.parser.errors as e


def parser(filename=None):
    """
    Generate a callable parser for each file. The filename is necessary to get better Error messages.

    :param filename: Name of the file, on which the parser will be applied
    :type filename: str
    :return: A parser for the file on filename
    """
    line_comment = Group(Suppress("--") + restOfLine + SkipTo(LineEnd()))("SingleLineComment")
    block_comment = nestedExpr("{-", "-}")("MultiLineComment")
    comment = Group(line_comment | block_comment)
    module_name = Group(delimitedList(Word(alphas.upper(),alphas),"."))("Module Name")
    module_exports = Group(Keyword("..") | Group(delimitedList(Word(printables, excludeChars=',)'))))("Module Exports")
    module_declaration = Group(
        Suppress("module").setFailAction(e.ModuleDeclarationMissingException(filename)) +
        module_name +
        Suppress("exposing") +
        Suppress("(") +
        module_exports+Suppress(")"))("Module Declaration")

    LPAR, RPAR = map(Suppress, '()')
    integer = Word(nums)
    real = Optional(Word(nums)) + '.' + Word(nums)
    expr = Forward()
    operand = Optional("-") + (real | integer)
    factor = operand | Group(LPAR + expr + RPAR)
    term = factor + ZeroOrMore(oneOf('* /') + factor)
    expr <<= term + ZeroOrMore(oneOf('+ -') + term)

    function_name = Word(alphas.lower())
    function_parameter = Word(alphas.upper()+alphas.lower())
    function_parameters = ZeroOrMore(function_parameter)("Function Parameter")
    function_body = expr
    function_declaration = Group(function_name + function_parameters + Suppress("=") + function_body)\
        ("Function Declaration")

    return module_declaration + ZeroOrMore(function_declaration | comment)("Body")


def print_ast(item, ident=0):
    """
    Pretty prints the AST to std.out.

    :param item: AST-Item to print (recursively iterates through the children)
    :param ident: Identation depth (defaults to 0 and is incremented for each recursive call)
    :type ident: int
    :return: None
    """
    try:
        for key, value in item.items():
            print("\t"*ident, key, "->", value)
            print_ast(value, ident + 1)
    except Exception:
        print("\t"*ident, item, "")
