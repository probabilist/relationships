"""3. We now model the one-to-one relation.

In this example, we have characters and hats, and we wish to model the
"is wearing" relation (a character is wearing a hat). Each character can
wear only one hat, and each hat can be worn by only one character.

We could start by following the previous example and giving each
character an `isWearing` attribute that will point to the hat the
character is wearing. But we need something else to make sure that two
characters cannot wear the same hat.

As we saw earlier, we can use properties to stop a character from
putting on a hat that is already being worn. But how can we know if a
hat is already being worn?

To do this, we introduce a `Manager` class.

"""

class Manager():
    def __init__(self):
        self.characters = []

class Hat():
    def __init__(self, style):
        self.style = style

class Character():
    """A character.

    Attributes:
        name (str): The name of the character.

    """

    def __init__(self, mgr, name):
        """Creating a character requires a manager. The manager adds the
        newly created character to its registry. The character itself
        stores a reference to its manager. The character's manager is
        accessed through a property with no setter, since the manager
        should not be changed.

        Args:
            mgr (Manager): The manager with which to register the newly
                created character.
            name (str): The name to assign to the newly created
                character.
                
        """
        mgr.characters.append(self)
        self.name = name
        self._manager = mgr
        self._isWearing = None

    @property
    def manager(self):
        """Manager: The Manager object that oversees this character in
        relation to other Character objects.
        """
        return self._manager

    @property
    def isWearing(self):
        """Hat: The hat that the character is wearing."""
        return self._isWearing

    def wear(self, hat):
        """Tries to put on a hat. Prints a message if the hat is already
        being worn.

        Args:
            hat (Hat): The hat to try to wear.
        """
        otherChars = self.manager.characters
        if any(char.isWearing == hat for char in otherChars):
            print('Someone is already wearing that hat.')
        else:
            self._isWearing = hat

if __name__ == '__main__':
    hat = Hat('helmet')
    mgr = Manager()
    char1 = Character(mgr, 'Conan')
    char2 = Character(mgr, 'Sonja')
    char1.wear(hat)
    print(char1.name + ' is wearing a ' + char1.isWearing.style)
    char2.wear(hat)
    print(char2.isWearing)
