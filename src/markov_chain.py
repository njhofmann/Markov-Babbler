import re
import random

class MarkovChain:

    def __init__(self):
        # Mapping of unique words to all possible words that followed it.
        self.markov_chain = dict()

        # The current state of this MarkovChain, or what key is it currently on.
        self.current_state = ''

    def add_file(self, file):
        """

        :param file:
        :return:
        """

        # Attempt to open given file and output its contents
        try:
            f = open(file)
        except IOError:
            return ""
        file_contents = f.read()

        # Clean the file's contents and convert them
        cleaned_text = re.split(' +|-|\n+', file_contents)
        errors = [".", ",", "(", ")", ":", ";", "?", "!", '"']
        for pos, word in enumerate(cleaned_text):
            n = ""
            for l in word:
                if l not in errors:
                    n += l
            cleaned_text[pos] = n.lower()

        # Now for each element in the cleaned text, see if the element has already been added to this Markov Chain - if
        # not create a new entry for it. Then add the next element to the current element's value list.
        for idx, word in enumerate(cleaned_text):
            if word not in self.markov_chain:
                self.markov_chain[word] = []

            if idx < (len(cleaned_text) - 1): # Last word has nothing that follows it
                next_word = cleaned_text[idx + 1]
                self.markov_chain[word].append(next_word)


    def next_state(self):
        """

        :return: the next selected state of this Markov Chain
        """
        if self.current_state == '':
            self.current_state = random.choice(list(self.markov_chain.keys()))
        else:
            possible_next_states = self.markov_chain[self.current_state]
            self.current_state = random.choice(list(possible_next_states))

        return self.current_state