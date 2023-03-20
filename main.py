'''
Main.py
Run this when wanting to run the script.
'''
from website import create_app
import sqlite3
from flask import g

DATABASE = 'rmu_combat.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

'''
"website" is a folder and thus a "package" within THIS app.
This "website" folder can be called, because of our __init__.py file.
Our __init__.py file is automatically run, so we can call those imports.
which creates the "create_app" piece.
'''
app = create_app()
'''
Feels a lot like creating the "main window" in TKinter.
We create an object from the create_app instantiation process.
We will pass that into our initilization function and be used to "run",
which is the METHOD on the app class.
''' 
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
    