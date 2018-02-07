import os

file1 = '/etc/odbcinst.ini'
file2 = 'libodbcpsqlS.so'
path2 = '/usr/lib64/'


def create_file(file1):
    f = open(file1, "w+")
    f.close()


def find_file(path1, file1):
    for root, dirs, files in os.walk(path1):
        if file1 in files:
            return os.path.join(root, file1)


create_file(file1)
found = find_file(path2, file2)
if type(found) == str:
    print found
