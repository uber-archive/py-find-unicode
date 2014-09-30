import argparse
import ast
import sys


version_info = (0, 1, 0)
__version__ = '.'.join(map(str, version_info))


def stringify(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return '%s.%s' % (stringify(node.value), node.attr)
    elif isinstance(node, ast.Subscript):
        return '%s[%s]' % (stringify(node.value), stringify(node.slice))
    elif isinstance(node, ast.Index):
        return stringify(node.value)
    elif isinstance(node, ast.Call):
        return '%s(%s, %s)' % (stringify(node.func), stringify(node.args), stringify(node.keywords))
    elif isinstance(node, list):
        return '[%s]' % (', '.join(stringify(n) for n in node))
    elif isinstance(node, ast.Str):
        return node.s
    else:
        return ast.dump(node)


class IllegalLine(object):

    def __init__(self, reason, node, filename):
        self.reason = reason
        self.lineno = node.lineno
        self.filename = filename
        self.node = node

    def __str__(self):
        return "%s:%d\t%s" % (self.filename, self.lineno, self.reason)

    def __repr__(self):
        return "IllegalLine<%s, %s:%s>" % (self.reason, self.filename, self.lineno)


class Checker(ast.NodeVisitor):

    def __init__(self, filename, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.filename = filename
        self.errors = []

    def visit_Call(self, node):
        function_name = stringify(node.func)
        if function_name == 'unicode':
            # There are a few cases to consider here:
            #   unicode() is OK (it return u'')
            #   unicode(something) is bad
            #   unicode(foo, bar) is OK (encoding is bar)
            #   unicode(foo, encoding='bar') is OK
            #   unicode(foo, *bar) is OK
            #   unicode(foo, **bar) is OK
            # So we're looking for calls with one argument and no
            # keywords/kwargs/starargs.
            if (len(node.args) == 1
                    and not (node.keywords or node.kwargs or node.starargs)):
                self.errors.append(IllegalLine(
                    'unicode() called without explicit encoding', node, self.filename))
            if len(node.args) >= 4:
                self.errors.append(IllegalLine(
                    'unicode() called with too many positional arguments',
                    node, self.filename))
        self.generic_visit(node)

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        item.parent = node
                        self.visit(item,)
            elif isinstance(value, ast.AST):
                value.parent = node
                self.visit(value)


def check(filename):
    c = Checker(filename=filename)
    with open(filename, 'r') as fobj:
        try:
            parsed = ast.parse(fobj.read(), filename)
            c.visit(parsed)
        except Exception:
            raise
    return c.errors


def main():
    parse_description = ('Look for patterns in python source files that might '
                         'indicate unicode unawareness')
    parse_epilog = ('Exit status is 0 if all files are okay, 1 if any files '
                    'have an error. Errors are printed to stdout.')
    parser = argparse.ArgumentParser(
        description=parse_description, epilog=parse_epilog)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('files', nargs='+', help='Files to check')
    args = parser.parse_args()

    errors = []
    for fname in args.files:
        these_errors = check(fname)
        if these_errors:
            print '\n'.join(str(e) for e in these_errors)
            errors.extend(these_errors)
    if errors:
        print '%d total errors' % len(errors)
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
