import sqlite3


def init_db():
    """Initializes the database."""
    confirm = raw_input('THIS WILL DELETE YOUR DB IF IT EXISTS. Are you sure'
                        ' you want to continue? [Y/n] ')
    if confirm == 'y' or confirm == 'Y':
        print 'creating db...'
        with sqlite3.connect("clients.db") as connection:
            c = connection.cursor()
            c.execute("DROP TABLE IF EXISTS clients")
            c.execute("CREATE TABLE clients(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT, birthdate TEXT, email TEXT, phone TEXT,"
                "address TEXT, citystate TEXT, notes TEXT, favoriteline TEXT,"
                "cabintype TEXT, diningtime TEXT, travelswith TEXT, trips TEXT)")
    else:
        print 'Exiting without making changes...'


def addclient(newclient):
    """Adds new client to database"""
    with sqlite3.connect("clients.db") as connection:
        c = connection.cursor()
        c.execute('INSERT INTO clients (name, birthdate, email, phone,'
            'address, citystate, notes, favoriteline, cabintype, diningtime,'
            'travelswith, trips) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (newclient))
        return c.lastrowid


def updateclient(updatedata):
    """Updates data for specific client"""
    with sqlite3.connect("clients.db") as connection:
        c = connection.cursor()
        c.execute('UPDATE clients SET name=?, birthdate=?, email=?, phone=?,'
            'address=?, citystate=?, notes=?, favoriteline=?, cabintype=?,'
            'diningtime=?, travelswith=?, trips=? WHERE id=?', (updatedata))
