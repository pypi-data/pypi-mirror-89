# bitman

## What is bitman?
This is a pure python module for managing and manipulating an array of bits. 

## How does it work?
bitman takes advantage of python's ability to handle big integers. The array of bits is simply an integer with its bit values set as desired. 

The array of bits is a class called bitman.

## Attributes of bitman

* **size**: It is an integer that holds the array size.
* **set(n, val)**: A function that sets the n-th bit to val.
* **get(n)**:	A function that returns the truth value of the n-th bit.
* **which(val)**: A list of positions with a value val (0 or 1).

## Installation
Please check https://pypi.org/project/bitman/ for the installable version.

You should be able to install with 
```
pip install bitman
```


## A quick tutorial

```python
>>> from bitman import bitman  	# import the bitman class
>>> a = bitman(size=5,init=1)  	# 'a' is now a bitman instance with 5 bits, all initialized to 1
>>> print(a)			# printing 'a' returns the string of bits as in a binary number
11111
>>> a				# simply typing 'a' at the command line also returns the bits in the same order
11111
>>> a.get(2)			# get the truth value of the bit at position 2
True
>>> a.set(0, 0)			# set the bit at position 0 to 0.
>>> a
11110
>>> a.set(2, 0)			# set the bit at position 2 to 0.
>>> a
11010
>>> a.get(2)			# the second bit has been set to False
False
>>> a.get(3)			# the third bit is still True
True
>>> a.which(0)			# list of bits in a that are 0 
[0, 2]
>>> a.which(1)			# list of bits in a that are 1
[1, 3, 4]
>>> a.size			# how many bits are to be represented by a?
5
>>> a
11010
>>> a.size=8			# let us resize the array
>>> a
00011010
```


## Invitation

You are welcome to improve bitman and suggest improvements.
