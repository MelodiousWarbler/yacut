from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ID_NOT_FOUND = 'Указанный id не найден'
NO_DATA = 'Отсутствует тело запроса'
NO_URL = '\"url\" является обязательным полем!'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map_obj = URLMap.query.filter_by(short=short_id).first()
    if url_map_obj is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map_obj.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not isinstance(data, dict):
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    url_map = URLMap.from_dict(data)
    url_map.save()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
