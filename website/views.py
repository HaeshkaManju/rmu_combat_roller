'''
We'll be using "Blueprint", a component of the Flask package.
Blueprint allows us to actually render python inside of our HTML.
Thus we're calling this file "Views".py because it enables us to
yeah... VIEW the code/HTML.
Incidentally, we'll also have a file called auth that does the
same thing, but it is for any elements pertaining to security.
'''
from flask import Blueprint, render_template, request, flash
from .db_calls import fetch_single_table, determine_attack_table, attack_roll_results
from .combat_math import *

# I'm going to use comments, for now, to separate the routes
## into individual categories.

##############################################################################
# Summarize Modifiers #
##############################################################################
validation_list_OB = ['defensive_bonus_modifiers_view', 'hit_loss_penalties_view',
                'movement_penalties_view', 'protect_view', 'subdual_view',
                'armors_penalty_vambraces_view']

validation_list_DB = ['defensive_bonus_modifiers_view']

validation_list_crits = ['charging_bonus_view', 'slaying_crit_mod_view']

def intify_modifiers(dict_obj, *attrs, default=0):
    result = dict_obj
    for attr in attrs:
        if attr not in result:
            return [0]
        result = result[attr]
        intified = [int(item) for item in result]
        print(intified)
    
    return intified

views = Blueprint('views',__name__)
'''
It is simply convention to name the above object "views",
or more accurately: to keep it the same name as the file,
for simplicity and clarity.
The 'views' in the parenthesis, refers to the folder where
the HTML will be stored.
'''

'''
The process for creating a route is as follows:
1) A decorator that uses the "views" reference.
2) Call the route method.
3) Supply the index (the /something) to indicate the URL.
4) A function, with a recognizable name.
5) A return, within the function, that decides what to render.
6) Finally - back in the __init__.py file: we register the route.
@views		.route()		("")
^ Decorator ^ route method.  ^ what HTML REF we want

'''
##################################################################
# Home #
##################################################################
@views.route("/", methods=['GET', 'POST'])
@views.route("home", methods=['GET', 'POST'])
def home():
    '''
    The above concept is called a function "deocrator".
    Using a double-decorator allows one or more routes to work 
        and be applied to the same end point.
        Weirdly useful when we're talking about "#" pages.
    / and home will be used to be the "landing page" for the
        the script.
    home html will extend from base.
    '''
    
    weapons = fetch_single_table("weapons")
    armor_type = fetch_single_table("armor_type")
    offensive_bonus_modifiers_view = fetch_single_table("offensive_bonus_modifiers_view")
    defensive_bonus_modifiers_view = fetch_single_table("defensive_bonus_modifiers_view")
    hit_loss_penalties_view = fetch_single_table("hit_loss_penalties_view")
    movement_penalties_view = fetch_single_table("movement_penalties_view")
    armors_penalty_vambraces_view = fetch_single_table("armors_penalty_vambraces_view")
    charging_bonus_view = fetch_single_table("charging_bonus_view")
    slaying_crit_mod_view = fetch_single_table("slaying_crit_mod_view")
    protect_view = fetch_single_table("protect_view")
    subdual_view = fetch_single_table("subdual_view")
    subdual_secondaries_view = fetch_single_table("subdual_secondaries_view")

    if request.method == "POST":
        '''
        This feels like it's going to run long.  Should this entire
            IF construct be its own function?  Is that possible?
        '''
        data = request.form.to_dict(flat=False)
        print(type(data))
        print(data)
        # Assess all of our OB mods.
        base_set_OB = []
        for i in validation_list_OB:
            base_set_OB.extend(intify_modifiers(data, i, default=False))
        print(base_set_OB)
        sum_OB_mods = sum(base_set_OB)
        print(f"OB Mods: {sum_OB_mods}")
        
        # Assess all of our DB mods.
        base_set_DB = []
        for i in validation_list_DB:
            base_set_DB.extend(intify_modifiers(data, i, default=False))
        print(base_set_DB)
        sum_DB_mods = sum(base_set_DB)
        print(f"DB Mods: {sum_DB_mods}")
        
        # Assess all of our Crit mods.
        base_set_crit = []
        for i in validation_list_crits:
            base_set_crit.extend(intify_modifiers(data, i, default=False))
        print(base_set_crit)
        sum_crit_mods = sum(base_set_crit)
        print(f"Crit Mods: {sum_crit_mods}")
        
        # All "Attacker" info
        attackTable = request.form.get("weapons")
        print(f"Attack Table: {attackTable}")
        attackerOB = request.form.get("ob")
        print(f"Attacker OB: {attackerOB}")
        # All "Defender" info
        defenderAT = request.form.get("armor_type")
        print(f"Defender Armor Type: {defenderAT}")
        defenderDB = request.form.get("db")
        print(f"Defender DB: {defenderDB}")
        # Random, Open-Ended Attack Roll
        ## Use the OEAttackRoll Function.
        
        # Run all the #s through combat_math
        calculatedOB = calc_attack_bonus(attackerOB, sum_OB_mods)
        calculatedDB = calc_defense_bonus(defenderDB, sum_DB_mods)
        calculatedRoll = roll_d100_fullOE()
        totalRoll = calc_total_attack_roll(calculatedOB, calculatedDB, calculatedRoll)
        
        chosen_table = determine_attack_table(attackTable)
        print(chosen_table)
        to_display = attack_roll_results(totalRoll, chosen_table, defenderAT)
        
        flash(f"Your Attack Roll is: {to_display}.", category="success")
        
    return render_template('home.html',
        weapons = weapons,
        armor_type = armor_type,
        offensive_bonus_modifiers_view = offensive_bonus_modifiers_view,
        defensive_bonus_modifiers_view = defensive_bonus_modifiers_view,
        hit_loss_penalties_view = hit_loss_penalties_view,
        movement_penalties_view = movement_penalties_view,
        charging_bonus_view = charging_bonus_view,
        slaying_crit_mod_view = slaying_crit_mod_view,
        protect_view = protect_view,
        subdual_view = subdual_view,
        subdual_secondaries_view = subdual_secondaries_view,
        armors_penalty_vambraces_view = armors_penalty_vambraces_view
        )
##################################################################
# Results #
##################################################################
@views.route("/results")
def results():
    '''
    To be used to display the results of combat rolls.
    Needs to take into account the Attacker and Defender info.
    Info needs to be passed into results(__) as variables.
    
    Not sure if this is needed.
    '''
    return render_template('results.html')
##################################################################
# Misc Table Displays #
##################################################################
@views.route("/tables")
def tables():
    '''
    To be used to display tables in whole form.
    These tables can be basic tables or contextualized tables.
    This should NOT be for displaying the results of combat rolls.
    Tables should be displayed based on a menu-select item by
        the user.
    '''
    from db_calls import validate_connection
    return render_template('tables.html')
##################################################################
# Attack Table Displays #
##################################################################

##################################################################
# Crit Table Displays #
##################################################################
@views.route("/crits")
def crits():
    '''
    '''
    return "base.html"
##################################################################
# Fumble Table Displays #
##################################################################

##################################################################
# User Input Displays #
##################################################################