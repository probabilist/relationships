from objrelations2 import Managed
from objrelations2 import ManyToOne, OneToOne, ManyToMany, OneToMany

ARMOR_WEIGHTS = ['light', 'medium', 'heavy']
CLASSES = ['mage', 'cleric', 'fighter']

class Character(Managed):
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

class Guild(Managed):
    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    def __repr__(self):
        return '<Guild ' + repr(self.name) + '>'

class Hat(Managed):
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

class Spell(Managed):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Spell ' + repr(self.name) + '>'

class Item(Managed):
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
    conan = Character('Conan', 'fighter', 1, 2)
    sonja = Character('Sonja', 'cleric', 1, 1)
    peewee = Character('Pee-Wee', 'mage', 2, 1)

    fg = Guild("Fighter's Guild", 2)
    mg = Guild("Mage's Guild", 2)

    helmet = Hat("Thor's Helmet", 'heavy')
    cap = Hat('Red Hood', 'light')

    fb = Spell('Fireball')
    sleep = Spell('Sleep')

    potion = Item('Elixir of Health')
    dagger = Item('Blade of Death')
    ring = Item('The One Ring')

    isEmployedBy = IsEmployedBy()
    employs = isEmployedBy.inverse

    isWearing = IsWearing()
    isWornBy = isWearing.inverse

    knows = Knows()
    isKnownBy = knows.inverse

    isCarrying = IsCarrying()
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
    isCarriedBy[ring] = conan
    while peewee in isCarrying.keys():
        peeweesItem = next(iter(isCarrying[peewee]))
        isCarrying.discard((peewee, peeweesItem))
        isCarrying[conan] = peeweesItem
    print(isCarrying, isCarriedBy, sep='\n')

