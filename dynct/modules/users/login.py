import datetime
from http.cookies import SimpleCookie
from urllib.error import HTTPError
from dynct.core.mvc.model import Model
from dynct.modules.comp.html_elements import TableElement, ContainerElement, Label, Input, SubmitButton
from dynct.modules.form.secure import SecureForm
from dynct.modules.commons.commons import Commons
from dynct.modules.users import session

from .users import GUEST


__author__ = 'justusadam'

login_prefix = 'login'
logout_prefix = 'logout'

_cookie_time_format = '%a, %d %b %Y %H:%M:%S GMT'

USERNAME_INPUT = Label('Username', label_for='username'), Input(name='username', required=True)
PASSWORD_INPUT = Label('Password', label_for='password'), Input(input_type='password', required=True, name='password')

LOGOUT_TARGET = '/login'

LOGOUT_BUTTON = ContainerElement('Logout', html_type='a', classes={'logout', 'button'},
                                 additional={'href': '/' + logout_prefix})

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


class LoginCommonHandler(Commons):
    source_table = 'user_management'

    def get_content(self, name):
        return LOGIN_COMMON


def login(model, url, client):
    if not client.check_permission('access login page'):
        raise HTTPError(str(url.path), 403, None, None, None)
    if url.post:
        if not url.post['username'] or not url.post['password']:
            raise ValueError
        username = url.post['username'][0]
        password = url.post['password'][0]
        token = session.start_session(username, password)
        if token:
            cookie = SimpleCookie({'SESS': token})
            m = Model(':redirect:/')
            m.cookies = cookie
            return m
        else:
            message = ContainerElement('Your Login failed, please try again.', classes={'alert'})
    else:
        message = ''
    model['content'] = ContainerElement(message, LOGIN_FORM)
    model.view = 'page'


def logout(model, url, client):
    user = client.user
    if user == GUEST:
        return ':redirect:/login'
    else:
        session.close_session(user)
        time = datetime.datetime.utcnow() - datetime.timedelta(days=1)

        if 'destination' in url.get_query:
            dest = url.get_query['destination'][0]
        else:
            dest = '/'
        model.cookies.load({'SESS': ''})
        model.cookies['SESS']['expires'] = time.strftime(_cookie_time_format)
        return ':redirect:' + dest