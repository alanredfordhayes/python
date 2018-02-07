

# Create a configuration file /etc/odbcinst.ini
file1 = '/etc/odbcinst.ini'


def create_file(file1):
    f = open(file1, "w+")
    f.close()


create_file(file1)
