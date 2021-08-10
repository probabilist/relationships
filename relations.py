from collections import defaultdict
from customabcs import BiMapping, MultiMapping

class bidict(BiMapping):
    """An invertible, one-to-one dictionary.

    The `bidict` object is implemented by linking a forward dictionary
    and a backward dictionary. Because of this, all keys and values must
    be immutable.

    Attributes:
        forward (dict): The dictionary that holds the bidict's keys and
            values.
        backward (dict): A dictionary whose keys and values are the
            values and keys, respectively, of the `forward` attribute.

    """

    def __init__(self):
        """Creates an empty bidict object."""
        self._forward = {}
        self._backward = {}

    def __getitem__(self, key):
        return self._forward[key]

    def __delitem__(self, key):
        val = self._forward[key]
        del self._forward[key]
        del self._backward[val]

    def __iter__(self):
        return self._forward.__iter__()

    def __len__(self):
        return len(self._forward)

    def __setfreeval__(self, key, val):
        self._forward[key] = val
        self._backward[val] = key

    def __inverse__(self):
        inverse = bidict()
        inverse._forward = self._backward
        inverse._backward = self._forward
        return inverse

    def __repr__(self):
        return 'bidict(' + repr(self._forward) + ')'

class dictplus(dict):
    """A dictionary with a `discard` method.

    """

    def discard(self, elem):
        """Removes the given key-value pair from the dictionary. Fails
        silently if `elem` is not a 2-tuple or if the given key is not
        in the dictionary.

        Args:
            elem (2-tuple): The key-value pair to remove.

        """
        try:
            key, val = elem
        except TypeError:
            return
        if key in self and self[key] == val:
            del self[key]

class dictofsets(MultiMapping):
    """A rudimentary multi-valued dictionary.

    A `dictofsets` object is a dictionary whose values are sets.

    The `__contains__`, `__iter__`, and `__len__` methods work
    differently than for ordinary dictionaries. If `d` is a `dictofsets`
    object, then `(k,v) in d` is equivalent to `v in d[k]`. The
    `__iter__` method returns an iterator of all key-value pairs. To
    iterate over keys, use the `keys` method. And `len(d)` is the total
    number of key-value pairs.

    The `__getitem__` method returns a frozen set, so key-value pairs
    can only be added with `d[k] = v`. The syntax `d[k].add(v)` will not
    work.

    A `dictofsets` object also has a `discard` method, so that
    `d.discard((k, v))` removes `v` from the set `d[k]`, if it is
    present.

    """
    def __init__(self):
        self._dict = defaultdict(set)

    def __contains__(self, elem):
        try:
            key, val = elem
        except TypeError:
            return False
        return (val in self._dict[key])

    def __iter__(self):
        for key in self._dict:
            for val in self._dict[key]:
                yield key, val

    def __len__(self):
        return sum(len(val) for val in self._dict.values())

    def discard(self, elem):
        """Removes the given key-value pair from the `dictofsets`. Fails
        silently if `elem` is not a 2-tuple or if the key-value pair is
        not in the `dictofsets`.

        Args:
            elem (2-tuple): The key-value pair to remove.

        """
        try:
            key, val = elem
        except TypeError:
            return
        self._dict[key].discard(val)
        if not self._dict[key]:
            del self._dict[key]

    def __getitem__(self, key):
        if key not in self._dict:
            raise KeyError(key)
        return frozenset(self._dict[key])

    def __setitem__(self, key, val):
        self._dict[key].add(val)

    def __delitem__(self, key):
        del self._dict[key]

    def keys(self):
        """Returns an iterator of the keys of `dictofsets`."""
        return self._dict.keys()

    def __inverse__(self):
        raise NotImplementedError

    def __repr__(self):
        return 'dictofsets(' + repr(dict(self._dict)) + ')'

class multidict(MultiMapping):
    """A more robust multi-valued dictionary that is easily inverted.

    It is a multi-mapping of immutables to immutables, implemented by
    embedding both a dictionary of sets, and a set of key-value pairs. A
    reversed dictionary and a reversed set are also embedded to
    implement the inverse mapping.

    """
    def __init__(self):
        """Constructs an empty multidict."""
        self._forward = dictofsets()
        self._backward = dictofsets()
        self._set = set()
        self._rset = set()

    def __contains__(self, item):
        return (item in self._set)

    def __iter__(self):
        return self._set.__iter__()

    def __len__(self):
        return len(self._set)

    def discard(self, elem):
        """Removes the given key-value pair, if present.

        Args:
            elem (2-tuple): The key-value pair to discard.

        """
        if elem in self:
            key, val = elem
            self._forward.discard((key, val))
            self._backward.discard((val, key))
            self._set.discard((key, val))
            self._rset.discard((val, key))

    def __getitem__(self, key):
        return self._forward[key]

    def __setitem__(self, key, val):
        self._forward[key] = val
        self._backward[val] = key
        self._set.add((key, val))
        self._rset.add((val, key))

    def __delitem__(self, key):
        if key not in self._forward.keys():
            raise KeyError(key)
        else:
            for val in self._forward[key]:
                self.discard((key, val))

    def keys(self):
        """Returns an iterator over the keys in the multidict."""
        return self._forward.keys()

    def __inverse__(self):
        inverse = multidict()
        return self._inverseinit(inverse)

    def _inverseinit(self, inverse):
        inverse._forward = self._backward
        inverse._backward = self._forward
        inverse._set = self._rset
        inverse._rset = self._set
        return inverse

    def copy(self):
        """Creates and returns a copy of the multidict object."""
        new = multidict()
        return self._fillcopy(new)

    def _fillcopy(self, new):
        for pair in self:
            new.add(pair)
        return new

    def __repr__(self):
        return 'multidict(' + repr(dict(self._forward._dict)) + ')'

class inversedict(multidict):
    """A `multidict` whose values are disjoint sets.

    Its inverse can be represented as a dictionary and is implemented as
    an `invertibledict` object.

    """
    def __init__(self):
        """Constructs an empty inversedict."""
        multidict.__init__(self)
        self._backward = dictplus()

    def __setitem__(self, key, val):
        if val in self._backward.keys():
            raise ValueError(val)
        multidict.__setitem__(self, key, val)

    def __inverse__(self):
        inverse = invertibledict()
        return self._inverseinit(inverse)

    def copy(self):
        """Creates and returns a copy of the inversedict object."""
        new = inversedict()
        return self._fillcopy(new)

    def __repr__(self):
        return 'inversedict(' + repr(dict(self._forward._dict)) + ')'

class invertibledict(multidict):
    """A more robust dictionary that is easily inverted.

    Its inverse is implemented as an `inversedict` object.

    """
    def __init__(self):
        """Constructs an empty invertibledict."""
        multidict.__init__(self)
        self._forward = dictplus()

    def __delitem__(self, key):
        if key not in self._forward.keys():
            raise KeyError(key)
        else:
            val = self._forward[key]
            self.discard((key, val))

    def __inverse__(self):
        inverse = inversedict()
        return self._inverseinit(inverse)

    def copy(self):
        """Creates and returns a copy of the invertibledict object."""
        new = invertibledict()
        return self._fillcopy(new)

    def __repr__(self):
        return 'invertibledict(' + repr(self._forward) + ')'

