import flask
from flask.views import MethodView

from models import Advertisement, Session

app = flask.Flask('advertisement_service')

@app.before_request
def before_request() -> None:
    flask.request.session = Session()

@app.after_request
def after_request(response: flask.Response) -> None:
    flask.request.session.close()

    return response

def create_advertisement(advertisement):
    flask.request.session.add(advertisement)
    flask.request.session.commit()


class AdvertisementView(MethodView):
    def get(self):
        pass

    def post(self):
        advertisement_data = flask.request.json
        advertisement = Advertisement(**advertisement_data)
        create_advertisement(advertisement)

        return flask.jsonify(advertisement.dict)

    def patch(self):
        pass

    def delete(self):
        pass


advertisement_view = AdvertisementView.as_view('advertisement')
app.add_url_rule('/', methods=['POST'], view_func=advertisement_view)

app.run(port=8080)
