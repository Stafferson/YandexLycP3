import sqlite3

from User import User

con = sqlite3.connect("yandex_lyc_p3.sqlite")
cur = con.cursor()
email = "tairka.mail@gmail.com"
password = "tair3461"
query = "SELECT EXISTS(SELECT 1 FROM Users WHERE email = '" + email + " and password = " + password + "');"
#query = "insert into Users(email, password) values(" + email + ", " + password + ")"
res = cur.execute(query).fetchall()
print(str(res))

s0 = User(6)
#print(s0.get_counter())
print(str(s0))
s1 = User(7)
#print(s1.get_counter())
print(str(s1))
