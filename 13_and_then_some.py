"""If we try to put a cap on the character's inventory, we run into a
problem. In the previous example, we add an item to a character's
inventory by setting the `Item.isCarriedBy` attribute. To implement an
inventory cap, we could try to change that attribute to a property and
use a setter that would check if the character's inventory is full. The
problem, though, is that the Item object would have no idea which
character is trying to pick it up.

Although there may be many ways around this problem, the most natural
one is to return to our work in Example 7 and implement "is carrying"
directly. After all, why should an item have control over whether it's
picked up or dropped. It's the Character object that should control such
methods.

So that's what we do here. We incorporate the code from Example 7 into
the previous example, and then implement the inventory cap. It's mostly
a case of copy and paste, so the code is presented without comments. But
there is one significant change you should look out for. The `isCarried`
method of the `IsCarrying` class has been changed to an `isCarriedBy`
method, and moved to the `Item` class where it belongs. In its place, we
put a more general `validate` method that we can customize as our code
evolves.

"""

from collections.abc import MutableSequence

class IsCarrying(MutableSequence):
    def __init__(self, char):
        self.char = char
        self.items = []

    def __getitem__(self, key):
        return self.items.__getitem__(key)

    def __setitem__(self, key, item):
        if isinstance(key, slice):
            raise NotImplementedError(
                'slice assignment not implemented'
            )
        if self.validate(item):
            self.items.__setitem__(key, item)
        else:
            print('cannot carry item')

    def __delitem__(self, key):
        self.items.__delitem__(key)

    def __len__(self):
        return self.items.__len__()

    def insert(self, key, item):
        if self.validate(item):
            self.items.insert(key, item)
        else:
            print('cannot carry item')

    def validate(self, item):
        return (item.isCarriedBy is None and len(self) < self.char.itemCap)

class Manager():
    def __init__(self):
        self.objects = []

    def make(self, class_, *args, **kargs):
        obj = class_(*args, **kargs)
        obj._m_manager = self
        self.objects.append(obj)
        return obj

    def getAll(self, class_):
        return [obj for obj in self.objects if isinstance(obj, class_)]

class Guild():
    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    @property
    def employs(self):
        mgr = self._m_manager
        return [
            char for char in mgr.getAll(Character) if char.isEmployedBy == self
        ]

class Hat():
    def __init__(self, style):
        self.style = style

class Spell():
    def __init__(self, name):
        self.name = name

class Item():
    def __init__(self, name):
        self.name = name

    @property
    def isCarriedBy(self):
        for char in self._m_manager.getAll(Character):
            if self in char.isCarrying:
                return char
            return None

class Character():
    def __init__(self, name, itemCap):
        self.name = name
        self.itemCap = itemCap
        self._isEmployedBy = None
        self._isWearing = None
        self.knows = []
        self.isCarrying = IsCarrying(self)

    @property
    def isEmployedBy(self):
        return self._isEmployedBy

    @isEmployedBy.setter
    def isEmployedBy(self, guild):
        if len(guild.employs) >= guild.cap:
            print('Sorry, the guild is full.')
        else:
            self._isEmployedBy = guild

    @property
    def isWearing(self):
        return self._isWearing

    @isWearing.setter
    def isWearing(self, hat):
        otherChars = self._m_manager.getAll(Character)
        if any(char.isWearing == hat for char in otherChars):
            print('Someone is already wearing that hat.')
        else:
            self._isWearing = hat

if __name__ == '__main__':
    mgr = Manager()
    char = mgr.make(Character, 'Conan', 2)
    potion = mgr.make(Item, 'Elixir of Health')
    dagger = mgr.make(Item, 'Blade of Death')
    ring = mgr.make(Item, 'The One Ring')
    char.isCarrying.append(potion)
    char.isCarrying.append(dagger)
    char.isCarrying.append(ring)
    print(char.name + ' is carrying the following items:')
    print([item.name for item in char.isCarrying])
