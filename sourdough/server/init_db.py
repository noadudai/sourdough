from sourdough.db.orm_config import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)