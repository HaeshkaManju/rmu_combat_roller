# combat_math
import random
'''
    This intent of this file is to process the math necessary to calculate:
    1) The total Offensive Bonus (OB) of the Attacker,
    2) The total Defensive Bonus (DB) of the Defender,
    3) The total Dice Roll of the Attack Roll,
    4) The final AttackRollValue.
    
    As of this time, this file will NOT handle:
    A) Combat Size Modifiers,
    B) Critical Severity Changes,
    C) Random or non-prescribed modifiers to OB/DB (such as a miscellaneous
        bonus of +10 from a DM's verbal say-so.)
    D) Any modifiers that would have been present on a character sheet
        such as skills, skill ranks, magic items, etc.
'''
   
# Most of these functions might have just become unecessary due to the way
## that I am getting the OB/DB in the first place.

##############################################################################
# Calculate Total Offensive Bonus #
##############################################################################

def calc_attack_bonus(offensive_bonus, *args):
    '''
    Purpose: Calculate part of the Total Offensive Bonus (OB) of an attack.
    OB is determined as:
        A) Skill Bonus +
        B) All Offensive Combat Modifiers +
        C) Miscellaneous Modifiers = Total OB.
    This function will only perform calculations on part B.  Part A will
        be assumed to have been calculated by the player through input in
        the "OB" field on the Input Screen.
        Part C will be assumed to have been included in A for now.
            Later implementation: add a bonus misc field.
    
    Why am I doing a separate set of Attack and Defender functions?
        Mostly because I want to make it visually easier for me to update
        this code later when there will surely be more things to factor.
    '''
    # initialize our base value to zero.
    total_OB = 0
    print(f"Initialized OB: {total_OB}")
    current_OB = int(offensive_bonus)
    print(f"Including Character Sheet OB: {current_OB}")
    # have a list of all of the possible modifiers.  Will likely be deleted
    ## later, but for now, useful to keep track of everything.
    modifiers = [*args]
    print(f"We are including these modifiers: {modifiers}.")
    total_of_modifiers = sum(modifiers)
    print(type(total_of_modifiers))
    print(f"Total of modifiers: {total_of_modifiers} OB.")
    
    return current_OB + total_of_modifiers

##############################################################################
# Calculate Total Defensive Bonus #
##############################################################################
def calc_defense_bonus(defensive_bonus, *args):
    '''
    Purpose: Calculate part of the Total Defensive Bonus (DB) of an attack.
    DB is determined as:
        A) Stat or Skill Bonus +
        B) All Defensive Combat Modifiers +
        C) Miscellaneous Modifiers = Total DB.
    This function will only perform calculations on part B.  Part A will
        be assumed to have been calculated by the player through input in
        the "DB" field on the Input Screen.
    '''
    # initialize our base value to zero.
    total_DB = 0
    print(f"Initialized DB: {total_DB}")
    current_DB = int(defensive_bonus)
    print(f"Including Character Sheet DB: {current_DB}")
    # have a list of all of the possible modifiers.  Will likely be deleted
    ## later, but for now, useful to keep track of everything.
    modifiers = [*args]
    print(f"We are including these modifiers: {modifiers}.")
    total_of_modifiers = sum(modifiers)
    print(f"Total of modifiers: {total_of_modifiers} DB.")
   
    return current_DB + total_of_modifiers

##############################################################################
# Full Open Ended D100 Dice Roll
##############################################################################
def roll_d100_fullOE():
    '''
    A D100 is a die that ranges in integer values from 1 to 100.
    An Open ended roll is one in which the die may be rolled again if the
        unmodified value falls within a certain range, and the totals are
        added together.
    WDice Rolls can be high, low, or full open-ended.
    Reroll and add (or subtract) the 2nd result to/from the first on:
    LOW: rolls of 01-05, roll again and subtract from the previous.
    HIGH: rolls of 96-100, roll again and add to the previous.
    FULL: Both Low and High logic applied.
    '''
    total_roll = 0
    print(f"total roll: {total_roll}")
    roll = random.randrange(1, 100, 1)
    total_roll += roll
    print(f"Roll: {roll}")
    print(f"Total Roll: {total_roll}")
    while roll >= 96:
        roll = random.randrange(1, 100, 1)
        print(f"Explody Roll: {roll}")
        total_roll += roll
        print(f"New Total Roll: {total_roll}")
    while roll <= 5:
        roll = random.randrange(1, 100, 1)
        print(f"Explody Roll: {roll}")
        total_roll -= roll
        print(f"New Total Roll: {total_roll}")
    return total_roll

##############################################################################
# Total Attack Roll
##############################################################################
def calc_total_attack_roll(modsOB, modsDB, diceRoll):
    '''
    Probably the least-ever necessary function, but for completeness' sake,
        I'm including it.  Gather the three calculated variables perform:
            final_OB - final_DB + attack roll = Total.
    This should give us the appropriate # to send into the Attack Table, and
        I want to be juggling as few data-names as possible.
    '''
    total_attack_roll = modsOB - modsDB + diceRoll
    print(f"Total Attack Roll is: {total_attack_roll}.")
    return total_attack_roll
    
##############################################################################
# TEST Calls
##############################################################################
'''
final_OB = calc_attack_bonus(2, 7, 3, 6, 18, -4, -10)
print(f"Total OB is: {final_OB}.")
final_DB = calc_defense_bonus(7, 5, 6, 7, -10, 1)
print(f"Total DB is: {final_DB}.")
attack_roll = roll_d100_fullOE()
print(f"Attack Roll is: {attack_roll}.")
calc_total_attack_roll(final_OB, final_DB, attack_roll)
'''
##############################################################################
##############################################################################