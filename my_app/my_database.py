import sqlite3
conn = sqlite3.connect("usersdata.db")
cur = conn.cursor()


# creating the usertable
def create_usertable():
    cur.execute("Create Table If Not Exists userstable(username TEXT,password TEXT)")


# adding the user
def add_usertable(username , password):
    cur.execute("Insert Into usertable(username , password) Values (?,?)",(username,password))
    conn.commit()


# adding user login
def login_user(username,password):
    cur.execute("Select * From usertable Where username =? And Password = ?" , (username,password))
    data = cur.fetchall()
    return data


# view all users
def view_all_users():
    cur.execute("Select * From usertable")
    data = cur.fetchall()
    return data
