import adnymicsLogParser.Parser
import sys, getopt
import os

targetfile = ""
targetpath = ""
dbname = ""
user = ""
password = None
host = "127.0.0.1"
port = "5432"


def graphics():
    print " ________    ________      ________      ________       _______       ________      "
    print "|\   __  \  |\   __  \    |\   __  \    |\   ____\     |\  ___ \     |\   __  \     "
    print "\ \  \|\  \ \ \  \|\  \   \ \  \|\  \   \ \  \___|_    \ \   __/|    \ \  \|\  \    "
    print " \ \   ____\ \ \   __  \   \ \   _  _\   \ \_____  \    \ \  \_|/__   \ \   _  _\   "
    print "  \ \  \___|  \ \  \ \  \   \ \  \\  \|   \|____|\  \    \ \  \_|\ \   \ \  \\  \|  "
    print "   \ \__\      \ \__\ \__\   \ \__\\ _\     ____\_\  \    \ \_______\   \ \__\|\ _\ "
    print "    \|__|       \|__|\|__|    \|__|\|__|   |\_________\    \|_______|    \|__|\|__| "
    print "                                                                                    "


if len(sys.argv) < 2:
    graphics()
    print "Invalid no of arguments passed. For manual please run with flag -h (Parse.py -h)"
    sys.exit(2)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:p:d:u:x:h:i:",
                               ["file=", "path=", "database", "username", "password", "host", "port", "cheatmode"])
except getopt.GetoptError:
    graphics()
    print 'USAGE: Parse.py -f <M:logFileName> -p <O:path/to/file> -d <M:dbname> -u <M:username> -x <O:password> -h <M:host> -i<M:port>'
    print 'mandatory arguments are marked as M: and optional with O:'
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        graphics()
        print 'USAGE: Parse.py -f <M:logFileName> -p <M:path/to/file> -d <M:dbname> -u <M:username> -x <O:password> -h <M:host> -i<M:port>'
        print 'mandatory arguments are marked as M: and optional with O:'
        sys.exit()
    elif opt in ("-f", "--file"):
        targetfile = arg
    elif opt in ("-p", "--path"):
        targetpath = arg
    elif opt in ("-d", "--database"):
        dbname = arg
    elif opt in ("-u", "--username"):
        user = arg
    elif opt in ("-x", "--password"):
        password = arg
    elif opt in ("-h", "--host"):
        host = arg
    elif opt in ("-i", "--port"):
        port = arg
    elif opt in ("--cheatmode"):
        targetfile = "test.log"
        targetpath = ""
        dbname = "testdb"
        user = "ritajasengupta"

if dbname is None or host is None or port is None or user is None or targetfile is None or targetpath is None:
    graphics()
    print "ERROR: Mandatory arguments cannot be null"
    print ""
    print 'USAGE: Parse.py -f <M:logFileName> -p <O:path/to/file> -d <M:dbname> -u <M:username> -x <O:password> -h <M:host> -i<M:port>'
    print 'mandatory arguments are marked as M: and optional with O:'
    sys.exit(2)

graphics()
if password is None:
    print "PASSWORD for db is not set, proceeding without password"
adnymicsLogParser.Parser.start(targetpath, targetfile, dbname, user, password, host, port)
print "process finished. Check logs for details."
