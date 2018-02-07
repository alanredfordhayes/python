import subprocess


psql_db = 'umds'
psql_pass = "'umds'"


def psql_create_user(psql_db, psql_pass):
    create_user = "CREATE USER %s WITH PASSWORD %s;" % (psql_db, psql_pass)
    args1 = ['sudo', '-u', 'postgres', 'psql', '-c', create_user]
    psql = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = psql.communicate()[0]
    return output


def main(psql_db, psql_pass):
    psql_create_user(psql_db, psql_pass)


main(psql_db, psql_pass)
