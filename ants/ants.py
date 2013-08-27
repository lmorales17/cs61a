"""
The ants module implements game logic for Ants Vs. SomeBees.
Name: Luis Morales and James Musk
Login: cs61a-3w and cs61a-wb
TA: Sharad Vikram
Section: 120
"""

import random
import sys
from ucb import main, interact, trace
from collections import OrderedDict


################
# Core Classes #
################


class Place(object):
    """A Place holds insects and has an exit to another Place."""

    def __init__(self, name, exit=None):
        """Create a Place with the given exit.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        if self.exit != None:
            self.exit.entrance = self

    def add_insect(self, insect):
        """Add an Insect to this Place.

        There can be at most one Ant in a Place, unless exactly one of them is
        a BodyguardAnt (Phase 2), in which case there can be two. If add_insect
        tries to add more Ants than is allowed, an assertion error is raised.

        There can be any number of Bees in a Place.
        """
        if insect.is_ant():
            # Phase 2: Special handling for BodyguardAnt
            if self.ant:
                if self.ant.can_contain(insect):
                    self.ant.contain_ant(insect)
                    self.ant.place = self
                else:
                    insect.contain_ant(self.ant)
                    self.ant = insect
                    insect.place = self
            else:
                assert self.ant is None, 'Two ants in {0}'.format(self)
                self.ant = insect
                insect.place = self
        else:
            self.bees.append(insect)
        insect.place = self



    def remove_insect(self, insect):
        """Remove an Insect from this Place."""
        if hasattr(insect, 'name') and insect.name == 'Queen' and insect.real_queen == True: #You can't remove the real queen!
            return
        if not insect.is_ant():
            self.bees.remove(insect)
        else:
            assert self.ant == insect, '{0} is not in {1}'.format(insect, self)
            if insect.ant != None:
                self.ant = insect.ant
                insect.place = None
                return
            self.ant = None
        insect.place = None

    def __str__(self):
        return self.name


class Insect(object):
    """An Insect, the base class of Ant and Bee, has armor and a Place."""
    watersafe = False
    ant = None

    def __init__(self, armor, place=None):
        """Create an Insect with an armor amount and a starting Place."""
        self.armor = armor
        self.place = place  # set by Place.add_insect and Place.remove_insect


    def reduce_armor(self, amount):
        """Reduce armor by amount, and remove the insect from its place if it
        has no armor remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_armor(2)
        >>> test_insect.armor
        3
        """
        self.armor -= amount
        if self.armor <= 0:
            print('{0} ran out of armor and expired'.format(self))
            self.place.remove_insect(self)

    def action(self, colony):
        """Perform the default action that this Insect takes each turn.

        colony -- The AntColony, used to access game state information.
        """

    def is_ant(self):
        """Return whether this Insect is an Ant."""
        return False

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    watersafe = True

    def sting(self, ant):
        """Attack an Ant, reducing the Ant's armor by 1."""
        ant.reduce_armor(1)

    def move_to(self, place):
        """Move from the Bee's current Place to a new Place."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Phase 2: Special handling for NinjaAnt
        """if self.place.ant != None:
            if self.place.ant.blocks_path == False:
                return False
            else:    
                return True
        else:
            False"""
        if (self.place.ant != None and self.place.ant.blocks_path == False) or self.place.ant == None:
            return False
        else:
            return True

    def action(self, colony):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        colony -- The AntColony, used to access game state information.
        """
        if self.blocked():
            self.sting(self.place.ant)
        else:
            if self.place.name != 'Hive' and self.armor > 0:
                self.move_to(self.place.exit)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    damage = 0
    food_cost = 0
    blocks_path = True
    container = False
    steroids = False

    def __init__(self, armor=1):
        """Create an Ant with an armor quantity."""
        Insect.__init__(self, armor)

    def is_ant(self):
        return True

    def can_contain(self, other):
        if self.container == True and self.ant == None and other.container == False:
            return True
        else:
            return False


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    food_cost = 2

    def action(self, colony):
        """Produce 1 additional food for the colony.

        colony -- The AntColony, used to access game state information.
        """
        colony.food += 1

