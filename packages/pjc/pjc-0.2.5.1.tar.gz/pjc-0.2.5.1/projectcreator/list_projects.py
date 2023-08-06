#
#  list_projects.py
#
#  Created by w0rng on 28.12.2020.
#  Copyright © 2020 w0rng. All rights reserved.
#


import os


def print_list_projects():
    path_configs = os.path.expanduser('~') + '/.config/project_creator/'
    for i in os.listdir(path_configs):
        print(i)
