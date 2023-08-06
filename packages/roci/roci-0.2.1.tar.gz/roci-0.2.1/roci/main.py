import os
from pkg_resources import resource_filename
from distutils.dir_util import copy_tree


def creator(directory):
    print("Hello, let's try create a nice new directory for you!")
    if os.path.exists(directory):
        print("this directory exists, better choose a different name")
    else:
        print("perfect, lets create a new directory called ", directory)
        os.makedirs(directory)
        path = resource_filename("roci", "structure/")
        copy_tree(path, directory)
        print("Done!")
