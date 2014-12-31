import collections
import functools
import re

from . import Config, DefaultConfig
from . import controller
from .. import _component
from dyc import dchttp
from .model import Model
from dyc.util import decorators
from dyc.util import typesafe

__author__ = 'justusadam'

controller_mapper = _component.get_component('ControllerMapping')


class Autoconf:
    """
    Chains Custom config, model config and default conf and assigns it to the model.

    Priority is given as follows:
     Model.config > custom config argument? > Controller.config? > DefaultConfig
     ? is optional, will be omitted if bool(?) == false
    """

    @typesafe.typesafe
    def __init__(self, conf:Config):
        self.custom_conf = conf

    def __call__(self, func):
        @functools.wraps(func)
        @decorators.apply_to_type(Model, controller.Controller)
        def wrap(model, controller):
            model.config = collections.ChainMap(*[a for a in [
                model.config,
                self.custom_conf,
                self.get_controller_conf(controller),
                DefaultConfig
            ]
                                                  if a])

        return wrap

    def get_controller_conf(self, controller):
        return controller.config if hasattr(controller, 'config') else None


class ControlFunction:
    @typesafe.typesafe
    def __init__(self, function, prefix:str, regex:(str, type(None)), method:str, query:(str, list, tuple, set, dict, bool)):
        if isinstance(function, ControlFunction):
            self.function = function.function
            self.wrapping = function.wrapping
        else:
            self.wrapping = []
            self.function = function
        self.wrapping.append(self)
        self.prefix = prefix
        self.orig_pattern = regex
        self.regex = re.compile(regex) if regex else None
        self.method = method
        self.query = query
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance:
            return self.function(self.instance, *args, **kwargs)
        return self.function(*args, **kwargs)

    def __repr__(self):
        if self.instance:
            return '<ControlMethod for prefix \'' + self.prefix + '\' with function ' + repr(
                self.function) + ' and instance ' + repr(self.instance) + '>'
        return '<ControlFunction for prefix \'' + self.prefix + '\' with function ' + repr(self.function) + '>'


class RestControlFunction(ControlFunction):
    def __call__(self, model, *args, **kwargs):
        model.json_return = super().__call__(*args, **kwargs)
        model.decorator_attributes |= {'no-view', 'json-format', 'string-return'}
        return model


def __controller_function(class_, prefix, regex:str=None, *, method=dchttp.RequestMethods.GET, query=False):
    def wrap(func):
        wrapped = class_(func, prefix, regex, method, query)
        controller_mapper.add_controller(prefix, wrapped)
        return wrapped

    return wrap


def __controller_method(class_, prefix, regex:str=None, *, method=dchttp.RequestMethods.GET, query=False):
    def wrap(func):
        wrapped = class_(func, prefix, regex, method, query)
        return wrapped

    return wrap


controller_function = functools.partial(__controller_function, ControlFunction)


def controller_class(class_):
    c_funcs = list(filter(lambda a: isinstance(a, ControlFunction), class_.__dict__.values()))
    if c_funcs:
        instance = class_()
        controller_mapper._controller_classes.append(instance)
        for item in c_funcs:
            for wrapped in item.wrapping:
                wrapped.instance = instance
                controller_mapper.add_controller(wrapped.prefix, wrapped)
    return class_


controller_method = functools.partial(__controller_method, ControlFunction)

rest_controller_function = functools.partial(__controller_function, RestControlFunction)

rest_controller_method = functools.partial(__controller_method, RestControlFunction)


class url_args:
    """
    Function decorator for controller Methods. Parses the Input (url) without prefix according to the regex.
    Unpacks groups into function call arguments.

    get and post can be lists of arguments which will be passed to the function as keyword arguments or booleans
    if get/post are true the entire query is passed to the function as keyword argument 'get' or 'post'
    if get/post are false no queries will passed

    if strict is true, only specified values will be accepted,
    and the existence of additional arguments will cause an error.

    :param regex: regex pattern or string
    :param get: list/tuple (subclasses) or boolean
    :param post: list/tuple (subclasses) or boolean
    :param strict: boolean
    :return:
    """

    def __init__(self, regex, *, get=False, post=False, strict:bool=False):
        self.get = self.q_comp(get, 'get')
        self.post = self.q_comp(post, 'post')
        self.regex = isinstance(regex, str) if re.compile(regex) else regex
        self.strict = strict

    def q_comp(self, q, name):
        if type(q) == bool:
            if q:
                return lambda a: {name: a}
            elif self.strict:
                return lambda a: bool(a) if False else {}
            else:
                return lambda a: {}
        elif issubclass(type(q), (list, tuple)):
            if self.strict:
                def f(a:list, b:dict):
                    d = b.copy()
                    for item in a:
                        if item not in d:
                            raise TypeError
                    return d

                return lambda a: len(q) == len(a.keys()) if f(q, a) else False
            return lambda a: {arg: a.get(arg) for arg in q}
        else:
            raise TypeError

    def __call__(self, func):
        def _generic(model, url, client):
            kwargs = dict(client=client)
            for result in [self.get(url.get_query), self.post(url.post)]:
                if result is False:
                    raise TypeError
                else:
                    kwargs.update(result)
            # return re.match(regex, str(url.path)).groups(), kwargs
            return func(*(model, ) + re.match(self.regex, url.path.prt_to_str(1)).groups(), **kwargs)

        return _generic