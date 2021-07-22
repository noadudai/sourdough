from typing import List

from sourdough.db.models.feeding_actions_table import FeedingActionModel
from sourdough.db.models.extractions_table import ExtractionModel
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActionModel
from sourdough.db.models.sourdough_table import SourdoughModel
from sourdough.db.models.sourdough_targets_table import SourdoughTargetModel
from sourdough.db.models.user_table import UserModel
from sourdough.db.orm_config import Session, Base, engine
from flask import Flask, request, jsonify
import datetime
import json

from sourdough.communication.actions import RefrigerationAction, FeedingAction, ExtractionAction, Action
from sourdough.communication.messages import PerformActionsMessage, SuccessMessage, FailedMessage

app = Flask(__name__)


# A flask function to create an account and it's sourdough, and adding them to the database.
@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    with Session() as session:
        data = request.args
        name = data['name']
        last_name = data['last_name']
        email = data['email']
        if session.query(session.query(UserModel).filter_by(email=email).exists()).scalar():
            message = FailedMessage("User already exists.")
            return json.dumps(message.to_dict())
        else:
            my_user_model = UserModel(name=name, last_name=last_name, email=email)
            session.add(my_user_model)
            session.flush()
            my_sourdough_model = SourdoughModel(user_id=my_user_model.id)
            session.add(my_sourdough_model)
            session.flush()
            not_in_fridge = RefrigeratorActionModel(sourdough_id=my_sourdough_model.id, in_or_out="out")
            session.add(not_in_fridge)
            session.commit()
            message = SuccessMessage("Success")
            return json.dumps(message.to_dict())


# A flask function to see all the users in the database.
@app.route('/show_all_users', methods=["GET", "POST"])
def show_all_users():
    with Session() as session:
        users = session.query(UserModel).all()
        return_list = [str(user) for user in users]
        return_str = str(return_list)
        return jsonify(return_str)


# A flask function to add a new sourdough target to the database for the specified user provided from the email.
@app.route('/add_a_target', methods=["GET", "POST"])
def adding_a_sourdough_target():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            date_of_action = request.args.get('date_of_action')
            date = datetime.datetime.fromisoformat(date_of_action)
            sourdough_weight_target = request.args.get('sourdough_weight_target_in_grams')
            user_model = get_user(user_email, session)
            my_target_model = SourdoughTargetModel(sourdough_id=user_model.id,
                                                   date_of_action=date,
                                                   sourdough_weight_target_in_grams=int(sourdough_weight_target))
            session.add(my_target_model)
            session.commit()
            message = SuccessMessage("Added sourdough target successfully")
            return json.dumps(message.to_dict())
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


# A flask function to add a new feeding action to the database for the specified user provided from the email.
@app.route('/add_a_feeding_action', methods=["GET", "POST"])
def adding_a_feeding_action():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            water_weight = request.args.get('water_weight_added_in_grams')
            flour_weight = request.args.get('flour_weight_added_in_grams')
            user_model = get_user(user_email, session)
            my_feeding_action_model = FeedingActionModel(sourdough_id=user_model.id,
                                                         water_weight_added_in_grams=int(water_weight),
                                                         flour_weight_added_in_grams=int(flour_weight))
            session.add(my_feeding_action_model)
            session.commit()
            message = SuccessMessage("Added a feeding action successfully.")
            return json.dumps(message.to_dict())
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


# A flask function to add a new extraction action to the database for the specified user provided from the email.
@app.route('/add_extraction', methods=["GET", "POST"])
def adding_extraction():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            sourdough_weight_extracted = request.args.get('sourdough_weight_used_in_grams')
            user_model = get_user(user_email, session)
            my_extraction_model = ExtractionModel(sourdough_id=user_model.id,
                                                  sourdough_weight_used_in_grams=int(sourdough_weight_extracted))
            session.add(my_extraction_model)
            session.commit()
            message = SuccessMessage("Added an extraction action successfully.")
            return json.dumps(message.to_dict())
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


