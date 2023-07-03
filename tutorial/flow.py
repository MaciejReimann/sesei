result_1 = 17 / 3  # returns a float, in this case 5.666666666666667
result_2 = 17 // 3  # returns an integer (floor division), in this case 5
result_3 = 17 % 3  # returns the remainder of the division (modulus), in this case 2
result_4 = 5**2  # returns 5 squared, in this case 25
result_5 = 5**3  # returns 5 cubed, in this case 125

word = "Python"
print(word[0:2])  # returns Py
print(word[2:5])  # returns tho
print(word[:2])  # returns Py
print(word[2:])  # returns thon17
print(word[-2:])  # returns on
print(word[:2] + word[2:])  # returns Python

"J" + word[1:]  # returns Jython
word[:2] + "py"  # returns Pypy

# CONTROL FLOW
x = int(input("Please enter an integer: "))
if x < 0:
    x = 0
    print("Negative changed to zero")
elif x == 0:  # substitute for switch case
    print("Zero")
elif x == 1:
    print("Single")
else:
    print("More")

# FOR LOOPS
words = ["cat", "window", "defenestrate"]
for w in words:
    print(w, len(w))

# when modifying the sequence you are iterating over
users = {"Hans": "active", "Peter": "inactive", "Klaus": "active"}
# strategy 1: iterate over a copy
for user, status in users.copy().items():
    if status == "inactive":
        del users[user]
# strategy 2: create a new collection
active_users = {}
for user, status in users.items():
    if status == "active":
        active_users[user] = status

# range() function - to iterate over a sequence of numbers
for i in range(5):
    print(i)  # the given end point is never part of the generated sequence

list(range(8, 10))  # returns [8, 9]
list(range(0, 10, 3))  # returns [0, 3, 6, 9]
list(range(-10, -100, -30))  # returns [-10, -40, -70]

# to iterate over the indices of a sequence
a = ["Mary", "had", "a", "little", "lamb"]
for i in range(len(a)):
    print(i, a[i])
# in most such cases, we'd use enumerate():
for i, v in enumerate(a):
    print(i, v)  # returns 0 Mary, 1 had, 2 a, 3 little, 4 lamb

range(
    10
)  # returns on object range(0, 10) - it doesn't create a list, which saves space
# such an object is iterable


# break, continue, else clauses on loops

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, "equals", x, "*", n // x)
            break
    else:  # loops MAY HAVE an else clause - runs when no break occurs
        # loop fell through without finding a factor
        print(n, "is a prime number")


class MyEmptyClass:
    pass


def do_something():
    pass  # a placeholder for a function or conditional body that does nothing


# match statement


def http_error(status):  # compare a subject value against a number of literals
    match status:
        case 400:
            return "Bad request"
        case 401 | 402 | 403:
            return "Not allowed"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the Internet"  # a wildcard, never fails to match, the default
