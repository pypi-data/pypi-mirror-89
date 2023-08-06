#
#  remove_config.py
#
#  Created by w0rng on 28.12.2020.
#  Copyright © 2020 w0rng. All rights reserved.
#

import os


def remove_config(config_name):
    path_configs = os.path.expanduser("~") + '/.config/project_creator/'

    if config_name not in os.listdir(path_configs):
        logging.error(f'Конфиг {config_name} не найден')
        exit(1)

    os.remove(f'{path_configs}{config_name}')
