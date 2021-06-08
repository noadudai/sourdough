from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.user_table import User
from sourdough.db.models.feeding_table import Feeding
from sourdough.db.models.leaven_table import Leaven
from sourdough.db.orm_config import Base, engine, Session
import datetime

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    my_user = User(name="Peeps", fullname="Peeps Peepsy", email="peeps@gmail.com")
    session = Session()
    session.add(my_user)
    session.flush()
    my_sourdough = Sourdough(weight=100, user_id=my_user.id)
    session.add(my_sourdough)
    session.commit()

    print(my_user.name)
    print(my_user.id)
