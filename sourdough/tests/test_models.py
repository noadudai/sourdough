import pytest
import datetime

from sqlalchemy.exc import IntegrityError

from sourdough.db.models.feeding_actions_table import FeedingActionModel
from sourdough.db.models.extractions_table import ExtractionModel
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActionModel
from sourdough.db.models.sourdough_table import SourdoughModel
from sourdough.db.models.sourdough_targets_table import SourdoughTargetModel
from sourdough.db.models.user_table import UserModel
import json

from sourdough.server.actions import RefrigerationAction, FeedingAction, ExtractionAction
from sourdough.server.messages import PerformActionsMessage, ActionsPerformedMessage


def test_create_a_user_and_a_sourdough_in_db(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()


def test_for_creating_a_target_with_all_information(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target = SourdoughTargetModel(sourdough_id=sourdough.id,
                                  date_of_action=datetime.date(2021, 7, 24),
                                  sourdough_weight_target_in_grams=150)
    session.add(target)
    session.commit()
    print(sourdough.sourdough_targets)


def test_see_if_there_are_more_than_one_user_in_db(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    user2 = UserModel(name="Noam", last_name="Dudaia", email="lgekfd@gamil.com")
    session.add(user)
    session.add(user2)
    session.commit()
    users = session.query(UserModel).all()
    return_list = [str(user) for user in users]
    if len(return_list) < 2:
        print("good")
    else:
        print("bad")


def test_raise_error_if_an_email_is_not_provided(session):
    user = UserModel(name="vks", last_name="jf")
    session.add(user)
    with pytest.raises(IntegrityError):
        session.commit()


def test_to_add_extraction_action_to_db(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    extraction_instance = ExtractionModel(sourdough_id=sourdough.id, sourdough_weight_used_in_grams=150)
    session.add(extraction_instance)
    session.commit()


def test_to_add_a_feeding_action_to_db(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    feeding_action = FeedingActionModel(sourdough_id=sourdough.id,
                                        water_weight_added_in_grams=10,
                                        flour_weight_added_in_grams=10)
    session.add(feeding_action)
    session.commit()


def test_to_add_a_refrigerator_action_to_db(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorActionModel(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()


def test_check_how_many_days_there_is_until_the_date_of_the_target_or_how_many_days_passed(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target_instance = SourdoughTargetModel(sourdough_id=sourdough.id,
                                           date_of_action=datetime.date(2021, 7, 6),
                                           sourdough_weight_target_in_grams=150)
    target_instance2 = SourdoughTargetModel(sourdough_id=sourdough.id,
                                            date_of_action=datetime.date(2021, 7, 18),
                                            sourdough_weight_target_in_grams=150)
    session.add(target_instance)
    session.add(target_instance2)
    session.commit()
    my_target_date = session.query(SourdoughTargetModel.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_target_date.date_of_action.date()
    delta = target - today
    return delta.days


def test_if_sourdough_starter_is_in_the_refrigerator(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorActionModel(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    my_refrigerator_action_model = session.query(RefrigeratorActionModel.in_or_out).filter_by(sourdough_id=sourdough.id)[-1]
    return my_refrigerator_action_model


def test_to_check_how_many_days_is_the_sourdough_starter_in_the_refrigerator(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorActionModel(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    my_refrigerator_date = session.query(RefrigeratorActionModel.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_refrigerator_date.date_of_action.date()
    delta = target - today
    return delta.days


def test_action_today(session):
    user = UserModel(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = SourdoughModel(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target_instance = SourdoughTargetModel(sourdough_id=sourdough.id,
                                           date_of_action=datetime.date(2021, 7, 27),
                                           sourdough_weight_target_in_grams=150)
    session.add(target_instance)
    session.commit()
    session.flush()
    refrigerator_model = RefrigeratorActionModel(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator_model)
    session.commit()
    session.flush()
    feeding_action_model = FeedingActionModel(sourdough_id=sourdough.id,
                                              water_weight_added_in_grams=50,
                                              flour_weight_added_in_grams=50)
    feeding_action2_model = FeedingActionModel(sourdough_id=sourdough.id,
                                               water_weight_added_in_grams=50,
                                               flour_weight_added_in_grams=50)
    session.add(feeding_action_model)
    session.add(feeding_action2_model)
    session.commit()
    target_weight = session.query(SourdoughTargetModel.sourdough_weight_target_in_grams).filter_by(sourdough_id=sourdough.id)[-1]
    refrigerator_state_model = session.query(RefrigeratorActionModel.in_or_out).filter_by(sourdough_id=sourdough.id)[-1]
    delta_target = sourdough.days_until_target
    delta_refrigerator = sourdough.days_in_refrigerator
    if delta_target < 0:
        if delta_refrigerator == 10:
            if sourdough.weight < sourdough.max_maintenance_weight:
                print(json.dumps(sourdough.is_over_maintenance_weight))
        elif 9 < delta_refrigerator > 1:
            refrigeration_action = RefrigerationAction(refrigerator_state_model.in_or_out)
            message = PerformActionsMessage([refrigeration_action])
            print(json.dumps(message.to_dict()))
        else:
            raise Exception("The sourdough starter is in the refrigerator more than the max 10 days!.")
    elif delta_target == 0:
        feeding_action = FeedingAction(str((target_weight.sourdough_weight_target_in_grams / 3) - 4),
                                       str((target_weight.sourdough_weight_target_in_grams / 3) - 4))
        extraction_action = ExtractionAction(str(target_weight.sourdough_weight_target_in_grams - 4))
        refrigeration_action = RefrigerationAction("in")
        action = [feeding_action, extraction_action, refrigeration_action]
        message = PerformActionsMessage(action)
        print(json.dumps(message.to_dict()))
    elif 0 < delta_target <= 2:
        feeding_action = FeedingAction(str(sourdough.weight), str(sourdough.weight))
        message = PerformActionsMessage([feeding_action])
        print(json.dumps(message.to_dict()))
    elif delta_target == 3:
        refrigeration_action = RefrigerationAction("out")
        extraction_action = ExtractionAction(str(sourdough.weight - 2))
        feeding_action = FeedingAction("2", "2")
        actions = [refrigeration_action, extraction_action, feeding_action]
        message = PerformActionsMessage(actions)
        print(json.dumps(message.to_dict()))
    elif 9 < delta_target > 3:
        refrigeration_action = RefrigerationAction("in")
        message = PerformActionsMessage([refrigeration_action])
        print(json.dumps(message.to_dict()))
    elif delta_target >= 10:
        print(json.dumps(sourdough.is_over_maintenance_weight))
