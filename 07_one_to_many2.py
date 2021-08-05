"""7. The previous implementation has a serious drawback. It offers no
good way to see what a character is carrying. An alternative is for each
character to store a list of items it is carrying. But that would just
be a many-to-many relation. To make this one-to-many, we need to have a
way to make sure two characters cannot carry the same item.

With hats, we used a manager to check if a hat is already worn, and then
used properties to stop the character from putting on the hat in that
case.

With items, we can also use a manager to see if an item is already being
carried. But how can we stop the character from picking up the item in
that case? Properties will not work because lists are mutable. A
property that points to a list can be changed even if it doesn't have a
setter.

To solve this problem, we will make our own custom list type.

"""

from collections.abc import MutableSequence

class IsCarrying(MutableSequence):
    """A custom list that prohibits items which are already carried.

    A custom list can be created by subclassing the `MutableSequence`
    abstract base class (ABC). When creating a custom list this way, you
    must implement `__getitem__`, `__setitem__`, `__delitem__`,
    `__len__`, and `insert`. Most of the other list methods are filled
    in by the ABC. The three exceptions are `sort`, `reverse`, and
    `copy`. If you want these methods, you must implement them yourself.
    We will not implement these methods here. For more information, see
    https://docs.python.org/3/library/collections.abc.html and
    Section 3.3.7 of https://docs.python.org/3/reference/datamodel.html.

    One thing to be careful with is that the `key` argument in
    `__getitem__` and `__setitem__` could be a `slice` object. In our
    example below, slices work fine in `__getitem__`. But to keep things
    simple, we are not allowing them in `__setitem__`.

    Attributes:
        char (Character): The character to which the list belongs.
        items (list of Item): The items the character is carrying.

    """
    def __init__(self, char):
        self.char = char
        self.items = []

    def __getitem__(self, key):
        return self.items.__getitem__(key)

    def __setitem__(self, key, item):
        """Raises an error if the key is a `slice` object. Otherwise,
        uses the `check` method to make sure the item is not already
        carried by another character. This must also be done in the
        `insert` method below.

        """
        if isinstance(key, slice):
            raise NotImplementedError(
                'slice assignment not implemented'
            )
        if self.isCarried(item):
            print('Someone is already carrying that')
        else:
            self.items.__setitem__(key, item)

    def __delitem__(self, key):
        self.items.__delitem__(key)

    def __len__(self):
        return self.items.__len__()

    def insert(self, key, item):
        if self.isCarried(item):
            print('Someone is already carrying that')
        else:
            self.items.insert(key, item)

    def isCarried(self, item):
        """Returns `True` if the given item is already carried by a
        character. Otherwise, returns `False`.
        """
        otherChars = self.char.manager.characters
        return any(item in char.isCarrying for char in otherChars)

class Manager():
    def __init__(self):
        self.characters = []

class Item():
    def __init__(self, name):
        self.name = name

class Character():
    def __init__(self, mgr, name):
        mgr.characters.append(self)
        self.name = name
        self._manager = mgr
        self.isCarrying = IsCarrying(self)

    @property
    def manager(self):
        return self._manager

if __name__ == '__main__':
    potion = Item('Elixir of Health')
    mgr = Manager()
    char1 = Character(mgr, 'Conan')
    char2 = Character(mgr, 'Sonja')
    char1.isCarrying.append(potion)
    print(char1.name + ' is carrying the following items:')
    print([item.name for item in char1.isCarrying])
    char2.isCarrying.append(potion)
    print(char2.name + ' is carrying the following items:')
    print([item.name for item in char2.isCarrying])
