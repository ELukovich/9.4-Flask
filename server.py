from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
# from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, Advertisement
from schema import CreateAdvertisement, UpdateAdvertisement



app = Flask("app")

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response

def get_advertisement_by_id(advertisement_id: int):
    advertisement = request.session.query(Advertisement).get(advertisement_id)
    if advertisement is None:
        raise HttpError(404, "Advertisement not found")
    return advertisement

def add_advertisement(advertisement: Advertisement):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Advertisement already exists")

def validate_json(json_data: dict, schema_class: Type[CreateAdvertisement] | Type[UpdateAdvertisement]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)



class AdvertisementView(MethodView):
    def get(self, advertisement_id: int):
        advertisement = get_advertisement_by_id(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        advertisement_data = validate_json(request.json, CreateAdvertisement)
        advertisement = Advertisement(**advertisement_data)
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def patch(self, advertisement_id: int):
        advertisement_data = validate_json(request.json, UpdateAdvertisement)
        advertisement = get_advertisement_by_id(advertisement_id)
        for field, value in advertisement_data.items():
            setattr(advertisement, field, value)
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def delete(self, advertisement_id: int):
        advertisement = get_advertisement_by_id(advertisement_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({"status": "Advertisement deleted"})



advertisement_view = AdvertisementView.as_view('advertisement_view')

app.add_url_rule('/advertisement/<int:advertisement_id>',
                 view_func=advertisement_view, methods=['GET', 'PATCH', 'DELETE']
                 )

app.add_url_rule('/advertisement', view_func=advertisement_view, methods=['POST'])


if __name__ == "__main__":
    app.run()
