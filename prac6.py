#!/usr/bin/env python3
#coding: utf-8

"""
Solution to a prac to give students experience using linked lists to implement a simple text editor.

@author
@since
@error_handling
@error_handling
@known_bugs
"""

import os

from unsorted_linked_list import UnsortedLinkedList


def main():
    """
    A simple command-line driven text editor.

    @modified   Javier Candeira
    @modified   Jerry Lu
    @since      2 September 2013

    @input      the commands to execute.
    @pre        none
    @post       see postconditions for individual methods in this class.
    @complexity have a look at the menu_q1 in the reverse_polish_notation.py
                that you used last week and add the complexity for this one.

    Please note that the complexities may change as you add
    functionality to this class -- don't forget to update this comment
    as you go.

    """

    my_list = UnsortedLinkedList()
    list_it = iter(my_list)
    quit = False
    input_line = None

    # Command parsing loop
    while not quit:
        # Read a command
        try:
            print("Possible commands: 'append' 'insert $line' 'printall' 'pwd' 'test' 'quit' 'write $filename' 'read $filename' delete $line' 'insert $line' 'print $line'")
            input_line = input("Enter your command: ")
        except IOError as e:
            print("Error reading from console or EOF character")
            input_line = ""

        command = input_line.split(" ")

        if command[0] == "write":
            write_to_file(list_it, command[1])
        elif command[0] == "read":
            read_from_file(list_it, command[1])
        elif command[0] == "printall":
            printall(list_it)
        elif command[0] == "print":
            try:
                print_n(list_it, int(command[1]))
            except Exception as e:
                print("Exception:", e)
        elif command[0] == "delete":
            try:
                delete_n(list_it, int(command[1]))
            except Exception as e:
                print("Exception:", e)
        elif command[0] == "append":
            print("Append: ")
            append_data = multi_line_input()
            print(append_data)
            append(list_it, append_data)
        elif command[0] == "insert":
            # check if n is negative
            try:
                n = int(command[1])

                if not validate_line_number(list_it, n) and n != 0:
                    raise Exception("Line number out of range.")

            # if int(command[1]) < 0:
            #     raise ValueError("Line number cannot be negative")

            # n = int(command[1])

            # taken from delete_n
            # if not validate_line_number(list_it, n) and n != 0:
            #     raise Exception("Line number out of range.")

                print("Insert: ")
                insert_data = multi_line_input()
                insert(list_it, insert_data, n)
            except ValueError:
                print("Line number needs to be an integer.")
            except Exception as e:
                print("Exception:", e)
        elif command[0] == "test":
            run_tests()
        elif command[0] == "quit":
            quit = True
        else:
            print("Unrecognized command or not enough arguments.")

def multi_line_input():
    """
    Allows user to input several lines, ends input when it hits "."
    """
    print("Enter a . by itself to save.")
    buffer = []
    while True:
        line = input()
        if line == ".":
            break
        buffer.append(line)

    return buffer

def write_to_file(list_it, file_name):
    """
    Stores each line of an UnsortedLinkedList into a file.

    @modified   Jerry Lu
    @since      1 September 2013
    @param      list_it: used to iterate over our linked list
    @param      file_name: is the name to be given the output file.
    @pre        file_name is a valid file name.
    @postevery  string in every node of the list is written into a new file
                created with name file_name, in the same order as it appears
                in the list. The list itself is not altered.
    @complexity O(1) currently, because the function so far does nothing,
                but this should change. So update this comment when you
                modify this method!
    """

    # Create a filehandle to do the output.
    try:
        f = open(file_name, "w")
    except IOError:
        # If opening the file didn't work...
        print("Error opening file:" + file_name + ".  File not saved.")
        return

    # loop through the list and output each line to the file.
    list_it.reset()

    for item in list_it:
        print(item, end='\n', file=f)

    f.close();
    print("Current buffer saved to file " + file_name)

def read_from_file(list_it, file_name):
    """
    Reads a text file line by line into an UnsortedLinkedList whose
    Iterator is passed in. If there is any data already in the list, the new
    data is added wherever the iterator is currently pointing to.

    @param list_it
               used to iterate over our linked list ADT.
    @param file_name
               is the text file to be loaded into memory.
    @pre none
    @post the list contains everything it had before in the same order, plus
          every line in the text file also in the same order it appears in
          the file. The file is not altered.
    @complexity O(N*(M+S)) where N is the number of lines in the list and. M
                is the complexity of reading a line from file. S is the
                complexity of adding a line to the list
    """

    try:
        # We use a context manager to open the file for reading
        with open(file_name, "r") as f:
            # The file is now open, let's read from it.
            for line in f:
                list_it.add_here(line.strip("\n"));
        # we don't need to close the file, the context manager does it!
        print("File " + file_name + " successfully read in")

    # We manage wrong filenames in our program, raise everything else
    except IOError as e:
        if "No such file" in str(e):
            print(str(e))
            return
        else:
            raise e

def printall(list_it):
    """Prints the entire buffer to the screen.

    @author     Jerry Lu
    @since      1 September 2013
    @param      list_it: iterator to traverse buffer
    @post       list_it will be at end of list.
    @complexity Best/Worst: O(N), where N is the size of the list.
    """
    list_it.reset()

    for item in list_it:
        print(item)


