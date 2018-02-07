import subprocess


psql_db = 'umds'
psql_db_password = 'Se!..Umd$..001..7'


def psql_create_user(db, password1):
    args1 = ['echo', password1]
    args2 = ['psql', 'createuser', '-d', db, '-P', '-s', '-E', db]
    echo = subprocess.Popen(args1, stdout=subprocess.PIPE)
    psql = subprocess.Popen(args2, stdin=echo.stdout, stdout=subprocess.PIPE)
    echo.stdout.close()
    output = psql.communicate()[0].rstrip()
    echo.wait()
    output_length = len(output)
    if (output_length != 0):
        return output


def main(psql_db, psql_db_password):
    psql_create_user(psql_db, psql_db_password)


main(psql_db, psql_db_password)
