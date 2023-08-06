#
#  __init__.py
#
#  Created by w0rng on 23.12.2020.
#  Copyright © 2020 w0rng. All rights reserved.
#

import os


__version__ = '0.2.4'
__author__ = 'w0rng'


user_dir = os.path.expanduser("~")

if not os.path.exists(f'{user_dir}/.config/'):
    os.mkdir(f'{user_dir}/.config/')

if not os.path.exists(f'{user_dir}/.config/project_creator/'):
    os.mkdir(f'{user_dir}/.config/project_creator/')
