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

from sourdough.communication.actions import RefrigerationAction, FeedingAction, ExtractionAction
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
            my_refrigerator_action_model = RefrigeratorActionModel(sourdough_id=user_model.id, in_or_out=in_or_out)
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


# A flask function that returns a dictionary with actions the user need to perform,
# according to all the data that is saved in ths database.
@app.route('/my_action_today', methods=["GET", "POST"])
def my_action_today():
    with Session() as session:
        try:
            user_email = request.args.get('email')
            user_model = get_user(user_email, session)
            my_sourdough_model = session.query(SourdoughModel).filter_by(user_id=user_model.id).one()
            days_until_target = my_sourdough_model.days_until_target
            days_in_refrigerator = my_sourdough_model.days_in_refrigerator
            target_weight = session.query(
                            SourdoughTargetModel.sourdough_weight_target_in_grams
                            ).filter_by(sourdough_id=my_sourdough_model.id)[-1]
            refrigerator_state_model = session.query(
                                       RefrigeratorActionModel.in_or_out).filter_by(sourdough_id=my_sourdough_model.id)[-1]
            if days_until_target < 0:
                if days_in_refrigerator == 10:
                    if my_sourdough_model.is_over_maintenance_weight:
                        refrigerator_action = RefrigerationAction("out")
                        feeding_action = FeedingAction(my_sourdough_model.weight, my_sourdough_model.weight)
                        refrigerator_action2 = RefrigerationAction("in")
                        actions = [refrigerator_action, feeding_action, refrigerator_action2]
                        message = PerformActionsMessage(actions)
                        return json.load(message.to_dict())
                    else:
                        refrigerator_action = RefrigerationAction("out")
                        extraction_action = ExtractionAction(my_sourdough_model.weight - 4)
                        refrigerator_action2 = RefrigerationAction("in")
                        actions = [refrigerator_action, extraction_action, refrigerator_action2]
                        message = PerformActionsMessage(actions)
                        return json.load(message.to_dict())
                elif 9 < days_in_refrigerator > 1:
                    refrigeration_action = RefrigerationAction(refrigerator_state_model.in_or_out)
                    message = PerformActionsMessage([refrigeration_action])
                    return json.dumps(message.to_dict())
                else:
                    raise Exception("The sourdough starter is in the refrigerator more than the max 10 days!.")
            elif days_until_target == 0:
                feeding_action = FeedingAction(str((target_weight.sourdough_weight_target_in_grams / 3) - 4),
                                               str((target_weight.sourdough_weight_target_in_grams / 3) - 4))
                extraction_action = ExtractionAction(str(target_weight.sourdough_weight_target_in_grams - 4))
                refrigeration_action = RefrigerationAction("in")
                action = [feeding_action, extraction_action, refrigeration_action]
                message = PerformActionsMessage(action)
                return json.dumps(message.to_dict())
            elif 0 < days_until_target <= 2:
                feeding_action = FeedingAction(str(my_sourdough_model.weight), str(my_sourdough_model.weight))
                message = PerformActionsMessage([feeding_action])
                return json.dumps(message.to_dict())
            elif days_until_target == 3:
                refrigeration_action = RefrigerationAction("out")
                extraction_action = ExtractionAction(str(my_sourdough_model.weight - 2))
                feeding_action = FeedingAction("2", "2")
                actions = [refrigeration_action, extraction_action, feeding_action]
                message = PerformActionsMessage(actions)
                return json.dumps(message.to_dict())
            elif 9 < days_until_target > 3:
                refrigeration_action = RefrigerationAction("in")
                message = PerformActionsMessage([refrigeration_action])
                return json.dumps(message.to_dict())
            elif days_until_target >= 10:
                if my_sourdough_model.is_over_maintenance_weight:
                    refrigerator_action = RefrigerationAction("out")
                    feeding_action = FeedingAction(my_sourdough_model.weight, my_sourdough_model.weight)
                    refrigerator_action2 = RefrigerationAction("in")
                    actions = [refrigerator_action, feeding_action, refrigerator_action2]
                    message = PerformActionsMessage(actions)
                    return json.load(message.to_dict())
                else:
                    refrigerator_action = RefrigerationAction("out")
                    extraction_action = ExtractionAction(my_sourdough_model.weight - 4)
                    refrigerator_action2 = RefrigerationAction("in")
                    actions = [refrigerator_action, extraction_action, refrigerator_action2]
                    message = PerformActionsMessage(actions)
                    return json.load(message.to_dict())
        except Exception as e:
            message_failed = FailedMessage(repr(e))
            return json.dumps(message_failed.to_dict())


# A function to check if the user with the given email is saved in the database, and returns the UserModel object.
# If the user is not in the database, returns an exception.
def get_user(email, session):
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
