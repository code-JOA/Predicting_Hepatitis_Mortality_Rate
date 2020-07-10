import sqlite3
conn = sqlite3.connect("usersdata.db")
cur = conn.cursor()


# functions
def create_usertable():
    """Method name : create_userstable
       Objective : create user table , add password
    """
    cur.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)")


def add_userdata(username,password):
    """
    Method name : add_userdata
    Objective : add data of the user
    """
    cur.execute("INSERT INTO userstable(username,password) VALUES (?,?)",(username,password))
    conn.commit()


def login_user(username,password):
    """Method name : login user
       Objective : fetch user data and password upon log-in
    """
    cur.execute("SELECT * FROM userstable WHERE username = ? AND password = ?" , (username,password))
    data = cur.fetchall()
    return data


def view_all_users():
    """Method name : login user
       Objective : view all user data
    """
    cur.execute("SELECT * FROM userstable")
    data = cur.fetchall()
    return data
