from core.base_handlers import FieldHandler
from core.page import Component

__author__ = 'justusadam'


class BaseFieldHandler(FieldHandler):
    def __init__(self, db, page_id, field_name):
        super().__init__(db)
        self.page_id = page_id
        self.field_name = field_name

    def compile(self):
        content = self.get_content()
        if not content:
            return False
        field = Component()
        field.content = content
        self._field = field
        self._is_compiled = True
        return True

    def get_content(self):
        return self.db.select('content' ,self.field_name, 'where page_id=' + self.page_id).fetchone()