def print_n(list_it, n):
    """
    Prints the Nth line in the list, where the first line is numbered 1.

    @author     Jeffrey Dowdle
    @since      3 September 2013
    @param      n: the nth line to be printed
    @pre        n must be an integer greater than 0
    @post       List is unchanged
    @complexity Best: O(1), if first line is the one we want to print.
                Worst: O(n), if the line we want to print is at the
                around the end of the list.
    """
    if not validate_line_number(list_it, n):
        raise Exception("Line number out of range.")

    # Reset iterator
    list_it.reset()
    counter = 1

    # call next() n times
    while counter < n:
        list_it.next()
        counter += 1

    print(list_it.next())

def delete_n(list_it, n):
    """
    Deletes the Nth line in the list, where the first line is numbered 1.

    @author     Jeffrey Dowdle
    @since      4 September 2013
    @param      n: the nth line to be deleted
    @pre        n must be an integer greater than 0
    @post       List length is reduced by 1 if delete is successful
    @complexity Best: O(1), if first line is the one we want to delete.
                Worst: O(n), if the line we want to delete is at the
                around the end of the list.
    """
    if not validate_line_number(list_it, n):
        raise Exception("Line number out of range.")

    # Reset iterator
    list_it.reset()
    counter = 1

    # call next() n times
    while counter < n:
        list_it.next()
        counter += 1

    print("Deleted line {0}: {1}".format(n, list_it.delete()))

def validate_line_number(list_it, n):
    """
    Checks if n is a valid line number

    @author     Jeffrey Dowdle
    @since      4 September 2013
    @pre        n needs to be an integer
    @complexity Best and worst: O(n), where n is the length of list_it
    """
    list_it.reset()

    # Find the length of the list
    length = 0
    for _ in list_it:
        length += 1

    # Check whether n is a valid line number
    return n <= length and n >= 1

def append(list_it, append_data):
    """
    Inserts some lines of text at the end of the list.

    @since      4 September 2013
    @pre        append_data is a list of strings.
    """
    # Reset iterators
    list_it.reset()

    ### append_data is a list.

    # Get to the last element in the list
    for _ in list_it:
        list_it.next()

    # Add elements at the end
    for lines in append_data:
        list_it.add_here(lines)

def insert(list_it, insert_data, n):
    """
    Inserts text at the nth line in the list

    @since      5 September 2013

    """


    # Reset iterators
    list_it.reset()

    # n = int(n)

    # Get to the nth line in the list
    for _ in range(n):
        list_it.next()

    # Add elements
    for lines in insert_data:
        list_it.add_here(lines)


# Let's write tests too
def run_tests():
    """
    Testrunner for the questions in Prac6

    @author Javier Candeira
    @complexity O(1) as it runs with static data.
    """
    try:
        test_read_from_file()
        test_write_to_file()
    except Exception as e:
        raise e

def test_read_from_file():
    """
    Test read_from_file()as requested in Q2 of Prac6

    @author Javier Candeira

    @complexity O(1) because it runs with static data.
    """
    # first we write out a test file
    with open("prac6_read_test", 'w') as out:
        file_strings = ["Dear Javier,", " ",
                        "This is a test that ReadFromFile() works."]
        for line in file_strings:
            print(line, file=out)

    # now we read it into our linked list
    test_read_list = UnsortedLinkedList()
    test_read_list_it = iter(test_read_list)
    print("Testing read_from_file... ")
    read_from_file(test_read_list_it, "prac6_read_test");
    test_read_list_it.reset();
    linecount = 1
    for s in file_strings:
        r = test_read_list_it.next()
        print("Expected at line " + str(linecount) + ": " + repr(s))
        print("There is at line " + str(linecount) + ": " + repr(r))
        if s == r:
            print("Line " + str(linecount) + " read in all right.")
        else:
            print("Line " + str(linecount) + " not good, sorry!")
        linecount = linecount + 1

def test_write_to_file():
    """
    Test writing to file the text held in the editor's iterator.

    @author Javier Candeira
    @complexity O(1) because it runs with static data.
    """
    # first we create an UnsortedLinkedList with text in it
    test_write_list = UnsortedLinkedList()
    test_write_list_it = iter(test_write_list);
    file_strings = ["Dear Javier,", "",
                    "This is a test that WriteToFile() works."]
    for s in file_strings:
        test_write_list_it.add_here(s)

    # then we write it into a file, and read it back into a linked list
    print("Testing writeToFile()...")
    write_to_file(test_write_list_it, "prac6_write_test.txt");
    test_write_list2 = UnsortedLinkedList()
    test_write_list_it2 = iter(test_write_list2)
    read_from_file(test_write_list_it2, "prac6_write_test.txt");

    test_write_list_it.reset()
    test_write_list_it2.reset()
    for tup in zip(test_write_list_it, test_write_list_it2):
        s, r = tup
        if s != r:
            raise Exception("writeToFile() doesn't work!, because '" + s
                                + "' is not equal to '" + r + "'.");
    print("write_to_file() works fine!")
    return

if __name__ == "__main__":
    main()
