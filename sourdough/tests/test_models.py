import pytest
import datetime

from sqlalchemy.exc import IntegrityError

from sourdough.db.models.feeding_actions_table import FeedingAction
from sourdough.db.models.extractions_table import Extraction
from sourdough.db.models.refrigerator_actions_table import RefrigeratorAction
from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.sourdough_targets_table import SourdoughTarget
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
    target = SourdoughTarget(sourdough_id=sourdough.id,
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


def test_to_add_extraction_action_to_db(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    extraction_instance = Extraction(sourdough_id=sourdough.id, sourdough_weight_used_in_grams=150)
    session.add(extraction_instance)
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
    feeding_action = FeedingAction(sourdough_id=sourdough.id,
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
    refrigerator = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
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
    target_instance = SourdoughTarget(sourdough_id=sourdough.id,
                                      date_of_action=datetime.date(2021, 7, 6),
                                      sourdough_weight_target_in_grams=150)
    target_instance2 = SourdoughTarget(sourdough_id=sourdough.id,
                                       date_of_action=datetime.date(2021, 7, 18),
                                       sourdough_weight_target_in_grams=150)
    session.add(target_instance)
    session.add(target_instance2)
    session.commit()
    my_target_date = session.query(SourdoughTarget.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_target_date.date_of_action.date()
    delta = target - today
    return delta.days


def test_if_sourdough_starter_is_in_the_refrigerator(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    my_refrigerator_action = session.query(RefrigeratorAction.in_or_out).filter_by(sourdough_id=sourdough.id)[-1]
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
    refrigerator = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    my_refrigerator_date = session.query(RefrigeratorAction.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_refrigerator_date.date_of_action.date()
    delta = target - today
    return delta.days


def test_what_action_can_i_do_today(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target_instance = SourdoughTarget(sourdough_id=sourdough.id,
                                      date_of_action=datetime.date(2021, 7, 27),
                                      sourdough_weight_target_in_grams=150)
    session.add(target_instance)
    session.commit()
    session.flush()
    my_target_date = session.query(SourdoughTarget.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    refrigerator = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    session.flush()
    feeding_action = FeedingAction(sourdough_id=sourdough.id,
                                   water_weight_added_in_grams=50,
                                   flour_weight_added_in_grams=50)
    feeding_action2 = FeedingAction(sourdough_id=sourdough.id,
                                    water_weight_added_in_grams=50,
                                    flour_weight_added_in_grams=50)
    session.add(feeding_action)
    session.add(feeding_action2)
    session.commit()
    my_refrigerator_action = session.query(RefrigeratorAction.in_or_out).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_target_date.date_of_action.date()
    delta = target - today
    my_refrigerator_date = session.query(RefrigeratorAction.date_of_action).filter_by(sourdough_id=sourdough.id)[-1]
    today = datetime.datetime.today().date()
    target = my_refrigerator_date.date_of_action.date()
    delta_refrigerator = target - today
    if delta.days < 0:
        if my_refrigerator_action.in_or_out == "in":
            if 9 < delta_refrigerator.days > 1:
                print("keep the sourdough starter in thr refrigerator")
            else:
                if sourdough.weight < 100:
                    refrigerator2 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="out")
                    session.add(refrigerator2)
                    session.commit()
                    session.flush()
                    print("take your sourdough stater out of the refrigerator and feed it 1:1:1, "
                          "and put it back in the refrigerator. feed " + str(sourdough.weight) + "grams water, and " +
                          str(sourdough.weight) + "grams flour.")
                    refrigerator3 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
                    session.add(refrigerator3)
                    session.commit()
                    session.flush()
                    feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                                    water_weight_added_in_grams=sourdough.weight,
                                                    flour_weight_added_in_grams=sourdough.weight)
                    session.add(feeding_action3)
                    session.commit()
                else:
                    refrigerator2 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="out")
                    session.add(refrigerator2)
                    session.commit()
                    session.flush()
                    extraction_weight = sourdough.weight-4
                    print("you don't have a target, take your sourdough stater out of the refrigerator and extract " +
                          str(extraction_weight) + "grams from it so it weigh 4 grams and feed it 1:1:1, "
                                                   "4 grams water and 4 grams flour.")
                    extraction_instance = Extraction(sourdough_id=sourdough.id,
                                                     sourdough_weight_used_in_grams=extraction_weight)
                    session.add(extraction_instance)
                    session.commit()
                    session.flush()
                    feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                                    water_weight_added_in_grams=sourdough.weight,
                                                    flour_weight_added_in_grams=sourdough.weight)
                    session.add(feeding_action3)
                    session.commit()
        else:
            print("the sourdough starter should be in the refrigerator. if you didn't specified a refrigerator action "
                  "with 'in' action please do so now.")
    else:
        if delta.days == 3:
            print("please take out the sourdough starter and feed it 1:1:1, " + str(sourdough.weight) +
                  "grams water, and " + str(sourdough.weight) + "grams flour. your target is in " + str(delta.days) +
                  " days.")
            refrigerator2 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="out")
            session.add(refrigerator2)
            session.commit()
            session.flush()
            feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                            water_weight_added_in_grams=sourdough.weight,
                                            flour_weight_added_in_grams=sourdough.weight)
            session.add(feeding_action3)
            session.commit()
        elif delta.days == 2:
            print("please feed your sourdough starter 1:1:1, " + str(sourdough.weight) + "grams water and " +
                  str(sourdough.weight) + "grams flour. your target is in " + str(delta.days) + " days.")
            feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                            water_weight_added_in_grams=sourdough.weight,
                                            flour_weight_added_in_grams=sourdough.weight)
            session.add(feeding_action3)
            session.commit()
        elif delta.days == 1:
            print("today is your targeted day. please feed yor sourdough starter 1:1:1, " + str(sourdough.weight) +
                  "grams water and " + str(sourdough.weight) +
                  "grams flour. extract the targeted sourdough weight you specified " +
                  str(my_target_date.sourdough_weight_target_in_grams) + "grams. and put it in the refrigerator until "
                                                                         "the next target.")
            feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                            water_weight_added_in_grams=sourdough.weight,
                                            flour_weight_added_in_grams=sourdough.weight)
            session.add(feeding_action3)
            session.commit()
            extraction_instance = Extraction(sourdough_id=sourdough.id,
                                             sourdough_weight_used_in_grams=my_target_date.sourdough_weight_target_in_grams)
            session.add(extraction_instance)
            session.commit()
            session.flush()
            refrigerator2 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
            session.add(refrigerator2)
            session.commit()
            session.flush()
        else:
            if my_refrigerator_action.in_or_out == "in":
                if 9 < delta_refrigerator.days > 1:
                    print("keep the sourdough starter in thr refrigerator")
                else:
                    if sourdough.weight < 100:
                        refrigerator2 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="out")
                        session.add(refrigerator2)
                        session.commit()
                        session.flush()
                        print("take your sourdough stater out of the refrigerator and feed it 1:1:1, "
                              "and put it back in the refrigerator. feed " + str(sourdough.weight) + "grams water, and " +
                              str(sourdough.weight) + "grams flour.")
                        refrigerator3 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
                        session.add(refrigerator3)
                        session.commit()
                        session.flush()
                        feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                                        water_weight_added_in_grams=sourdough.weight,
                                                        flour_weight_added_in_grams=sourdough.weight)
                        session.add(feeding_action3)
                        session.commit()
                    else:
                        refrigerator2 = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="out")
                        session.add(refrigerator2)
                        session.commit()
                        session.flush()
                        extraction_weight = sourdough.weight - 4
                        print("you have " + str(delta.days) + " days until the target. take your sourdough stater out "
                              "of the refrigerator and extract " + str(extraction_weight) +
                              "grams from it so it weigh 4 grams and feed it 1:1:1, 4 grams water and 4 grams flour.")
                        extraction_instance = Extraction(sourdough_id=sourdough.id,
                                                         sourdough_weight_used_in_grams=extraction_weight)
                        session.add(extraction_instance)
                        session.commit()
                        session.flush()
                        feeding_action3 = FeedingAction(sourdough_id=sourdough.id,
                                                        water_weight_added_in_grams=sourdough.weight,
                                                        flour_weight_added_in_grams=sourdough.weight)
                        session.add(feeding_action3)
                        session.commit()
            else:
                print(
                    "the sourdough starter should be in the refrigerator. if you didn't specified a refrigerator action"
                    " with 'in' action please do so now.")


