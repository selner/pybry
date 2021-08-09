import uuid
from datetime import date, timedelta, datetime
from functools import partial


# from arrow import Arrow
# from sqlalchemy import DateTime

import json as basejson

from jsoncomment import JsonComment
import os


class ForgivingJSONDecoder(basejson.JSONDecoder):

    def __init__(self, object_hook=None, *args, **kwargs):
        super().__init__(object_hook=self.as_object, *args, **kwargs)

    def as_object(self, dct):
        key, val = dct
        try:
            func = None
            if 'uuid' in key:
                func = uuid.UUID
            elif 'date' in key or 'datetime' in key:
                func = datetime.fromisoformat
            elif 'time' in key or 'timestamp' in key:
                func = datetime.fromtimestamp
            # elif 'set' in key:
            #     func = set

            if func and callable(func):
                val = partial(func, dict[key])
                dct[key] = val
        except Exception as ex:
            pass

        return dct


class ForgivingJSONEncoder(basejson.JSONEncoder):
    """The default Flask JSON encoder.  This one extends the default simplejson
    encoder by also supporting ``db.DateTime`` objects, ``UUID`` as well as
    ``Markup`` objects which are serialized as RFC 822 db.DateTime db.Strings (same
    as the HTTP date format).  In order to support more data types override the
    :meth:`default` method.
    """

    def default(self, o):
        """Implement this method in a subclass such that it returns a
        serializable object for ``o``, or calls the base implementation (to
        raise a :exc:`TypeError`).

        For example, to support arbitrary iterators, you could implement
        default like this::

            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                return JSONEncoder.default(self, o)
        """
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        elif isinstance(o, timedelta):
            return {
                '__type__': 'timedelta',
                'days': o.days,
                'seconds': o.seconds,
                'microseconds': o.microseconds,
            }
        # elif isinstance(o, Arrow):
        #     return self.default(o.db.DateTime)
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, set):
            return list(o)
        # elif isinstance(o, DateTime):
        #     return {
        #         '__type__': 'db.DateTime',
        #         'year': o.year,
        #         'month': o.month,
        #         'day': o.day,
        #         'hour': o.hour,
        #         'minute': o.minute,
        #         'second': o.second,
        #         'microsecond': o.microsecond,
        #     }

        else:
            try:
                return list(iter(o))
            except TypeError:
                pass

        try:
            return basejson.JSONEncoder.default(self, o)
        except TypeError:
            pass

        return "<JSONSerializationFailed>"


def dump(*args, **kw):
    if not ('cls' in kw and kw['cls']):
        kw['cls'] = ForgivingJSONEncoder

    from json import dump
    return dump( *args, **kw)


def dumps(data, *args, **kw):
    if not ('cls' in kw and kw['cls']):
        kw['cls'] = ForgivingJSONEncoder
    from json import dumps
    return dumps(data, *args, **kw)


def dumpf(sourcepath, *args, **kwargs):
    with open(sourcepath, "w") as fp:
        from jsoncomment import JsonComment
        jsc = JsonComment()
        return jsc.dump(fp=fp, *args, **kwargs)

def loadf(sourcepath, *args, **kw):
    jsc = JsonComment()
    if not ('cls' in kw and kw['cls']):
        kw['cls'] = ForgivingJSONDecoder
    return jsc.loadf(sourcepath, *args, **kw)


def loads(*args, **kw):
    if not ('cls' in kw and kw['cls']):
        kw['cls'] = ForgivingJSONDecoder
    jsc = JsonComment()

    return jsc.loads(*args, **kw)


def load(*args, **kw):
    jsc = JsonComment()
    return jsc.load(*args, **kw)




class ForgivingJson(object):
    _data = None
    _tmpfile = None

    @property
    def filename(self):
        return self._tmpfile

    def as_dict(self):
        return dumps(self._data, indent=2, cls=ForgivingJSONEncoder)

    def as_json(self):
        return dumps(self._data, indent=2, cls=ForgivingJSONEncoder)

    def __init__(self, sourcepath=None):
        if sourcepath:
            import temp
            self._tmpfile = temp.tempfile() #
    #        self._tmpfile = tempfile.TemporaryFile(prefix=os.path.basename(__file__), suffix="loader")
            if os.path.isfile(sourcepath) or os.path.islink(sourcepath):
                if sourcepath and str(sourcepath).endswith(".json"):
                    import jsoncomment
                    jsc = jsoncomment.JsonComment()
                    self._data = jsc.loadf(sourcepath)
                    dumpf(self._tmpfile, self._data, cls=ForgivingJSONEncoder)

    def from_json(self):
        return self._data

    @staticmethod
    def dump(*args, **kw):
        if not ('cls' in kw and kw['cls']):
            kw['cls'] = ForgivingJSONEncoder

        from json import dump
        return dump(*args, **kw)

    @staticmethod
    def dumps(*args, **kw):
        if not ('cls' in kw and kw['cls']):
            kw['cls'] = ForgivingJSONEncoder
        from json import dumps
        return dumps( *args, **kw)

    @staticmethod
    def dumpf(sourcepath, *args, **kwargs):
        with open(sourcepath, "w") as fp:
            jsc = JsonComment()
            return jsc.dump(fp=fp, *args, **kwargs)

    @staticmethod
    def loadf(sourcepath, *args, **kw):
        jsc = JsonComment()
        if not ('cls' in kw and kw['cls']):
            kw['cls'] = ForgivingJSONDecoder
        return jsc.loadf(sourcepath, *args, **kw)

    @staticmethod
    def loads(*args, **kw):
        if not ('cls' in kw and kw['cls']):
            kw['cls'] = ForgivingJSONDecoder
        jsc = JsonComment()

        return jsc.loads(*args, **kw)

    @staticmethod
    def load(*args, **kw):
        jsc = JsonComment()
        return jsc.load(*args, **kw)

    @staticmethod
    def load_from_file(filepath, *args, **kw):
        with open(filepath, "r") as fp:
            jsonval = fp.read()

            jsc = JsonComment()
            return jsc.loads(jsonval, *args, **kw)



