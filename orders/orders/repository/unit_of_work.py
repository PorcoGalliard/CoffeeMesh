from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class UnitOfWork:
    def __init__(self):
        # obtain the session factory object
        self.session_maker = sessionmaker(
            bind=create_engine('sqlite:///orders.db')
        )

    def __enter__(self):
        # open new database session
        self.session = self.session_maker()
        # return the instance of unit of work object
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            # if an exception took place, rollback the database transaction
            self.rollback()
            self.session.close()
        self.session.close()
