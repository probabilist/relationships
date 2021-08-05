"""2. Suppose we want to add restrictions on joining a guild. For
example, maybe only fighters can join a Fighter's Guild. We can do that
with properties.

"""

class Guild():
    def __init__(self, name):
        self.name = name

class Character():
    """A character.

    Attributes:
        name (str): The name of the character.

    """

    def __init__(self, name):
        self.name = name
        self._belongsTo = None

    @property
    def belongsTo(self):
        """Guild: The guild to which the character belongs."""
        return self._belongsTo

    @belongsTo.setter
    def belongsTo(self, guild):
        # Here is where you can check that the character is eligible to
        # join the given guild, and take action if they are not.
        self._belongsTo = guild

if __name__ == '__main__':
    fg = Guild("Fighter's Guild")
    char = Character('Conan')
    char.belongsTo = fg
    print(char.name + ' is in the ' + char.belongsTo.name)
