from unittest import TestCase
from src.markov_chain import MarkovChain
from tests.equal_dicts import equal_dicts


class TestMarkovChain(TestCase):

    def test_first_order_words_simple(self):
        mc = MarkovChain()
        mc.order = 1
        mc.add_string('The quick brown fox jumps over the lazy fox.')

        actual_chain = {('the',): ['quick', 'lazy'],
                        ('quick',): ['brown'],
                        ('brown',): ['fox'],
                        ('fox',): ['jumps'],
                        ('jumps',): ['over'],
                        ('over',): ['the'],
                        ('lazy',): ['fox']}

        self.assertTrue(equal_dicts(mc.markov_chain, actual_chain))

    def test_first_order_words_complex(self):
        mc = MarkovChain()
        mc.order = 1
        mc.add_string('I felt happy because I saw the others were happy and because I knew I should feel happy, but I '
                      'was not really happy.')

        actual_chain = {('i',): ['felt', 'saw', 'knew', 'should', 'was'],
                        ('felt',): ['happy'],
                        ('happy',): ['because', 'and', 'but'],
                        ('because',): ['i', 'i'],
                        ('saw',): ['the'],
                        ('the',): ['others'],
                        ('others',): ['were'],
                        ('were',): ['happy'],
                        ('and',): ['because'],
                        ('knew',): ['i'],
                        ('should',): ['feel'],
                        ('feel',): ['happy'],
                        ('but',): ['i'],
                        ('was',): ['not'],
                        ('not',): ['really'],
                        ('really',): ['happy']}

        self.assertTrue(equal_dicts(mc.markov_chain, actual_chain))


    def test_two_order_words_complex(self):
        pass

    def test_first_order_chars_simple(self):
        mc = MarkovChain()
        mc.order = 1
        mc.set_production_state_to_chars()
        mc.add_chars('pneumonoultramicroscopicsilicovolcanoconiosis')

        actual_chain = {('p',): ['n', 'i'],
                        ('n',): ['e', 'o', 'o', 'i'],
                        ('e',): ['u'],
                        ('u',): ['m', 'l'],
                        ('m',): ['o', 'i'],
                        ('o',): ['n', 'u', 's', 'p', 'v', 'l', 'c', 'n', 's'],
                        ('l',): ['t', 'i', 'c'],
                        ('t',): ['r'],
                        ('r',): ['a', 'o'],
                        ('a',): ['m', 'n'],
                        ('i',): ['c', 'c', 'l', 'c', 'o', 's'],
                        ('c',): ['r', 'o', 's', 'o', 'a', 'o'],
                        ('s',): ['c', 'i', 'i'],
                        ('v',): ['o']}

        self.assertTrue(equal_dicts(actual_chain, mc.markov_chain))
