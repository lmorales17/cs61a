"""The Game of Hog"""

from dice import four_sided_dice, six_sided_dice, make_test_dice
from ucb import main, trace, log_current_line, interact

goal = 100          # The goal of Hog is to score 100 points.
commentary = False  # Whether to display commentary for every roll.


# Taking turns

def roll_dice(num_rolls, dice=six_sided_dice, who='Boss Hogg', ones_lose=True):
    """Calculate WHO's turn score after rolling DICE for NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A function of no args and returns an integer outcome.
    who:        Name of the current player, for commentary.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Must roll at least zero.'
    k = 0
    score = 0
    rolled_one = False
    while k != num_rolls:
        outcome, k = dice(), k+1
        if ones_lose and outcome == 1: #pig out rule
            rolled_one = True   
        score = outcome + score
        if commentary:
            announce(outcome, who)
    if rolled_one:
        return 1
    else:
        return score
        

def take_turn(num_rolls, opp_score, dice=six_sided_dice, who='Boss Hogg', ones_lose=True):
    """Simulate a turn in which WHO chooses to roll NUM_ROLLS, perhaps 0.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args and returns an integer outcome.
    who:             Name of the current player, for commentary.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    if commentary:
        print(who, 'is going to roll', num_rolls, 'dice')
    turn_score = roll_dice(num_rolls, dice, who, ones_lose)
    if num_rolls == 0: #free bacon rule
        turn_score = (opp_score//10)+1
    if turn_score%6 == 0: #touchdown rule
        turn_score = (turn_score/6) + turn_score
    return turn_score

def take_turn_test():
    """Test the roll_dice and take_turn functions using test dice."""
    print('-- Testing roll_dice with deterministic test dice --')
    dice = make_test_dice(4, 6, 1)
    assert roll_dice(2, dice) == 10, 'First two rolls total 10'

    dice = make_test_dice(4, 6, 1)
    assert roll_dice(3, dice) == 1, 'Third roll is a 1'

    dice = make_test_dice(1, 2, 3)
    assert roll_dice(3, dice) == 1, 'First roll is a 1'

    print('-- Testing take_turn --')
    dice = make_test_dice(4, 6, 1)
    assert take_turn(2, 0, dice) == 10, 'First two rolls total 10'

    dice = make_test_dice(4, 6, 1)
    assert take_turn(3, 20, dice) == 1, 'Third roll is a 1'

    print('-- Testing Free Bacon rule --')
    assert take_turn(0, 34) == 4, 'Opponent score 10s digit is 3'
    assert take_turn(0, 71) == 8, 'Opponent score 10s digit is 7'
    assert take_turn(0,  7) == 1, 'Opponont score 10s digit is 0'

    print('-- Testing Touchdown rule --')
    dice = make_test_dice(6)
    assert take_turn(1, 0, dice) == 7, 'Original score was 6'
    assert take_turn(2, 0, dice) == 14, 'Original score was 12'
    assert take_turn(0, 50, dice) == 7, 'Original score was 6'

    print('-- Testing 49ers rule --')
    dice = make_test_dice(1)
    assert roll_dice(3, dice, ones_lose=False) == 3, '49ers rule in effect'
    assert take_turn(10, 0, dice, ones_lose=False) == 10, '49ers rule in effect'
    assert take_turn(6, 0, dice, ones_lose=False) == 7, '49ers and Touchdown rule'

    '*** You may add more tests here if you wish ***'

    print('Tests for roll_dice and take_turn passed.')


# Commentator

def announce(outcome, who):
    """Print a description of WHO rolling OUTCOME."""
    print(who, 'rolled a', outcome)
    print(draw_number(outcome))

def draw_number(n, dot='*'):
    """Return a text representation of rolling the number N.
    If a number has multiple possible representations (such as 2 and 3), any
    valid representation is acceptable.

    >>> print(draw_number(5))
     -------
    | *   * |
    |   *   |
    | *   * |
     -------

    >>> print(draw_number(6, '$'))
     -------
    | $   $ |
    | $   $ |
    | $   $ |
     -------
    """
    if n == 1:
        c = True
        f, b, s = False, False, False
    elif n == 2:
        f = True
        c, s,  b = False, False, False
    elif n == 3:
        f, c = True, True
        s, b = False, False
    elif n == 4:
        b, f = True, True
        s, c = False, False
    elif n == 5:
        s = False
        c, f, b = True, True, True
    elif n == 6:
        f, b, s = True, True, True
        c = False
    return draw_dice(c, f, b, s, dot)

def draw_dice(c, f, b, s, dot):
    """Return an ASCII art representation of a die roll.

    c, f, b, & s are boolean arguments. This function returns a multi-line
    string of the following form, where the letters in the diagram are either
    filled if the corresponding argument is true, or empty if it is false.

     -------
    | b   f |
    | s c s |
    | f   b |
     -------

    The sides with 2 and 3 dots have 2 possible depictions due to rotation.
    Either representation is acceptable.

    This function uses Python syntax not yet covered in the course.

    c, f, b, s -- booleans; whether to place dots in corresponding positions.
    dot        -- A length-one string to use for a dot.
    """
    assert len(dot) == 1, 'Dot must be a single symbol'
    border = ' -------'
    def draw(b):
        return dot if b else ' '
    c, f, b, s = map(draw, [c, f, b, s])
    top = ' '.join(['|', b, ' ', f, '|'])
    middle = ' '.join(['|', s, c, s, '|'])
    bottom = ' '.join(['|', f, ' ', b, '|'])
    return '\n'.join([border, top, middle, bottom, border])


# Game simulator

def num_allowed_dice(score, opponent_score):
    """Return the maximum number of dice allowed this turn. The maximum
    number of dice allowed is 10 unless the sum of SCORE and
    OPPONENT_SCORE has a 7 as its ones digit.

    >>> num_allowed_dice(1, 0)
    10
    >>> num_allowed_dice(5, 7)
    10
    >>> num_allowed_dice(7, 10)
    1
    >>> num_allowed_dice(3, 24)
    1
    """
    #Ensures Hog Tied Rule Gets Implemented
    tester = score+opponent_score
    if tester%10 == 7 or tester//10 == 7 or (tester//10)-10 == 7:
        return 1
    else:
        return 10

def select_dice(score, opponent_score):
    """Select 6-sided dice unless the sum of scores is a multiple of 7.

    >>> select_dice(4, 24) == four_sided_dice
    True
    >>> select_dice(16, 64) == six_sided_dice
    True
    """
    #Ensures Hog Wild Rule Is Implemented
    tester = score+opponent_score
    if tester%7 == 0:
        return four_sided_dice
    else:
        return six_sided_dice

def other(who):
    """Return the other player, for players numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return (who + 1) % 2

def name(who):
    """Return the name of player WHO, for player numbered 0 or 1."""
    if who == 0:
        return 'Player 0'
    elif who == 1:
        return 'Player 1'
    else:
        return 'An unknown player'

def play(strategy0, strategy1):
    """Simulate a game and return 0 if the first player wins and 1 otherwise.

    A strategy function takes two scores for the current and opposing players.
    It returns the number of dice that the current player will roll this turn.

    If a strategy returns more than the maximum allowed dice for a turn, then
    the maximum allowed is rolled instead.

    strategy0:  The strategy function for player 0, who plays first.
    strategy1:  The strategy function for player 1, who plays second.
    """
    player0_score = 0
    player1_score = 0
    player = 0 # Which player is about to take a turn, 0 (first) or 1 (second)
    ones_lose = True
    while player0_score < 100 and player1_score < 100:
        if player == 0:
            roll_number0 = strategy0(player0_score, player1_score)
            if roll_number0 > num_allowed_dice(player0_score, player1_score): #Enforces maximum dice number rule
                roll_number0 = num_allowed_dice(player0_score, player1_score)
            dice_type0 = select_dice(player0_score, player1_score)
            if player0_score == 49:
                ones_lose = False
            roll_score0 = take_turn(roll_number0, player1_score, dice_type0, name(player), ones_lose)
            player0_score = player0_score+roll_score0
            player = other(player)
            ones_lose = True
        if player == 1:
            roll_number1 = strategy1(player1_score, player0_score)
            if roll_number1 > num_allowed_dice(player1_score, player0_score): #Enforces maximum dice number rule
                roll_number1 = num_allowed_dice(player1_score, player0_score)
            dice_type1 = select_dice(player1_score, player0_score)
            if player1_score == 49:
                ones_lose = False
            roll_score1 = take_turn(roll_number1, player0_score,dice_type1, name(player), ones_lose)
            player1_score = player1_score+roll_score1
            player = other(player)
            ones_lose = True
    if player0_score > player1_score:
        player = 0
    else:
        player = 1
    return player

# Basic Strategy

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two game scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice to roll.

    If a strategy returns more than the maximum allowed dice for a turn, then
    the maximum allowed is rolled instead.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


# Experiments (Phase 2)

def make_average(fn, num_samples=5000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> avg_dice = make_average(dice)
    >>> avg_dice()
    3.75
    >>> avg_score = make_average(roll_dice)
    >>> avg_score(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    def foo(*args):
        k = 0
        total = 0
        while k < num_samples:
            result = fn(*args)
            total = result+total
            k += 1
        return (total/num_samples)
    return foo

def compare_strategies(strategy, baseline=always_roll(5)):
    """Return the average win rate (out of 1) of STRATEGY against BASELINE."""
    as_first = 1 - make_average(play)(strategy, baseline)
    as_second = make_average(play)(baseline, strategy)
    return (as_first + as_second) / 2  # Average the two results

def eval_strategy_range(make_strategy, lower_bound, upper_bound):
    """Return the best integer argument value for MAKE_STRATEGY to use against
    the always-roll-5 baseline, between LOWER_BOUND and UPPER_BOUND (inclusive).

    make_strategy -- A one-argument function that returns a strategy.
    lower_bound -- lower bound of the evaluation range.
    upper_bound -- upper bound of the evaluation range.
    """
    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print('Win rate against the baseline using', value, 'value:', win_rate)
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value

def run_experiments():
    """Run a series of strategy experiments and report results."""
    result = eval_strategy_range(always_roll, 1, 10)
    print('Best always_roll strategy:', result)

    if True: # Change to True when ready to test make_comeback_strategy
        result = eval_strategy_range(make_comeback_strategy, 5, 15)
        print('Best comeback strategy:', result)

    if False: # Change to True when ready to test make_mean_strategy
        result = eval_strategy_range(make_mean_strategy, 1, 10)
        print('Best mean strategy:', result)

    "*** You may add additional experiments here if you wish ***"


# Strategies

def make_comeback_strategy(margin, num_rolls=5):
    """Return a strategy that rolls one extra time when losing by MARGIN."""
    def strategy(score, opponent_score):        
        num_rolls1 = num_rolls
        if opponent_score-score > margin:
            num_rolls1 = num_rolls1+1
        return num_rolls1
    return strategy

def make_mean_strategy(min_points, num_rolls=5):
    """Return a strategy that attempts to give the opponent problems."""
    def strategy(score, opponent_score):
        num_rolls1 = num_rolls
        if min_points <  (opponent_score//10)+1:
            num_rolls1 = 0
            return num_rolls1
        tester = score+opponent_score
        neo_tester = (tester+((opponent_score//10)+1))
        if neo_tester%10 == 7 or neo_tester//10 == 7 or  (neo_tester//10)-10 == 7:
            num_rolls1 = 0
            return num_rolls1
        if neo_tester%7 == 0:
            num_rolls1 = 0
            return num_rolls1
        return num_rolls1
    return strategy

def final_strategy(score, opponent_score):
    """Our final strategy uses several groups of conditionals in order to decide how many dice to roll. We ordered these groups of conditionals from most to least important, in order to ensure that they would be executed in this order as well. We threw in a final else statement which varies the num_roll according to what your score is in reference to the opponent's score: ie, how conservatively or risky to play just in general.
    """
    free_bacon = (opponent_score//10)+1
    scores_sum = (opponent_score+score)
    
    #Highly Prioritized Strategies
    if (100-score) <= free_bacon:
        return 0
    if score == 49:
        return 10
    elif score == 48 or score == 47:
        return 10

    #Mean Strategies Which Weaken the Opponent
    if (scores_sum+free_bacon)%10 == 7 or (scores_sum+free_bacon)//10 == 7 or ((scores_sum+free_bacon)//10)-10 ==7:
        return 0
    if (scores_sum+free_bacon)%7 == 0:
        return 0

    #General Strategy
    if (score>96):
        return 1
    elif (score>90):
        return 2
    if (score-opponent_score) > 30:
        return 3
    if (score-opponent_score) > 0:
        return 4
    else:
        return (int)((opponent_score-score)//10+5)


    
def final_strategy_test():
    """Compares final strategy to the baseline strategy."""
    print('-- Testing final_strategy --')
    print('Win rate:', compare_strategies(final_strategy))



# Interaction.  You don't need to read this section of the program.

def interactive_strategy(score, opponent_score):
    """Prints total game scores and returns an interactive tactic.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    print('Current score:', score, 'to', opponent_score)
    while True:
        response = input('How many dice will you roll? ')
        try:
            result = int(response)
        except ValueError:
            print('Please enter a positive number')
            continue
        if result < 0:
            print('Please enter a non-negative number')
        else:
            return result

def play_interactively():
    """Play one interactive game."""
    global commentary
    commentary = True
    print("Shall we play a game?")
    winner = play(interactive_strategy, always_roll(5))
    if winner == 0:
        print("You win!")
    else:
        print("The computer won.")

def play_basic():
    """Play one game in which two basic strategies compete."""
    global commentary
    commentary = True
    winner = play(always_roll(5), always_roll(6))
    if winner == 0:
        print("Player 0, who always wants to roll 5, won.")
    else:
        print("Player 1, who always wants to roll 6, won.")

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--take_turn_test', '-t', action='store_true')
    parser.add_argument('--play_interactively', '-p', action='store_true')
    parser.add_argument('--play_basic', '-b', action='store_true')
    parser.add_argument('--run_experiments', '-r', action='store_true')
    parser.add_argument('--final_strategy_test', '-f', action='store_true')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if execute:
            globals()[name]()
