from dyc.modules import Module
from dyc import modules
theming = modules.import_module('theming')
from dyc.util import time, decorators
from dyc.backend import orm
usersmodel = modules.import_module('.model', 'users')
commonsmodel = modules.import_module('.model', 'commons')


__author__ = 'Justus Adam'


class ContentHandler(orm.BaseModel):
    module = orm.ForeignKeyField(Module)
    machine_name = orm.CharField(unique=True)
    path_prefix = orm.CharField(unique=True)


class ContentTypes(orm.BaseModel):
    machine_name = orm.CharField(unique=True)
    content_handler = orm.ForeignKeyField(ContentHandler)
    display_name = orm.CharField(null=True)
    theme = orm.ForeignKeyField(theming.Theme)
    description = orm.TextField(null=True)


class Page(orm.BaseModel):
    content_type = orm.ForeignKeyField(ContentTypes)
    page_title = orm.CharField()
    creator = orm.ForeignKeyField(usersmodel.User)
    published = orm.BooleanField(default=False)
    date_created = orm.DateField(default=time.utcnow())
    menu_item = orm.ForeignKeyField(commonsmodel.MenuItem, null=True)


@decorators.multicache
def field(name):
    class FieldData(orm.BaseModel):
        class Meta:
            db_table = name + '_data'

        page_type = orm.CharField()
        page_id = orm.IntegerField()
        content = orm.TextField()

    return FieldData


class FieldType(orm.BaseModel):
    machine_name = orm.CharField(unique=True)
    handler = orm.CharField(null=False)


class FieldConfig(orm.BaseModel):
    field_type = orm.ForeignKeyField(FieldType)
    content_type = orm.ForeignKeyField(ContentHandler)
    weight = orm.IntegerField(default=0)
    description = orm.TextField(null=True)

