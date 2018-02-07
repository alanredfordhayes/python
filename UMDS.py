import os

file1 = '/etc/odbcinst.ini'
file2 = 'psqlodbcw.so'
file3 = 'libodbcpsqlS.so'
path = '/usr/lib64/'


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
        append_line = """
        [PostgreSQL]
        Description=PostgreSQL ODBC driver (Unicode version)
        Driver64=%s
        Setup64=%s
        Debug=0
        CommLog=1
        UsageCount=1
        """ % (found2, found3)
        return append_line


def edit_file(file, data):
    f = open(file, "w")
    f.write(data)
    f.close


create_file(file1)
found2 = find_file(path, file2)
found3 = find_file(path, file3)
pg_odb = odbcinst_data(found2, found3)
edit_file(file1, pg_odb)
