import re
import random


class MarkovChain:

    def __init__(self):
        # Mapping of unique words to all possible words that followed it.
        self.markov_chain = dict()

        # The current state of this MarkovChain, or what key is it currently on.
        self.current_state = ()

        # 2D array of the formatted contents of all strings and files added to this Markov Chain. Used to recompute
        # the Markov Chain when the order changes.
        self.history = []

        # The current order of this Markov Chain, or how many prior states are considered when producing the next
        # state of this Markov Chain. Should always be > 0.
        self.order = 2

    def add_string(self, string):
        """
        Given a string - properly formats it, converts it to a list of each word, stores it in the history, then adds it
        tog this Markov Chain.
        :param string: string to format and add
        :return: None
        """
        cleaned_text = re.split(' +|-|\n+', string)
        errors = re.compile('\.|,|\(|\)|:|;|\?|!|"')
        for idx in range(len(cleaned_text)):
            word = cleaned_text[idx]
            word = word.lower()
            word = errors.sub('', word)
            cleaned_text[idx] = word
        self.history.append(cleaned_text)
        self.add_to_markov_chain(cleaned_text)

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

    def add_to_markov_chain(self, formatted_text):
        """
        Given a list of formatted text, adds its contents to this Markov Chain. Each order length number of elements,
        found by preceding down the list element by element, is added to the Markov Chain as is is the following
        element.
        :param formatted_text: list of text to add to this Markov Chain
        :return: None
        """
        for idx, word in enumerate(formatted_text):
            if (idx + self.order) <= (len(formatted_text) - 1):  # Last state has nothing that follows it
                cur_state = []

                for next_word_idx in range(self.order):
                    next_word = formatted_text[idx + next_word_idx]
                    cur_state.append(next_word)

                cur_state = tuple(cur_state)

                following_word = formatted_text[idx + self.order]
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
        elif new_order != self.order:
            self.order = new_order
            self.markov_chain = {}
            self.current_state = ()

            for stored_text in self.history:
                self.add_to_markov_chain(stored_text)

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

    def generate_sentence(self, sentence_length):
        """
        Returns a sentence of the given sentence length (X) by stringing together the results of X calls to
        next_state(), then applying capitalization to the first letter and adding a random ending punctuation to the
        end.
        :param sentence_length: length of sentence to produce
        :return: sentenced of variable length produced by this Markov Chain
        """
        result = ''
        for i in range(sentence_length):
            to_add = self.next_state()

            if to_add is None:
                return ''

            result += to_add

            if i != sentence_length - 1:
                result += ' '

        endings = ['.', '!', '?']
        endings_weights = [8, 1, 1]
        ending = random.choices(endings, endings_weights)[0]
        return result[0].upper() + result[1:] + ending