def random_or_none(l):
    """Return a random element of list l, or return None if l is empty."""
    return random.choice(l) if l else None


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    food_cost = 4
    min_range = 0
    max_range = 10

    def nearest_bee(self, hive):
        """Return the nearest Bee in a Place that is not the Hive, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee.

        Problem B5: This method returns None if there is no Bee in range.
        """

        place = self.place
        counter = 0
        while place.name != 'Hive': #iterate over places in front of ant until it reaches the hive
            if random_or_none(place.bees) != None and counter >= self.min_range and counter <= self.max_range: #ensures that the iteration doesn't stop if a bee is found but it is not in range
                return random_or_none(place.bees)
            place = place.entrance
            counter += 1
        return None

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its armor."""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, colony):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee(colony.hive))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    name = 'Hive'

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, colony):
        exits = [p for p in colony.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(colony.time, []):
            bee.move_to(random.choice(exits))


class AntColony(object):
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    queen -- the place where the queen resides
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """
    def __init__(self, strategy, hive, ant_types, create_places, food=4):
        """Create an AntColony for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        hive -- a Hive full of bees
        ant_types -- a list of ant constructors
        create_places -- a function that creates the set of places
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.hive = hive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.configure(hive, create_places)

    def configure(self, hive, create_places):
        """Configure the places in the colony."""
        self.queen = Place('AntQueen')
        self.places = OrderedDict()
        self.bee_entrances = []
        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = hive
                self.bee_entrances.append(place)
        register_place(self.hive, False)
        create_places(self.queen, register_place)

    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        while len(self.queen.bees) == 0 and len(self.bees) > 0:
            self.hive.strategy(self)    # Bees invade
            self.strategy(self)         # Ants deploy
            for ant in self.ants:       # Ants take actions
                if ant.armor > 0:
                    ant.action(self)
            for bee in self.bees:       # Bees take actions
                if bee.armor > 0:
                    bee.action(self)
            self.time += 1
        if len(self.queen.bees) > 0:
            print('The ant queen has perished. Please try again.')
        else:
            print('All bees are vanquished. You win!')

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        constructor = self.ant_types[ant_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + ant_type_name)
        else:
            self.places[place_name].add_insect(constructor())
            self.food -= constructor.food_cost

    def remove_ant(self, place_name):
        """Remove an Ant from the Colony."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status

def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]

def interactive_strategy(colony):
    """A strategy that starts an interactive session and lets the user make
    changes to the colony.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking:
    colony.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('colony: ' + str(colony))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

def start_with_strategy(args, strategy):
    usage = """python3 [ants.py|ants_gui.py] [OPTIONS]
    Run the Ants vs. SomeBees project.

    -h, --help      Prints this help message
    -f, --full      Loads a full layout and assault plan
    -w, --water     Loads a full map with water.
    -i, --insane    Loads an insane assault plan. Good luck!
    """
    if "-h" in args or "--help" in args:
        print(usage)
        return
    assault_plan = make_test_assault_plan()
    layout = test_layout
    if '-f' in args or '--full' in args:
        assault_plan = make_full_assault_plan()
        layout = dry_layout
    if '-w' in args or '--water' in args:
        layout = mixed_layout
    if '-i' in args or '--insane' in args:
        assault_plan = make_insane_assault_plan()
    AntColony(strategy, Hive(assault_plan), ant_types(), layout).simulate()


###########
# Layouts #
###########

def mixed_layout(queen, register_place, length=8, tunnels=3, moat_frequency=3):
    """Register Places with the colony."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)

def test_layout(queen, register_place, length=8, tunnels=1):
    mixed_layout(queen, register_place, length, tunnels, 0)

def dry_layout(queen, register_place, length=8, tunnels=3):
    mixed_layout(queen, register_place, length, tunnels, 0)


#################
# Assault Plans #
#################


