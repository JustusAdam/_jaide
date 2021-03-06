from ..machinery import component
import pathlib


default_settings = {
    # the order in this list dictates the order in which
    # these modules will be activated
    'modules': [],
    'module_directories': [],

    'allow_hidden_files': False,
    # Setting the above option to true will allow access to files
    # starting with a '.' via the file handler/url
    # it is highly recommended to NOT set this flag to true!


    'browser_caching': False,
    'hashing_algorithm': 'sha256',
    'hashing_rounds': 100000,
    'hash_length': 64,
    'salt_length': 16,

    'logging_level': 'debug',

    'server': {
        'port': 9012,
        'host': 'localhost',
        'ssl_port': 9443,
    },

    # 0:MULTI_TABLE, 1:TREE
    'pathmap_type': 0,
    'middleware': [
        'framework.middleware.alias.Middleware',
        'dycm.file.PathHandler',
        'framework.middleware.ssl.ConditionalRedirect',
        # 'framework.middleware.rest.JSONTransform'
    ],


    'anti_csrf': True,
    'default_headers': {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-cache',
    },

    'database': {
        'name': ':memory:',
        'type': 'SQlite'
    },

    # 0:WSGI, 1:PLAIN
    'server_type': 0,
    'propagate_errors': True,

    'http_enabled': True,
    'https_enabled': False,
    'dc_basedir': str(pathlib.Path(__file__).parent.parent.parent.resolve()),
    'sess_token_length': 16,
    'sess_length': -1
}


@component.component('settings', (default_settings, ))
class SettingsDict(dict):
    pass