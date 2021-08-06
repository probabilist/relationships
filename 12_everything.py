"""12. Finally, let's put the hats (Example 3) and the spells (Example
5) into the mix, and put back the guild cap, so that all our relations
are together. We will make three changes so that everything looks
consistent.

First, we will change the `wear` method in Example 3 to a setter for the
`isWearing` property. That way, we can set a character's hat with the
same syntax by which we set their guild.

Next, we will rename the `inventory` method to `isCarrying`, since
that's exactly what it is (the inverse of the "is carried by" relation).

Finally, notice  that the `members` method is just the inverse of the
"belongs to" relation. If a character belongs to a guild, then the guild
employs that character. We will therefore rename the `members` method to
`employs` and, for greater clarity, rename `belongsTo` to `isEmployedBy`.

Altogether, we have implemented four distinct relations: "is employed
by" (many-to-one), "is wearing" (one-to-one), "knows" (many-to-one), and
"is carrying" (one-to-many), and . We also have implementations for the
inverses of two of them: "employs", the one-to-many inverse of "is
employed by", and "is carried by", the many-to-one inverse of "is
carrying".

"""

class Manager():
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
    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    @property
    def employs(self):
        mgr = self._m_manager
        return [
            char for char in mgr.getAll(Character) if char.isEmployedBy == self
        ]

class Hat():
    def __init__(self, style):
        self.style = style

class Spell():
    def __init__(self, name):
        self.name = name

class Item():
    def __init__(self, name):
        self.name = name
        self.isCarriedBy = None

class Character():
    def __init__(self, name):
        self.name = name
        self._isEmployedBy = None
        self._isWearing = None
        self.knows = []

    @property
    def isEmployedBy(self):
        return self._isEmployedBy

    @isEmployedBy.setter
    def isEmployedBy(self, guild):
        if len(guild.employs) >= guild.cap:
            print('Sorry, the guild is full.')
        else:
            self._isEmployedBy = guild

    @property
    def isWearing(self):
        return self._isWearing

    @isWearing.setter
    def isWearing(self, hat):
        otherChars = self._m_manager.getAll(Character)
        if any(char.isWearing == hat for char in otherChars):
            print('Someone is already wearing that hat.')
        else:
            self._isWearing = hat

    @property
    def isCarrying(self):
        mgr = self._m_manager
        return [
            item for item in mgr.getAll(Item) if item.isCarriedBy == self
        ]

if __name__ == '__main__':
    mgr = Manager()
    fg = mgr.make(Guild, "Fighter's Guild", 2)
    hat = mgr.make(Hat, 'helmet')
    fb = mgr.make(Spell, 'Fireball')
    potion = mgr.make(Item, 'Elixir of Health')
    char1 = mgr.make(Character, 'Conan')
    char2 = mgr.make(Character, 'Sonja')
    char3 = mgr.make(Character, 'Pee-Wee')
    char1.isEmployedBy = fg
    char2.isEmployedBy = fg
    char3.isEmployedBy = fg
    print('Members of the ' + fg.name + ':')
    print([char.name for char in fg.employs])
    char1.isWearing = hat
    char2.isWearing = hat
    print(char1.name + ' is wearing a ' + char1.isWearing.style)
    print(char2.isWearing)
    char2.knows.append(fb)
    print(char2.name + ' knows the following spells:')
    print([spell.name for spell in char2.knows])
    potion.isCarriedBy = char1
    print(char1.name + ' is carrying the following items:')
    print([item.name for item in char1.isCarrying])
