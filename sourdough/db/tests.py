from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.sourdough_targets_table import SourdoughTargets
from sourdough.db.models.user_table import User
from sourdough.db.models.feeding_actions_table import FeedingActions
from sourdough.db.models.leaven_extractions_table import LeavenExtractions
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActions
from sourdough.db.orm_config import Base, engine, Session
from flask import Flask, request, jsonify

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


# @app.route('/add_a_target')
# def adding_a_sourdough_target():
  #   name = request.args.get('name')
  #   last_name = request.args.get('last_name')
  #   date_time = request.args.get('when')
  #   sourdough_weight = request.args.get('sourdough_weight_target_in_grams')
  #   session = Session()
  #   my_user = session.query(User).filter(name=name).filter(last_name=last_name)
  #   my_sourdough = session.query(Sourdough).flter_by(user_id=my_user.id)
  #   my_target = SourdoughTargets(sourdough_id=my_sourdough.id,
  #                                when=date_time,
  #                                sourdough_weight_target_in_grams=int(sourdough_weight))
  #   session.add(my_target)
  #   session.commit()
  #   return "A new target created"


Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run()

