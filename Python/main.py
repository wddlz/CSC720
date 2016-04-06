import re


# Layout features
# Tabs count
def tabs_count():
    pattern = re.compile('\t')
    return pattern


# Spaces count
def spaces_count():
    pattern = re.compile(' ')
    return pattern


# Empty lines TODO doesnt get only empty lines but all new line chars
def empty_lines_count():
    pattern = re.compile('\n')
    return pattern


# All white space
def white_space_count():
    pattern = re.compile('\s')
    return pattern


# Inner word split
def inner_word_split():
    pattern = re.compile('(?<!(^|[A-Z]))(?=[A-Z])|(?<!^)(?=[A-Z][a-z])')
    return pattern


# Underscore split
def underscore_split():
    pattern = re.compile('_+')
    return pattern


# Identifier split
def identifier_split():
    pattern = re.compile('(\W|\d)+')
    return pattern


# Equals sign alignment of setting variables
# TODO: how? is any = sign preceded or followed by a number of spaces > 1 proof of alignment?
def equals_split():
    pattern = re.compile('')
    return pattern


# Comment count
# TODO: how to tell multiple consecutive comments?
# TODO: does it matter ("lines of comments" vs amount of lines of code commented)?
# TODO: different pattern per language, // or /* for java, # for python, etc
def comment_split(s):
    pattern = re.compile('')
    return pattern


# Count ID Sequences
def count_identifier_sequences(n, s):
    sequences = identifier_sequences(n, s)
    return count_sequences(sequences)


# Count Word Sequences
def count_word_sequences(n, s):
    sequences = word_sequences(n, s)
    return count_sequences(sequences)


# IdentifierSequences
def identifier_sequences(n, s):
    results = 0
    return results


# WordSequences
def word_sequences(n, s):
    results = 0
    return results

# AllIdentifiers
# AllWords


# CountSequences
def count_sequences(sequences):
    frequency = 0
    return frequency

# Identifiers
# Words


# Count keywords, takes in keyword to be counted, TODO refuse lines inside comments?
def keyword_count(keyword):
    pattern = re.compile(r'\b' + keyword + r'\b')
    return pattern


# Increment counts
def increment_key_count_by_one(key, i_seq):
    if key not in i_seq:
        i_seq[key] = 0
    i_seq[key] += 1


def increment_key_count_by_value(key, i_seq, val):
    if key not in i_seq:
        i_seq[key] = 0
    i_seq[key] += val


def main():
    # TODO: loop through files to collect data
    print "Filename for reading:"
    filename = raw_input("> ")
    print "Text file input %r:" % filename
    txt = open(filename)
    seq = {'idSeq': 0, 'charCount': 0, 'udSeq': 0, 'tbSeq': 0, 'spSeq': 0, 'wsSeq': 0, 'cuSeq': 0, 'tsSeq': 0,
           'emSeq': 0}

    # keywords in javascript from ECMAScript 6
    javascript_keywords = ['break', 'case', 'class', 'catch', 'const', 'continue', 'debugger', 'default', 'delete',
                           'do', 'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in',
                           'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var',
                           'void', 'while', 'with', 'yield']

    with txt as t:
        for l in t:
            increment_key_count_by_value('charCount', seq, len(l))
            underscores = underscore_split().findall(l)
            increment_key_count_by_value('udSeq', seq, len(underscores))
            # Table 3 Layout Features
            tabs = tabs_count().findall(l)
            increment_key_count_by_value('tbSeq', seq, len(tabs))
            spaces = spaces_count().findall(l)
            increment_key_count_by_value('spSeq', seq, len(spaces))
            whitespace = white_space_count().findall(l)
            increment_key_count_by_value('wsSeq', seq, len(whitespace))
            if l.strip().startswith('{') or l.strip().startswith('}'):
                # need boolean to see if this is the majority of lines
                increment_key_count_by_one('cuSeq', seq)
            if l.startswith('\t'):  # need boolean to see if this is the majority of lines
                increment_key_count_by_one('tsSeq', seq)
            if len(l.strip()) == 0:  # empty line
                increment_key_count_by_one('emSeq', seq)
            # Table 4 Syntax Features
            for keyword in javascript_keywords:
                word = keyword_count(keyword).findall(l)
                increment_key_count_by_value(keyword + 'Seq', seq, len(word))


        increment_key_count_by_one('idSeq', seq)
        print "character count: ", seq['charCount']
        print "dict['idSeq']: ", seq['idSeq']
        print "underlines: ", seq['udSeq']
        print "T3| tabs: ", seq['tbSeq']
        print "T3| spaces: ", seq['spSeq']
        print "T3| empty lines count: ", seq['emSeq']
        print "T3| whitespace: ", seq['wsSeq']
        print "T3| lines that start with curly brackets: ", seq['cuSeq']
        print "T3| line starts with tab: ", seq['tsSeq']
        for keyword in javascript_keywords:
            print "T4| keyword count (" + keyword + "): ", seq[keyword + 'Seq']
if __name__ == "__main__":
    main()



