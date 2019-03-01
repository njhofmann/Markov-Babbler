from unittest import TestCase
import random


def equal_dicts(a, b):
    """
    Returns if two dictionaries in the form of "key -> list of values" are "equal" in the sense each dict contains the
    same set of keys, and each key in both dicts has lists of values with the same set of items (independent of ordering
    or non-unique items)
    :param a: first dict to check
    :param b: second dict to check
    :return: true if above conditions for "equality" are met by a and b
    """
    if len(a) != len(b):
        return False

    for key, value in a.items():
        if key not in b:
            return False

        b_value = b.get(key)

        value = sorted(value)
        b_value = sorted(b_value)

        value_length = len(value)
        if value_length != len(b_value):
            return False

        for idx in range(value_length):
            if value[idx] != b_value[idx]:
                return False

    return True


class TestEqualDicts(TestCase):

    def test_two_empty_dicts(self):
        a = {}
        b = {}
        self.assertTrue(equal_dicts(a, b))

    def test_a_is_empty(self):
        a = {}
        b = {'a': []}
        self.assertFalse(equal_dicts(a, b))

    def test_b_is_empty(self):
        a = {'a': []}
        b = {}
        self.assertFalse(equal_dicts(a, b))

    def test_one_key_empty_lists(self):
        a = {'a': []}
        b = {'a': []}
        self.assertTrue(equal_dicts(a, b))

    def test_one_key_one_empty_list(self):
        a = {'a': ['foo', 'bar']}
        b = {'a': []}
        self.assertFalse(equal_dicts(a, b))

    def test_one_key_one_element_same(self):
        a = {'a': ['foo']}
        b = {'a': ['foo']}
        self.assertTrue((equal_dicts(a, b)))

    def test_one_key_one_element_diff(self):
        a = {'a': ['foo']}
        b = {'a': ['bar']}
        self.assertFalse((equal_dicts(a, b)))

    def test_one_key_one_element_same_length(self):
        a = {'a': ['foo', 'foo', 'foo']}
        b = {'a': ['foo', 'foo', 'foo']}
        self.assertTrue((equal_dicts(a, b)))

    def test_one_key_one_element_diff_length(self):
        a = {'a': ['foo', 'foo', 'foo']}
        b = {'a': ['foo', 'foo']}
        self.assertFalse(equal_dicts(a, b))

    def test_one_key_same_lists_unique_same_ordering(self):
        a = {'a': ['foo', 'bar', 'boo']}
        b = {'a': ['foo', 'bar', 'boo']}
        self.assertTrue(equal_dicts(a, b))

    def test_one_key_same_lists_duplicate_same_ordering(self):
        a = {'a': ['foo', 'bar', 'boo', 'bar', 'foo']}
        b = {'a': ['foo', 'bar', 'boo', 'bar', 'foo']}
        self.assertTrue(equal_dicts(a, b))

    def test_one_key_same_lists_unique_diff_ordering(self):
        a = {'a': ['boo', 'foo', 'bar']}
        b = {'a': ['foo', 'bar', 'boo']}
        self.assertTrue(equal_dicts(a, b))

    def test_one_key_same_lists_duplicate_diff_ordering(self):
        a = {'a': ['boo', 'foo', 'bar',  'bar', 'foo']}
        b = {'a': ['foo', 'bar', 'boo', 'bar', 'foo']}
        self.assertTrue(equal_dicts(a, b))

    def test_two_elements(self):
        a = {'a': ['boo', 'foo', 'bar', 'bar', 'foo'],
             'b': ['woo', 'hah', 'woo', 'bor']}
        b = {'a': ['foo', 'bar', 'boo', 'bar', 'foo'],
             'b': ['hah', 'woo', 'woo', 'bor']}
        self.assertTrue(equal_dicts(a, b))

    def test_large_random_dicts(self):
        for j in range(1000):
            a = {}
            b = {}
            for idx in range(random.randint(10, 100)):
                values = [i for i in range(idx)]
                random.shuffle(values)
                a[idx] = values
                random.shuffle(values)
                b[idx] = values

            self.assertTrue(equal_dicts(a, b))