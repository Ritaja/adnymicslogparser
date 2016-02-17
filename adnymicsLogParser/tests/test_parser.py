import psycopg2
import pytest

from adnymicsLogParser import Parser

# test specific variables
database = "testdb"
user = "ritajasengupta"
password = "ritajasengupta"
host = "127.0.0.1"
port = "5432"
path = "/Users/ritajasengupta/git/adnymicsTask/adnymicsLogParser/tests/"
filename = "sample.log"
cursor = None


def setup_module(module):
    '''

    set up the connections to be used in tests

    :param module: module object

    '''
    # open connection for tests
    connection = psycopg2.connect(database=database, user=user,
                                  password=password, host=host,
                                  port=port)
    connection.autocommit = True
    global cursor
    cursor = connection.cursor()


def teardown_function(function):
    '''

    Clear DB after each test

    :param function: function object

    '''
    cursor.execute("DROP TABLE IF EXISTS orders_products;")
    cursor.execute("DROP TABLE IF EXISTS orders;")


def test_with_all_arguments():
    '''

    tests log parser on sample logs, when all mandatory arguments are passed

    '''
    Parser.start(path, filename, database, user, password, host, port)
    cursor.execute("select count(*) from orders;")
    assert cursor.fetchone()[0] == 12, "Expected to see 12 rows added to the orders table"
    cursor.execute("select count(*) from orders_products;")
    assert cursor.fetchone()[0] == 28, "Expected to see 28 rows added to the orders_products table"


def test_multiple_runs():
    '''

    tests multiple runs on the same log. Checks if the program fails to recognise already inserted datapoints.

    '''
    Parser.start(path, filename, database, user, password, host, port)
    Parser.start(path, filename, database, user, password, host, port)
    Parser.start(path, filename, database, user, password, host, port)
    cursor.execute("select count(*) from orders;")
    assert cursor.fetchone()[0] == 12, "Expected to see 12 rows added to the orders table"
    cursor.execute("select count(*) from orders_products;")
    assert cursor.fetchone()[0] == 28, "Expected to see 28 rows added to the orders_products table"


def test_without_password():
    '''

    tests DB connection without providing password. Checks if programs throws appropriate error

    '''
    try:
        Parser.start(targetpath=path, targetfile=filename, dbname=database, user=user, password=None, host=host,
                     port=port)
    except IOError as e:
        assert e.message == "IOError: could not connect to DB. Check logs for details", "Unexpected error message"
    except Exception:
        pytest.fail("Expected to see IOError")


def test_not_created_db():
    '''

    tests if program throws appropriate eror when trying to operate on psql db which is not created

    '''
    try:
        Parser.start(targetpath=path, targetfile=filename, dbname="some", user=user, password=password, host=host,
                     port=port)
    except IOError:
        pass
    except Exception:
        pytest.fail("Expected to see IOError")


def test_unknown_host():
    '''

    tests connection when some unknown host is provided

    '''
    try:
        Parser.start(targetpath=path, targetfile=filename, dbname=database, user=user, password=password,
                     host="198.0.0.1",
                     port=port)
    except IOError:
        pass
    except Exception:
        pytest.fail("Expected to see IOError")


def test_invalid_path():
    '''

    checks if program throws proper error when an invalid is provided as target path.

    '''
    try:
        Parser.start(targetpath="/b", targetfile=filename, dbname=database, user=user, password=password, host=host,
                     port=port)
    except EnvironmentError:
        pass
    except Exception:
        pytest.fail("Expected to see RuntimeError")