class AssaultPlan(dict):
    """The Bees' plan of attack for the Colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def __init__(self, bee_armor=3):
        self.bee_armor = bee_armor

    def add_wave(self, time, count):
        """Add a wave at time with count Bees that have the specified armor."""
        bees = [Bee(self.bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the hive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]

def make_test_assault_plan():
    return AssaultPlan().add_wave(2, 1).add_wave(3, 1)

def make_full_assault_plan():
    plan = AssaultPlan().add_wave(2, 1)
    for time in range(3, 15, 2):
        plan.add_wave(time, 1)
    return plan.add_wave(15, 8)

def make_insane_assault_plan():
    plan = AssaultPlan(4).add_wave(1, 2)
    for time in range(3, 15):
        plan.add_wave(time, 1)
    return plan.add_wave(15, 20)



##############
# Extensions #
##############


class Water(Place):
    """Water is a place that can only hold 'watersafe' insects."""
    def add_insect(self, insect):
        """Add insect if it is watersafe, otherwise reduce its armor to 0."""
        print('added', insect, insect.watersafe)
        Place.add_insect(self, insect)
        if not insect.watersafe:
            insect.reduce_armor(insect.armor)


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 4
    implemented = True

    def reduce_armor(self, amount):
        enemy_bee_list = self.place.bees[:]
        Ant.reduce_armor(self, amount)
        if self.armor <= 0:
            for bee in enemy_bee_list:
                Insect.reduce_armor(bee, self.damage)


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 3 places away."""

    name = 'Long'
    min_range = 4
    food_cost = 3
    implemented = True


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees within 3 places."""

    name = 'Short'
    max_range = 3
    food_cost = 3
    implemented = True


class WallAnt(Ant):
    """WallAnt is an Ant which has a large amount of armor."""

    name = 'Wall'
    food_cost = 4
    implemented = True

    def __init__(self):
        self.armor = 4
        Ant.__init__(self, self.armor)


class NinjaAnt(Ant):
    """NinjaAnt is an Ant which does not block the path and does 1 damage to
    all Bees in the exact same Place."""

    name = 'Ninja'
    food_cost = 6
    blocks_path = False
    implemented = True
    damage = 1

    def action(self, colony):
        for bee in self.place.bees[:]:
            Insect.reduce_armor(bee, self.damage)


class ScubaThrower(ThrowerAnt):
    """ScubaThrower is a ThrowerAnt which is watersafe."""

    name = 'Scuba'
    food_cost = 5
    watersafe = True
    implemented = True


class HungryAnt(Ant):
    """HungryAnt will take three "turns" to eat a Bee in the same space as it.
    While eating, the HungryAnt can't eat another Bee.
    """
    name = 'Hungry'
    food_cost = 4
    implemented = True
    time_to_digest = 3


    def __init__(self):
        Ant.__init__(self)
        self.digesting = 0

    def eat_bee(self, bee):
        if bee:
            bee.reduce_armor(bee.armor)
            self.digesting = self.time_to_digest

    def action(self, colony):
        if self.digesting > 0:
            self.digesting -= 1
        else:
            self.eat_bee(random_or_none(self.place.bees))



class BodyguardAnt(Ant):
    """BodyguardAnt provides protection to other Ants."""
    name = 'Bodyguard'
    food_cost = 4
    container = True
    implemented = True

    def __init__(self):
        Ant.__init__(self, 2)
        self.ant = None  # The Ant hidden in this bodyguard

    def contain_ant(self, ant):
        self.ant = ant

    def reduce_armor(self, amount):
        place_info = self.place
        Ant.reduce_armor(self, amount)
        if self.armor <= 0:
            place_info.ant = self.ant

    def action(self, colony):
        if self.ant:
            self.ant.action(colony)


class QueenPlace(object):
    """Stores the location of the Queen of the colony, as well as the original colony place information"""
    def __init__(self, colony_location, queen_location):
        self.colony_location = colony_location
        self.queen_location = queen_location

    @property
    def bees(self):
        return self.colony_location.bees + self.queen_location.bees 
        



class QueenAnt(ThrowerAnt):
    """The Queen of the colony.  The game is over if a bee enters her place."""

    name = 'Queen'
    watersafe = True
    implemented = True
    food_cost = 2
    actualizations = 0
    real_queen = True

    def __init__(self):
        ThrowerAnt.__init__(self, 1)
        QueenAnt.actualizations += 1 #calling QueenAnt instead of self keeps the actualizations variable non-local
        if QueenAnt.actualizations > 1: #ensures that only one Queen can be placed per game
            self.real_queen = False

    def action(self, colony):
        """A queen ant throws a leaf, but also doubles the damange of ants
        behind her.  Impostor queens do only one thing: die."""
        if not self.real_queen: #Kills the imposter queen
            return self.reduce_armor(self.armor)       
        colony_location = colony.queen #stores the original colony information
        colony.queen = QueenPlace(colony_location, self.place) #ensures that the game ends once a bee either reaches the end of the tunnel or enters the queen's place
        ThrowerAnt.action(self, colony)
        places = self.place.exit #place behind the queen
        while places: #iterates through ants in the places behind the queen
            if places.ant:
                if not places.ant.steroids: #ensures no exponential growth of damage
                    places.ant.damage = 2*(places.ant.damage)
                    places.ant.steroids = True
            places = places.exit



class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = True

    def __init__(self):
        Ant.__init__(self, 0)


##################
# Status Effects #
##################

def make_slow(action):
    """Return a new action method that calls action every other turn.

    action -- An action method of some Bee
    """
    "*** YOUR CODE HERE ***"

def make_stun(action):
    """Return a new action method that does nothing.

    action -- An action method of some Bee
    """
    "*** YOUR CODE HERE ***"

def apply_effect(effect, bee, duration):
    """Apply a status effect to a Bee that lasts for duration turns."""
    "*** YOUR CODE HERE ***"

"""
class SlowThrower(ThrowerAnt):
    """'ThrowerAnt that causes Slow on Bees.'"""

    name = 'Slow'
    food_cost = 4
    implemented = False

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 3)

    def make_slow(self, action):
        if colony.time % 2 == 0:
            return action

    def apply_effect(self, effect, bee, duration):
        bee.action


class StunThrower(ThrowerAnt):
    """'ThrowerAnt that causes Stun on Bees.'"""

    name = 'Stun'
    food_cost = 6
    implemented = False

    def throw_at(self, target):
        if target:
            apply_effect(make_stun, target, 1)

    def make_stun(self, action):

    def make_slow(self, effect, bee, duration):
"""

@main
def run(*args):
    start_with_strategy(args, interactive_strategy)
