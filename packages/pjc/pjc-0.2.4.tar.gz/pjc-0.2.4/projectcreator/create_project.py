#!/usr/bin/python3
#
#  create_project.py
#
#  Created by w0rng on 12.09.2018.
#  Copyright © 2020 w0rng. All rights reserved.
#


import json
import os
import logging


def create_project(project_type, project_name):
    path_configs = os.path.expanduser("~") + '/.config/project_creator/'

    if project_type not in os.listdir(path_configs):
        logging.error(f'Конфиг {project_type} не найден')
        exit(1)

    if os.path.exists(project_name):
        logging.error(f'Проект {project_name} уже существует')
        exit(1)
    else:
        os.mkdir(project_name)
        os.chdir(f'./{project_name}/')

    with open(path_configs+project_type) as f:
        config = json.load(f)

    if 'path' in config:
        logging.info('Создание папок')
        create_folders(config['path'])

    if 'files' in config:
        logging.info('Создание файлов')
        for f in config['files']:
            create_file(f, config['files'][f])

    if 'commands' in config:
        logging.info('Выполнение команд')
        for commands in config['commands']:
            run_command(commands)


def __get_folders(folders, path=''):
    """Возвращает пути к папкам"""
    for folder in folders:
        yield f'{path}{folder}/'
        if len(folders[folder]):
            yield from __get_folders(folders[folder], f'{path}{folder}/')


def create_folders(folders):
    """Создает структуру папок"""
    for path in __get_folders(folders):
        if not os.path.exists(path):
            os.mkdir(path)


def create_file(name, lines):
    """Создает файл name с содержимым lines"""
    if os.path.exists(name):
        logging.warning(f'{name} существует')
        return None
    with open(name, 'w') as file:
        for line in lines:
            file.write(line)


def run_command(commands):
    """Выполняет команду commands"""
    os.system(commands)
