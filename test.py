import collections
import random
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


def tokenize(code):
    token_specification = [
        ('WORD', r'\w+'),
        ('OTHER', r'\W+'),
        ('NEWLINE', r'\n'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            yield Token(kind, value, line_num, 0)
        else:
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


words = {}


def gen(word: str):
    if word in words:
        return words[word]
    # todo generate
    length = len(word)
    all_upper = word.upper() == word
    first_upper = word[0].upper() == word[0]

    new_word = ''
    for i in range(length):
        new_word += chr(random.randint(ord('a'), ord('z')))

    if all_upper:
        new_word = new_word.upper()
    elif first_upper:
        new_word = new_word[0].upper() + new_word[1:]

    words[word] = new_word
    return new_word


statements = '''
A, Fairy TALE is a type of short story that typically features folkloric fantasy characters, such as dwarves, elves,
fairies, giants, gnomes, goblins, mermaids, trolls, unicorns, or witches, and usually magic or enchantments.
Fairy tales may be distinguished from other folk narratives such as legends (which generally involve belief in the
veracity of the events described)[1] and explicitly moral tales, including beast fables. The term is mainly used for
stories with origins in European tradition and, at least in recent centuries, mostly relates to children's literature.
'''

random.seed('uprt')

print(statements)

for token in tokenize(statements):
    if token.type == 'WORD':
        print(gen(token.value), end='')
    else:
        print(token.value, end='')