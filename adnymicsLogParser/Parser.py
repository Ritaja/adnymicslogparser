#!/usr/bin/env python
import logging
import os

from adnymicsLogParser.lib.DBConnection import PSQLConnection
from adnymicsLogParser.lib.DBTable import Table, Orders, Orders_products
from adnymicsLogParser.lib.DataModel import Model
from adnymicsLogParser.lib.LogUtil import LogModel
from adnymicsLogParser.logs.logging_setup import setup_logging

# object refernce to orders table
orders = None
# obeject reference to orders_products table
orders_products = None
setup_logging()
logger = logging.getLogger(__name__)


def worker_daemon(path=os.path.join(os.path.dirname(__file__), "tests/"), filename="test.log"):
    '''

    '''
    pass


def worker_simple(targetpath, targetfile, dbname, user, password, host, port):
    '''
    Simple worker which opens a psql connection, creates required tables.

    '''
    if targetpath == "":
        targetpath = os.path.join(os.path.dirname(__file__), "tests/")

    logger.info("starting simple worker for log parsing")
    psql = PSQLConnection(database=dbname, user=user, password=password, host=host, port=port)
    connection = psql.open_connection()
    check_and_create_tables(psql, connection)
    # find all files in the directory
    for file in os.listdir(targetpath):
        if file.startswith(targetfile.split(".")[0]):
            parse_and_write(path=targetpath, filename=file)
    # work done close the connection
    psql.close_connection()


def check_and_create_tables(db, connection):
    '''
    Checks if the required tables are not present in the db, then creates them.

    :param db: the proper db object to use
    :param connection: the db connection object to communicate to the db with
    '''
    global orders
    global orders_products
    # required tables does not exist on the DB, create
    if not db.check_table_exists("orders") and not db.check_table_exists("orders_products"):
        table_orders = Model().load_data("adnymicsLogParser/data/table_orders")
        table_products = Model().load_data("adnymicsLogParser/data/table_products")
        table = Table(connection)
        orders = table.create_table(table_orders)
        orders_products = table.create_table(table_products)

    # required tables are present, proceed by just creating appropriate object
    else:
        logger.info("tables exist in DB.Proceeding without creation of tables")
        orders = Orders(connection)
        orders_products = Orders_products(connection)


def parse_and_write(path, filename, batchsize=5):
    '''
    Parses the given log file and writes the missing datapoints in the DB.

    :param filename: the log file to parse
    :param batchsize: the batchsize of reading/writing ops. default 5
    :raises: IOError on failing to open/locate provided log file
    '''
    i = 0
    log_match = []
    try:
        logger.info("Attempting to read from log file %s" % filename)
        with open(path + filename) as f:
            lines = f.readlines()
    except Exception as e:
        logger.error("cannot read log file %s. Error:%s" % (filename, e))
        raise IOError("cannot read log file %s. See log for details" % filename)

    if len(lines) == 0:
        logger.error("log file %s has 0 readable lines" % filename)
        return None
    # the log has multiple lines, read and process them as per batchsize
    if len(lines) > 2:
        for line in lines:
            log_match.append(LogModel.get_match(line))
            # log_match = check_and_append(log_match, LogModel.get_match(line))
            i += 1
            if i == batchsize:
                logger.info("batchsize reached,writing out data_points to DB.")
                write_db(tuple(log_match))
                del log_match[:]
                i = 0

        # for the residual no of lines, greater than batchsize
        if len(log_match) > 0:
            logger.info("writing %d residual data points (number exceeding batchsize)" % len(log_match))
            write_db(tuple(log_match))

    # the log file has only one data point that can be written
    else:
        logger.info("log file %s has only one datapoint(one relevant log line)" % filename)
        log_match.append(LogModel.get_match(lines))
        # log_match = check_and_append(log_match, LogModel.get_match(lines))
        write_db(tuple(log_match))


def write_db(log_match):
    '''
    Inserts the required datapoints in the DB.
    :param log_match: the datastructure containing data points to write to DB.
    :raises: AttributeError when the number of tables created/configured is less than required for operation
    '''
    # the no of tables initiated is less than required, something wrong, abort
    if orders_products is None or orders is None:
        logger.error("Required tables were not createdproperly or associated properly in data structure.")
        raise AttributeError("Tables not created/associated properly.")

    # prepare data for the orders_products table
    table_products_data = LogModel.create_order_product_pair(log_match)

    # write data points on db
    orders.insert_datapoint(log_match)
    orders_products.insert_datapoint(table_products_data)


def start(targetpath, targetfile, dbname, user, password, host, port):
    '''
    The main controller for the parser script.
    :return:
    '''
    worker_simple(targetpath, targetfile, dbname, user, password, host, port)
