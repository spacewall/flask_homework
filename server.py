import flask
from flask.views import MethodView

from models import Advertisement, User, Session

app = flask.Flask('advertisement_service')

@app.before_request
def before_request() -> None:
    flask.request.session = Session()

@app.after_request
def after_request():
    flask.request.session.close()

def create_advertisement(advertisement):
    flask.request.session.add(advertisement)


class AdvertisementView(MethodView):
    def get(self):
        advertisement = ...
        pass

    def post(self):
        advertisement_data = flask.request.json
        advertisement = Advertisement(**advertisement_data)
        create_advertisement(advertisement)

        return flask.jsonify(advertisement.__dict__)

    def patch(self):
        pass

    def delete(self):
        pass
