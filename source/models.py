from flask import Flask 

#TODO
class DataBase:
    def __init__(self, db):
        pass

class Message(DataBase):
    def __init__(self, db, table):
        super().__init__(db)
        self.table = table


class ChatRoom(DataBase):
    def __init__(self, db, table):
        self().__init__(db)
        self.table = table
        self.banned_users = set()
        self.room_list = set()
        self.users = set()

#TODO
class User(DataBase):
	def __init__(self, db, table):
		self().__init__(db)
		self.table = table
		pass	
