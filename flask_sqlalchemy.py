from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import backref, declarative_base, relationship, scoped_session, sessionmaker


class _QueryProperty:
    def __init__(self, db):
        self.db = db

    def __get__(self, obj, cls):
        return self.db.session.query(cls)


class SQLAlchemy:
    Column = Column
    Date = Date
    ForeignKey = ForeignKey
    Integer = Integer
    String = String
    Text = Text
    relationship = staticmethod(relationship)
    backref = staticmethod(backref)

    def __init__(self):
        self.engine = None
        self.session = scoped_session(sessionmaker(autoflush=False, autocommit=False))

        class Base:
            query = _QueryProperty(self)

        self.Model = declarative_base(cls=Base)

    def init_app(self, app):
        config = getattr(app, "config", app)
        uri = config["SQLALCHEMY_DATABASE_URI"]
        self.engine = create_engine(uri, pool_pre_ping=True)
        self.session.configure(bind=self.engine)
        self.Model.query = _QueryProperty(self)

    def create_all(self):
        self.Model.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.Model.metadata.drop_all(bind=self.engine)
