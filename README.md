# advanced-dtypes
Advanced DataTypes is a package for Python that provides access faster, feature-rich data types not provided in the standard library, motivated by my thoughts of "why is that not a thing?"
The aim of the project is to fill out the holes in the standard library data types' feature-set while improving upon the performance of the existing feature-set.

## Constant Store
Constant Store is a class that provides a namespace within which to store constants on a class attribute basis. Class definition is very simple:
```py
from advanced_dtypes import ConstStore


class Example(ConstStore):
    NAME_1 = "some_value"
    NAME_2 = 23
```

The class is built to populate a set and dictionary on import, which drives many of the features of the class, as well as the \_\_slots\_\_ attribute, which helps boost performance.
Since the class attributes are maintained, names can be directly dot-referenced.
```py
>> Example.NAME_1 == "some_value"
True
>> type(Example.NAME_1) == str
True
```

`ConstStore` also provides an interface for the following functionality:
```py
>> len(Example)
2
>> 23 in Example
True
>> Example(23)
NAME_2
>> Example["NAME_2"]
23
>> [value for value in Example]
["some_value", 23]
```

You should be aware, however, that non-hashable objects will have slower performance in lookups such as `in`, `Class(value)` and `Class[name]`.


## Fast Enum
`FastEnum` is simply a faster implementation of the existing standard library `Enum`.

Definition is exactly the same as a standard enum:
```py
from advanced_dtypes import FastEnum


class Example(FastEnum):
    NAME_1 = "some_value"
    NAME_2 = 23
```

Similarly, standard enum functionality remains:
```py
>> Example.NAME_1
<Example.NAME_1: some_value>
>> Example.NAME_1.name
NAME_1
>> Example.NAME_1.value
some_value
>> Example("some_value")
<Example.NAME_1: some_value>
>> Example["NAME_1"]
<Example.NAME_1: some_value>
>> len(Example)
2
>> [item for item in Example]
[<Example.NAME_1: some_value>, <Example.NAME_2: 23>]
>> Example.NAME_1 == Example.NAME_1
True
```

The only functional addition in this instance is equality checking of members against values directly:
```py
>> Example.NAME_1 == "some_value"
True
```


## How To Install
```sh
pip install advanced-dtypes
```
