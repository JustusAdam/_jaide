__author__ = 'justusadam'

TRACKER_TABLE_CREATION_QUERY = 'create table created_tables (' \
                               'id int unsigned not null auto_increment unique primary key, ' \
                               'created_table varchar(500) not null unique, source_module_name varchar(500) not null, ' \
                               'source_module_id int unsigned not null);'

SETUP_TABLE_CREATION_QUERIES = (
    {
        'table_name': 'page_handlers',
        'module_name': 'core',
        'columns': (
            'id int unsigned not null auto_increment unique primary key comment \'primary key used for identification\'',
            'handler_module int not null comment \'identifier for the module providing the handler\'',
            'handler_name varchar(500) comment \'human readable name of the page handler\''
        )
    }, {
        'table_name': 'modules',
        'module_name': 'core',
        'columns': (
            'id int unsigned not null auto_increment unique primary key comment \'primary key used for identification\'',
            'module_name varchar(500) not null unique comment \'machine readable name for the module\'',
            'module_path varchar(500) comment \'name of the modules package provided correctly configured __init__.py or file '
                'that is reachable by (omit ".py")\''
        )
    }, {
        'table_name': 'content_types',
        'module_name': 'core',
        'columns': (
            'id int unsigned not null auto_increment unique primary key comment \'primary key used for identification\'',
            'content_type_name varchar(500) not null unique comment \'name of the content type\'',
            'page_handler int not null comment \'id of the associated page handler type\'',
            'description text comment \'human readable content type description\''
        )
    }, {
        'table_name': 'page_fields',
        'module_name': 'core',
        'columns': (
            'id int unsigned not null auto_increment unique primary key comment \'primary id for machine convenience\'',
            'field_name varchar(500) not null, content_type int not null comment \'id of associated content type\'',
            'description text comment \'human readable field type description\''
        )
    }, {
        'table_name': 'page_fields_instances',
        'module_name': 'core',
        'columns': (
            'id int unsigned not null auto_increment unique primary key comment \'primary id used to identify fields\'',
            'field_type int not null comment \'id of associated field type\'',
            'field_contents longtext not null comment \'contents of the field\''
        )
    }, {
        'table_name': 'alias',
        'module_name': 'core',
        'columns': (
            'id int unsigned not null auto_increment unique primary key comment \'unique identifier\'',
            'source_id int not null comment \'page id of the source page\'',
            'alias varchar(500) not null unique comment \'page alias\''
        )
    }
)
SETUP_DATABASE_POPULATION_QUERIES = (
    {
        'into_table': 'modules',
        'into_cols': ('module_name', 'module_path'),
        'values': ('core', '.')
    },
)
DEFAULT_MODULES = ('adminpages', 'atlanta', 'entity', 'common_elements')
COREMODULES_DIRECTORY = 'coremodules'
MODULES_DIRECTORY = 'custom/modules'