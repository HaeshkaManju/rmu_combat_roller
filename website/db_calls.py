'''
Helper Functions for DB Management
Functions for calling components of the database.
Divide this into files/classes as appropriate once I know what all needs to exist
    in the first place.
'''
import sqlite3

########################################################################################
# Pro Forma.
# helper_connection(), validate_connection(), and tuple_to_list
## are used to (see individual explanations)
########################################################################################
def helper_connection():
    '''
    Helper function to shortcut the other code.  Just import this
    into every other usage where we ask to look at the database.
    '''
    conn = sqlite3.connect('rmu_combat.db')
    curs = conn.cursor()
    return conn, curs
    
def validate_connection():
    '''
    This is meant to validate that I am successfully connecting to the database.
    This should be used whenever we create a new page, initially, to verify that
    jinja and the environment are looking into the correct folders, and that we
    have set the right paths for our connections.
    '''
    # conn_val should ONLY have a simple boolean on row1.
    ## All this is checking, is that this table has that singular row.
    conn, curs = helper_connection()
    result = curs.execute("SELECT * FROM 'conn_val'").fetchall()
    
    if (len(result))>0:
        print("You're connected.")
        verify_connection = 1
        conn.close()
    else:
        print("You're not connected.")
        verify_connection = 0
        conn.close()   
    return verify_connection

validate_connection()

def tuple_to_list(x):
    '''
    The Database is going to return a list from the individual tuples.
    Use whenever we need to have a list of lists from our DB calls.
    '''
    if type(x) == tuple:
        return list(x)
    elif type(x) == str:
        return [x]
    return "something derpy happened."
########################################################################################
# Fetching a Single Table and Displaying all of its Contents.
########################################################################################
def fetch_single_table(tableName):
    '''
    Hopefully, as the name of this function suggests: call this when we have
    1) an input
    2) a context where we need the full contents of a single database table.
    
    UPDATE ME: When we have user input in the Flask portion ready to go.
    
    Any table in the database with a "_view" at the end of the name is meant
        to be used with fetch_single_table()
    Any table with RAW in the name MUST muse this function.
    I feel like everything within the big for loop could be summarized as:
        row = list(map(str, row))
        but... I'm not sure what the best way to do this is.
    '''
    conn, curs = helper_connection()
    single_table_data = curs.execute(f"SELECT * FROM {tableName};").fetchall()
    conn.close()
    if (len(single_table_data))>0:
        #for row in single_table_data:
        #    row = list(row)
        #    row = [str(r) for r in row]
        #    print(", ".join(row))
        return single_table_data
    else:
        return None

############################################
# WARNO! #
############################################
'''
I opted to create a VIEW of the table and call
    the view table instead of the table
    itself.
Query Used:
CREATE VIEW weapons_view AS
SELECT weapon_name AS 'Weapon Name' FROM weapons;
ALL views should be constructed such that the
column names are user-readable. e.g.:
    "Weapon Name" not "weapon_name".
'''
########################################################################################
# Fetching a single Row from a single Table and Displaying all of its Contents.
########################################################################################
def fetch_single_result_from_single_table(tableName, argId):
    '''
    Yes, it's a long function name.  But, it's clear.
    We want a single result, from a single table.
    
    We are taking in a LOT of information in the
    query, but then we're dialing-in and grabbing
    only the specific row we need for display.
    
    This function should NEVER be called on a table/view that has
    "RAW" in the name.
    
    This currently does NOT work, as intended because it is lacking context.
    (see what happens when using 'skill_rank_bonus_view' and 5 as inputs.
    - Next step: add WHERE HAVING clause
    '''
    conn, curs = helper_connection()
    single_table_data = curs.execute(f"SELECT * FROM {tableName};").fetchall()
    conn.close()
    # Data comes in as a List of Tuples, we need List of Lists.
    single_table_data = [tuple_to_list(x) for x in single_table_data]
    # Find the Match of the User Selection.
    result = [x for x in single_table_data if argId in x]
    for row in result:
        row = [str(r) for r in row]
        print(", ".join(row))
    
#table = fetch_single_table('armors_penaltWy_full_suit')
#print("#")
#fetch_single_result_from_single_table('skill_rank_bonus_view', 5)

########################################################################################
# Determine which Table [attack type] to use from Attacks Table.
########################################################################################
def determine_attack_table(argId):
    '''
    In an attempt to keep everything to "one function, one purpose" and because I keep 
        finding weird edge case where other functions "didn't quite" meet the mark, I'm
        making a function that specifically determines which attack table to call to
        complete an attackRoll.
    Operation:
    -) Get the Selection from the User Input.
    1) Pass-in the beautified table_name (such as: "Arming Sword") into db."attacks".
    2) Get the table_reference back as a result.
    -) This table_reference will be used in the Determine Attack Roll Results to know
        which "att_{foo}" to use.
    '''
    conn, curs = helper_connection()
    single_table_data = curs.execute(f"SELECT weapon_name AS 'Weapon', table_reference AS 'Tbl Ref' FROM XREF_weapons LEFT JOIN weapon_categories ON XREF_weapons.category_id = weapon_categories.id LEFT JOIN weapons ON XREF_weapons.weapon_name_id = weapons.id LEFT JOIN attacks ON XREF_weapons.table_reference_id = attacks.id WHERE `Weapon` = '{argId}';").fetchall()
    conn.close()
    print(single_table_data)
    for row in single_table_data:
        row = [str(r) for r in row]
        row.pop(0)
        row = ", ".join(row)
        print(row)
    return row
    
