import datetime

from dynct.modules.comp.html_elements import TableElement, ContainerElement, Label, Input, SubmitButton
from dynct.modules.form.secure import SecureForm
from dynct.core import handlers
from dynct.modules.users.users import GUEST
from . import session


__author__ = 'justusadam'

login_prefix = 'login'
logout_prefix = 'logout'

_cookie_time_format = '%a, %d %b %Y %H:%M:%S GMT'

USERNAME_INPUT = Label('Username', label_for='username'), Input(name='username', required=True)
PASSWORD_INPUT = Label('Password', label_for='password'), Input(input_type='password', required=True, name='password')

LOGOUT_TARGET = '/login'

LOGOUT_BUTTON = ContainerElement('Logout', html_type='a', classes={'logout', 'button'},
                                 additionals={'href': '/' + logout_prefix})

LOGIN_FORM = SecureForm(
    TableElement(
        USERNAME_INPUT,
        PASSWORD_INPUT
    )
    , action='/' + login_prefix, classes={'login-form'}, submit=SubmitButton(value='Login')
)

LOGIN_COMMON = SecureForm(
    ContainerElement(
        *USERNAME_INPUT + PASSWORD_INPUT
    )
    , action='/' + login_prefix, classes={'login-form'}, submit=SubmitButton(value='Login')
)


class LoginHandler(handlers.content.Content, handlers.base.RedirectMixIn):
    permission = 'access login page'

    def __init__(self, url, client):
        super().__init__(client)
        self.url = url
        self.message = ''
        self.page_title = 'Login'

    def process_content(self):
        return ContainerElement(self.message, LOGIN_FORM)

    def _process_post(self):
        if not self.url.post['username'] or not self._url.post['password']:
            raise ValueError
        username = self.url.post['username'][0]
        password = self.url.post['password'][0]
        token = session.start_session(username, password)
        if token:
            self.add_morsels({'SESS': token})
            self.redirect('/iris/1')
        else:
            self.message = ContainerElement('Your Login failed, please try again.', classes={'alert'})




class LoginCommonHandler(handlers.common.Commons):
    source_table = 'user_management'

    def get_content(self, name):
        return LOGIN_COMMON