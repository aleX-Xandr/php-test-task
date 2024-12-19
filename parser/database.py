from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator


class Database:
    def __init__(self, db_url: str) -> None:
        """
        Constructor
        """
        self.engine = create_engine(db_url)
        self.__session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager for handling exceptions and closing session
        """
        with self.__session() as session:
            try:
                yield session
            except Exception as e:
                session.rollback()
                raise e
            else:
                session.commit()
            finally:
                session.close()