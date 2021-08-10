from types import MethodType
from customabcs import BiMapping, MultiMapping
from relations import bidict, multidict, inversedict, invertibledict

class Manager():
    """An object that creates and manages other objects.

    Attributes:
        nextID (int): The next id number available to assign to a new
            managed object.
        objects (dict of int:obj): A dictionary of managed objects
            indexed by id numbers.

    """
    def __init__(self):
        """Creates a Manager object, sets its `nextID` property to 1,
        and creates an empty `objects` dictionary.

        """
        self.nextID = 1
        self.objects = {}

    def make(self, class_, *args, **kargs):
        """Creates an object of the given class and attaches to it a
        reference to the calling Manager object and a reference to its
        ID number. Then increments the `nextID` property and adds the
        newly created object to the `objects` dictionary.

        """
        obj = class_(*args, **kargs)
        obj._m_manager = self
        obj._m_id = self.nextID
        self.nextID += 1
        self.objects[obj._m_id] = obj
        return obj

class OneToOne(BiMapping):
    """A one-to-one relation mapping objects to objects.

    The OneToOne object, as well as all objects in the relation, should
    be managed by a common Manager object (or be `None`). Otherwise, a
    OneToOne object functions just like a bidict object.

    The OneToOne class is meant to be subclassed. Subclasses may wish to
    override the `validate` method to provide restrictions on adding a
    pair to the relation. The `validate` method is called whenever
    `__setitem__` is called. If `validate` returns True, the
    `__setitem__` method proceeds normally. Otherwise, `__setitem__`
    simply returns None. If the subclass wishes to raise an error when
    validation fails, the error should be raised from within the
    `validate` method.

    Attributes:
        map (bidict of int:int): The relation is stored under the
            hood as a bidict mapping IDs to IDs, where the IDs are
            provided by the common Manager object.

    """

    def __init__(self):
        self.map = bidict()

    def __getitem__(self, key):
        keyID = None if key is None else key._m_id
        valID = self.map[keyID]
        val = None if valID is None else self._m_manager.objects[valID]
        return val

    def __delitem__(self, key):
        keyID = None if key is None else key._m_id
        del self.map[keyID]

    def __iter__(self):
        return (
            None if keyID is None else self._m_manager.objects[keyID]
            for keyID in self.map
        )

    def __len__(self):
        return len(self.map)

    def __setfreeval__(self, key, val):
        if self.validate(key, val):
            keyID = None if key is None else key._m_id
            valID = None if val is None else val._m_id
            self.map[keyID] = valID

    def __inverse__(self):
        inverse = self._m_manager.make(OneToOne)
        inverse.map = self.map.inverse
        def validate(slf, key, val):
            return slf.inverse.validate(val, key)
        inverse.validate = MethodType(validate, inverse)
        return inverse

    def validate(self, key, val):
        """Checks if the given key-value pair may be added to the
        relation. As implemented here, the method always returns True.
        Subclasses should override this method to produce custom
        behavior.

        Args:
            key (obj): The key to validate.
            val (obj): The value to validate.

        Returns:
            bool: True if the key-value pair may be added, False
                otherwise.

        """
        return True

    def __repr__(self):
        disp = 'OneToOne({'
        for key, val in self.items():
            disp += repr(key) + ': ' + repr(val) + ',\n '
        return disp + '})'

