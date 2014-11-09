from dynct.modules.users.user_information import UsersOverview
from .login import LoginCommonHandler, login_prefix, logout_prefix
from dynct.modules import admin
from . import users, session
from .admin_actions import CreateUser, factory, PermissionOverview, EditPermissions
from . import user_information
from .controller import UserController

__author__ = 'justusadam'

name = 'users'

role = 'user_management'

START_REGION = 'sidebar_left'

START_THEME = 'default_theme'


def admin_handler(h_name):
    handlers = {
        'create_user': CreateUser,
        'user_overview': UsersOverview,
        'view_permissions': PermissionOverview,
        'edit_permissions': EditPermissions
    }
    return handlers[h_name]


def common_handler(item_type):
    handlers = {
        login_prefix: LoginCommonHandler,
        'user_information': user_information.UserInformationCommon
    }
    return handlers[item_type]


def prepare():
    from dynct import core
    from dynct.modules import comp

    # add login page
    core.add_content_handler('login', name, login_prefix)
    core.add_content_handler('logout', name, logout_prefix)
    core.add_content_handler('users', name, 'users')

    # add login common
    comp.add_commons_config('login', 'login', name, True, 1)
    comp.add_commons_config('login', START_REGION, 0, START_THEME)
    # dn.add_item('login', 'user_management', ('english', 'User Login'))

    # add user information common
    comp.add_commons_config('user_information', 'user_information', name, True, 1)
    comp.assign_common('user_information', START_REGION, 1, START_THEME)
    # dn.add_item('user_information', 'user_management', ('english', 'Your Account Information'))

    # add admin pages
    admin.new_category('user', 'Users')

    admin.new_subcategory('user_management', 'Add and Edit Users', 'user')
    admin.new_page('create_user', 'Register new User', 'user_management', name)
    admin.new_page('user_overview', 'Overview', 'user_management', name)

    admin.new_subcategory('permission_management', 'View and edit Permissions', 'user', 5)
    admin.new_page('view_permissions', 'View Permissions', 'permission_management', name)
    admin.new_page('edit_permissions', 'Edit Permissions', 'permission_management', name)
    #admin.new_page('delete_user', 'Remove a User Account', 'user_management', name)