import re


class MarkovChain:
    """
    From one or more inputted .txt file, generates a Markov Chain of all the words in those files.
    """

    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
        self.converted_file = self.file_to_string()
        self.output_mc = self.create_markov_chain()

    def unique_items(self, list):
        """
        Takes in a list, produces output list of each unique item in input list
        :param list: the list to read
        :return: list of each unique item in given list
        """
        items = []
        for i in list:
            if i not in items:
                items.append(i)
        return items

    def file_to_string(self):
        """
        Takes the text in input file and converts it into one long string
        :return: String of all words in given input file
        """
        try:
            f = open(self.file_to_read)
        except IOError:
            return ""
        string = f.read()
        return string

    def clean_string(self, text):
        """
        Takes in a string and converts it to a list where each word (as designated by whitespace or a hypen) is an
        element, removes all unwanted characters from each word (like periods and colons) and sets every letter to
        lowercase
        :param text: string to format
        :return: formatted list of strings
        """
        text = re.split(' +|-', text)
        errors = [".", ",", "(", ")", ":", ";", "?", "!", '"']
        for pos, word in enumerate(text):
            n = ""
            for l in word:
                if l not in errors:
                    n += l
            text[pos] = n.lower()

        return text

    def generate_word_pairs(self, text):
        """
        Takes in output text from file_to_string, makes a list of all two words next to each other
        :param text:
        :return:
        """
        word_pairs = []
        for pos in range(len(text)):
            if pos != (len(text) - 1):
                word_pairs.append(text[pos:pos + 2])
            else:
                word_pairs.append([text[pos], text[0]])
        return word_pairs

    # Creates Markov Chain from
    def create_markov_chain(self):
        mc = {}
        cleaned_text = self.clean_string(self.converted_file)
        words = self.unique_items(cleaned_text)
        word_pairs = self.generate_word_pairs(cleaned_text)
        unique_wp = self.unique_items(word_pairs)

        # Creates starting dictionary of every unique word in file
        for w in words:
            mc[w] = {}

        for w in mc:
            t = 0  # How many times word appears in file
            c = 0  # How many times iterated word appeared in previous word_pairs that had word as first element
            for pair in word_pairs:
                if pair[0] == w:  # If first word in iterated word pair matches iterated word, add 1 to t
                    t += 1

            for wp in unique_wp:  # Iterates over each unique word_pair
                if wp[0] == w:  # If first word in unique word_pair matches currently iterated word
                    a = 0  # How many times does unique word pair appear in file
                    l = []
                    for pair in word_pairs:  # Iterates over ALL word_pairs in file
                        if wp == pair:  # If iterated unique word_pair matches iterated word_pair in list of ALL
                                        # word_pairs
                            a += 1

                    for num in range(c, a + c):  # Creates range from how many times word appear before to c + how many
                                                 # times word appeared in current iterated word_pair
                        l.append(num)
                    c += a
                    mc[w][wp[
                        1]] = l  # Adds unique word_pair and its generated range into Markov Chain for currently
                                 # word currently being iterated over
            mc[w] = [t, mc[w]]  # Replaces dictionary value of each word with list

        return mc