class ManyToMany(MultiMapping):
    """A many-to-many relation mapping objects to objects.

    The ManyToMany object, as well as all objects in the relation,
    should be managed by a common Manager object (or be `None`).
    Otherwise, a ManyToMany object functions just like a multidict
    object.

    The ManyToMany class is meant to be subclassed. Subclasses may wish
    to override the `validate` method to provide restrictions on adding
    a pair to the relation. The `validate` method is called whenever
    `__setitem__` is called. If `validate` returns True, the
    `__setitem__` method proceeds normally. Otherwise, `__setitem__`
    simply returns None. If the subclass wishes to raise an error when
    validation fails, the error should be raised from within the
    `validate` method.

    Attributes:
        map (multidict of int:int): The relation is stored under the
            hood as a multidict mapping IDs to IDs, where the IDs are
            provided by the common Manager object.

    """

    def __init__(self):
        self.map = multidict()

    def __contains__(self, elem):
        try:
            key, val = elem
        except TypeError:
            return False
        keyID = None if key is None else key._m_id
        valID = None if val is None else val._m_id
        return keyID, valID in self.map

    def __iter__(self):
        return (
            (
                None if keyID is None else self._m_manager.objects[keyID],
                None if valID is None else self._m_manager.objects[valID]
            )
            for keyID, valID in self.map
        )

    def __len__(self):
        return len(self.map)

    def discard(self, elem):
        try:
            key, val = elem
        except TypeError:
            return
        keyID = None if key is None else key._m_id
        valID = None if val is None else val._m_id
        return self.map.discard((keyID, valID))

    def __getitem__(self, key):
        keyID = None if key is None else key._m_id
        try:
            return tuple(
                None if valID is None else self._m_manager.objects[valID]
                for valID in self.map[keyID]
            )
        except KeyError:
            raise KeyError(key)

    def __setitem__(self, key, val):
        if self.validate(key, val):
            keyID = None if key is None else key._m_id
            valID = None if val is None else val._m_id
            self.map[keyID] = valID

    def __delitem__(self, key):
        keyID = None if key is None else key._m_id
        try:
            del self.map[keyID]
        except KeyError:
            raise KeyError(key)

    def keys(self):
        return (
            None if keyID is None else self._m_manager.objects[keyID]
            for keyID in self.map.keys()
        )

    def __inverse__(self):
        inverse = self._m_manager.make(ManyToMany)
        return self._inverseinit(inverse)

    def _inverseinit(self, inverse):
        inverse.map = self.map.inverse
        def validate(slf, key, val):
            return slf.inverse.validate(val, key)
        inverse.validate = MethodType(validate, inverse)
        return inverse        

    def validate(self, key, val):
        """Checks if the given key-value pair may be added to the
        relation. As implemented here, the method always returns True.
        Subclasses should override this method to produce custom
        behavior.

        Args:
            key (obj): The key to validate.
            val (obj): The value to validate.

        Returns:
            bool: True if the key-value pair may be added, False
                otherwise.

        """
        return True

    def __repr__(self):
        disp = 'ManyToMany({'
        for key in self.keys():
            disp += repr(key) + ': ' + repr(self[key]) + ',\n '
        return disp + '})'

class ManyToOne(ManyToMany):
    """A many-to-one relation mapping objects to objects.

    The ManyToOne object, as well as all objects in the relation, should
    be managed by a common Manager object (or be `None`). Otherwise, a
    ManyToOne object functions just like an invertibledict object.

    The ManyToOne class is meant to be subclassed. Subclasses may wish
    to override the `validate` method to provide restrictions on adding
    a pair to the relation. The `validate` method is called whenever
    `__setitem__` is called. If `validate` returns True, the
    `__setitem__` method proceeds normally. Otherwise, `__setitem__`
    simply returns None. If the subclass wishes to raise an error when
    validation fails, the error should be raised from within the
    `validate` method.

    Attributes:
        map (invertibledict of int:int): The relation is stored under
            the hood as a multidict mapping IDs to IDs, where the IDs
            are provided by the common Manager object.

    """

    def __init__(self):
        self.map = invertibledict()

    def __inverse__(self):
        inverse = self._m_manager.make(OneToMany)
        return self._inverseinit(inverse)

    def __getitem__(self, key):
        keyID = None if key is None else key._m_id
        try:
            valID = self.map[keyID]
        except KeyError:
            raise KeyError(key)
        return None if valID is None else self._m_manager.objects[valID]

    def __repr__(self):
        disp = 'ManyToOne({'
        for key in self.keys():
            disp += repr(key) + ': ' + repr(self[key]) + ',\n '
        return disp + '})'

class OneToMany(ManyToMany):
    """A one-to-many relation mapping objects to objects.

    The OneToMany object, as well as all objects in the relation, should
    be managed by a common Manager object (or be `None`). Otherwise, a
    OneToMany object functions just like an inversedict object.

    The OneToMany class is meant to be subclassed. Subclasses may wish
    to override the `validate` method to provide restrictions on adding
    a pair to the relation. The `validate` method is called whenever
    `__setitem__` is called. If `validate` returns True, the
    `__setitem__` method proceeds normally. Otherwise, `__setitem__`
    simply returns None. If the subclass wishes to raise an error when
    validation fails, the error should be raised from within the
    `validate` method.

    Attributes:
        map (inversedict of int:int): The relation is stored under the
            hood as a multidict mapping IDs to IDs, where the IDs are
            provided by the common Manager object.

    """

    def __init__(self):
        self.map = inversedict()

    def __inverse__(self):
        inverse = self._m_manager.make(ManyToOne)
        return self._inverseinit(inverse)

    def __repr__(self):
        disp = 'OneToMany({'
        for key in self.keys():
            disp += repr(key) + ': ' + repr(self[key]) + ',\n '
        return disp + '})'



