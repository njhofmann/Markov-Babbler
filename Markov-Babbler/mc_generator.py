class Markov_Chain:
    """From an input .txt file, generates a Markov Chain of all words in file"""
    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
        self.converted_file = self.file_to_string()
        self.output_mc = self.create_markov_chain()

    def unique_items(self, list):
        #Takes in a list, produces ouput list of each unique item in input list
        items = []
        for i in list:
            if i not in items:
                items.append(i)
        return items

    def file_to_string(self):
        #Takes the text in input file and converts it into one long string
        f = open(self.file_to_read)
        string = f.read()
        return string

    def clean_input_text(self, text):
        #Takes in file_to_string output, makes it a list where each word is a list,
        #erases all unwanted characters like periods and colons, then lowers all letters
        text = text.split()
        errors = [".", ",", "(", ")", ":", ";", "?", "!", "-"]
        for pos, word in enumerate(text):
            n = ""
            for l in word:
                if l not in errors:
                    n += l
            text[pos] = n.lower()

        return text

    def generate_word_pairs(self, text):
        #Takes in output text from file_to_string, makes a list of all two words next to each other
        word_pairs = []
        for pos in range(len(text)):
            if pos != (len(text) - 1):
                word_pairs.append(text[pos:pos + 2])
            else:
                word_pairs.append([text[pos], text[0]])
        return word_pairs

    def create_markov_chain(self):
        #Creates Markov Chain from
        mc = {}
        cleaned_text = self.clean_input_text(self.converted_file)
        words = self.unique_items(cleaned_text)
        word_pairs = self.generate_word_pairs(cleaned_text)
        unique_wp = self.unique_items(word_pairs)

        #Creates starting dictionary of every unique word in file
        for w in words:
            mc[w] = {}


        for w in mc:
            t = 0 #How many times word appears in file
            c = 0 #How many times iterated word appeared in previous word_pairs that had word as first element
            for pair in word_pairs:
                if pair[0] == w: #If first word in iterated word pair matches iterated word, add 1 to t
                    t += 1

            for wp in unique_wp: #Iterates over each unique word_pair
                if wp[0] == w: #If first word in unique word_pair matches currently iterated word
                    a = 0 #How many times does unique word pair appear in file
                    l = []
                    for pair in word_pairs: #Iterates over ALL word_pairs in file
                        if wp == pair: #If iterated unique word_pair matches iterated word_pair in list of ALL word_pairs
                            a += 1

                    for num in range(c, a + c): #Creates range from how many times word appear before to c + how many times
                                                #word appeared in current iterated word_pair
                        l.append(num)
                    c += a
                    mc[w][wp[1]] = l #Adds unique word_pair and its generated range into Markov Chain for currently iterated word
            mc[w] = [t, mc[w]] #Replaces dictionary value of each word with list

        return mc
