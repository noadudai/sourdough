import pytest
import datetime

from sqlalchemy.exc import IntegrityError

from sourdough.db.models.feeding_actions_table import FeedingActions
from sourdough.db.models.leaven_extractions_table import LeavenExtractions
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActions
from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.sourdough_targets_table import SourdoughTargets
from sourdough.db.models.user_table import User


def test_create_a_user_and_a_sourdough_in_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()


def test_for_creating_a_target_with_all_information(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target = SourdoughTargets(sourdough_id=sourdough.id,
                              date_of_action=datetime.date(2021, 7, 24),
                              sourdough_weight_target_in_grams=150)
    session.add(target)
    session.commit()
    print(sourdough.sourdough_targets)


def test_see_if_there_are_more_than_one_user_in_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    user2 = User(name="Noam", last_name="Dudaia", email="lgekfd@gamil.com")
    session.add(user)
    session.add(user2)
    session.commit()
    users = session.query(User).all()
    return_list = [str(user) for user in users]
    if len(return_list) < 2:
        print("good")
    else:
        print("bad")


def test_raise_error_if_an_email_is_not_provided(session):
    user = User(name="vks", last_name="jf")
    session.add(user)
    with pytest.raises(IntegrityError):
        session.commit()


def test_to_add_a_leaven_extraction_action_to_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    leaven_instance = LeavenExtractions(sourdough_id=sourdough.id, sourdough_weight_used_in_grams=150)
    session.add(leaven_instance)
    session.commit()


def test_to_add_a_feeding_action_to_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    feeding_action = FeedingActions(sourdough_id=sourdough.id,
                                    water_weight_added_in_grams=10,
                                    flour_weight_added_in_grams=10)
    session.add(feeding_action)
    session.commit()


def test_to_add_a_refrigerator_action_to_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorActions(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()


def test_check_how_many_days_there_is_until_the_date_of_the_target_or_how_many_days_passed(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target_instance = SourdoughTargets(sourdough_id=sourdough.id,
                                       date_of_action=datetime.date(2021, 7, 6),
                                       sourdough_weight_target_in_grams=150)
    target_instance2 = SourdoughTargets(sourdough_id=sourdough.id,
                                        date_of_action=datetime.date(2021, 7, 18),
                                        sourdough_weight_target_in_grams=150)
    session.add(target_instance)
    session.add(target_instance2)
    session.commit()
    my_target_date = session.query(SourdoughTargets.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_target_date.date_of_action.date()
    delta = target - today
    return delta


def test_if_sourdough_starter_is_in_thr_refrigerator(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorActions(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    my_refrigerator_action = session.query(RefrigeratorActions.in_or_out).filter_by(sourdough_id=sourdough.id)[-1]
    return my_refrigerator_action


def test_to_check_how_many_days_is_the_sourdough_starter_in_the_refrigerator(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorActions(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    my_refrigerator_date = session.query(RefrigeratorActions.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_refrigerator_date.date_of_action.date()
    delta = target - today
    return delta