def test_action_today(session):
    user = User(name="Noa", last_name="Dudai", email="lgek@gamil.com")
    session.add(user)
    session.commit()
    session.flush()
    sourdough = Sourdough(user_id=user.id)
    session.add(sourdough)
    session.commit()
    session.flush()
    target_instance = SourdoughTarget(sourdough_id=sourdough.id,
                                      date_of_action=datetime.date(2021, 7, 27),
                                      sourdough_weight_target_in_grams=150)
    session.add(target_instance)
    session.commit()
    session.flush()
    refrigerator = RefrigeratorAction(sourdough_id=sourdough.id, in_or_out="in")
    session.add(refrigerator)
    session.commit()
    session.flush()
    feeding_action = FeedingAction(sourdough_id=sourdough.id,
                                   water_weight_added_in_grams=50,
                                   flour_weight_added_in_grams=50)
    feeding_action2 = FeedingAction(sourdough_id=sourdough.id,
                                    water_weight_added_in_grams=50,
                                    flour_weight_added_in_grams=50)
    session.add(feeding_action)
    session.add(feeding_action2)
    session.commit()
    target_weight = session.query(SourdoughTarget.sourdough_weight_target_in_grams).filter_by(sourdough_id=sourdough.id)[-1]
    delta_target = sourdough.days_until_target
    delta_refrigerator = sourdough.days_in_refrigerator
    if delta_target < 0:
        if delta_refrigerator == 10:
            if sourdough.weight < sourdough.max_maintenance_weight:
                return sourdough.is_over_maintenance_weight
        elif 9 < delta_refrigerator > 1:
            action = {"days in": str(delta_refrigerator), "days until out": str(delta_refrigerator-10)}
            print(action)
#            return jsonify(action)
        else:
            raise Exception("The sourdough starter is in the refrigerator more than the max 10 days!.")
    elif delta_target == 0:
        action = {"action1": "feed " + str((target_weight.sourdough_weight_target_in_grams / 3)-4) + "grams flour and water",
                  "action2": "extraction target " + str(target_weight.sourdough_weight_target_in_grams-4) + "grams",
                  "action3": "refrigerator in"}
        print(action)
#        return jsonify(action)
    elif 0 < delta_target <= 2:
        action = {"action": "feed " + str(sourdough.weight) + "grams flour and water"}
        print(action)
#        return jsonify(action)
    elif delta_target == 3:
        action = {"action1": "refrigerator out",
                  "action2": "extract " + str(sourdough.weight - 2) + "grams",
                  "action3": "feed 2grams flour and 2grams water"}
        print(action)
#        return jsonify(action)
    elif 9 < delta_target > 3:
        action = {"days in": str(delta_refrigerator), "days until out": str(delta_target-3)}
        print(action)
#        return jsonify(action)
    elif delta_target >= 10:
        return sourdough.is_over_maintenance_weight

