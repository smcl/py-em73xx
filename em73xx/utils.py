def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def quote(s):
    return "\"" + s + "\""


def unquote(s):
    if s.startswith('"'):
        s = s[1:]

    if s.endswith('"'):
        s = s[:-1]

    return s
