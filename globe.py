import sqlite3

#Create connection to db
db=sqlite3.connect("/ABSOLUTE/PATH/TO/INSTALL/DIR/rshells.db")
# db=sqlite3.connect("rshells.db")
curse=db.cursor()