########################################################################################
# Determine Attack Roll Results
########################################################################################
def attack_roll_results(attackRoll, attack_table, armor_type):
    '''
    This should be the "main" event so-to-speak.
    Steps:
    1) We want the calculations from: combat_math.py: calc_total_attack_roll.
    2) Take this information and include the attack_table and the armor_type.
    3) Feed the information into the long SQL query.
    4) Display ONLY a single set of information: The Hits, Crit Severity and Crit Type
        for the particular set of parameters.
    5) Add later: visual cleanup if there is no critical.
    6) Questions: How to handle size mod for weapons?
    The desired result.
    The result should be printed as a concatenation of "INT, Crit_type, Crit_severity":
        Thus: 17AP, not 17 A P.
        This will be implemented later.
    '''
    # ENABLE the "roll crit" button if the attack produced results that include a critical
        # i.e. the presence of a severity and a type, not just an INT.
    ## should this be a separate function? It feels separate.  Dunno
    print(attack_table)
    conn, curs = helper_connection()
    single_table_data = curs.execute(
        f"SELECT at{armor_type}_hits  AS AT{armor_type}_H, severity AS AT{armor_type}_S, crit_type AS AT{armor_type}_C FROM {attack_table} LEFT JOIN crit_severity ON {attack_table}.at{armor_type}_crit_sev_id = crit_severity.id LEFT JOIN crit_type_desc ON {attack_table}.at{armor_type}_crit_type_id = crit_type_desc.id WHERE {attackRoll} BETWEEN roll_min AND roll_max;").fetchall()
    print(single_table_data)
    
    conn.close()
    # Data comes in as a List of Tuples, we need List of Lists.
    single_table_data = [tuple_to_list(x) for x in single_table_data]
    # Find the Match of the User Selection.
    for row in single_table_data:
        row = [str(r) for r in row]
        print(", ".join(row))
        return row
    
#stabby_result = attack_roll_results(113, 'att_spear', 7)
#print(f"Stabby Results: {stabby_result}.")


########################################################################################
# All individual input choice fetches
########################################################################################
def fetch_armor_type(argId):
    '''
    
    '''
    conn, curs = helper_connection()
    single_table_data = curs.execute(f"SELECT `AT` FROM armor_type_view WHERE `AT` = {argId};").fetchall()
    conn.close()
    # Data comes in as a List of Tuples, we need List of Lists.
    single_table_data = [tuple_to_list(x) for x in single_table_data]
    # Find the Match of the User Selection.
    result = [x for x in single_table_data if argId in x]
    for row in result:
        row = [str(r) for r in row]
        print(", ".join(row))

#chosenAT = fetch_armor_type(2)

def fetch_vambraces_penalty(argId):
    '''
    
    '''
    conn, curs = helper_connection()
    single_table_data = curs.execute(f"SELECT `Missile Penalty` FROM armors_penalty_vambraces_view WHERE AT = {argId};").fetchall()
    conn.close()
    # Data comes in as a List of Tuples, we need List of Lists.
    single_table_data = [tuple_to_list(x) for x in single_table_data]
    # Find the Match of the User Selection.
    for row in single_table_data:
        row = [str(r) for r in row]
        print(", ".join(row))

#chosen_vambraces_penalty = fetch_vambraces_penalty(3)

def fetch_charging_bonus(argId):
    '''
    
    '''
    if argId == 0:
        value = 0
        return value
    else:
        conn, curs = helper_connection()
        single_table_data = curs.execute(f"SELECT `Size Bonus` FROM charging_bonus_view WHERE `Size Bonus` = {argId};").fetchall()
        conn.close()
        # Data comes in as a List of Tuples, we need List of Lists.
        # Find the Match of the User Selection.
        for row in single_table_data:
            row = [str(r) for r in row]
            a = row.pop(0)
            return a

#chosen_charging_bonus = fetch_charging_bonus(2)
#print(chosen_charging_bonus)

def fetch_all_defensive_bonus_modifiers(*args):
    '''
    I did this dumb.  Ignore me.
    '''
    if args == 0:
        value = 0
        return value
    else:
        conn, curs = helper_connection()
        single_table_data = []
        for a in args:
            x = curs.execute(f"SELECT `DB Mod` FROM defensive_bonus_modifiers_view WHERE `DB Mod` = {a};").fetchone()
            x = [tuple_to_list(x) for x in single_table_data]
            single_table_data.append(x)
        print(single_table_data)
        
        conn.close()
            # Data comes in as a List of Tuples, we need List of Lists.
            # Find the Match of the User Selection.
        single_table_data = [tuple_to_list(x) for x in single_table_data]
        for row in single_table_data:
            row = [str(r) for r in row]
            return row

#listofhorseshit = fetch_all_defensive_bonus_modifiers(10, 10, 20, 20)
#print(listofhorseshit)

########################################################################################
# Determine Critical Roll Results
########################################################################################
def critical_roll_results(critical_severity, critical_type):
    '''
    Once we have the damage results, we need to allow the player to press the "roll crit"
        button and then determine the critical result according to the appropriate table.
    We need the severity (Begins at "A" and moves up to "F") [G+ TB implemented later]
    We need the critical type.
    The type determines on which table we roll,
    The severity determines against which column we compare the roll.
    We will need a d100 roll (NOT open-ended) (it's own function.)
    '''
    # Look-up critical type table based on input of critical type.
    # roll = d100_roll()
    # check roll vs severity column.
    # display ALL results that use that column.
    ## Print a concatenated version.
    ## Print a long-form version.
    ### Long-form version uses crit_result_terms table.
    pass


############################################
# WARNO! #
############################################
'''
To be implemented later:
    1) 'Ambush' modifying critical results.
    2) weapon size modifiers to damage.
    - This does mean variant weapons won't be
        implemented for the time being.
    3) Criticals with severities "above" 'F'.
    4) Additional Criticals from a single
        attack.
'''