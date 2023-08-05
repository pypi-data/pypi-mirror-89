
# AttribDict

## Introduction

AttribDict is an easy to use and easy to read dict, it is more flexible and human readable.

## Examples

```python
>>> from attribdict import AttribDict as Dict
>>> _d = {"attr"+str(i): i for i in range(4)}
>>> d = Dict(_d)
>>> d.attr4.subattr1.subsubattr1 = 123
>>> d.attr5 = {"subattr"+str(i): i for i in range(3)}
>>> print(d)
attr0: 0
attr1: 1
attr2: 2
attr3: 3
attr4:
    - subattr1:
        - subsubattr1: 123
attr5:
    - subattr0: 0
    - subattr1: 1
    - subattr2: 2
```

## Installation

```
pip install attribdict
```