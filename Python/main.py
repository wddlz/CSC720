import re
import math


# Lexical features
# Count ternary operators
def ternary_sequences():
    pattern = re.compile('\s\?\s')
    return pattern


# Function count
# TODO No longer need as AST tree can handle
def function_count():
    pattern = re.compile(r'\bfunction\b')
    return pattern


# var count
# TODO No longer need as AST tree can handle
def var_count():
    pattern = re.compile(r'\bvar\b')
    return pattern


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
def inner_word_split(): # does not work in python
    pattern = re.compile('(?<!(^|[A-Z]))(?=[A-Z])|(?<!^)(?=[A-Z][a-z])')
    return pattern


# Underscore split
def underscore_split():
    pattern = re.compile('_+')
    return pattern


# Identifier split
# TODO No longer need as AST tree can handle
def identifier_split():
    pattern = re.compile('(\W|\d)+')
    return pattern


# Equals sign alignment of setting variables
# TODO: how? is any = sign preceded or followed by a number of spaces > 1 proof of alignment?
# TODO No longer need as AST tree can handle
def equals_split():
    pattern = re.compile('(?<!=|!)=(?!=)')
    return pattern


# Comment count
# TODO: how to tell multiple consecutive comments? Can't assume all // are comments.
# TODO: does it matter ("lines of comments" vs amount of lines of code commented)?
# TODO: different pattern per language, // or /* for java, # for python, etc
def comment_split():
    pattern = re.compile('//')
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


# Count keywords, takes in keyword to be counted
# TODO refuse lines inside comments? Difficult to do as double forward slash also appears in URLs so we cannot
# TODO assume all words after '//' are invalid.
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
    filename = ''
    print "User ID of files: "
    user_id = raw_input("> ")
    print "User ID %r: " % user_id
    while filename != '-1':
        print "Filename for reading (write \'-1\' when finished):"
        filename = raw_input("> ")
        print "Text file input %r:" % filename
        if filename == '-1':
            break
        txt = open(filename)
        seq = {'idSeq': 0, 'charCount': 0, 'udSeq': 0, 'tbSeq': 0, 'spSeq': 0, 'wsSeq': 0, 'cuSeq': 0, 'tsSeq': 0,
               'emSeq': 0, 'coSeq': 0}
        length_list = []
        deviation = 0
        unique_keywords = 0

        # numKeyword
        lexical_keywords = ['for', 'do', 'while', 'if', 'else if', 'else', 'switch']

        # keywords in javascript from ECMAScript 6
        javascript_keywords = ['break', 'case', 'class', 'catch', 'const', 'continue', 'debugger', 'default', 'delete',
                               'do', 'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in',
                               'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof',
                               'var', 'void', 'while', 'with', 'yield']
        with txt as t:
            for l in t:
                increment_key_count_by_one('lineCount', seq)
                increment_key_count_by_value('charCount', seq, len(l))
                length_list.append(len(l))
                underscores = underscore_split().findall(l)
                increment_key_count_by_value('udSeq', seq, len(underscores))
                # Table 2 Lexical Features
                for keyword in lexical_keywords:
                    lex_word = keyword_count(keyword).findall(l)
                    increment_key_count_by_value(keyword + 'LexSeq', seq, len(lex_word))
                ternary = ternary_sequences().findall(l)
                increment_key_count_by_value('teSeq', seq, len(ternary))
                comment = comment_split().findall(l)
                if len(comment) > 0:
                    increment_key_count_by_one('coSeq', seq)
                equals = equals_split().findall(l)
                increment_key_count_by_value('eqSeq', seq, len(equals))
                function = function_count().findall(l)
                increment_key_count_by_value('fuSeq', seq, len(function))
                var = var_count().findall(l)
                increment_key_count_by_value('vaSeq', seq, len(var))
                # Table 3 Layout Features
                tabs = tabs_count().findall(l)
                increment_key_count_by_value('tbSeq', seq, len(tabs))
                spaces = spaces_count().findall(l)
                increment_key_count_by_value('spSeq', seq, len(spaces))
                whitespace = white_space_count().findall(l)
                increment_key_count_by_value('wsSeq', seq, len(whitespace))
                if l.strip().startswith('{'):  # or l.strip().startswith('}')
                    # TODO need boolean to see if this is the majority of lines
                    increment_key_count_by_one('cuSeq', seq)
                elif l.strip().startswith('}'):
                    increment_key_count_by_one('clSeq', seq)
                if l.startswith('\t'):  # TODO need boolean to see if this is the majority of lines
                    increment_key_count_by_one('tsSeq', seq)
                if len(l.strip()) == 0:  # empty line
                    increment_key_count_by_one('emSeq', seq)
                # Table 4 Syntax Features
                for keyword in javascript_keywords:
                    word = keyword_count(keyword).findall(l)
                    increment_key_count_by_value(keyword + 'Seq', seq, len(word))

            if not txt.closed:
                txt.close()

            # TODO output to file per id?
            output = open("output" + user_id + ".txt", 'a+')
            output.write("test\n")
            output.write("T3| whitespace: " + str(seq['wsSeq']))

            if not output.closed:
                output.close()

            average_length = seq['charCount'] / float(seq['lineCount'])
            for length in length_list:
                deviation += math.pow(length - average_length, 2)
            variance = deviation / float(seq['lineCount'])
            print "average standard deviation of line length: ", math.sqrt(variance)
            print "line count: ", seq['lineCount']
            print "character count: ", seq['charCount']
            print "underlines: ", seq['udSeq']
            print "T2| literals (single equals): ", seq['eqSeq']  #
            print "T2| function count: ", seq['fuSeq']  #
            print "T2| var count: ", seq['vaSeq']  #
            print "T2| avgLineLength: ", average_length
            print "T2| comment(//) count: ", seq['coSeq']
            for keyword in lexical_keywords:
                print "T2| lexical keyword count (" + keyword + "): ", seq[keyword + 'LexSeq'] #
                if seq[keyword + 'LexSeq'] > 0:
                    unique_keywords += 1
            print "T2| unique keywords: ", unique_keywords
            print "T2| ternary: ", seq['teSeq']
            print "T3| tabs: ", seq['tbSeq']
            print "T3| spaces: ", seq['spSeq']
            print "T3| empty lines count: ", seq['emSeq']
            print "T3| whitespace: ", seq['wsSeq']
            print "T3| lines that start with open curly brackets: ", seq['cuSeq']  #
            print "T3| lines that start with end curly brackets: ", seq['clSeq']
            print "T3| balance of brackets: ", seq['cuSeq'] - seq['clSeq']
            print "T3| line starts with tab: ", seq['tsSeq']
            for keyword in javascript_keywords:
                print "T4| keyword count (" + keyword + "): ", seq[keyword + 'Seq']


if __name__ == "__main__":
    main()
