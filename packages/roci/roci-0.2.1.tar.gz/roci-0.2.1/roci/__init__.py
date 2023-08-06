import sys

__version__ = '0.2.0'


def direc_dumper():
    if (len(sys.argv) == 1) or (len(sys.argv) > 2):
        raise ValueError("You need to give 1 argument to the command line, \
                         this will be the name of the new directory")

    directory = str(sys.argv[1]).strip()
    from roci.main import creator as create
    create(directory)
