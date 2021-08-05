"""1. Here we model a many-to-one relation.

In this example, we have characters and guilds, and we wish to model the
"belongs to" relation (a character belongs to a guild). Each character
can belong to only one guild, but multiple characters can belong to the
same guild.

In this example, there is no cap on how many characters can belong to a
given guild. In mathematical parlance, a many-to-one relation is just a
function. For a generic function, there is no cap to how many elements
in the domain can be mapped to the same point in the range. For
instance, a constant function maps everything to the same point.

If we wish to impose a cap, then we have a more complicated
relationship. More on that later.

"""

class Guild():
    def __init__(self, name):
        self.name = name

class Character():
    """A character.

    Attributes:
        name (str): The name of the character.
        belongsTo (Guild): The guild to which the character belongs.

    """

    def __init__(self, name, guild):
        self.name = name
        self.belongsTo = guild

if __name__ == '__main__':
    fg = Guild("Fighter's Guild")
    char = Character('Conan', fg)
    print(char.name + ' is in the ' + char.belongsTo.name)
