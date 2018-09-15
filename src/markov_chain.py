import re
import random
import enum


class Content(enum.Enum):
    """
    Enum specifying which type of content a MarkovChain should work with, words or chars.
    """
    WORDS = 'words'
    CHARS = 'chars'


class MarkovChain:
    """
    Represents a N-order Markov Chain computed from the contents of added files and strings, then produces
    pseudo-comprehensible word orderings or text based off current order, and the words and their ordering of added
    strings.
    """

    def __init__(self):
        # Mapping of unique words to all possible words that followed it.
        self.markov_chain = dict()

        # The current state of this MarkovChain, or what key is it currently on.
        self.current_state = ()

        # Single string of the formatted contents of all strings and files added to this Markov Chain. Used to recompute
        # the Markov Chain when the order or production state changes.
        self.history = ''

        # The current order of this Markov Chain, or how many prior states are considered when producing the next
        # state of this Markov Chain. Should always be > 0.
        self.order = 2

        # The content this MarkovChain is currently producing as per the Content enum, either words or chars.
        self._production_state = Content.WORDS

    def set_production_state_to_words(self):
        """
        Sets this Markov Chain to work with words.
        :return: None
        """
        self._production_state = Content.WORDS

    def set_production_state_to_chars(self):
        """
        Sets this Markov Chain to work with individual characters.
        :return: None
        """
        self._production_state = Content.CHARS

    def add_string(self, string):
        """
        Given a string - properly formats it, converts it to a list of each word, stores it in the history, then adds it
        tog this Markov Chain.
        :param string: string to format and add
        :return: None
        """
        replace_errors = re.compile('[.,():;?!"]')
        space_errors = re.compile('\n+|-')

        string = string.lower()
        string = replace_errors.sub('', string)
        string = space_errors.sub(' ', string)

        self.history += string
        if self._production_state is Content.WORDS:
            self.add_word(string)
        elif self._production_state is Content.CHARS:
            self.add_chars(string)

    def add_file(self, file):
        """
        Grabs, formats, stores, and then adds the string contents of the file at the given file path to this Markov
        Chain.
        :param file: file path of the file to use
        :return: None
        """

        # Attempt to open given file and output its contents
        try:
            f = open(file)
        except IOError:
            return ""
        file_contents = f.read()

        self.add_string(file_contents)

    def add_word(self, formatted_text):
        """
        Same as add_chars, but with whole words (denoted by spaces) instead of individual characters.
        :param formatted_text: list of text to add to this Markov Chain
        :return: None
        """
        formatted_text = re.split(' +', formatted_text)
        self.add_chars(formatted_text)

    def add_chars(self, string):
        """
        Given a long string of words, adds its contents to this Markov Chain. Each order length number of chars,
        found by preceding down the list element by element, is added to the Markov Chain as is is the following
        element.
        :param string:
        :return:
        """
        for idx in range(len(string)):
            if (idx + self.order) <= (len(string) - 1):  # Last state has nothing that follows it
                cur_state = []

                for next_word_idx in range(self.order):
                    next_word = string[idx + next_word_idx]
                    cur_state.append(next_word)

                cur_state = tuple(cur_state)

                following_word = string[idx + self.order]

                if cur_state not in self.markov_chain:
                    self.markov_chain[cur_state] = [following_word]
                else:
                    self.markov_chain[cur_state].append(following_word)

    def recompute_markov_chain(self, new_order):
        """
        Recomputes this Markov Chain based off the new given order and the formatted contents of previously added
        strings and files. If the given new order is the same as the current order, no change is made.
        :param new_order: new order to base this Markov Chain off
        :return: None
        """
        if new_order < 1:
            raise ValueError('And order must be > 0!')
        else:
            self.order = new_order
            self.markov_chain = {}
            self.current_state = ()

            if self._production_state is Content.WORDS:
                self.add_word(self.history)
            elif self._production_state is Content.CHARS:
                self.add_chars(self.history)

    def recompute_markov_chain_with_words(self):
        """
        Recomputes this Markov Chain with words
        :return: None
        """
        self.set_production_state_to_words()
        self.recompute_markov_chain(self.order)

    def recompute_markov_chain_with_chars(self):
        """
        Recomputes this Markov Chain with words
        :return: None
        """
        self.set_production_state_to_chars()
        self.recompute_markov_chain(self.order)

    def next_state(self):
        """
        Selects and returns the next state of this Markov chain based off this Markov Chain's current state. If no
        current state has been selected, or the current state does not exist in the current markov chain - randomly
        selects one key.
        :return: the next selected state of this Markov Chain
        """
        if len(self.markov_chain) != 0:
            if self.current_state not in self.markov_chain:
                self.current_state = ()

            if len(self.current_state) == 0: # If current state hasn't been selected, select random key.
                self.current_state = random.choice(list(self.markov_chain.keys()))
            else:
                possible_next_states = self.markov_chain[self.current_state]
                next_state = random.choice(list(possible_next_states))
                temp_cur_state = list(self.current_state)
                temp_cur_state = temp_cur_state[1:]
                temp_cur_state.append(next_state)
                temp_cur_state = tuple(temp_cur_state)
                self.current_state = temp_cur_state
            return self.current_state[-1]

    def generate_sentence(self, sentence_length, grammar=True):
        """
        Returns a sentence of the given sentence length (X) by stringing together the results of X calls to
        next_state(), then applying capitalization to the first letter and adding a random ending punctuation to the
        end.
        :param sentence_length: length of sentence to produce
        :param grammar: whether or not to add capitalization and ending marks to the produced sentence
        :return: sentenced of variable length produced by this Markov Chain
        """
        result = ''
        for i in range(sentence_length):
            to_add = self.next_state()

            if to_add is None:
                return ''

            result += to_add

            if i != sentence_length - 1 and self._production_state is Content.WORDS:
                result += ' '

        if grammar:
            endings = ['.', '!', '?']
            endings_weights = [8, 1, 1]
            ending = random.choices(endings, endings_weights)[0]
            return result[0].upper() + result[1:] + ending

        return result
