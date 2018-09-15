import enum
class Content(enum.Enum):
    """
    Enum specifying which type of content a MarkovChain should work with, words or chars.
    """
    WORDS = 'words'
    CHARS = 'chars'

a = Content.WORDS
print(a is Content.WORDS)