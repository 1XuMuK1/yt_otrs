from sqlalchemy import (
    create_engine,
    Column, String, Integer, ForeignKey, Boolean, DateTime, Text
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from config import DB_STRING

Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    otrs_ticket_number = Column(String)
    otrs_id = Column(String)
    youtrack_id = Column(String)
    date_create = Column(DateTime)
    date_update = Column(DateTime)
    is_closed = Column(Boolean)
    queueid = Column(Integer)
    stateid = Column(Integer)


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('ticket.id'))
    ticket = relationship('Ticket', backref=backref('articles', lazy=True))
    otrs_from = Column(String)
    youtrack_from = Column(String)
    title = Column(String)
    body = Column(Text)
    youtrack_id = Column(String)
    otrs_id = Column(String)


class Attachment(Base):
    __tablename__ = 'attachment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship('Article', backref=backref('attachments', lazy=True))
    filename = Column(String)
    filepath = Column(String)


db = create_engine(DB_STRING)
Session = sessionmaker(db)
session = Session()

# Base.metadata.create_all(db)
