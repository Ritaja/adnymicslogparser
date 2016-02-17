# ADNYMICS LOG PARSER

log parser to parse logs and enter data points in postgre SQL.

### Version
0.0.1

### Tech

The major frameworks/tools used:

* [psycopg2] - Python-PostgreSQL Database Adapter
* [Pytest] - python test framework
* [Sphinx] - documentation generator
* [Tox] - generic virtualenv management and test command line tool

### Installation

clone the repository from the available hosting site, relocate to the directory of the project and proceed.

You need pip to install the project:

```sh
$ python setup-standalon.py install
```

this relies internally on pip to pull down resources from `requirements.txt`

If the setup has installed all the depandant resources successfully in your virtualenv/environment, you should have `Tox` installed by now. If you wish to run tests, there are two ways to do this.

The first way is to execute from the project folder (`adnymicsTask`):

```sh
$ py.test
```

This will test the app in the current environment, using the predefined tests.

The second option is to let `Tox` spin up a fresh virtualenv and install requirements and test on it. To achive that simply do:

```sh
$ tox
```

### Basic usage

The program can be run from the command line. The startup scrip is called `Parse.py` and takes arguments.

the general format to use it is:

```sh
$ cd adnymicsTask
$ python Parse.py -f <M:logFileName> -p <M:path/to/file> -d <M:dbname> -u <M:username> -x <O:password> -h <M:host> -i<M:port>
```
OR
```sh
$ python Parse.py --file= <M:logFileName> --path= <M:path/to/file> --database= <M:dbname> --username= <M:username> --password= <O:password> --host= <M:host> --port= <M:port>
```
mandatory arguments are marked as M: and optional with O:

**Detail (ed) flags:**

| Flag          | Explanation                                                                                                                                                                                                                |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -h            | Help                                                                                                                                                                                                                       |
| -f / --file   | Filename, the name of the log to parse. The program will look for  all log files in the directory that starts with this name and parse them. Ex: "sample.log" will make the program parse "sample0.log", "sample1.log" etc |
| -p/--path     | The target path or the path where the log files should be looked up.  Ex: "path/to/file"                                                                                                                                   |
| -d/--database | The name of the psql database to use                                                                                                                                                                                       |
| -u/--username | The username for the database                                                                                                                                                                                              |
| -x/--password | The password required to connect to DB. Can be skipped, if the  user has password-less access to DB                                                                                                                        |
| -h/--host     | The host name for the DB. Ex: "127.0.0.1"                                                                                                                                                                                  |
| -i/--port     | The port where the psql is running

It is also possible to obtain help from the program with the `-h` flag:

```sh
$ python Parse.py -h
```

**NOTE** do not append a trailing '/' when defing the target path. The initial script, already does that for you. As an example, for targetpath 'path/to/file/' just provide 'path/to/file' dropping the trailing '/'

If the password is not provided, the program assumes that the user has passwordless access to the database.

### Logs

The logs are configured only for the file handler. The log file created is named parser.log, for convenience it is placed under `adnymicsTask` folder.

The same file appends all error, info and debug streams. The handler is rotating file handler, so when log becomes full, it will push old logs to a numbered log file (E.x: parser0.log)


[psycopg2]:https://pypi.python.org/pypi/psycopg2
[pytest]:http://pytest.org/latest/
[Sphinx]:http://www.sphinx-doc.org/en/stable/
[Tox]:https://tox.readthedocs.org/en/latest/
