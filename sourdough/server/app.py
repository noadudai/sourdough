from sourdough.db.models.sourdough_table import Sourdough
from sourdough.db.models.user_table import User
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


# Base.metadata.create_all(engine)
