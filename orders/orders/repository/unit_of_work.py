from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class UnitOfWork:
    def __init__(self):
        self.session_maker = sessionmaker(
            bind=create_engine('sqlite:///orders.db')
        )
