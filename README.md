# rmu_combat_roller
A Combat Roller for Rolemaster Unified.

This Combat Roller is designed for the following:
- A browser-operable micro app in Flask,
- Allowing a user to enter Attacker and Defender data, 
- Based on Rolemaster Unified combat rules,
- to generate hit and critical results.

This roller uses bootstrap GUI elements to allow the user to select their Offensive Bonus (OB), Defensive Bonus (DB), Armor Type (AT), positioning modifiers, and applies a randomly rolled result (or assigned die roll), using Rolemaster's famous "exploding die" mechanic to generate results according to Rolemaster's combat table structure.

Out of respect for ICE, I have removed the ability to see their combat tables, only a few can be accessed via the database.  The SQLite3 database is easy to use, and you can readily add data to the tables to include the additional combat charts, as desired.  If you would like automated help adding the data, please message me directly and I will be happy to supply you with the necessary functions (either a python script or a SQLite3 script) to handle the data additions.

Technology Stack:
- Python 3.11,
- SQLite3,
- HTML/JS,
- Bootstrap 4.1.1,

Libraries:
- Flask,
- SQLAlchemy
- sqlite3, 
- random

Visual considerations: An order-handler for structuring the symbols in the critical results to match the updated book (from core release) may be a good aesthetic improvememnt.

Feel free to download and use in your campaigns!  May all your hits be crits, and never trip over an imaginary, deceased turtle.
