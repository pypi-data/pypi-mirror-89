"""
Parsing errors.

Here you find all the errors that may be thrown during the parsing process.
"""

class ModuleDeclarationMissingException(Exception):
    """Exception thrown when the module declaration is absent."""

    def __init__(self, filename):
        """Initialize the Exception, with the filename so that the error message is more helpful.

        :param filename: Name of the file that is missing a module declaration.
        :type filename: str
        :returns: The exception explaining the error.
        :rtype: Exception
        """
        self.message = """\
-- EMPTY MODULE --------------------------------------------- {0}

I ran into something unexpected when parsing your code!


I am looking for one of the following things:

    a definition or type annotation
    a port declaration
    a type declaration
    an import
    an infix declaration
    whitespace""".format(filename)
        super().__init__(self.message)

    def __call__(self, *args, **kwargs):
        """
        Raise the Exception.

        :param args:
        :param kwargs:
        :return:
        """
        raise self
