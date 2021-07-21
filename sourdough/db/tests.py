from sourdough.db.models.sourdough_table import SourdoughModel
from sourdough.db.models.sourdough_targets_table import SourdoughTargetModel
from sourdough.db.models.user_table import UserModel
from sourdough.db.models.feeding_actions_table import FeedingActionModel
from sourdough.db.models.extractions_table import ExtractionModel
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActionModel
from sourdough.db.orm_config import Base, engine, Session
from flask import Flask, request, jsonify
import datetime
import json

from sourdough.communication.actions import TargetAction, FeedingAction, ExtractionAction, RefrigerationAction
from sourdough.communication.messages import ActionsPerformedMessage, PerformActionsMessage, SuccessMessage

app = Flask(__name__)


@app.route('/create_account')
def create_account():
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    session = Session()
    if session.query(session.query(UserModel).filter_by(email=email).exists()).scalar():
        return SuccessMessage.failed("Failed!. User is already exists.")
    else:
        my_user_model = UserModel(name=name, last_name=last_name, email=email)
        session.add(my_user_model)
        session.flush()
        my_sourdough_model = SourdoughModel(user_id=my_user_model.id)
        session.add(my_sourdough_model)
        session.commit()
        return SuccessMessage.success()


@app.route('/show_all_users')
def show_all_users():
    session = Session()
    users = session.query(UserModel).all()
    return_list = [str(user) for user in users]
    return_str = str(return_list)
    return jsonify(return_str)


@app.route('/add_a_feeding_action')
def adding_a_feeding_action():
    user_email = request.args.get('email')
    water_weight = request.args.get('water_weight_added_in_grams')
    flour_weight = request.args.get('flour_weight_added_in_grams')
    session = Session()
    user_model = user_is_in_db(user_email)
    my_feeding_action_model = FeedingActionModel(sourdough_id=user_model.id,
                                                 water_weight_added_in_grams=int(water_weight),
                                                 flour_weight_added_in_grams=int(flour_weight))
    session.add(my_feeding_action_model)
    session.commit()
    feeding_action = FeedingAction(water_weight, flour_weight)
    message = ActionsPerformedMessage([feeding_action])
    return json.dumps(message.to_dict())


@app.route('/add_a_target')
def adding_a_sourdough_target():
    user_email = request.args.get('email')
    date_of_action = request.args.get('date_of_action')
    date = datetime.datetime.fromisoformat(date_of_action)
    sourdough_weight_target = request.args.get('sourdough_weight_target_in_grams')
    session = Session()
    my_user_model = session.query(UserModel.id).filter_by(email=user_email).one()
    my_target_model = SourdoughTargetModel(sourdough_id=my_user_model.id,
                                           date_of_action=date,
                                           sourdough_weight_target_in_grams=int(sourdough_weight_target))
    session.add(my_target_model)
    session.commit()
    target_action = TargetAction(date, sourdough_weight_target)
    message = ActionsPerformedMessage([target_action])
    return json.dumps(message.to_dict())


@app.route('/add_extraction')
def adding_extraction():
    user_email = request.args.get('email')
    sourdough_weight_extracted = request.args.get('sourdough_weight_used_in_grams')
    session = Session()
    user_id_model = session.query(UserModel.id).filter_by(email=user_email).one()
    my_sourdough_model = session.query(SourdoughModel).filter_by(user_id=user_id_model.id).one()
    if 0 < my_sourdough_model.weight > int(sourdough_weight_extracted):
        my_extraction_model = ExtractionModel(sourdough_id=user_id_model.id,
                                              sourdough_weight_used_in_grams=int(sourdough_weight_extracted))
        session.add(my_extraction_model)
        session.commit()
        extraction_action = ExtractionAction(sourdough_weight_extracted)
        message = ActionsPerformedMessage([extraction_action])
        return json.dumps(message.to_dict())
    else:
        raise Exception("There is not enough sourdough starter for this amount of extraction weight.")


@app.route('/add_a_refrigerator_action')
def adding_a_refrigerator_action():
    user_email = request.args.get('email')
    in_or_out = request.args.get('in_or_out')
    session = Session()
    user_id_model = session.query(UserModel.id).filter_by(email=user_email).one()
    my_refrigerator_action_model = RefrigeratorActionModel(sourdough_id=user_id_model.id, in_or_out=in_or_out)
    session.add(my_refrigerator_action_model)
    session.commit()
    refrigeration_action = RefrigerationAction(in_or_out)
    message = ActionsPerformedMessage([refrigeration_action])
    return json.dumps(message.to_dict())


