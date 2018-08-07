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

        :param string:
        :return:
        """
        cleaned_text = self.format_and_store(string)
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

        # Format the file's contents and store them in the history.
        cleaned_text = self.format_and_store(file_contents)

        # Add the formatted text to the current Markov Chain
        self.add_to_markov_chain(cleaned_text)

    def format_and_store(self, string):
        """

        :param string:
        :return:
        """
        cleaned_text = re.split(' +|-|\n+', string)
        errors = re.compile('\.|,|\(|\)|:|;|\?|!|"')
        for idx in range(len(cleaned_text)):
            word = cleaned_text[idx]
            word = word.lower()
            word = errors.sub('', word)
            cleaned_text[idx] = word
        self.history.append(cleaned_text)
        return cleaned_text

    def add_to_markov_chain(self, formatted_text):
        """

        :param formatted_text:
        :return:
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
        Recomputes this Markov Chain based off the new given order.
        :param new_order:
        :return: None
        """
        if new_order < 1:
            raise ValueError('And order must be > 0!')

        self.markov_chain = {}
        self.current_state = ()
        self.order = new_order
        for stored_text in self.history:
            self.add_to_markov_chain(stored_text)

    def next_state(self):
        """
        Selects and returns the next state of this Markov chain based off this Markov Chain's current state.
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

        :param sentence_length:
        :return:
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
