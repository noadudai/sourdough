import pytest

from sourdough.db.models.user_table import User


def test_create_sourdough_in_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    print(user)
    assert 0



