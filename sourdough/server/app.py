from sourdough.db.models.feeding_actions_table import FeedingActions
from sourdough.db.models.leaven_extractions_table import LeavenExtractions
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActions
from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.sourdough_targets_table import SourdoughTargets
from sourdough.db.models.user_table import User
from sourdough.db.orm_config import Base, engine, Session
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)


@app.route('/create_account')
def create_account():
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    my_user = User(name=name, last_name=last_name, email=email)
    session = Session()
    session.add(my_user)
    session.flush()
    my_sourdough = Sourdough(user_id=my_user.id)
    session.add(my_sourdough)
    session.commit()
    return "created"


@app.route('/show_all_users')
def show_all_users():
    session = Session()
    users = session.query(User).all()
    return_list = [str(user) for user in users]
    return_str = str(return_list)
    return jsonify(return_str)


@app.route('/add_a_target')
def adding_a_sourdough_target():
    user_email = request.args.get('email')
    date_of_action = request.args.get('date_of_action')
    date = datetime.datetime.strptime(date_of_action, '%Y-%m-%d %H:%M:%S')
    sourdough_weight = request.args.get('sourdough_weight_target_in_grams')
    session = Session()
    my_user = session.query(User.id).filter_by(email=user_email).one()
    my_target = SourdoughTargets(sourdough_id=my_user.id,
                                 date_of_action=date,
                                 sourdough_weight_target_in_grams=int(sourdough_weight))
    session.add(my_target)
    session.commit()
    return "A new target created"


@app.route('/add_a_feeding_action', methods=['GET', 'POST'])
def adding_a_feeding_action():
    user_email = request.args.get('email')
    water_weight = request.args.get('water_weight_added_in_grams')
    flour_weight = request.args.get('flour_weight_added_in_grams')
    session = Session()
    user_id = session.query(User.id).filter_by(email=user_email).one()
    my_feeding_action = FeedingActions(sourdough_id=user_id.id,
                                       water_weight_added_in_grams=int(water_weight),
                                       flour_weight_added_in_grams=int(flour_weight))
    session.add(my_feeding_action)
    session.commit()
    return "A new feeding action added"


@app.route('/add_a_leaven_extraction')
def adding_a_leaven_extraction():
    user_email = request.args.get('email')
    sourdough_weight = request.args.get('sourdough_weight_used_in_grams')
    session = Session()
    user_id = session.query(User.id).filter_by(email=user_email).one()
    my_leaven_extraction = LeavenExtractions(sourdough_id=user_id.id,
                                             sourdough_weight_used_in_grams=int(sourdough_weight))
    session.add(my_leaven_extraction)
    session.commit()
    return "A new leaven extraction added"


@app.route('/add_a_refrigerator_action')
def adding_a_refrigerator_action():
    user_email = request.args.get('email')
    in_or_out = request.args.get('in_or_out')
    session = Session()
    user_id = session.query(User.id).filter_by(email=user_email).one()
    my_refrigerator_action = RefrigeratorActions(sourdough_id=user_id.id, in_or_out=in_or_out)
    session.add(my_refrigerator_action)
    session.commit()
    return "A new refrigerator action added"


# Base.metadata.create_all(engine)
