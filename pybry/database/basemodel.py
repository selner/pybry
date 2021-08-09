import os
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlservice import ModelBase, SQLClient
from sqlalchemy import ForeignKey, MetaData, select, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, relationship, backref
from sqlalchemy.orm import as_declarative

DeclarativeBase = declarative_base()

metadata = MetaData()


@as_declarative(metadata=metadata)
class Model(ModelBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @property
    def tablename(self):
        return str(self.__tablename__)

    @classmethod
    def find_one(cls, **kwargs):
        """Query this table for a single row matching kwargs filters."""
        return cls.query.filter_by(**kwargs).one()

    @classmethod
    def find_one_or_404(cls, **kwargs):
        """Query this table for a single row, flask.abort(404) if not found."""
        try:
            cls.find_one(**kwargs)
        except (NoResultFound, MultipleResultsFound):
            os.abort(404)

    @classmethod
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        cls.query.session.add(obj)
        return obj

    @staticmethod
    @classmethod
    def find_create(cls, create_args=None, **kwargs):
        """Find or create an instance of this model.
        Optionally provide arguments used only for creating the object, not
        querying.
        """
        try:
            return cls.find_one(**kwargs)
        except NoResultFound:
            create_args = dict(create_args or {})
            create_args.update(kwargs)
            return cls.create(**create_args)


def get_database_client(dbfilepath):
    from nturl2path import pathname2url
    dburi = 'sqlite:////' + pathname2url(dbfilepath)
    cfg = {
        "SQL_DATABASE_URI": dburi,  # f'sqlite:////tmp/ragingpull/ragingpull.db',
        "SQL_ISOLATION_LEVEL": "SERIALIZABLE",
        # "SQL_ECHO": True,
        # "SQL_ECHO_POOL": False,
        # "SQL_CONVERT_UNICODE": True,
        # "SQL_POOL_SIZE": 5,
        # "SQL_POOL_TIMEOUT": 30,
        # "SQL_POOL_RECYCLE": 3600,
        # "SQL_MAX_OVERFLOW": 10,
        "SQL_AUTOCOMMIT": False,
        "SQL_AUTOFLUSH": False,
        "SQL_EXPIRE_ON_COMMIT": False
    }

    dbclient = SQLClient(cfg, model_class=Model)
    dbclient.create_all()

    dbclient.flush()
    dbclient.reflect()

    return dbclient


def get_model_properties(model):
    return [str(desc) for desc in model.class_mapper().all_orm_descriptors]


def find_or_create(objtype, data, db):
    try:
        res = db.query(objtype).filter_by(**data).one()
    except Exception as ex:
        res = None

    if not res:
        res = objtype(**data)

    return res
