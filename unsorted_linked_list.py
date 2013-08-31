#!/usr/bin/python3

"""
This file implements the list data type using linked nodes.

@author         Javier Candeira, from a Java implementation by
                Maria Garcia de la Banda and Brendon Taylor
@since          15 Feb 2013
@input          none
@output         only for regression testing
@errorHandling  none
@knownBugs      ListIterator is missing reset() and add_here()
                as these would be implemented by the students.
"""

from node import Node

class UnsortedLinkedList:
    """
    A linked list implementation.

    Invariants for the class:
        (1) head points to the first node in the list, or null if empty
        (2) each node points to the next node in the position in the list
    """

    def __init__(self, size=None):
        """
        Creates an empty object of the class, i.e., an empty linked list.

        Since the list is implemented with linked nodes, we don't need a size;
        parameter `size` is however included to provide compatibility with the
        interface of the ArrayList, and then disregarded.

        @post           an empty list object is created
        @complexity     best and worst case: O(1)

        """
        self.head = None

    def is_empty(self):
        """
        Determines if the list has any elements.

        @return         false if list has elements, true if empty
        @complexity     best and worst case: O(1)
        """
        return self.head is None

    def __nonzero__(self):
        """
        For boolean context evaluation of unsorted linked lists under Python2.

        Double-underscore methods plug into the syntax of Python.
        In Python2, my_list.__nonzero__() will be called when a program
        uses the syntax "if my_list" to check whether it's not empty.

        @return         true if list has elements, false if empty
        @complexity     best and worst case: O(1)
        """
        return not self.is_empty()

    def __bool__(self):
        """
        For boolean context evaluation of unsorted linked lists under Python3.

        Double-underscore methods plug into the syntax of Python.
        In Python3, my_list.__bool__() will be called when a program
        uses the syntax "if my_list" to check whether it's not empty.

        Here we implement it via __nonzero__ for compatibility with Python2.

        @return         true if list has elements, false if empty
        @complexity     best and worst case: O(1)
        """
        return self.__nonzero__()

    # In Python functions and methods are first-class,
    # so we can just assign them to names
    __bool__ = __nonzero__
    # Now the __bool__ function doesn't just return the result of calling
    # __nonzero___, but the very same function.

    def is_full(self):
        """
        Determines whether the list is full.

        Since it is implemented with linked nodes, it will never be.
        Method introduced for consistency with the CustomList implemented
        with arrays.

        @return     false
        @complexity best and worst case: O(1)
        """
        return False

    def reset(self):
        """
        Resets the list to an empty state.

        @post           the list is empty
        @complexity     best and worst case: O(1)
        """
        self.head = None

    def add_first(self, new_item):
        """
        Adds a new node (containing the input item) as the head of the list.

        @param          new_item to add to this linked list
        @post           list has one more element after the method is called
        @post           list[0] equals new_item after the method is called
        @complexity     best and worst case: O(1)
        """
        self.head = Node(new_item, self.head)

    def add(self, new_item):
        """
        For unsorted linked lists, "add()" is synonymous with "add_first()"
        """
        self.add_first(new_item)

    def find_linear(self, item):
        """
        Internal method for finding the first node containing the input item.

        @param      item to find
        @return     None if the item does not appear in the list and,
                    otherwise, the address of the first node the item
                    appears in
        @complexity best case: O(1) (first item), worst case: O(N) (not there)
        """
        current = self.head
        while current is not None and current.item != item:
            current = current.link;
        return current

    def delete_item(self, delitem):
        """
        Deletes the first node (if any) containing the input item.

        @param      del_item, first instance of which to be deleted
        @return     True if item was in list and has been deleted
        @post       if item was in list, list has one fewer elements
        @post       if item was in list one or more times, only first one
                    will have been removed
        @post       if item wasn't in list, list is unchanged
        @throws     Exception thrown if item does not exist in the linked list
        @complexity best case: O(1) (first item), worst case: O(N) (not there)
        """
        if self.head is None:           # list is empty
            raise LookupError("can't delete item from empty list")
        elif self.head.item == delitem:    # item is first element of list
            self.head = self.head.link
        else:
            current = self.head.link    # look for item in elements #2 to last
            previous = self.head
            while current is not None and current.item != delitem:
                previous = current
                current = current.link
            if current is None:         # element wasn't there
                raise LookupError('item not found')
            else:                       # item was found
                previous.link = current.link
        return True


    class ListIterator:
        """
        Implements a list iterator conformant to the Java Iterator interface.

        This class extends the Python iterator protocol with some special
        methods not required in Python, namely delete(), has_next() and peek().

        @author     Javier Candeira, based on Java code by
                    Maria Garcia de la Banda and Brendon Taylor
        """

        def __init__(self, linked_list):
            """
            Creates a new iterator for the current list object.

            @post       the created iterator object has the current property
                        pointing to the head of the list and previous to None.
            @complexity best and worst case: O(1)

            """
            self.linked_list = linked_list
            self.current = linked_list.head
            self.previous = None

        def __iter__(self):
            """required so Python recognises it as an iterator"""
            return self

        def __next__(self):
            """
            Returns the item of the current node and moves to the next one.

            This method implements the Python3 iterator interface.

            If all nodes have been iterated over, it throws an exception.

            @return     the item of the current node of the iterator
            @throws     Exception thrown if no item exists *here*
            @post       the iterator pointer is set at the item following the
                        current item, or None if we hit the end of the list.
            @complexity best and worst case: O(1)
            """
            # Raising the StopIteration exception is the standard way of
            # finishing an iterator in Python. It's not an error.
            if self.current is None:              # we reached the end
                raise StopIteration("no more elements in list")
            else:
                item = self.current.item
                self.previous = self.current
                self.current = self.current.link
                return item

        def next(self):
            """
            Returns the item of the current node and moves to the next one.

            This method provides compatibility with Python2 iterators.

            Python 2 used iter.next(), Python 3 uses next(iter), with the
            next() builtin function plugging into each object's __next__()
            special double underscore function as seen above.
            """
            return self.__next__()

        def delete(self):
            """
            Returns the item of the current node, deletes it, moves to next one.

            If all nodes had already been iterated over, it throws
            an exception.

            Not in the Python iterator protocol, because Python iterators
            aren't supposed to mutate the data structures they iterate on,
            but we are implementing the Java iterator interface, which allows
            mutation.

            @throws     StopIteration thrown if the node is None
            @post       if there is an element that has not yet been
                        iterated over, it isdeleted and the iterator's current
                        node will be pointed at the next element
            @complexity best and worst case: O(1)
            """
            if not self.has_next:                   # we reached the end
                raise StopIteration("no more elements in list")
            else:
                item = self.current.item
                newcurrent = self.current.link

                if self.previous is None:           # we are at first element
                    self.linked_list.head = newcurrent
                else:                               # elements #2 to last
                    self.previous.link = newcurrent
                self.current = newcurrent

                return item

        def peek(self):
            """
            Returns the item of the node currently pointed to by the iterator.
            If all nodes have been iterated over, it throws the StopIteration
            exception, thus finishing the iterator.

            Not in the Python iterator protocol, but we are implementing
            the Java iterator interface, which has a peek() method.

            @return     the item of node currently pointed to by the iterator
            @throws     StopIteration thrown if no item exists *here*
            @post       iterator is unchanged after the call
            @complexity  best and worst case: O(1)
            """
            try:
                # Just in case someone tries to peek over the line.
                return self.current.item
            except AttributeError:
                raise StopIteration("no more elements in list")

        def has_next(self):
            """
            Used to check whether the iterator has already gone through all
            items already, or there are some left to iterate.

            Not in the Python iterator protocol, but we are implementing
            the Java iterator interface, which has a has_next() method.

            @return     true if there is an element that has not yet
                        been iterated over, false otherwise
            @complexity  best and worst case: O(1)
            """
            return self.current is not None

        def reset(self):
            """Resets the iterator to point to the head of the list.

            @author     Jeffrey Dowdle
            @since      31 Aug 2013
            @post       Iterator is changed, points to head of the list.
                        previous will point to None.
            @complexity Best/Worst: O(1)
            """
            self.current = self.linked_list.head
            self.previous = None

        def add_here(self, new_item):
            """Adds an item to the list, between previous and current.

            @author     Jeffrey Dowdle
            @since      31 Aug 2013
            @param      new_item: item to be added
            @post       new_item will be added to the list, between previous
                        and current. previous will point the newly added item.
            @complexity Best/Worst: O(1)
            """
            new_node = Node(new_item, None)

            if self.linked_list.is_empty():
                self.linked_list.head = new_node
                self.previous = new_node
                self.current = None
            else:
                if self.previous is None:
                    new_node.link = self.linked_list.head
                    self.linked_list.head = new_node
                    self.previous = new_node
                elif self.current is None:
                    self.previous.link = new_node
                    self.previous = new_node
                else:
                    self.previous.link = new_node
                    new_node.link = self.current
                    self.previous = new_node


    def delete_item_via_iterator(self, delitem):
        """Same as delete_item() above, only this time using internal iterator
        """
        it = iter(self)
        while it.has_next():
            if it.peek() != delitem:
                next(it)
            else:
                it.delete()
                return True
        raise LookupError("item not found")

    def __iter__(self):
        """
        Double-underscore methods plug into the syntax of Python.
        The double underscore function __iter__ is a hook for the Python
        iteration syntax "for x in y" or for the explicit creation of the
        iterator with "iter(y)"
        """
        return self.ListIterator(self)

    def __repr__(self):
        """
        Double-underscore methods plug into the syntax of Python.
        Used to convert the elements of the queue into an unambiguous string,
        following the order front-to-back. Used by `repr(my_list)`.

        @return     Unambiguous string representation of the list
        @post       List is unchanged
        @complexity Best and worst case: O(N)*O_(_repr_,join) (that is, O(N)
                    multiplied by whatever complexity __repr__ of the
                    underlying items and concatenation).
        """
        return " ".join(repr(item) for item in self)

    def __str__(self):
        """
        Used to convert the elements of the queue into an human-readable string,
        following the order front-to-back. Used by `str(my_list)`.

        For this particular structure, __str__() is the same as __repr__

        @return     Human-readable string representation of the list
        @post       List is unchanged
        @complexity Best and worst case: O(N)*O_(_repr_,join) (that is, O(N)
                    multiplied by whatever complexity __repr__ of the
                    underlying items and concatenation).
        """
        return self.__repr__()

    # As above, we assign the name `__str__` to mean the `__repr__` function.
    __str__ = __repr__
    # Now the __str__ function doesn't just return the result of calling
    # __repr___, but the very same function.


