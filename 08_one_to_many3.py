"""8. Example 6 gave a very easy way to model the "isCarrying" relation,
by implementing its inverse, the "isCarriedBy" relation. But there was a
problem. We had no way to get a character's inventory.

Example 6 solved that problem, but we had to construct a custom list
type.

Here's another way to implement our relation. Like Example 6, we will
implement the inverse, "isCarriedBy". Then, as in Example 4, we will
use a manager to give us a way to access a character's inventory. In
fact, this implementation is just the reverse of Example 4.

But there is one thing to notice. The way we use the manager here is
different than all the previous examples. Here, it won't be the
characters that are managed. It will be the items.

"""

class Manager():
    def __init__(self):
        self.items = []

    def getInventory(self, char):
        """Returns a list of all the managed items that are carried by
        the given character.

        """
        return [
            item for item in self.items if item.isCarriedBy == char
        ]

class Item():
    def __init__(self, mgr, name):
        mgr.items.append(self)
        self.name = name
        self.isCarriedBy = None
        self._manager = mgr

    @property
    def manager(self):
        return self._manager

class Character():
    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    mgr = Manager()
    potion = Item(mgr, 'Elixir of Health')
    char1 = Character('Conan')
    char2 = Character('Sonja')
    potion.isCarriedBy = char1
    print(char1.name + ' is carrying the following items:')
    print([item.name for item in mgr.getInventory(char1)])
    print(char2.name + ' is carrying the following items:')
    print([item.name for item in mgr.getInventory(char2)])
    potion.isCarriedBy = char2
    print(char1.name + ' is carrying the following items:')
    print([item.name for item in mgr.getInventory(char1)])
    print(char2.name + ' is carrying the following items:')
    print([item.name for item in mgr.getInventory(char2)])
