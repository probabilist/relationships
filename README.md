# relationships

## Custom abstract base classes

`customabcs.py` provides the following abstract base classes.

* `BiMapping`: An abstract one-to-one mapping that is invertible. Inherits from `collections.abc.MutableMapping`.
* `RelSet`: An abstract relational set. Inherits only set relations, not set operations. Does not require an iterator-based construction method. Inherits from `collections.abc.Collection`.
* `MutableRelSet`: An abstract mutable relational set. Inherits from `RelSet`. Also inherits the `update` and `difference_update` methods.
* `MultiMapping`: An abstract multi-valued mapping that is invertible. Inherits from `MutableRelSet`.

## Custom dictionary-like data types

`relations.py` provides the following custom dictionary-like data types.

* `bidict`: An invertible, one-to-one dictionary.
* `dictplus`: A dictionary with a `discard` method.
* `dictofsets`: A rudimentary multi-valued dictionary.
* `multidict`: A more robust multi-valued dictionary that is easily inverted.
* `inversedict`: A `multidict` whose values are disjoint sets. Its inverse is an `invertibledict` object.
* `invertibledict`: A more robust dictionary that is easily inverted. Its inverse is an `inversedict` object.

## Examples

`objrelations.py` uses a factory pattern to construct object mappings from these new data types.

`example.py` illustrates the use of the object mappings with typical game objects like `Character`, `Spell`, `Guild`, and so on.