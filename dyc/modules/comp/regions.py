from dyc import core
from dyc.modules.commons import model as commonsmodel
from . import page, model
from dyc.util import html

__author__ = 'justusadam'


class RegionHandler:
    modules = core.Modules

    def __init__(self, region_name, region_config, theme, client):
        self.client = client
        self.name = region_name
        self.theme = theme
        self.commons = self.get_all_commons(region_name, theme)
        self.config = region_config

    def get_all_commons(self, name, theme):
        region_info = model.Common.select().where(model.Common.region == name,
                                                  model.Common.theme == core.model.Theme.get(machine_name=theme))
        if region_info:
            return [
                self.get_item(commonsmodel.CommonsConfig.get(commonsmodel.CommonsConfig.machine_name == a.machine_name),
                              a.render_args, a.show_title) for a in region_info]
        else:
            return []

    def get_item(self, item:commonsmodel.CommonsConfig, render_args, show_title):

        handler = self.modules[item.handler_module].common_handler(item.element_type)(item, render_args, show_title,
                                                                                      self.client)

        return Common(item.machine_name, handler, item.element_type)

    def wrap(self, value):
        classes = ['region', 'region-' + self.name.replace('_', '-')]
        if 'classes' in self.config:
            if isinstance(self.config['classes'], str):
                classes.append(self.config['classes'])
            else:
                classes += self.config['classes']
        return html.ContainerElement(html.ContainerElement(*value, classes={'region-wrapper', 'wrapper'}),
                                     classes=set(classes))

    def compile(self):
        stylesheets = []
        meta = []
        scripts = []
        cont_acc = []
        if self.commons:
            c = [item.handler.compile() for item in self.commons]
            for comp_item in c:
                if comp_item:
                    stylesheets += comp_item.stylesheets
                    meta += comp_item.metatags
                    scripts += comp_item.metatags
                    cont_acc.append(comp_item.content)
            content = self.wrap(cont_acc)
        else:
            content = ''

        return page.Component(content, stylesheets=stylesheets, metatags=meta, scripts=scripts)


class Common:
    def __init__(self, name, handler, item_type):
        self.name = name
        self.handler = handler
        self.item_type = item_type