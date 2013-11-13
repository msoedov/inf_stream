"""
Iterable filter with potential infinite sequence/stream.

Drops from the sequence/stream predefined element at the end and beginning. Also truncates occurring
this element more than N times, N>0. For example filtering element "":

 ["", "abc", "123", "", "x", "", "", "y", "", "" ] ->

 ["abc", "123", "", "x", "", "y"]

- sequence: generator, truncates obsolete predefined strings which occur more than N times, N>0
- linear_sequence:  generator, truncates obsolete predefined strings which occur only once
- Sequence: optional useful class (abc?) to be inherited from, with builtin sequence based iterator behaviour
"""


import os
import sys
from collections import deque
import abc


LINE_SEPARATOR = "\n"

EOS = '-1\n'  # end of stream

SEQUENCE_END = "SEQUENCE_END"


def sequence(iterable, symbol="", inbound=1):
    """
    sequence( iterable: object with Iterable behavior,
              symbol: String,
              inbound: Int) -> generator function

    >>> list(sequence(["a", "b", "", "", "c", ""]))
    ['a', 'b', '', 'c']
    >>> list(sequence(["*","a", "b", "*", "*", "*", "c", "*"], symbol="*", inbound=2))
    ['a', 'b', '*', '*', 'c']

    """
    fifo = deque()
    ## deque could be replaced with a list,
    ## please consider that pop() complexity would become O(1) and pop(0) - O(N)
    ## both deque's popleft() and pop() are O(1)
    ## deque is more efficient in comparison to a list, if fifo is big enough
    if inbound < 1:
        raise ValueError("Bad inbound value: %d" % inbound)
    numerator = inbound
    for item in iterable:
        if item == symbol:
            numerator += 1
        else:
            numerator = 0
        if numerator > inbound:
            continue
        if fifo and numerator:
            yield fifo.popleft()
        fifo.append(item)

    while fifo and fifo[-1] == symbol:
        fifo.pop()
    for rest in fifo:
       yield  rest


def linear_sequence(iterable, symbol=""):
    """
    linear_sequence( iterable: object with Iterable behavior,
              symbol: String,
              inbound: Int) -> generator function

    >>> list(linear_sequence(["a", "b", "", "", "c", ""]))
    ['a', 'b', '', 'c']

    """
    inbound=1
    numerator = inbound
    send_out = None
    for item in iterable:
        if item == symbol:
            numerator += 1
        else:
            numerator = 0
        if numerator > inbound:
            continue
        if send_out is not None:
            yield send_out
        send_out = item
    if send_out != symbol and send_out is not None:
        yield send_out


class Sequence(object):
    # __metaclass__ = abc.ABCMeta
    iter_type = None
    symbol = None
    inbound = None
    def __new__(cls, *args, **kwargs):
        pass

    def __iter__(self):
        return sequence(self.iter_type, self.symbol, self.inbound)


def input_generator():
    sys.stdin.flush()
    while True:
        line = sys.stdin.readline()
        if line == EOS:
            break
        yield line.strip("\n")


def bind():
    transform = sequence(input_generator())
    for i in transform:
        sys.stdout.write(i + LINE_SEPARATOR)


def doc_tests():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    if SEQUENCE_END in os.environ:
        EOS = os.environ[SEQUENCE_END]

    bind()
