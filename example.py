from objrelations import Manager
from objrelations import ManyToOne, OneToOne, ManyToMany, OneToMany

ARMOR_WEIGHTS = ['light', 'medium', 'heavy']
CLASSES = ['mage', 'cleric', 'fighter']

class Character():
    def __init__(self, name, class_, spellCap, invCap):
        if class_ not in CLASSES:
            raise ValueError(class_)
        self.name = name
        self.class_ = class_
        self.spellCap = spellCap
        self.invCap = invCap

    @property
    def classIndex(self):
        return CLASSES.index(self.class_)

    def __repr__(self):
        return '<Character ' + repr(self.name) + '>'

class Guild():
    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    def __repr__(self):
        return '<Guild ' + repr(self.name) + '>'

class Hat():
    def __init__(self, style, weight):
        if weight not in ARMOR_WEIGHTS:
            raise ValueError(weight)
        self.style = style
        self.weight = weight

    @property
    def weightIndex(self):
        return ARMOR_WEIGHTS.index(self.weight)

    def __repr__(self):
        return '<Hat ' + repr(self.style) + '>'

class Spell():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Spell ' + repr(self.name) + '>'

class Item():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Item ' + repr(self.name) + '>'

class IsEmployedBy(ManyToOne):
    def validate(self, char, guild):
        if guild in self.values() and len(self.inverse[guild]) >= guild.cap:
            print('The guild is full!')
            return False
        return True

class IsWearing(OneToOne):
    def validate(self, char, hat):
        if hat.weightIndex > char.classIndex:
            print(
                'A ' + char.class_ + ' cannot wear '
                + hat.weight + ' armor!'
            )
            return False
        return True

class Knows(ManyToMany):
    def validate(self, char, spell):
        if char in self.keys() and len(self[char]) >= char.spellCap:
            print('Your spellbook is full!')
            return False
        return True

class IsCarrying(OneToMany):
    def validate(self, char, item):
        if char in self.keys() and len(self[char]) >= char.invCap:
            print('Your backpack is full!')
            return False
        return True

if __name__ == '__main__':
    mgr = Manager()

    conan = mgr.make(Character, 'Conan', 'fighter', 1, 2)
    sonja = mgr.make(Character, 'Sonja', 'cleric', 1, 1)
    peewee = mgr.make(Character, 'Pee-Wee', 'mage', 2, 1)

    fg = mgr.make(Guild, "Fighter's Guild", 2)
    mg = mgr.make(Guild, "Mage's Guild", 2)

    helmet = mgr.make(Hat, "Thor's Helmet", 'heavy')
    cap = mgr.make(Hat, 'Red Hood', 'light')

    fb = mgr.make(Spell, 'Fireball')
    sleep = mgr.make(Spell, 'Sleep')

    potion = mgr.make(Item, 'Elixir of Health')
    dagger = mgr.make(Item, 'Blade of Death')
    ring = mgr.make(Item, 'The One Ring')

    isEmployedBy = mgr.make(IsEmployedBy)
    employs = isEmployedBy.inverse

    isWearing = mgr.make(IsWearing)
    isWornBy = isWearing.inverse

    knows = mgr.make(Knows)
    isKnownBy = knows.inverse

    isCarrying = mgr.make(IsCarrying)
    isCarriedBy = isCarrying.inverse

    isEmployedBy[conan] = fg
    isEmployedBy[sonja] = fg
    isEmployedBy[peewee] = fg
    isEmployedBy[peewee] = mg
    print(isEmployedBy, employs, sep='\n')

    isWearing[conan] = helmet
    try:
        isWearing[sonja] = helmet
    except ValueError:
        print(isWornBy[helmet].name + ' is wearing ' + helmet.style)
    isWearing[sonja] = cap
    print(isWearing, isWornBy, sep='\n')

    knows[conan] = fb
    knows[conan] = sleep
    knows[sonja] = sleep
    isKnownBy[fb] = sonja
    isKnownBy[fb] = peewee
    isKnownBy[sleep] = peewee
    print(knows, isKnownBy, sep='\n')

    isCarrying[peewee] = dagger
    isCarrying[peewee] = ring
    isCarrying[sonja] = ring
    isCarrying[sonja] = potion
    del isCarriedBy[ring]
    isCarrying[sonja] = potion
    try:
        isCarrying[conan] = potion
    except ValueError:
        print(isCarriedBy[potion].name + ' is carrying ' + potion.name)
    del isCarrying[peewee]
    isCarrying[conan] = dagger
    isCarrying[conan] = ring
    print(isCarrying, isCarriedBy, sep='\n')
