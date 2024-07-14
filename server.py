import flask
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Advertisement, Session

app = flask.Flask('advertisement_service')

@app.before_request
def before_request() -> None:
    flask.request.session = Session()

@app.after_request
def after_request(response: flask.Response) -> None:
    flask.request.session.close()

    return response


class HttpError(Exception):
    def __init__(self, status_code, message) -> None:
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    json_response = flask.jsonify({'status': 'error', 'message': error.message})
    json_response.status_code = error.status_code

    return json_response

def get_advertisement(advertisement_id: int) -> Advertisement:
    advertisement = flask.request.session.get(Advertisement, advertisement_id)

    if advertisement is None:
        raise HttpError(status_code=404, message="advertisement doesn't exist")
    
    return advertisement

def add_advertisement(advertisement: Advertisement) -> None:
    try:
        flask.request.session.add(advertisement)
        flask.request.session.commit()

    except IntegrityError:
        raise HttpError(status_code=409, message='the advertisment with the same header already exists')


class AdvertisementView(MethodView):
    def get(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)

        return flask.jsonify(advertisement.dict)

    def post(self):
        advertisement_data = flask.request.json
        advertisement = Advertisement(**advertisement_data)
        add_advertisement(advertisement)

        return flask.jsonify(advertisement.dict)

    def patch(self, advertisement_id: int):
        advertisement_data: dict = flask.request.json
        advertisement = get_advertisement(advertisement_id)

        for field, value in advertisement_data.items():
            setattr(advertisement, field, value)

        add_advertisement(advertisement)

        return flask.jsonify(advertisement.dict)

    def delete(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        flask.request.session.delete(advertisement)
        flask.request.session.commit()

        return flask.jsonify({'status': 'deleted'})


advertisement_view = AdvertisementView.as_view('advertisement')
app.add_url_rule('/', methods=['POST'], view_func=advertisement_view)
app.add_url_rule('/<int:advertisement_id>/', methods=['GET', 'DELETE', 'PATCH'], view_func=advertisement_view)

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)
