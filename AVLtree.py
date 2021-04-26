# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:09:11 2020

@author: VinLes
"""

import io
import sys
from collections import deque


# lets rewrite the print
def print_(e):
    sys.stdout.write(str(e) + "\n")


class Node:
    __slots__ = ["key", "left", "right", "height", "balance"]

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0
        self.balance = 0


class NodeHolder:
    __slots__ = ["node"]

    def __init__(self):
        self.node = None


class AVLTree:
    __slots__ = ["root"]

    def __init__(self):
        self.root = None

    def find(self, keyToFind, currentNode, parent):

        if currentNode == None:
            return currentNode, parent

        elif currentNode.key == keyToFind:
            return currentNode, parent

        elif currentNode.key > keyToFind:
            self.rebalance(currentNode.left)
            return self.find(keyToFind, currentNode.left.node, currentNode)

        elif currentNode.key < keyToFind:
            self.rebalance(currentNode.right)
            return self.find(keyToFind, currentNode.right.node, currentNode)

    def exists(self, key):

        if self.root == None:
            print_("false")
            return False

        if self.root.node == None:
            print_("false")
            return False

        nodeFound, parent = self.find(key, self.root.node, None)

        if nodeFound == None:
            print_("false")
            return False

        elif nodeFound.key == key:
            print_("true")
            return True

    def insert(self, key):

        if self.root == None or self.root.node == None:
            self.root = NodeHolder()
            self.root.node = Node(key)
            self.root.node.left = NodeHolder()
            self.root.node.right = NodeHolder()
            return

        nodeFound, parent = self.find(key, self.root.node, self.root.node)

        if nodeFound == None:
            if parent.key > key:
                parent.left.node = Node(key)
                parent.left.node.left = NodeHolder()
                parent.left.node.right = NodeHolder()

            elif parent.key < key:
                parent.right.node = Node(key)
                parent.right.node.left = NodeHolder()
                parent.right.node.right = NodeHolder()

            self.update_heights(self.root)
            self.update_balances(self.root)

        elif nodeFound.key == key:
            # print_("Key is already present!")
            return 'key_present'

    def delete(self, keyToDelete, currentNode, parent):

        if currentNode != None:
            if currentNode.node != None:

                if currentNode.node.key == keyToDelete:
                    if currentNode.node.left.node == None and currentNode.node.right.node == None:
                        currentNode.node = None

                    elif currentNode.node.left.node != None and currentNode.node.right.node == None:
                        currentNode.node = currentNode.node.left.node

                    elif currentNode.node.left.node == None and currentNode.node.right.node != None:
                        currentNode.node = currentNode.node.right.node

                    elif currentNode.node.left.node != None and currentNode.node.right.node != None:

                        # local successor
                        successor = currentNode.node.right.node
                        while successor and successor.left.node:
                            successor = successor.left.node

                        if successor:
                            currentNode.node.key = successor.key
                            self.delete(successor.key, currentNode.node.right,
                                        currentNode)

                elif currentNode.node.key > keyToDelete:
                    return self.delete(keyToDelete, currentNode.node.left,
                                       currentNode)

                elif currentNode.node.key < keyToDelete:
                    return self.delete(keyToDelete, currentNode.node.right,
                                       currentNode)

    def traverse(self, root):

        if root == None:
            return []
        if root.node == None:
            return []

        result = deque()
        nodes = [root]

        while len(nodes) != 0:
            n = nodes.pop()
            result.append(n.node.key)

            if n.node.left.node != None:
                nodes.append(n.node.left)

            if n.node.right.node != None:
                nodes.append(n.node.right)
        return result

    def update_heights(self, n):
        if n.node != None:
            if n.node.left != None:
                self.update_heights(n.node.left)
            if n.node.right != None:
                self.update_heights(n.node.right)

            if n.node.left.node != None and n.node.right.node != None:
                n.node.height = 1 + \
                    max(n.node.left.node.height, n.node.right.node.height)

            elif n.node.left.node != None and n.node.right.node == None:
                n.node.height = 1 + n.node.left.node.height

            elif n.node.left.node == None and n.node.right.node != None:
                n.node.height = 1 + n.node.right.node.height

            elif n.node.left.node == None and n.node.right.node == None:
                n.node.height = 0

    def update_balances(self, n):
        if n.node != None:
            if n.node.left != None:
                self.update_balances(n.node.left)
            if n.node.right != None:
                self.update_balances(n.node.right)

            if n.node.left.node != None and n.node.right.node != None:
                n.node.balance = n.node.left.node.height - n.node.right.node.height

            elif n.node.left.node != None and n.node.right.node == None:
                n.node.balance = n.node.left.node.height - (-1)

            elif n.node.left.node == None and n.node.right.node != None:
                n.node.balance = -1 - n.node.right.node.height

            elif n.node.left.node == None and n.node.right.node == None:
                n.node.balance = 0

    def rotate_right(self, n):
        """
        when YOUR tree lokes like this stick:
           /
          / <- leftNodeInTheMiddle
         /
        """
        leftNodeInTheMiddle = n.node.left.node
        nothingOrRight = leftNodeInTheMiddle.right.node
        oldRoot = n.node

        n.node = leftNodeInTheMiddle
        oldRoot.left.node = nothingOrRight
        leftNodeInTheMiddle.right.node = oldRoot

    def rotate_left(self, n):
        """
        when YOUR tree lokes like this stick:
        \
         \ <- rightNodeInTheMiddle
          \
        """
        # new root
        rightNodeInTheMiddle = n.node.right.node
        """ sometimes tree looks more comples then stick, like that :
         \
         /\
           \
         if node in the middle has left child thant see picture  "insert 6"
         if no you need return a particluar None object - here, my NodeHolder with None
        """
        nothingOrLeft = rightNodeInTheMiddle.left.node
        oldRoot = n.node

        n.node = rightNodeInTheMiddle
        oldRoot.right.node = nothingOrLeft
        rightNodeInTheMiddle.left.node = oldRoot

    def rebalance(self, n):

        if n != None and n.node != None:

            # update hights and calculate balances
            self.update_heights(n)
            self.update_balances(n)

            # if unbalanced, balance factor == 2 or -2
            while n.node.balance <= -2 or n.node.balance >= 2:
                # If balance is positive, then tree is heavier to the left
                if n.node.balance >= 2:

                    # Left Right Case, if new root is heavier on the right
                    if n.node.left.node.balance <= -1:
                        self.rotate_left(n.node.left)
                        self.update_heights(n)
                        self.update_balances(n)

                    # rotate right
                    self.rotate_right(n)
                    self.update_heights(n)
                    self.update_balances(n)

                # If balance is negative, then tree is heavier to the right
                if n.node.balance <= -2:
                    # Right Left Case, if new root is heavier on the left
                    if n.node.right.node.balance >= 1:
                        self.rotate_right(n.node.right)
                        self.update_heights(n)
                        self.update_balances(n)

                    # rotate left
                    self.rotate_left(n)
                    self.update_heights(n)
                    self.update_balances(n)

    def inorder_traverse(self, n):

        result = deque()

        if not n:
            return result
        if not n.node:
            return result

        if n.node.left.node != None:
            result.extend(self.inorder_traverse(n.node.left))

        result.append(n.node.key)

        if n.node.right.node != None:
            result.extend(self.inorder_traverse(n.node.right))

        return result

    def inorder_traverse_sup(self, n, key):

        result = deque()

        if not n:
            return result
        if not n.node:
            return result

        if n.node.left.node != None:
            if n.node.key >= key:
                result.extend(self.inorder_traverse_sup(n.node.left, key))

        if n.node.key >= key:
            result.append(n.node.key)

        if len(result) >= 2:
            return result

        if n.node.right.node != None:
            result.extend(self.inorder_traverse_sup(n.node.right, key))

        return result

    def inorder_traverse_pre(self, n, key):

        result = deque()

        if not n:
            return result
        if not n.node:
            return result

        if n.node.right.node != None:
            if n.node.key <= key:
                result.extend(self.inorder_traverse_pre(n.node.right, key))

        if n.node.key <= key:
            result.append(n.node.key)

        if len(result) >= 2:
            return result

        if n.node.left.node != None:
            result.extend(self.inorder_traverse_pre(n.node.left, key))

        return result

    def successor(self, key):
        nodes = self.inorder_traverse_sup(self.root, key)

        if len(nodes) >= 1:
            if nodes[0] != key:
                return nodes[0]
        if len(nodes) >= 2:
            return nodes[1]
        return 'none'

    def predecessor(self, key):

        nodes = self.inorder_traverse_pre(self.root, key)

        if len(nodes) >= 1:
            if nodes[0] != key:
                return nodes[0]
        if len(nodes) >= 2:
            return nodes[1]

        return 'none'


tree = AVLTree()

'''
Example:

insert 1
insert 10
insert -1
insert -1
exists 10
true
prev 1
-1
next 1
10
'''

while 1:

    op = [s.strip() for s in sys.stdin.readline().split()]

    if len(op) == 2:
        o = op[0]
        e = int(op[1])

        if o.startswith("i"):
            tree.insert(e)

        elif o.startswith("e"):
            tree.exists(e)

        elif o.startswith("p"):
            print_(tree.predecessor(e))

        elif o.startswith("n"):
            print_(tree.successor(e))

        elif o.startswith("d"):
            tree.delete(e, tree.root, None)

    else:
        break