@app.route('/my_action_today')
def my_action_today():
    user_email = request.args.get('email')
    session = Session()
    my_user_model = session.query(UserModel.id).filter_by(email=user_email).one()
    my_sourdough_model = session.query(SourdoughModel).filter_by(user_id=my_user_model.id).one()
    delta_target = my_sourdough_model.days_until_target
    delta_refrigerator = my_sourdough_model.days_in_refrigerator
    target_weight = session.query(
                    SourdoughTargetModel.sourdough_weight_target_in_grams
                    ).filter_by(sourdough_id=my_sourdough_model.id)[-1]
    refrigerator_state_model = session.query(
                               RefrigeratorActionModel.in_or_out).filter_by(sourdough_id=my_sourdough_model.id)[-1]
    if delta_target < 0:
        if delta_refrigerator == 10:
            if my_sourdough_model.is_over_maintenance_weight:
                refrigerator_action = RefrigerationAction("out")
                feeding_action = FeedingAction(my_sourdough_model.weight, my_sourdough_model.weight)
                refrigerator_action2 = RefrigerationAction("in")
                actions = [refrigerator_action, feeding_action, refrigerator_action2]
                message = PerformActionsMessage(actions)
                return message.to_dict()
            else:
                refrigerator_action = RefrigerationAction("out")
                extraction_action = ExtractionAction(my_sourdough_model.weight - 4)
                refrigerator_action2 = RefrigerationAction("in")
                actions = [refrigerator_action, extraction_action, refrigerator_action2]
                message = PerformActionsMessage(actions)
                return message.to_dict()
        elif 9 < delta_refrigerator > 1:
            refrigeration_action = RefrigerationAction(refrigerator_state_model.in_or_out)
            message = PerformActionsMessage([refrigeration_action])
            return json.dumps(message.to_dict())
        else:
            raise Exception("The sourdough starter is in the refrigerator more than the max 10 days!.")
    elif delta_target == 0:
        feeding_action = FeedingAction(str((target_weight.sourdough_weight_target_in_grams / 3) - 4),
                                       str((target_weight.sourdough_weight_target_in_grams / 3) - 4))
        extraction_action = ExtractionAction(str(target_weight.sourdough_weight_target_in_grams - 4))
        refrigeration_action = RefrigerationAction("in")
        action = [feeding_action, extraction_action, refrigeration_action]
        message = PerformActionsMessage(action)
        return json.dumps(message.to_dict())
    elif 0 < delta_target <= 2:
        feeding_action = FeedingAction(str(my_sourdough_model.weight), str(my_sourdough_model.weight))
        message = PerformActionsMessage([feeding_action])
        return json.dumps(message.to_dict())
    elif delta_target == 3:
        refrigeration_action = RefrigerationAction("out")
        extraction_action = ExtractionAction(str(my_sourdough_model.weight - 2))
        feeding_action = FeedingAction("2", "2")
        actions = [refrigeration_action, extraction_action, feeding_action]
        message = PerformActionsMessage(actions)
        return json.dumps(message.to_dict())
    elif 9 < delta_target > 3:
        refrigeration_action = RefrigerationAction("in")
        message = PerformActionsMessage([refrigeration_action])
        return json.dumps(message.to_dict())
    elif delta_target >= 10:
        if my_sourdough_model.is_over_maintenance_weight:
            refrigerator_action = RefrigerationAction("out")
            feeding_action = FeedingAction(my_sourdough_model.weight, my_sourdough_model.weight)
            refrigerator_action2 = RefrigerationAction("in")
            actions = [refrigerator_action, feeding_action, refrigerator_action2]
            message = PerformActionsMessage(actions)
            return message.to_dict()
        else:
            refrigerator_action = RefrigerationAction("out")
            extraction_action = ExtractionAction(my_sourdough_model.weight - 4)
            refrigerator_action2 = RefrigerationAction("in")
            actions = [refrigerator_action, extraction_action, refrigerator_action2]
            message = PerformActionsMessage(actions)
            return message.to_dict()


@app.route('/my_sourdough_starter_weight')
def my_sourdough_starter_weight():
    user_email = request.args.get('email')
    session = Session()
    my_user = session.query(UserModel.id).filter_by(email=user_email).one()
    my_sourdough = session.query(SourdoughModel).filter_by(user_id=my_user.id).one()
    my_weight = my_sourdough.weight
    return json.dumps(my_weight)


def user_is_in_db(email):
    session = Session()
    user = session.query(session.query(UserModel).filter_by(email=email).exists()).scalar()
    if user:
        return session.query(UserModel).filter_by(email=email).one()
    else:
        raise Exception("There is no user with this email.")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()

