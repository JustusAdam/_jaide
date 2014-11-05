"""
Implementation of the setup routine.

Currently uses the framework to dynamically create elements, once the basic site functionality has been implemented
and hardened this should be refactored to remove the framework elements and store the raw html in a separate file.
"""
from dynct.core import Modules
from dynct.core.handlers.content import Content
from dynct.backend.database import DatabaseError, Database
from . import module_operations
from dynct.modules.comp.html_elements import ContainerElement, List, TableElement
from dynct.util.config import read_config, write_config
from dynct.includes import bootstrap
from dynct.modules.users.admin_actions import CreateUser


__author__ = 'justusadam'


# HACK special class for the initial user
class InitialUser(CreateUser):
    def check_own_permission(self):
        return True


def try_database_connection():
    try:
        test_database = Database()
        if test_database.check_connection():
            return ContainerElement(
                'The connection with the database was successfully established, you may continue with this setup',
                html_type='p') + ContainerElement('Continue', html_type='a', classes=['continue', 'button'],
                                                  additionals=['href="/setup/{next_page}"'])
        else:
            return ContainerElement(
                'The connection with the database could not be established. Please review your settings '
                'and then reload this page', html_type='p')
    except DatabaseError:
        return ContainerElement(
            'The connection with the database could not be established. Please review your settings and then '
            'reload this page', html_type='p')


class SetupHandler(Content):
    def __init__(self, url):
        super().__init__(url, None)

    def _fill_model(self):
        config = read_config('cms/config')
        setup_pages = {
            0: {
                'title': 'Setup of your CMS Installation',
                'content': str(
                    ContainerElement(
                        ContainerElement(
                            'Welcome to the setup process of your \'dynamic_content\' content management system.',
                            html_type='p'),
                        ContainerElement(
                            'These pages will guide you trough the necessary steps and tests that need to be taken to ensure \'dynamic_content\' will function properly for you.',
                            html_type='p'),
                        ContainerElement(
                            'During this process you will be required to enter and confirm sensible data to your installation as well as set a password for the administration user. It is therefore recommended that you perform this setup directly on the server or ahead of deployment or utilizing a secure and encrypted connection.',
                            html_type='p'),
                        ContainerElement(
                            'I hope that you will enjoy and be pleased with \'dynamic_content\'.', html_type='p'),
                        ContainerElement('Continue', html_type='a', classes=['continue', 'button'],
                                         additionals=['href="/setup/{next_page}"'])
                    )
                )
            },
            1: {
                'title': 'Overview',
                'content': str(
                    ContainerElement(
                        ContainerElement('The following steps will be taken during this setup', html_type='h3'),
                        List(
                            'Verifying Database Information',
                            'Configure site information',
                            'Set up an admin user',
                            list_type='ul'
                        ),
                        ContainerElement('Continue', html_type='a', classes=['continue', 'button'],
                                         additionals=['href="/setup/{next_page}"'])
                    )
                )
            },
            2: {
                'title': 'Verifying Database Configuration',
                'content':
                    str(
                        ContainerElement(
                            TableElement(
                                ['Type', config['database_type']],
                                ['Host', config['database_connection_arguments']['host']],
                                ['Database Name', config['database_connection_arguments']['database']],
                                ['User', config['database_connection_arguments']['user']],
                                ['Password', config['database_connection_arguments']['passwd']]),
                            ContainerElement('Please verify that these settings are correct or change '
                                             'them accordingly in the \'config.json\' file.',
                                             html_type='p'),
                            '{db_con}'
                        )
                    )
            },
            3: {
                'title': 'Executing initial queries on the database',
                'content': str(
                    ContainerElement(
                        ContainerElement(
                            'The following step will execute the initial queries to the database requred for \'dynamic_content\' to function. This will create new tables and fill them according to the installation specifications provided sufficient access to the database has been granted.',
                            html_type='p'),
                        ContainerElement('This step is required to proceed', html_type='p'),
                        ContainerElement(
                            'If you are certain, that the database has been properly configured to allow sufficient access to \'dynamic_content\' and are content with this software making changes to your database please click \'Continue\'',
                            html_type='p'),
                        ContainerElement('Continue', html_type='a', classes=['button', 'continue'],
                                         additionals='href="/setup/{next_page}"')
                    )
                )
            },
            4: {
                'title': '{result}',
                'content': str(
                    ContainerElement(
                        '{message}',
                        ContainerElement('{link}', html_type='a', classes=['continue', 'button'],
                                         additionals=['href="{target}"'])))
            },
            5: {
                'title': 'Create an admin account',
                'content': '{user_form}'
            },
            6: {}
        }
        generic = {
            'sidebar_left': '<div class="sidebar" style="height: 1px;"></div>',
            'pagetitle': 'Setting up your CMS installation'
        }
        self._model.update(setup_pages[self._url.page_id])

        self._model.update(generic)
        message = ''
        if self._url.page_id == 2:
            db = Database()
            self._model['content'] = self._model['content'].format(db_con=try_database_connection())
            del db
        if self._url.page_id == 4:
            db = Database()
            db.connect()
            setup_result = self.setup_wrapper()
            self._model['content'] = self._model['content'].format(**setup_result)
            self._model['title'] = self._model['title'].format(**setup_result)
            del db
        elif self._url.page_id == 5:
            handler = InitialUser(self._url, None)
            handler.destination = '/setup/6'
            content = handler.compiled
            self._model['content'] = self._model['content'].format(user_form=content.content)
        elif self._url.page_id == 6:
            config['setup'] = False
            write_config(config, 'cms/config.json')
            self.redirect('/iris/1')
        self._model['content'] = self._model['content'].format(this=self._url.path,
                                                               next_page=self._url.page_id + 1,
                                                               message=message)
        super()._fill_model()

    def setup(self):

        core_config = read_config('core/config')
        core_config['path'] = 'core'

        try:
            # HACK separately registering and activating core
            module_operations._activate_module(core_config)

            module_operations.register_installed_modules()
            for module in bootstrap.DEFAULT_MODULES:
                if not module_operations.activate_module(module):
                    print('Could not activate module ' + module)
                    return False
            Modules().reload()
            return True
        except DatabaseError as err:
            print(err)
            return False

    def setup_wrapper(self):
        if self.setup():
            return {
                'result': 'Success',
                'message': str(
                    ContainerElement(
                        ContainerElement('Your installation has been successful.', html_type='p'),
                        ContainerElement('All necessary tables have been created and filled in the database',
                                         html_type='p'),
                        ContainerElement('You may proceed.', html_type='p'))),
                'target': '/setup/{next_page}',
                'link': 'Continue'
            }
        else:
            return {
                'result': 'Failed',
                'message': str(
                    ContainerElement(
                        ContainerElement('Your installation has failed.', html_type='p'),
                        ContainerElement('Please revisit you settings and try again.',
                                         html_type='p'),
                        ContainerElement(
                            'Please ensure the database does not contain any tables that this CMS'
                            ' is trying to create', html_type='p'),
                        ContainerElement(
                            'You may delete all existing tables that should be created by clicking reset',
                            html_type='p'),
                        ContainerElement('Reset', html_type='a', classes='button',
                                         additionals=['href="{this}?reset=True"']))),
                'target': '/setup',
                'link': 'Restart'
            }