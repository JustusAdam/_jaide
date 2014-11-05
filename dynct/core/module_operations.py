from importlib import import_module
from pathlib import Path

from dynct.core import database_operations
from dynct.errors.exceptions import ModuleError
from dynct.util.config import read_config
from dynct.backend.database import DatabaseError
from dynct.includes import bootstrap


__author__ = 'justusadam'

basedir = str(Path(__file__).parent.parent.resolve())


def activate_module(module_name):
    print('Activating module: ' + module_name)
    if is_active(module_name):
        print('Module ' + module_name + ' is already active.')
        return True
    path = get_module_path(module_name)

    if path is None:
        print('Module ' + module_name + ' could not be activated')
        return False
    module_conf = read_config(path + '/config.json')
    module_conf['path'] = path

    return _activate_module(module_conf)


def _activate_module(module_conf):
    try:
        init_module(module_conf['path'])
    except DatabaseError as error:
        print(error)
        return False

    _set_module_active(module_conf['name'])
    return True


def register_content_handler(module_conf):
    print('registering content handler ' + module_conf['name'])
    if 'path_prefix' in module_conf:
        path_prefix = module_conf['path_prefix']
    else:
        path_prefix = module_conf['name']
    try:
        database_operations.ContentHandlers().add_new(module_conf['name'], module_conf['name'], path_prefix)
    except DatabaseError as error:
        print('Failed to register page handler ' + module_conf['name'])
        print(error)


def get_module_id(module_name):
    return database_operations.ModuleOperations().get_id(module_name)


def init_module(module_path):
    module = import_module(module_path.replace('/', '.'))
    try:
        module.prepare()
    except ModuleError as error:
        print(error)
        print('it seems no prepare() method could be found')


def get_module_path(module):
    return database_operations.ModuleOperations().get_path(module)


def _set_module_active(module_name):
    database_operations.ModuleOperations().set_active(module_name)


def is_active(module_name):
    try:
        result = database_operations.ModuleOperations().ask_active(module_name)
    except DatabaseError:
        return False
    return result == 1


def register_installed_modules():
    register_modules(discover_modules())


def discover_modules():
    filename = bootstrap.MODULE_CONFIG_NAME
    accumulator = []
    for directory in bootstrap.MODULES_DIRECTORIES + bootstrap.COREMODULES_DIRECTORIES:
        for file in Path(directory).iterdir():
            if file.is_dir():
                configpath = file / filename
                if configpath.exists():
                    info = read_config(str(configpath))
                    if check_info(info):
                        info['path'] = str(file)
                        accumulator.append(info)
    return accumulator


def register_modules(r_modules):
    if isinstance(r_modules, (list, tuple)):
        for module in r_modules:
            register_single_module(module)
    else:
        register_single_module(r_modules)


def register_single_module(moduleconf):
    assert isinstance(moduleconf, dict)
    print('registering module ' + moduleconf['name'])
    db_op = database_operations.ModuleOperations()
    try:
        path = db_op.get_path(moduleconf['name'])
        if path[0] != moduleconf['path']:
            db_op.update_path(moduleconf['name'], moduleconf['path'])
    except (DatabaseError, TypeError):
        db_op.add_module(moduleconf['name'], moduleconf['path'], moduleconf['role'])


def check_info(info):
    keys = info.keys()
    necessary_attributes = bootstrap.NECESSARY_MODULE_ATTRIBUTES
    for attr in necessary_attributes:
        if attr not in keys:
            return False
    return True


def get_active_modules():
    modules = {}
    for item in database_operations.ModuleOperations().get_enabled():
        print('loading module ' + item['name'])
        modules[item['name']] = import_module('dynct.' + item['path'].replace('/', '.'))

    return modules