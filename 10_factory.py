"""10. Notice that in the last example, the manager had to track both
characters and items. This introduced some redundancy into our code.
Both the Item class and the Character class have a lot of the same code.
If we ever want to change it, we'll have to change it in both places. As
we add more and more relationships, this problem will multiply and
become very serious.

To solve this, we will eliminate all references to the manager from the
code that defines the Item and Character classes. Instead, we will use
the manager itself to create the objects we want to work with. This is
accomplished by giving the Manager class a `make` method.

We also eliminate the `characters` and `items` attributes from the
Manager class. Instead, we will use a new `getAll` method. In this way,
we can manage as many classes as we want, and we don't have to add new
attributes to the Manager class.

"""

class Manager():
    """A manager that creates and catalogs objects and their relations.

    Attributes:
        objects (list of obj): A list of objects created and managed by
            the manager.

    """

    def __init__(self):
        self.objects = []

    def make(self, class_, *args, **kargs):
        """Creates an instance of the given class, adds it to the
        object list, and returns it.

        """
        obj = class_(*args, **kargs)
        self.objects.append(obj)
        return obj

    def getAll(self, class_):
        """Returns a list of all managed objects that are instances of
        the given class. This one method replaces the `characters` and
        `items` attributes from the previous example.

        """
        return [obj for obj in self.objects if isinstance(obj, class_)]

    def getMembers(self, guild):
        return [
            char for char in self.getAll(Character) if char.belongsTo == guild
        ]

    def getInventory(self, char):
        return [
            item for item in self.getAll(Item) if item.isCarriedBy == char
        ]

class Guild():
    def __init__(self, name):
        self.name = name

class Item():
    def __init__(self, name):
        self.name = name
        self.isCarriedBy = None

class Character():
    def __init__(self, name):
        self.name = name
        self.belongsTo = None

if __name__ == '__main__':
    mgr = Manager()
    fg = mgr.make(Guild, "Fighter's Guild")
    char1 = mgr.make(Character, 'Conan')
    char2 = mgr.make(Character, 'Sonja')
    potion = mgr.make(Item, 'Elixir of Health')
    print('Guilds:')
    print([guild.name for guild in mgr.getAll(Guild)])
    print('Characters:')
    print([char.name for char in mgr.getAll(Character)])
    print('Items:')
    print([item.name for item in mgr.getAll(Item)])
    char1.belongsTo = fg
    char2.belongsTo = fg
    potion.isCarriedBy = char1
    print(char1.name + ' is in the ' + char1.belongsTo.name)
    print(char2.name + ' is in the ' + char2.belongsTo.name)
    print('Members of the ' + fg.name + ':')
    print([char.name for char in mgr.getMembers(fg)])
    print(char1.name + ' is carrying the following items:')
    print([item.name for item in mgr.getInventory(char1)])
    print(char2.name + ' is carrying the following items:')
    print([item.name for item in mgr.getInventory(char2)])
