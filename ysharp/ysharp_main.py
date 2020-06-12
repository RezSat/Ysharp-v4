try:
    import ysharp.ysharp_lexer as ysharp_lexer
    import ysharp.ysharp_parser as ysharp_parser
    import ysharp.ysharp_interpreter as ysharp_interpreter
except ModuleNotFoundError:
    import ysharp_lexer as ysharp_lexer
    import ysharp_parser as ysharp_parser
    import ysharp_interpreter as ysharp_interpreter
import pprint
from os import path
import logging
from copy import deepcopy


def read_file(filename):
    file_ = open(path.abspath(filename), "r")
    file_contents = file_.read()
    file_.close()
    return file_contents


def get_objects(filename):
    text = read_file(filename)
    lexer = ysharp_lexer.YsharpLexer()
    parser = ysharp_parser.YsharpParser()
    tree = parser.parse(lexer.tokenize(text))
    program = ysharp_interpreter.Process(
        tree, filename=path.abspath(filename), imported=True
    )
    program.run()
    return (deepcopy(program.objects), deepcopy(program.global_items["OBJECTS"]))


def main(filename, verbose=False, tree=None):
    defult_functions = get_objects(
        path.join(path.dirname(path.abspath(__file__)), "defult.yshp")
    )
    if tree is None:
        text = read_file(filename)
        pp = pprint.PrettyPrinter(indent=2)
        lexer = ysharp_lexer.YsharpLexer()
        parser = ysharp_parser.YsharpParser()
        if verbose:
            for tok in lexer.tokenize(text):
                print(tok)
        tree = parser.parse(lexer.tokenize(text))
        if verbose:
            pp.pprint(tree)
    program = ysharp_interpreter.Process(tree, filename=path.abspath(filename))
    program.objects.update(defult_functions[0])
    program.global_items["OBJECTS"].update(defult_functions[1])
    program.run()
