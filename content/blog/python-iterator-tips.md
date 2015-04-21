Title: Python Iterator Tips
Tags: python, tips, programming

Python's iterator protocol is a **powerful** tool in your arsenal.

An `Iterator` is an object that returns streams of data.
To be an iterator an instance just have to have a next() method.
Repeated calls to the iterator’s next() method return successive items in the
stream. When no more data are available a StopIteration exception is
raised instead.
As iterators preserve state, take care reusing them.
As an example, the first loop below will print 1,2,3 where as the second 
will print nothing.

```python
>>> an_iter = iter([1, 2, 3])
>>> for x in an_iter:
...     print x
...
1
2
3
>>> for x in an_iter:
...     print x
...
```


An `Iterable` is a class that can generate an `Iterator`. For example 
list, tuples and strings are all iterable. To be an iterable a class
just has to have an __iter__ method that will return an iterator.
Iterables can be looped over multiple time as each time a new iter is generated;
```python
>>> seq = (1, 2, 3)
>>> for x in seq:
...     print x
...
1
2
3
>>> for x in seq:
...     print x
...
1
2
3
```
but once the iterator has been generated it can't be reused.
```python
>>> an_iter = iter(seq)
>>> for x in an_iter:
...     print x
...
1
2
3
>>> for x in an_iter:
...     print x
...
```



If you're currently returning a list from a function consider instead
returning an iterator.  For example;

```python
# Bad
def get_all_lines():
    all_lines = []
    for filename in ALL_FILES:
        for line in open(filename):
            all_lines.append(line)
    return all_lines

# Better is to achieve this with a generator.
# This means calling the function below will return an iterator.
def get_all_lines_iter():
    for filename in ALL_FILES:
        for line in open(filename):
            yield line
```


If client code wants to search the lines for string all files will be read
into memory even if the line were looking for is in the first file.

```python
>>> for line in get_all_lines():
>>>    if SEARCH_STRING in line:
>>>         print "YAY"
YAY
```

This is far more efficient as we wont go through the steps of reading
**every** file and storing it in a list when its not needed.
It's more flexible too. If the client code wants a list they can call;

```python
listified = list(get_all_lines_iter())
```

or you might want a tuple instead;
```python
tuplified = tuple(get_all_lines_iter())
```

The same applied with list comprehensions;

```python
# Don't do
def some_func():
   return [x for x in some_other_iteratable]

# Instead the following will again return an iterator
def some_func():
   return (x for x in some_other_iteratable)
```

Iterables can be used with the
[itertools](https://docs.python.org/2/library/itertools.html) package to do
some cool things very efficiently;

```python
>>> import itertools

# Create some iterable objects
>>> a = (1, 2, 3)
>>> b = ('a', 'b', 'c')
>>> c = (None, 0.3, False)

# Create an iterable object containing iterables
>>> seq_of_seq = (a, b, c)

# Chain will iterate through each iterable in turn till all iterables run out
# of items
>>> for x in itertools.chain.from_iterable(seq_of_seq):
...     print repr(x)
...
1
2
3
'a'
'b'
'c'
None
0.3
False

# izip takes one item from each iterable on each iteration.
# It stops when the shortest iterator runs out of items.
>>> for x, y in itertools.izip(a, b):
...     print repr(x), repr(y)
...
1 'a'
2 'b'
3 'c'

# cycle will loop over an iterator indefinitely.
# It achieves this by caching results on first run around the iterator.
>>> for n, x in itertools.izip(
...         range(20),
...         itertools.cycle(itertools.chain.from_iterable(seq_of_seq))):
...     print n, repr(x)
...
0 1
1 2
2 3
3 'a'
4 'b'
5 'c'
6 None
7 0.3
8 False
9 1
10 2
11 3
12 'a'
13 'b'
14 'c'
15 None
16 0.3
17 False
18 1
19 2
```
