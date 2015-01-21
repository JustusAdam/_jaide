"""
The fundamental settings consisting of non-changing,
as in not changing within this version of the software,
values required to make dynamic_content functional.

Might need to be expanded.
"""
from pathlib import Path
from dyc.util import structures


__version__ = '0.2'
__author__ = 'Justus Adam'


LoggingLevel = structures.Enumeration('Logging', ('LOG_WARNINGS', 'LOG_ERRORS', 'THROW_ERRORS', 'THROW_ALL'))
RunLevel = structures.Enumeration('RunLevel', ('TESTING', 'DEBUG', 'PRODUCTION'))
PathMaps = structures.Enumeration('PathMaps', ('MULTI_TABLE', 'TREE'))
ServerTypes = structures.Enumeration('ServerTypes', ('WSGI', 'PLAIN'))
Distributions = structures.Enumeration('Distributions', ('FULL', 'STANDARD', 'FRAMEWORK'))


# the order in this list dictates the order in which these modules will be activated
DEFAULT_MODULES = (
    'admin',
    'users',
    'commons',
    'file',
    'i18n',
    'fileupload',
    'theming',
    'wysiwyg',
    'node'
    )
FILE_DIRECTORIES = {
    'theme': (
        'custom/themes',
        'themes'
        ),
    'private': 'custom/files/private',
    'public': 'custom/files/public'
    }
MODULES_DIRECTORIES = ('custom/modules', 'modules')
COREMODULES_DIRECTORIES = ('core',)
MODULE_CONFIG_NAME = 'config.json'
ALLOW_HIDDEN_FILES = False
# Setting the above option to true will allow access to files starting with a '.' via the file handler/url
# it is highly recommended to NOT set this flag to true!
ALLOW_INDEXING = True
BROWSER_CACHING = False
HASHING_ALGORITHM = 'sha256'
HASHING_ROUNDS = 100000
HASH_LENGTH = 64
SALT_LENGTH = 16
DEFAULT_THEME = 'default_theme'
DEFAULT_ADMIN_THEME = 'admin_theme'
LOGGING_LEVEL = LoggingLevel.THROW_ALL
SERVER = structures.ServerArguments(port=9012, host='localhost', ssl_port=9443)
DATABASE = structures.DatabaseArguments(
            'mysql', 'python_cms', True, 'python_cms', 'python_cms', 'localhost')
BASEDIR = str(Path(__file__).parent.resolve())
RUNLEVEL = RunLevel.TESTING
I18N_SUPPORT_ENABLED = False
SUPPORTED_LANGUAGES = {
    'en_us': 'english (us)',
    'en_gb': 'english (gb)',
    'de': 'german',
    'fr': 'french'
    }
BASE_LANGUAGE = 'en_us'
DEFAULT_LANGUAGE = 'en_us'
PATHMAP_TYPE = PathMaps.MULTI_TABLE
LOGFILE = 'app.log'
MIDDLEWARE = (
    'dyc.middleware.alias.Middleware',
    'dyc.modules.file.PathHandler',
    'dyc.middleware.trailing_slash.RemoveTrailingSlash'
    )
ANTI_CSRF = True
DEFAULT_HEADERS = {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-cache'
    }
SERVER_TYPE = ServerTypes.WSGI
PROPAGATE_ERRORS = True
DISTRIBUTION = Distributions.STANDARD
HTTP_ENABLED = True
HTTPS_ENABLED = True
SSL_CERTFILE = '../dynamic-content.org.crt'
SSL_KEYFILE = '../dynamic-content.org.key'


# delete names that are not settings
del Path, structures
