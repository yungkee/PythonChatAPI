import sys
import 
from flask import Flask 

#TODO
class DataBase:
    def __init__(self, db):
        self.db = dev
        self.con = r.

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

    def add_user(self, user, room):
        source.db(self.db).table(self.table).filter({'room':room, 'room_user':user}).delete().run(self.conn)

    def user_list(self, room):
        users = source.db(self.db).table(self.table).filter({'room': room}).run(self.conn)
        user_list = []
        for user in users:
            user_list.append(user['room_user'])
        user_count = len(user_list)
        return user_list, user_count

#TODO
class User(DataBase):
	def __init__(self, db, table):
		self().__init__(db)
		self.table = table
		pass	
