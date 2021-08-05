"""6. We next model the one-to-many relation.

In this example, we have characters and items, and we wish to model the
"is carrying" relation (a character is carrying an item).

The one-to-many relation is just the reverse of the many-to-one, and so
there is a very easy implementation. We simply use the "is carried by"
relation instead, which is many-to-one.

This way of doing it has a serious drawback, though. It offers us no
easy way to see what a character is carrying. More on this later.

"""

class Character():
    def __init__(self, name):
        self.name = name

class Item():
    """An item.

    Attributes:
        name (str): The name of the item.
        carriedBy (Character): The character that is carrying the item.

    """

    def __init__(self, name):
        self.name = name
        self.isCarriedBy = None

if __name__ == '__main__':
    char = Character('Conan')
    sword = Item('Long Sword')
    sword.isCarriedBy = char
    print(sword.isCarriedBy.name + ' is carrying the ' + sword.name)
