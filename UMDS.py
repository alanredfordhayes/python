import os

file1 = '/etc/odbcinst.ini'
file2 = 'psqlodbcw.so'
file3 = 'libodbcpsqlS.so'
file4 = '/etc/odbc.ini'
file5 = '.s.PGSQL.5432'
path1 = '/var/run/postgresql/'
path = '/usr/lib64/'
db = 'umds'
link_dst = '/tmp/', file5


def create_file(file1):
    f = open(file1, "w+")
    f.close()


def find_file(path1, file1):
    for root, dirs, files in os.walk(path1):
        if file1 in files:
            return os.path.join(root, file1)


def open_file_append(file1, append_line):
    f = open(file1, "w+")
    f.write(append_line)
    f.close()


def odbcinst_data(found2, found3):
    if type(found2) == str and type(found3) == str:
        append_line = """[PostgreSQL]
Description=PostgreSQL ODBC driver (Unicode version)
Driver64=%s
Setup64=%s
Debug=0
CommLog=1
UsageCount=1""" % (found2, found3)
        return append_line


def odbc_data(db):
    TNS_SERVICE = db
    USER_ID = db
    UserID = db
    User = db
    Database = db
    data = '''[UMDS_DSN]
;DB_TYPE = PostgreSQL
;SERVER_NAME = localhost
;SERVER_PORT = 5432
;TNS_SERVICE = %s
;USER_ID = %s
Driver = PostgreSQL
DSN = UMDS_DSN
ServerName = localhost
PortNumber = 5432
Server = localhost
Port = 5432
UserID = %s
User = %s
Database = %s''' % (TNS_SERVICE, USER_ID, UserID, User, Database)
    return data


def create_link(found, dst):
    print dst
    if type(found) == str:
        os.symlink(found, dst)


def edit_file(file, data):
    f = open(file, "w")
    f.write(data)
    f.close


create_file(file1)
found2 = find_file(path, file2)
found3 = find_file(path, file3)
pg_odbcinst = odbcinst_data(found2, found3)
edit_file(file1, pg_odbcinst)
create_file(file4)
pg_odbc_data = odbc_data(db)
edit_file(file4, pg_odbc_data)
found4 = find_file(path1, file5)
create_link(found4, link_dst)
