from dynct.backend.database import Database
import inspect



class ARObject:
    _table = ''
    database = Database()

    def __init__(self):
        self._is_real = False
        self._updated = False

    def __setattr__(self, key, value):
        if key in self.values:
            if not self._updated:
                self._updated = True
        super().__setattr__(key, value)

    @classmethod
    def get(cls, **descriptor):
        """
        Retrieve a single Object from the database.
        :param descriptor: Should be one ore more table keys.
        :return:
        """
        cursor = cls._get(**descriptor)
        return cls(cursor.fetchone())

    @classmethod
    def get_many(cls, range_, sort_by=None, **descriptors):
        """
        Retrieves many objects and returns a list of them.
        :param range_:
        :param descriptors:
        :return:
        """

        return [cls()]

    @classmethod
    def get_all(cls, sort_by=None, **descriptors):
        """
        Retrieves all objects described by descriptors.
        :param sort_by:
        :param descriptors:
        :return:
        """
        tail = {
            True: 'order by ' + sort_by,
            False: ''
        }[bool(sort_by)]
        cursor = cls._get(tail, **descriptors)
        return [cls(*a) for a in cursor.fetchall()]

    @classmethod
    def _get(cls, _tail:str='', **descriptors):
        return cls.database.select(cls.values(), cls._table, ' and '.join([a + ':=' + a for a in descriptors]), descriptors)

    def save(self):
        if self._updated or not self._is_real:
            if self._is_real:
                v = ', '.join([a + '=:' + a for a in self.values()])
                connection.execute('update ' + self._table + ' set ' + v + ' where ')

    @classmethod
    def values(cls) -> list:
        return inspect.getargspec(cls.__init__)[0][1:]