from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

class Database:
    def __init__(self):
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        # db_path = os.path.join(BASE_DIR, "db.sqlite3")
        # self._db_url = f"sqlite:///{db_path}"
        self._db_url = ("sqlite:///C:/Users/Andrew/Desktop/SSU"
                       "/3_semestr/Yandex_back/Blogicum4/django_sprint4/blogicum/db.sqlite3")
        self._engine = create_engine(self._db_url)

    @contextmanager
    def session(self):
        connection = self._engine.connect()

        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
            connection.close()
        except Exception:
            session.rollback()
            raise


database = Database()
Base = declarative_base()