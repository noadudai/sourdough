from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.sourdough_targets_table import SourdoughTargetModel
from sourdough.db.models.user_table import UserModel
from sourdough.db.models.feeding_actions_table import FeedingActionModel
from sourdough.db.models.extractions_table import ExtractionModel
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActionModel
from sourdough.db.orm_config import Base, engine, Session
from flask import Flask, request, jsonify
import datetime
import json

app = Flask(__name__)


@app.route('/create_account')
def create_account():
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    my_user = UserModel(name=name, last_name=last_name, email=email)
    session = Session()
    session.add(my_user)
    session.flush()
    my_sourdough = Sourdough(user_id=my_user.id)
    session.add(my_sourdough)
    session.commit()
    return json.dumps({"action performed": "create account action"})


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
    user_id = session.query(UserModel.id).filter_by(email=user_email).one()
    my_feeding_action = FeedingActionModel(sourdough_id=user_id.id,
                                           water_weight_added_in_grams=int(water_weight),
                                           flour_weight_added_in_grams=int(flour_weight))
    session.add(my_feeding_action)
    session.commit()
    return json.dumps({"action performed": "feeding action"})


@app.route('/add_a_target')
def adding_a_sourdough_target():
    user_email = request.args.get('email')
    date_of_action = request.args.get('date_of_action')
    date = datetime.datetime.strptime(date_of_action, '%Y-%m-%d')
    sourdough_weight_target = request.args.get('sourdough_weight_target_in_grams')
    session = Session()
    my_user = session.query(UserModel.id).filter_by(email=user_email).one()
    my_target = SourdoughTargetModel(sourdough_id=my_user.id,
                                     date_of_action=date,
                                     sourdough_weight_target_in_grams=int(sourdough_weight_target))
    session.add(my_target)
    session.commit()
    return json.dumps({"action performed": "sourdough target action"})


@app.route('/add_extraction')
def adding_extraction():
    user_email = request.args.get('email')
    sourdough_weight_extracted = request.args.get('sourdough_weight_used_in_grams')
    session = Session()
    user_id = session.query(UserModel.id).filter_by(email=user_email).one()
    my_extraction = ExtractionModel(sourdough_id=user_id.id,
                                    sourdough_weight_used_in_grams=int(sourdough_weight_extracted))
    session.add(my_extraction)
    session.commit()
    return json.dumps({"action performed": "extraction action"})


@app.route('/add_a_refrigerator_action')
def adding_a_refrigerator_action():
    user_email = request.args.get('email')
    in_or_out = request.args.get('in_or_out')
    session = Session()
    user_id = session.query(UserModel.id).filter_by(email=user_email).one()
    my_refrigerator_action = RefrigeratorActionModel(sourdough_id=user_id.id, in_or_out=in_or_out)
    session.add(my_refrigerator_action)
    session.commit()
    return json.dumps({"action performed": "refrigerator action"})


@app.route('/my_action_today')
def my_action_today():
    user_email = request.args.get('email')
    session = Session()
    my_user = session.query(UserModel.id).filter_by(email=user_email).one()
    my_sourdough = session.query(Sourdough).filter_by(user_id=my_user.id).one()
    delta_target = my_sourdough.days_until_target
    delta_refrigerator = my_sourdough.days_in_refrigerator
    target_weight = session.query(SourdoughTargetModel.sourdough_weight_target_in_grams).filter_by(sourdough_id=my_sourdough.id)[-1]
    if delta_target < 0:
        if delta_refrigerator == 10:
            if my_sourdough.weight < my_sourdough.max_maintenance_weight:
                return json.dumps(my_sourdough.is_over_maintenance_weight)
        elif 9 < delta_refrigerator > 1:
            action = {"actions to perform": {"days in": str(delta_refrigerator) + "days in the refrigerator",
                                             "refrigerator action": "days in for" + str(
                                                 delta_refrigerator - 10) + " days"}}
            return json.dumps(action)
        else:
            raise Exception("The sourdough starter is in the refrigerator more than the max 10 days!.")
    elif delta_target == 0:
        action = {"actions to perform": {"feeding action":
                                             {"water": str((target_weight.sourdough_weight_target_in_grams / 3) - 4),
                                              "flour": str((target_weight.sourdough_weight_target_in_grams / 3) - 4)},
                                         "extraction action": {
                                             "extract": str(target_weight.sourdough_weight_target_in_grams - 4)},
                                         "refrigerator action": "in"}}
        return json.dumps(action)
    elif 0 < delta_target <= 2:
        action = {"actions to perform": {"feeding action": {"water": str(my_sourdough.weight), "flour": str(my_sourdough.weight)}}}
        return json.dumps(action)
    elif delta_target == 3:
        action = {"actions to preform": {"refrigerator action": "out",
                                         "extraction action": {"extract": str(my_sourdough.weight - 2)},
                                         "feeding action": {"water": "2", "flour": "2"}}}
        return json.dumps(action)
    elif 9 < delta_target > 3:
        action = {"actions to preform": {"days in": str(delta_refrigerator) + "days in the refrigerator",
                                         "refrigerator action": "in for " + str(delta_target - 3) + " days"}}
        return json.dumps(action)
    elif delta_target >= 10:
        return json.dumps(my_sourdough.is_over_maintenance_weight)


@app.route('/my_sourdough_starter_weight')
def my_sourdough_starter_weight():
    user_email = request.args.get('email')
    session = Session()
    my_user = session.query(UserModel.id).filter_by(email=user_email).one()
    my_sourdough = session.query(Sourdough).filter_by(user_id=my_user.id).one()
    my_weight = my_sourdough.weight
    return json.dumps(my_weight)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