## REGRESSION TESTING CODE
##
## Two test cases: empty lists and non-empty lists.
## Boundary analysis gives four cases: 0 elements, 1, 2, and many (5).

def test_nonzero_bool():
    """Two test cases: empty list, and non-empty lists
    Boundary analysis gives four cases: 0 elements, 1, 2, and many (5).
    """
    my_list = UnsortedLinkedList()
    print("Testing __nonzero__() and __bool__()")
    print("Expected False, got ", my_list.__nonzero__())
    print("Expected False, got ", my_list.__bool__())
    my_list.add_first(9)
    print("Expected True, got ", my_list.__nonzero__())
    print("Expected True, got ", my_list.__bool__())
    my_list.add_first(0)
    print("Expected True, got ", my_list.__nonzero__())
    print("Expected True, got ", my_list.__bool__())
    my_list.add_first(1)
    my_list.add_first(2)
    my_list.add_first(14)
    print("Expected True, got ", my_list.__nonzero__())
    print("Expected True, got ", my_list.__bool__())

def test_is_empty():
    """We test emptiness of a sequence or container with special double
    underscore methods __nonzero__ (Python2) or __bool__ (Python3).
    Those methods are tested in the above function."""
    print("Method is_empty doesn't exist. Instead:")
    test_nonzero_bool()

