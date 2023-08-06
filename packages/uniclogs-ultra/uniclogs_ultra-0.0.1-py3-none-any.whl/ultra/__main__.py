import sys
import os
import getopt
import ultra.models
import ultra.server


def daemonize(pid_file):
    # Check for a pidfile to see if the daemon is already running
    try:
        with open(pid_file, 'r') as pf:

            pid = int(pf.read().strip())
    except IOError:
        pid = None

    if pid:
        sys.stderr.write("pid file {0} already exist.\n".format(pid_file))
        sys.exit(1)

    try:
        pid = os.fork()
        if pid > 0:
            # exit from parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('fork failed: {0}\n'.format(err))
        sys.exit(1)

    # decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'a+')
    se = open(os.devnull, 'a+')

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    pid = str(os.getpid())
    with open(pid_file, 'w+') as f:
        f.write(pid + '\n')


def usage():
    message = """"
        usage:\n
        python3 ultra.py      : to run as a process.
        python3 ultra.py -d   : to run as a daemon.
        python3 ultra.py -h   : this message.
        """

    print(message)


def main() -> None:
    pid_file = "/run/ultrad.pid"
    daemon_flag = False

    opts, args = getopt.getopt(sys.argv[1:], "dh")
    for opt, arg in opts:
        if opt == "-d":
            daemon_flag = True
        elif opt == "-h":
            usage()
            exit(0)
        else:
            usage()
            exit(1)

    if daemon_flag:
        daemonize(pid_file)

    ultra.server.run()

    if daemon_flag:
        # remove pid file
        os.remove(pid_file)
