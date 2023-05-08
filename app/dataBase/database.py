import contextlib
import os
from typing import Iterator

from sqlalchemy import Engine, create_engine, Connection
from sqlalchemy.orm import declarative_base, sessionmaker, Session
""" SQL Database Setup"""
Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self):
        self._engine: Engine | None = None
        self._session_maker: sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_engine(host)
        self._session_maker = sessionmaker(autocommit=False, bind=self._engine)
        Base.metadata.create_all(bind=self._engine)

    def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @contextlib.contextmanager
    def connect(self) -> Iterator[Connection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise

    @contextlib.contextmanager
    def session(self) -> Iterator[Session]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


sessionmanager = DatabaseSessionManager()
