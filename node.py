#!/usr/bin/python3

"""
This module implements the Node data type as an auxiliary data structure.

@author           Javier Candeira, based on Java code by
                  Maria Garcia de la Band and Brendon Taylor
@since            6th February 2013
@input            none
@output           none
@errorHandling    none
@knownBugs        none
"""

class Node:
    """
    Nodes where items are stored in the queue.
    """

    def __init__(self, new_item="", successor_node=None):
        """
        Creates a new node, with the input new_item as data and linked
        to the node successor_node.

        Can also be called without parameters to create an empty node 
        (with an empty string as its item)

        @param new_item to store in this node
        @param successor_node refers to the successor node in the queue
        @post  a node object is created with data new_item and linked 
               to successor_node
        @complexity  best and worst case: O(1)
        """
        self.item = new_item
        self.link = successor_node