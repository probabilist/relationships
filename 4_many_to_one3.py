"""4. Let us now return to the many-to-one "belongs to" relation,
describing characters belonging to guilds. You may have noticed that the
way we implemented it has a big shortcoming. Given a guild, there is no
easy way to get a list of its members. We can now accomplish that using
the Manager class from the previous example.

This also gives us a way to cap the number of characters in a guild.

"""

class Manager():
    def __init__(self):
        self.characters = []

    def getMembers(self, guild):
        """Returns a list of all the managed characters that belong to
        the given guild.

        """
        return [
            char for char in self.characters if char.belongsTo == guild
        ]

class Guild():
    """A guild.

    Attributes:
        name (str): The name of the guild.
        cap (int): The maximum number of members allowed in the guild.

    """

    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

class Character():
    def __init__(self, mgr, name):
        mgr.characters.append(self)
        self.name = name
        self._manager = mgr
        self._belongsTo = None

    @property
    def manager(self):
        return self._manager

    @property
    def belongsTo(self):
        return self._belongsTo

    @belongsTo.setter
    def belongsTo(self, guild):
        """If the guild is full, prints a message. Otherwise, assigns
        the guild to the character.

        """
        if len(mgr.getMembers(guild)) >= guild.cap:
            print('Sorry, the guild is full.')
        else:
            self._belongsTo = guild

if __name__ == '__main__':
    fg = Guild("Fighter's Guild", 2)
    mgr = Manager()
    char1 = Character(mgr, 'Conan')
    char2 = Character(mgr, 'Sonja')
    char3 = Character(mgr, 'Pee-Wee')
    char1.belongsTo = fg
    print(char1.name + ' is in the ' + char1.belongsTo.name)
    char2.belongsTo = fg
    print(char2.name + ' is in the ' + char2.belongsTo.name)
    char3.belongsTo = fg
    print(char3.belongsTo)
    print('Members of the ' + fg.name + ':')
    print([char.name for char in mgr.getMembers(fg)])
