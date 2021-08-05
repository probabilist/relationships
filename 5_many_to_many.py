"""5. Here we model the many-to-many relation.

In this example, we have characters and spells, and we wish to model the
"knows" relation (a character knows a spell). A character can know many
spells and a spell can be known by many characters.

"""

class Spell():
    def __init__(self, name):
        self.name = name

class Character():
    """A character.

    Attributes:
        name (str): The name of the character.
        knows (list of Spell): The spells that the character knows.

    """

    def __init__(self, name):
        self.name = name
        self.knows = []

if __name__ == '__main__':
    fb = Spell('Fireball')
    char = Character('Merlin')
    char.knows.append(fb)
    print(char.name + ' knows the following spells:')
    print([spell.name for spell in char.knows])
