def magic():
    return 'foo'

# OK, returns u'''
unicode()

# Not OK, no encoding supplied
unicode('foo')

# Also not OK, no encoding supplied
unicode('foo' + 'bar')

# OK, positional encoding supplied
unicode('foo', 'utf-8')

# OK, positional encoding and error argument supplied
unicode('foo', 'utf-8', 'ignore')

# Not OK, no encoding
unicode(magic())

# Not OK, incorrect number of positional args
unicode(1, 2, 3, 4)

# OK, encoding supplied as stararg
ARGS = ['utf-8']
unicode('foo', *ARGS)

# OK, encoding supplied as kwarg
KWARGS = {'encoding': 'utf-8'}
unicode('foo', **KWARGS)
