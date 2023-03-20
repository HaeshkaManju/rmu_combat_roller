# models.py
# apparently ".", allows you to import the current package?
from . import db
from flask_login import UserMixin

class Attack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = (db.String(40))
    
class OffenseCalculator():
    offensive_bonus = 0