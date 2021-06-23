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
    user = User(name=name, last_name=last_name, email=email)
    session = Session()
    session.add(user)
    session.commit()
    return "created"


Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run()

