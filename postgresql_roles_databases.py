import subprocess


psql_db = 'umds'
psql_db_password = 'Se!..Umd$..001..7'


def psql_create_user(psql_db, psql_db_pass):
    create_user = 'CREATE USER', psql_db, 'WITH PASSWORD', psql_db_pass, ';'
    args1 = ['psql', '-c', create_user]
    psql = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = psql.communicate()[0]
    return output


def main(psql_db, psql_db_password):
    psql_create_user(psql_db, psql_db_password)


main(psql_db, psql_db_password)
