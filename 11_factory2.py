"""11. There's something unnatural about the last example. Consider the
fact that a Character object can't access its own inventory, and a Guild
object can't access it's own members. If those objects had access to the
Manager object, they could. But they don't have any such access. In
Example 9, they did. It was stored in the `_manager` attribute. But that
has been removed.

We can put it back, but it will have to be the manager that creates and
sets that attribute.

"""

class Manager():
    """Below, we modify the `make` method by adding one line. Namely,
    after creating a new object, the manager adds a reference to itself.
    Adding attributes to created objects could be dangerous. We wouldn't
    want to overwrite an attribute that the class itself created. In
    this case, it's not a problem. But as our code grows, as we get more
    and more classes and the manager starts adding more and more
    attributes, we could be in trouble. With that in mind, we will make
    a convention that every attribute added by the manager will begin
    with `_m_`. This should be sufficient to avoid any naming conflicts.

    By adding this self-reference, guilds can now access their members
    and characters can access their inventory. We have therefore moved
    the `getMembers` and `getInventory` methods to the Guild and
    Character classes, where they belong.

    """

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
    def __init__(self, name):
        self.name = name

    @property
    def members(self):
        mgr = self._m_manager
        return [
            char for char in mgr.getAll(Character) if char.belongsTo == self
        ]

class Item():
    def __init__(self, name):
        self.name = name
        self.isCarriedBy = None

class Character():
    def __init__(self, name):
        self.name = name
        self.belongsTo = None

    @property
    def inventory(self):
        mgr = self._m_manager
        return [
            item for item in mgr.getAll(Item) if item.isCarriedBy == self
        ]

if __name__ == '__main__':
    mgr = Manager()
    fg = mgr.make(Guild, "Fighter's Guild")
    char1 = mgr.make(Character, 'Conan')
    char2 = mgr.make(Character, 'Sonja')
    potion = mgr.make(Item, 'Elixir of Health')
    char1.belongsTo = fg
    char2.belongsTo = fg
    potion.isCarriedBy = char1
    print('Members of the ' + fg.name + ':')
    print([char.name for char in fg.members])
    print(char1.name + ' is carrying the following items:')
    print([item.name for item in char1.inventory])
    print(char2.name + ' is carrying the following items:')
    print([item.name for item in char2.inventory])
