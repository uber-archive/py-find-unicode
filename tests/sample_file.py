def magic():
    return 'foo'

unicode()                          # OK
unicode('foo')                     # BAD
unicode('foo' + 'bar')             # BAD
unicode('foo', 'utf-8')            # OK
unicode('foo', 'utf-8', 'ignore')  # OK
unicode(magic())                   # BAD

ARGS = ['utf-8']
unicode('foo', *ARGS)              # OK

KWARGS = {'encoding': 'utf-8'}
unicode('foo', **KWARGS)           # OK
