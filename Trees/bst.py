__author__ = 'VGN'
import unittest


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None  # of type BSTNode
        self.right = None  # of type BSTNode
        self.parent = None  # of type BSTNode

    def __repr__(self):
        return str(self.key)


class BST:
    """Binary Search Tree implementation with property left_subtree <= root <= right_subtree"""

    def __init__(self, root):
        self.root = root  # of type BSTNode

    def search(self, key):
        if self._recursive_search(self.root, key) is None:
            return False
        return True

    def insert(self, key):
        self._recursive_insert(self.root, key)

    def find_min(self):
        if self.root is None:
            raise Exception("No min in empty tree")
        return self._recursive_min(self.root).key

    def find_max(self):
        if self.root is None:
            raise Exception("No max in empty tree")
        return self._recursive_max(self.root).key

    def inorder_traversal(self):
        output_list = list()
        self._recursive_inorder_traversal(self.root, output_list)
        return output_list

    def delete(self, key):
        bstnode = self._recursive_search(self.root, key)
        #case 1 when bstnode is leaf node
        if bstnode.left is None and bstnode.right is None:
            self._delete_node_leaf(bstnode)
        #case 2 when bstnode has 1 child
        elif bstnode.left is None or bstnode.right is None:
            self._delete_node_one_child(bstnode)
        #case 3 when bstnode has 2 children
        else:
            predecessor = self._predecessor_node(key)
            #swap node with predecessor
            tmp = bstnode.key
            bstnode.key = predecessor.key
            predecessor.key = tmp
            # now delete predecessor
            if predecessor.left is None:
                #case 1
                self._delete_node_leaf(predecessor)
            else:
                #case 2
                self._delete_node_one_child(predecessor)
            predecessor = bstnode
        bstnode = None

    def _delete_node_leaf(self, bstnode):
        """
        case1: delete node with no children/leaf node
        :param bstnode:
        :return:
        """
        parent = bstnode.parent
        if parent.left == bstnode:
            parent.left = None
        else:
            parent.right = None

    def _delete_node_one_child(self, bstnode):
        """
        case2: delete node with 1 child(either left/right)
        :param bstnode:
        :return:
        """
        if bstnode.left is None:
            child = bstnode.right
        else:
            child = bstnode.left
        parent = bstnode.parent
        if parent.left == bstnode:
            parent.left = child
        else:
            parent.right = child

    def predecessor(self, key):
            node = self._predecessor_node(key)
            if node is None:
                return node
            return node.key

    def _predecessor_node(self, key):
        bstnode = self._recursive_search(self.root, key)
        # max value in left subtree
        if bstnode.left is not None:
            return self._recursive_max(bstnode.left)
        else:
            # follow parent pointers until you get smaller key
            parent = bstnode.parent
            while parent is not None:
                if parent.key < bstnode.key:
                    return parent
                parent = parent.parent
            return None

    def _recursive_delete(self, bstnode, key):
        if bstnode is None:
            raise Exception("key not found in BST")
        # successful search
        if bstnode.key == key:
            return bstnode
        elif bstnode.key >= key:
            bst_left = self._recursive_delete(bstnode.left, key)
            if bst_left.left is None and bst_left.right is None: # leaf node
                bstnode.left = None
        else:
            bst_right = self._recursive_delete(bstnode.right, key)
            if bst_right.left is None and bst_right.right is None: # leaf node
                bstnode.right = None
        return bstnode

    def _recursive_inorder_traversal(self, bstnode, output_list):
        if bstnode is None:
            return
        self._recursive_inorder_traversal(bstnode.left, output_list)
        output_list.append(bstnode.key)
        self._recursive_inorder_traversal(bstnode.right, output_list)

    def _recursive_max(self, bstnode):
        if bstnode.right is None:
            return bstnode
        return self._recursive_max(bstnode.right)

    def _recursive_min(self, bstnode):
        if bstnode.left is None:
            return bstnode
        return self._recursive_min(bstnode.left)

    def _recursive_search(self, bstnode, key):
        # unsuccessful search
        if bstnode is None:
            return None
        # successful search
        if bstnode.key == key:
            return bstnode
        elif bstnode.key >= key:
            return self._recursive_search(bstnode.left, key)
        else:
            return self._recursive_search(bstnode.right, key)

    def _recursive_insert(self, bstnode, key):
        if bstnode is None:
            return BSTNode(key)
        # successful search
        if bstnode.key == key:
            return bstnode
        elif bstnode.key >= key:
            bst_left = self._recursive_insert(bstnode.left, key)
            bstnode.left = bst_left
            bst_left.parent = bstnode
        else:
            bst_right = self._recursive_insert(bstnode.right, key)
            bstnode.right = bst_right
            bst_right.parent = bstnode
        return bstnode


class BSTTest(unittest.TestCase):
    def construct_binary_tree(self):
        root = BSTNode(3)
        root_left = BSTNode(1)
        root_right = BSTNode(5)
        root_left_right = BSTNode(2)
        root_right_left = BSTNode(4)
        root.left = root_left
        root.right = root_right
        root_left.parent = root
        root_right.parent = root
        root_left.right = root_left_right
        root_right.left = root_right_left
        root_left_right.parent = root_left
        root_right_left.parent = root_right
        bst = BST(root)
        return bst

    def test_search_positive(self):
        bst = self.construct_binary_tree()
        self.assertTrue(bst.search(3))

    def test_search_negative(self):
        bst = self.construct_binary_tree()
        self.assertFalse(bst.search(9))

    def test_insert_positive(self):
        bst = self.construct_binary_tree()
        bst.insert(9)
        self.assertTrue(bst.search(9))

    def test_min(self):
        bst = self.construct_binary_tree()
        self.assertTrue(bst.find_min() == 1)
        bst.insert(0)
        self.assertTrue(bst.find_min() == 0)

    def test_max(self):
        bst = self.construct_binary_tree()
        self.assertTrue(bst.find_max() == 5)
        bst.insert(9)
        self.assertTrue(bst.find_max() == 9)

    def test_inorder_traversal(self):
        bst = self.construct_binary_tree()
        self.assertTrue(bst.inorder_traversal() == [1, 2, 3, 4, 5])

    def test_delete_leaf(self):
        bst = self.construct_binary_tree()
        self.assertTrue(bst.search(4))
        bst.delete(4)
        self.assertFalse(bst.search(4))
        self.assertTrue(bst.search(5))
        bst.delete(5)
        self.assertFalse(bst.search(5))
        self.assertTrue(bst.find_max() == 3)

    def test_delete_one_child_node(self):
        bst = self.construct_binary_tree()
        bst.delete(5)
        self.assertFalse(bst.search(5))
        self.assertTrue(bst.search(4))
        self.assertTrue(bst.find_max() == 4)

    def test_predecssor(self):
        bst = self.construct_binary_tree()
        self.assertTrue(bst.predecessor(3) == 2)
        self.assertTrue(bst.predecessor(4) == 3)
        self.assertTrue(bst.predecessor(2) == 1)
        self.assertIsNone(bst.predecessor(1))

    def test_delete_two_children_node(self):
        bst = self.construct_binary_tree()
        bst.insert(9)
        bst.delete(5)
        self.assertTrue(bst.search(9))
        self.assertTrue(bst.search(4))





if __name__ == '__main__':
    unittest.main()


