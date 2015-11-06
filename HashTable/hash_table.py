__author__ = 'VGN'

import unittest


class ChainingHashTable:
    """
     class which implements the hash table using chaining
    """

    _primes = [
        7, 13, 31, 61, 127, 251, 509, 1021, 2039, 4093, 8191, 16381,
       32749, 65521, 131071, 262139, 524287, 1048573, 2097143, 4194301,
        8388593, 16777213, 33554393, 67108859, 134217689, 268435399,
        536870909, 1073741789, 2147483647]

    def __init__(self):
        self._list_current_size_index = 0 # to keep track of the position of the primes(which keeps track of the size of the chaining list
        self._bucket_size = ChainingHashTable._primes[self._list_current_size_index]
        self._chaining_list = self._init_list(self._bucket_size)
        self.keys_size = 0  # size of keys
        self._key_list = list() # to keep track of keys to return as iterable

    def _init_list(self, size):
        input_list = list()
        for i in range(0, size):
            input_list.append(None)
        return input_list

    def __setitem__(self, key, value):
        if self.keys_size >= 10 * self._bucket_size:
            self._list_current_size_index +=1
            self._bucket_size = ChainingHashTable._primes[self._list_current_size_index]
            self._resize(self._bucket_size)
        self._insert(self._chaining_list, key, value)

    def _insert(self, input_list, key, value):
        index = hash(key) % len(input_list)
        if input_list[index] is None:
            input_list[index] = Node(key, value)
            self.keys_size += 1
            self._key_list.append(key)
        else:
            #search if given key exists
            node = self._get_node(input_list, key)
            if node is not None:
                node.value = value
            else:
                #key does not exist
                first = input_list[index]
                tmp = first
                first = Node(key, value)
                first.next = tmp
                input_list[index] = first
                self.keys_size += 1
                self._key_list.append(key)

    def __getitem__(self, key):
        node = self._get_node(self._chaining_list, key)
        if node is None:
            return node
        else:
            return node.value

    def _get_node(self, input_list, key):
        index = hash(key) % len(input_list)
        if input_list[index] is None:
            return None
        first = input_list[index]
        while first is not None:
            if first.key == key:
                return first
            first = first.next
        return None

    def _resize(self, size):
        self.keys_size = 0 # reset to 0
        tmp_list = self._init_list(size)
        for i in range(0, len(self._chaining_list)):
            keys = self._get_keys(i)
            for key in keys:
                value = self._get_node(self._chaining_list, key).value
                self._insert(tmp_list, key, value)
        self._chaining_list = tmp_list

    def __iter__(self):
        """
        iter_list = list()
        for index in range(0, self._bucket_size):
            iter_list += self._get_keys(index)
        """
        return iter(self._key_list)

    def _get_keys(self, index):
        """ Get list of keys at specific index"""
        key_list = list()
        first = self._chaining_list[index]
        if first is None:
            return key_list
        while first is not None:
            key_list.append(first.key)
            first = first.next
        return key_list


class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None # of type Node


class HashTableTest(unittest.TestCase):
    """Test class for verifying hash table"""

    def test1(self):
        chaining_table = ChainingHashTable()
        chaining_table[20] = "hello"
        chaining_table[30] = "dorje"
        chaining_table[30] = "maka"
        self.assertTrue(chaining_table[20] == "hello")
        self.assertTrue(chaining_table[30] == "maka")
        for i in chaining_table:
            print i

if __name__ == '__main__':
    unittest.main()