# A flask function to add a new refrigeration action to the database for the specified user provided from the email.
@app.route('/add_a_refrigerator_action', methods=["GET", "POST"])
def adding_a_refrigerator_action():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            in_or_out = request.args.get('in_or_out')
            user_model = get_user(user_email, session)
            my_sourdough = session.query(SourdoughModel).filter_by(user_id=user_model.id).one()
            if my_sourdough.last_refrigerator_action.in_or_out == in_or_out:
                raise Exception("Sourdough refrigeration state must be different")
            my_refrigerator_action_model = RefrigeratorActionModel(sourdough_id=my_sourdough.id, in_or_out=in_or_out)
            session.add(my_refrigerator_action_model)
            session.commit()
            message = SuccessMessage("Added a refrigeration action successfully.")
            return json.dumps(message.to_dict())
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


# A flask function that returns the sourdough starter weight for the specified user provided from the email.
@app.route('/my_sourdough_starter_weight', methods=["GET", "POST"])
def my_sourdough_starter_weight():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            user_model = get_user(user_email, session)
            my_sourdough = session.query(SourdoughModel).filter_by(user_id=user_model.id).one()
            my_weight = my_sourdough.weight
            return json.dumps(my_weight)
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


def keep_sourdough_at_maintenance(sourdough_model) -> List[Action]:
    actions_to_perform = list()

    if sourdough_model.in_refrigerator:
        if sourdough_model.days_in_refrigerator > 10:
            # if sourdough is too long in the fridge, extract from it so it reaches minimum maintenance weight
            if not sourdough_model.extracted_today:
                extract = ExtractionAction(sourdough_model.weight - sourdough_model.min_maintenance_weight)
                actions_to_perform.append(extract)
            elif sourdough_model.fed_today:
                # if already extracted, feed it by its own weight
                feed = FeedingAction(sourdough_model.weight, sourdough_model.weight)
                actions_to_perform.append(feed)
        else:
            """
            sourdough is at maintenance and isnt too long in the fridge. do nothing
            """

    else:
        # sourdough in maintenance must be in fridge
        fridge_action = RefrigerationAction("in")
        actions_to_perform.append(fridge_action)

    return actions_to_perform


@app.route('/my_action_today', methods=["GET", "POST"])
def my_action_today():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            user_model = get_user(user_email, session)
            sourdough_model: SourdoughModel = session.query(SourdoughModel).filter_by(user_id=user_model.id).one()

            actions_to_perform = list()

            if sourdough_model.has_upcoming_targets:
                next_sourdough_target = sourdough_model.next_sourdough_target
                if next_sourdough_target.days_from_today > 3:
                    # if target is more than 3 days in the future, keep at maintenance
                    actions_to_perform += keep_sourdough_at_maintenance(sourdough_model)

                elif 0 < next_sourdough_target.days_from_today <= 3:
                    # if in the 3 last days before target, feed to triple weight every day
                    if sourdough_model.in_refrigerator:
                        fridge_action = RefrigerationAction("out")
                        actions_to_perform.append(fridge_action)
                    if not sourdough_model.fed_today:
                        feed = FeedingAction(sourdough_model.weight, sourdough_model.weight)
                        actions_to_perform.append(feed)

                elif next_sourdough_target.days_from_today == 0:
                    # if today is the target day, feed until target weight
                    missing_weight = next_sourdough_target.sourdough_weight_target_in_grams - sourdough_model.weight
                    feed = FeedingAction(missing_weight / 2, missing_weight / 2)
                    actions_to_perform.append(feed)
            else:
                # sourdough has no upcoming targets
                actions_to_perform += keep_sourdough_at_maintenance(sourdough_model)

            # send message back to requester
            message = PerformActionsMessage(actions_to_perform)
            return json.dumps(message.to_dict())
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


# A function to check if the user with the given email is saved in the database, and returns the UserModel object.
# If the user is not in the database, returns an exception.
def get_user(email, session) -> UserModel:
    try:
        return session.query(UserModel).filter_by(email=email).one()
    except Exception as e:
        print(f"User do not exist: {repr(e)}")
        raise Exception("There is no user with this email.")


@app.route('/is_user_in_database', methods=["GET", "POST"])
def is_user_in_db():
    with Session() as session:
        try:
            data = request.args
            email = data['email']
            if session.query(session.query(UserModel).filter_by(email=email).exists()).scalar():
                message = SuccessMessage("Success")
                return json.dumps(message.to_dict())
            else:
                raise Exception("There is no user with this email.")
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
