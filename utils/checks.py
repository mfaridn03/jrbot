import sqlite3

conn = sqlite3.connect('Data.db')
c = conn.cursor()

class Checks:  # WIP
    def __init__(self, bot):
        self.bot = bot
    
    def has_char(self, user):
        pass
        
