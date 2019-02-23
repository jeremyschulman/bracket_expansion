# bracket_expansion

This library provides functions that allow you to define a string
that contains brackets with numeric-ranges, and then expands that
into a list of actual values.

There are two functions defined.  The first function `bracket_expansion`
will create a generator.  You can then iterate through the generator.

The expansion supports multiple brackets.  See examples.

If you want to create a concrete list from the generate, there is
a function called `expand` which will do this as a convenience.

# Installation

````bash
$ pip install bracket_expansion
````

# Usage

Simple example:

````python
from bracket_expansion import bracket_expansion

for if_name in bracket_expansion("Ethernet[1-48]"):
    print(if_name)
````

Would result in the output:

```bash
Ethernet1
Ethernet2
Ethernet3
...
Ethernet48
```

Multiple brackets:

You can define multiple brackets in the expression:

````python
from bracket_expansion import bracket_expansion

for if_name in bracket_expansion("Ethernet[1-2]/[1-10]"):
    print(if_name)
````

Would result in the output:

```bash
Ethernet1/1
Ethernet1/2
...
Ethernet1/10
Ethernet2/1
Ethernet2/2
...
Ethernet2/10
```

For more details see the `bracket_expansion` docstring.
