"""9. Let's now combine Examples 4 and 8. We will have characters,
guilds, and items. We want to implement two relations, "belongsTo" and
"isCarriedBy". For simplicity, we'll remove the cap on guild membership.

"""

class Manager():
    def __init__(self):
        self.characters = []
        self.items = []

    def getMembers(self, guild):
        return [
            char for char in self.characters if char.belongsTo == guild
        ]

    def getInventory(self, char):
        return [
            item for item in self.items if item.isCarriedBy == char
        ]

class Guild():
    def __init__(self, name):
        self.name = name

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
    def __init__(self, mgr, name):
        mgr.characters.append(self)
        self.name = name
        self._manager = mgr
        self.belongsTo = None

    @property
    def manager(self):
        return self._manager

if __name__ == '__main__':
    fg = Guild("Fighter's Guild")
    mgr = Manager()
    char1 = Character(mgr, 'Conan')
    char2 = Character(mgr, 'Sonja')
    potion = Item(mgr, 'Elixir of Health')
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