def test_is_full():
    """Three test cases: overfull lists, full lists and non-full lists.
    Boundary analysis gives three cases: n<f elements, n==f, and n>f.
    """
    my_list = UnsortedLinkedList(3)
    print("TESTING is_full()")
    my_list.add_first(9)
    print("Expected False, got ", my_list.is_full())
    my_list.add_first(0)
    my_list.add_first(1)
    print("Expected False, got ", my_list.is_full())
    my_list.add_first(2)
    my_list.add_first(14)
    print("Expected False, got ", my_list.is_full())

def test_add_first():
    """One test case: a list of any length.
    We should also check for lenght increase by one, but implementing a len()
    function has been left as an exercise to the students.
    """
    my_list = UnsortedLinkedList(5)
    print("TESTING addFirst()")
    my_list.add_first(9)
    print("Expected 9, got ", my_list.head.item)
    my_list.add_first(5)
    print("Expected 5, got ", my_list.head.item)
    my_list.add_first(1)
    my_list.add_first(14)
    print("Expected 14, got ", my_list.head.item)

def test_delete_item():
    """For successful deletion, three boundary conditions: delete first
    element, last element, and random middle element.
    One fourth test for attempting to delete a non-existing element.
    """
    my_list = UnsortedLinkedList()
    my_list.add_first(8)
    my_list.add_first(7)
    my_list.add_first(5)
    my_list.add_first(5)
    my_list.add_first(4)
    my_list.add_first(3)
    my_list.add_first('eggs')
    my_list.add_first('spam')
    my_list.add_first(0)
    print("TESTING delete_item()")
    print("Expected True, got ", my_list.delete_item(5))
    print("    with list 0 'spam' 'eggs' 3 4 5 7 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item('spam'))
    print("    with list 0 'eggs' 3 4 5 7 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item(0))
    print("    with list 'eggs' 3 4 5 7 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item(7))
    print("    with list 'eggs' 3 4 5 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item(8))
    print("    with list 'eggs' 3 4 5, got ", my_list)
    print("Now attempting to delete 10, which doesn't exist")
    try:
        my_list.delete_item(10)
        print("Excepted an exception, but something went wrong")
    except LookupError as error:
        print("Expected: <class 'LookupError'> : item not found")
        print("Got     : ", type(error), ": ", error)

def test_delete_item_via_iterator():
    """For successful deletion, three boundary conditions: delete first
    element, last element, and random middle element.
    One fourth test for attempting to delete a non-existing element.
    """
    my_list = UnsortedLinkedList()
    my_list.add_first(8)
    my_list.add_first(7)
    my_list.add_first(5)
    my_list.add_first(5)
    my_list.add_first(4)
    my_list.add_first(3)
    my_list.add_first('eggs')
    my_list.add_first('spam')
    my_list.add_first(0)
    print("TESTING delete_item_via_iterator()")
    print("Expected True, got ", my_list.delete_item_via_iterator(5))
    print("    with list 0 'spam' 'eggs' 3 4 5 7 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item_via_iterator('spam'))
    print("    with list 0 'eggs' 3 4 5 7 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item_via_iterator(0))
    print("    with list 'eggs' 3 4 5 7 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item_via_iterator(7))
    print("    with list 'eggs' 3 4 5 8, got ", my_list)
    print("Expected True, got ", my_list.delete_item_via_iterator(8))
    print("    with list 'eggs' 3 4 5, got ", my_list)
    print("Now attempting to delete 10, which doesn't exist")
    try:
        my_list.delete_item_via_iterator(10)
        print("Expected an exception, but something went wrong")
    except LookupError as error:
        print("Expected: <class 'LookupError'> : item not found")
        print("Got     : ", type(error), ": ", error)

def test_find_linear():
    """Two test cases: the item is not in the list and it is in it.
    Subclasses for the class in which the item is in: is the first slot
    the last, or in the middle.
    Boundary analysis gives five cases: slot 0, slot 1, slot used-2, slot
    used-1, and some slot in the middle.
    """
    my_list = UnsortedLinkedList(8)
    my_list.add_first(0)
    my_list.add_first(1)
    my_list.add_first(2)
    my_list.add_first(14)
    my_list.add_first(20)
    my_list.add_first(30)
    my_list.add_first(40)
    my_list.add_first(50)
    print("TESTING find_linear()")
    print("Expected None, got ", my_list.find_linear(9))
    print("Expected 0, got ", my_list.find_linear(0).item)
    print("Expected 1, got ", my_list.find_linear(1).item)
    print("Expected 14, got ", my_list.find_linear(14).item)
    print("Expected 40, got ", my_list.find_linear(40).item)
    print("Expected 50, got ", my_list.find_linear(50).item)

def test_add_item():
    """
    Tests the add item function. Checks all four cases outlined in the prac
    sheet.

    complexity  Best/Worst: O(1)
    """
    print()
    print("-- TESTING add_item() --")
    print()

    print("Trying with empty list")
    test_list = UnsortedLinkedList(10)
    it = iter(test_list)
    it.add_item("Hello")
    print("adding item: 'Hello'...")
    print("Expected:", "'Hello'")
    print("     Got:", test_list)
    print()

    print("Adding elements at various places...")
    test_list = UnsortedLinkedList(10)
    for i in range(10,0,-1):
        test_list.add_first(i)
    it = iter(test_list)
    it.next()
    it.next()
    it.add_item("Hello")
    it.next()
    it.next()
    it.add_item("Bye")
    it.reset()
    it.add_item("reset")
    it.next()
    it.add_item(1.5)
    print(test_list)
    print("Head: {0}, Previous: {1}, Current: {2}".format(test_list.head.item, it.previous.item, it.current.item))
    print()

    print("Trying to add at start of list...")
    test_list = UnsortedLinkedList(10)
    for i in range(10,0,-1):
        test_list.add_first(i)
    it = iter(test_list)
    it.add_item("Hello")
    print(test_list)
    print("Head: {0}, Previous: {1}, Current: {2}".format(test_list.head.item, it.previous.item, it.current.item))
    print()

    print("Trying at end of list...")
    test_list = UnsortedLinkedList(10)
    for i in range(10,0,-1):
        test_list.add_first(i)
    it = iter(test_list)
    for _ in range(10):
        it.next()
    it.add_item("Hello")
    print(test_list)
    print("Head: {0}, Previous: {1}, Current: {2}".format(test_list.head.item, it.previous.item, it.current))
    print()

if __name__ == "__main__":
    # Run the tests when the module is called from the command line
    try:
        test_is_empty()
        test_is_full()
        test_add_first()
        test_delete_item()
        test_delete_item_via_iterator()
        test_find_linear()
        test_add_item()
    except Exception as e:
        print("Error, unexpected exception: ", e)
        raise e
