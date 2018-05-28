import random as r

class Markov_Babbler:
    """From some input Markov Chain, generates a psuedo-random sentence"""
    def __init__(self, mc):
        self.mc = mc
        self.result = self.generate_markov_babbler()
        self.sentence = self.make_sentence()

    def generate_markov_babbler(self):
        #Creates random text from Markov Chain 8 to 15 words long
        output = ""
        is_first_word = True
        current_word = ""
        num_of_words = r.randint(8, 15)

        for num in range(num_of_words):
            if is_first_word == True: #Selects random first word from all words in MC
                current_word = r.choice(list(self.mc))
                is_first_word = False
            else:
                #Selects next word in MC based off perviously selected word
                rn = r.randint(0, self.mc[current_word][0] - 1)
                next_words = self.mc[current_word][1]

                for w in next_words:
                    if rn in next_words[w]:
                        current_word = w
            output += current_word + " "
        return output

    def make_sentence(self):
        #Cleans up randomly generated text to make it look like an actual sentence
        p = self.result
        end_puncs = {".":[0, 1, 2, 3, 4, 5, 6, 7], "?":[8], "!":[9]} #Possible ending punctuations
        what_punc = r.randint(0, 9)

        #Adds selected ending punc to random text
        for k in end_puncs:
            if what_punc in end_puncs[k]:
                p = p[0:len(p)-1] + k

        p = p[0].upper() + p[1:len(p)] #Capitalizes first word in text

        return p

