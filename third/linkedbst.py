"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from random import sample
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root

        while node is not None:
            if item == node.data:
                return node.data

            if item < node.data:
                node = node.left
            else:
                node = node.right

        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        node = self._root
        # Helper function to search for item's position

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            while node != None:
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmaxinleft(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currrent_node = top.left
            while not currrent_node.right == None:
                parent = currrent_node
                currrent_node = currrent_node.right
            top.data = currrent_node.data
            if parent == top:
                top.left = currrent_node.left
            else:
                parent.right = currrent_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        removed = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currrent_node = self._root
        while not currrent_node == None:
            if currrent_node.data == item:
                removed = currrent_node.data
                break
            parent = currrent_node
            if currrent_node.data > item:
                direction = 'L'
                currrent_node = currrent_node.left
            else:
                direction = 'R'
                currrent_node = currrent_node.right

        # Return None if the item is absent
        if removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currrent_node.left == None \
                and not currrent_node.right == None:
            liftmaxinleft(currrent_node)
        else:

            # Case 2: The node has no left child
            if currrent_node.left == None:
                new_child = currrent_node.right

                # Case 3: The node has no right child
            else:
                new_child = currrent_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                olddata = probe.data
                probe.data = new_item
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size
        return height < 2*log(size+1, 2)-1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        edited = self.inorder()
        result = []
        for element in edited:
            if low <= element <= high:
                result.append(element)
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def recursive(tree, first, last):
            if first <= last:
                middle = (first + last) // 2
                self.add(tree[middle])
                recursive(tree, first, middle - 1)
                recursive(tree, middle + 1, last)
        if not self.is_balanced():
            tree = list(self.inorder())
            self.clear()
            recursive(tree, 0, len(tree) - 1)
        # return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        items = []
        for element in self:
            if element > item:
                items.append(element)
        return min(items) if len(items) != 0 else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        items = []
        for element in self:
            if element < item:
                items.append(element)
        return max(items) if len(items) != 0 else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r") as data:
            words = []
            for line in data:
                words += line.split()
        words = sorted(sample(words, 10000))
        random_words = sample(words, 1000)
        start = time.time()
        for element in random_words:
            if element in words:
                pass
        end = time.time()
        # tree in alphabet
        tree = LinkedBST()
        for element in words:
            tree.add(element)
        time1 = time.time()
        for element in random_words:
            if element in tree:
                pass
        end1 = time.time()
        # tree not in alphabet
        sampled_word = sample(words, len(words))
        tree1 = LinkedBST()
        for element in sampled_word:
            tree1.add(element)
        time2 = time.time()
        for element in random_words:
            if element in tree1:
                pass
        end2 = time.time()
        # rebalanced tree
        tree1.rebalance()
        time3 = time.time()
        for element in random_words:
            if element in tree1:
                pass
        end3 = time.time()
        print(
            f"Час пошуку 1000 слів з використанням методів вбудованого типу list: {end - start} сек")
        print(
            f"Час пошуку 1000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку, яке будується на основі послідовного додавання в дерево слів зі словника, який впорядкований за абеткою: {end1 - time1} сек")
        print(
            f"Час пошуку 1000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку, яке будується на основі послідовного додавання в дерево слів зі словника який не впорядкований за абеткою (слова у дерево додаються випадковим чином): {end2 - time2} сек")
        print(
            f"Час пошуку 1000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку, яке будується на основі послідовного додавання в дерево слів зі словника який не впорядкований за абеткою (слова у дерево додаються випадковим чином): {end3 - time3} сек")


# if __name__ == '__main__':
#     bst = LinkedBST()

#     # bst.add(5)
#     # bst.add(3)
#     # bst.add(6)
#     # bst.add(1)
#     # bst.add(4)
#     # print(bst.range_find(4, 7))
#     a = LinkedBST()
#     a.demo_bst("words.txt")
